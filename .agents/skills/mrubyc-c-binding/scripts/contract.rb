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
rejects(ArgumentError, "keyword guard missing rescued") { BindingContract.keyword_guard }
check(BindingContract.keyword_effects == 0, "keyword guard missing no side effects")
rejects(ArgumentError, "keyword guard unknown rescued") { BindingContract.keyword_guard(mode: :write, other: 1) }
check(BindingContract.keyword_effects == 0, "keyword guard unknown no side effects")
rejects(TypeError, "keyword guard wrong type rescued") { BindingContract.keyword_guard(mode: "write") }
check(BindingContract.keyword_effects == 0, "keyword guard wrong type no side effects")
check(BindingContract.keyword_guard(mode: :write), "keyword guard normal")
check(BindingContract.keyword_effects == 1, "keyword guard normal one side effect")
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

def value_rejects(error)
  caught = false
  begin
    yield
  rescue error
    caught = true
  end
  raise "missing value exception" unless caught
  raise "value error caused side effect" unless BindingContract.value_effects == 0
end

def type_case(name, tag, normal, wrong, outside, empty)
  BindingContract.value_reset
  value_rejects(TypeError) { BindingContract.typed(tag, wrong) }
  value_rejects(TypeError) { BindingContract.typed(tag, nil) } unless tag == 1
  if outside
    value_rejects(outside[0]) { BindingContract.typed(tag, outside[1]) }
  end
  raise "typed value mismatch" unless BindingContract.value_equal(BindingContract.typed(tag, normal), normal)
  if empty
    raise "empty value mismatch" unless BindingContract.value_equal(BindingContract.typed(tag, empty[0]), empty[0])
  end
  check(BindingContract.value_effects == (empty ? 2 : 1), name)
end

module ValueOther
end

def value_cases
  type_case("typed nil contract", 1, nil, 1, nil, nil)
  type_case("typed false contract", 2, false, 0, nil, nil)
  type_case("typed true contract", 3, true, false, nil, nil)
  type_case("typed Integer contract", 4, -32768, 1.0, [RangeError, 32768], [0])
  type_case("typed Float contract", 5, 3.0, 3, [RangeError, 3.5], [0.0])
  type_case("typed Symbol contract", 6, :write, "write", [ArgumentError, :invalid], nil)
  type_case("typed Class contract", 7, BindingContract.value_make(7), 1, [ArgumentError, String], nil)
  type_case("typed Module contract", 8, BindingContract.value_make(8), 1, [ArgumentError, ValueOther], nil)
  type_case("typed Object contract", 9, BindingContract.value_make(9), 1, [ArgumentError, BindingContract::ValueData.new], nil)
  type_case("typed Proc contract", 10, Proc.new { 7 }, 1, nil, [Proc.new {}])
  type_case("typed Array contract", 11, [-32768, 32767], 1, [RangeError, [1, 32768]], [[]])
  type_case("typed String contract", 12, "text", 1, [RangeError, "123456789"], [""])
  type_case("typed Range contract", 13, (1..2), 1, [RangeError, (1..32768)], [(2...2)])
  type_case("typed Hash contract", 14, {value: 1}, 1, [RangeError, {value: 32768}], [{}])
  type_case("typed Exception contract", 15, BindingContract.value_make(15), 1,
            [RangeError, RuntimeError.new("123456789")], [RuntimeError.new("")])

  BindingContract.value_reset
  value_rejects(ArgumentError) { BindingContract.typed }
  value_rejects(ArgumentError) { BindingContract.typed(0, nil) }
  value_rejects(RangeError) { BindingContract.typed(4, -32769) }
  value_rejects(RangeError) { BindingContract.typed(5, 1.0 / 0.0) }
  value_rejects(RangeError) { BindingContract.typed(5, 0.0 / 0.0) }
  value_rejects(RangeError) { BindingContract.typed(5, 32768.0) }
  check(BindingContract.value_effects == 0, "typed arity EMPTY and numeric boundaries")

  value_rejects(ArgumentError) { BindingContract.typed(12, "a\0b") }
  value_rejects(TypeError) { BindingContract.typed(11, [1, nil]) }
  value_rejects(RangeError) { BindingContract.typed(11, [1, 2, 3, 4, 5]) }
  value_rejects(TypeError) { BindingContract.typed(13, ("a".."b")) }
  value_rejects(RangeError) { BindingContract.typed(13, (2..1)) }
  value_rejects(TypeError) { BindingContract.typed(14, {"value" => 1}) }
  value_rejects(ArgumentError) { BindingContract.typed(14, {invalid: 1}) }
  value_rejects(ArgumentError) { BindingContract.typed(15, Exception.new("ok")) }
  check(BindingContract.value_effects == 0, "typed composite rejection before side effects")

  value_rejects(ArgumentError) { BindingContract.nested }
  value_rejects(TypeError) { BindingContract.nested(nil) }
  value_rejects(TypeError) { BindingContract.nested([1]) }
  value_rejects(TypeError) { BindingContract.nested([[1], [nil]]) }
  value_rejects(RangeError) { BindingContract.nested([[1], [32768]]) }
  value_rejects(RangeError) { BindingContract.nested([[], [], [], [], []]) }
  value_rejects(RangeError) { BindingContract.nested([[1, 2, 3, 4, 5]]) }
  raise "empty nested mismatch" unless BindingContract.nested([]) == 0
  raise "nested copy mismatch" unless BindingContract.nested([[1], [], [2]]) == 3
  check(BindingContract.value_effects == 2, "nested Array full validation before buffer copy")

  BindingContract.value_reset
  value_rejects(TypeError) { BindingContract.build_pair(nil) }
  value_rejects(RuntimeError) { BindingContract.build_pair(true) }
  result = BindingContract.build_pair(false)
  check(result[:value][0].class == BindingContract::ValueData && BindingContract.value_effects == 1,
        "Array Hash construction and partial failure cleanup")

  [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15].each do |tag|
    value = BindingContract.value_make(tag)
    raise "C factory mismatch" unless BindingContract.value_equal(BindingContract.typed(tag, value), value)
  end
  check(true, "C value factories round trip")
  nil
end

value_cases
BindingContract.value_ownership

def helper_cases
  BindingContract.value_reset
  [0, 1, 3, 5, 7].each do |selector|
    value_rejects(ArgumentError) { BindingContract.helper(selector) }
  end
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14].each do |selector|
    value_rejects(TypeError) { BindingContract.helper(selector, nil) }
  end
  value_rejects(TypeError) { BindingContract.helper(7, 0) }
  value_rejects(TypeError) { BindingContract.helper(5, :write) }
  check(BindingContract.value_effects == 0, "beta helpers rescue before side effects")
  samples = [[0, nil, nil], [1, -3.75, -3], [2, 4, 4], [3, 4, 4.0],
             [4, 3.5, 3.5], [5, "", ""], [6, "s", "s"], [7, false, 0], [8, true, 1],
             [9, -3.75, -3], [10, 3, 3], [11, 4, 4.0], [12, 3.5, 3.5],
             [13, "s", "s"], [14, "", ""], [15, 3.5, 3], [16, 3, 3.0], [17, 3, "3"]]
  samples.each do |sample|
    raise "helper result mismatch" unless BindingContract.helper(sample[0], sample[1]) == sample[2]
  end
  defaults = [[2, 7], [4, 2.0], [6, "d"], [8, 1], [9, 0], [10, 7],
              [11, 0.0], [12, 2.0], [13, nil], [14, "d"]]
  defaults.each do |sample|
    raise "helper default mismatch" unless BindingContract.helper(sample[0]) == sample[1]
  end
  raise "nil converter mismatch" unless BindingContract.helper(15, nil) == 0 &&
    BindingContract.helper(16, nil) == 0.0 && BindingContract.helper(17, nil) == ""
  check(true, "beta helpers defaults truncation and converters")
end

helper_cases
puts "PASS ALL binding-contract"
