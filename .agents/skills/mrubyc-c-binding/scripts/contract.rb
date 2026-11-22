def check(value, name)
  raise "FAIL #{name}" unless value
  puts "PASS #{name}"
end

def rejects(error, name)
  caught = false
  begin
    yield
  rescue error
    caught = true
  end
  check(caught, name)
end

check(BindingContract.ownership, "ownership")
check(BindingContract.layout == 0, "layout no positional arguments")
check(BindingContract.layout({a: 1}) == 100, "layout positional Hash not keyword")
check(BindingContract.layout(7) == 100, "layout positional no block")
check(BindingContract.layout(7) { 8 } == 101, "layout block at argc+1")
check(BindingContract.layout(7, a: 1) == 110, "layout keyword hash at argc+1")
check(BindingContract.layout(7, a: 1) { 8 } == 111, "layout keyword block at argc+2")
check(BindingContract.layout(7, **{}) { 8 } == 101, "layout empty keyword hash removed")
check(BindingContract.keyword(3, required: "x") == ["x", 4, 3], "keyword default and retained String")
check(BindingContract.keyword(3, **{required: "x", optional: 9}) == ["x", 9, 3], "keyword splat and explicit option")
rejects(ArgumentError, "keyword required") { BindingContract.keyword(3) }
rejects(ArgumentError, "keyword unknown") { BindingContract.keyword(3, required: "x", other: 1) }
rejects(TypeError, "keyword nil provided not missing") { BindingContract.keyword(3, required: nil) }
rejects(TypeError, "keyword optional nil not default") { BindingContract.keyword(3, required: "x", optional: nil) }
check(BindingContract.dict(required: 1) == {}, "keyword dict empty")
check(BindingContract.dict(required: 1, other: "kept") == {other: "kept"}, "keyword dict transfers remainder")
BindingContract.save_block { |n| n + 7 }
check(BindingContract.saved.call(5) == 12, "retained block invoked from Ruby")
BindingContract.clear_block
check(BindingContract.saved == nil, "retained block released")
rejects(ArgumentError, "missing block") { BindingContract.save_block }
check(BindingContract.send_c("a", "b") == "ab", "mrbc_send C target borrows argument")

class RubyTarget
  def ruby_method
    42
  end
end
rejects(NotImplementedError, "mrbc_send rejects Ruby method") { BindingContract.send_method(RubyTarget.new, "ruby_method") }
rejects(NoMethodError, "mrbc_send missing method") { BindingContract.send_method(BindingContract, "no_such_method") }
rejects(BindingContractError, "mrbc_send C exception detected") { BindingContract.send_method(BindingContract, "fail_method") }
check(BindingContract.statistics == 31, "raise returns to C and exception flag observed")
check(BindingContract.numeric(3.75) == 3, "MRBC_ARG_I accepts Float truncates")
rejects(TypeError, "MRBC_ARG_I rejects nil") { BindingContract.numeric(nil) }
rejects(ArgumentError, "MRBC_ARG_I missing") { BindingContract.numeric }
check(BindingContract.guarded(7) == 7, "guarded normal")
rejects(TypeError, "guarded rejects nil") { BindingContract.guarded(nil) }
rejects(ArgumentError, "guarded rejects missing") { BindingContract.guarded }
check(BindingContract.guarded_count == 1, "raise-then-return prevents side effects")
puts "PASS ALL binding-contract"
