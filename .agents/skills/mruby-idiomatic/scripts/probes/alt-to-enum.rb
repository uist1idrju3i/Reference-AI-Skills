def check(condition, detail)
  unless condition
    puts "FAIL alt-to-enum " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

def visit(count)
  raise ArgumentError, "negative count" if count < 0
  count.times { |index| yield index }
end
values = []
visit(3) { |index| values << index }
check(values == [0, 1, 2], "direct block")
visit(0) { check(false, "empty yielded") }
reject_nil { visit(-1) { } }
puts "PASS alt-to-enum"
