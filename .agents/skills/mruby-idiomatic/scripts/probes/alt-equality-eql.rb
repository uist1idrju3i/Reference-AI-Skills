def check(condition, detail)
  unless condition
    puts "FAIL alt-equality-eql " + detail
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

def same_integer(left, right)
  left.is_a?(Integer) && right.is_a?(Integer) && left == right
end
check(same_integer(2, 2), "same integer")
check(!same_integer(2, 2.0), "different numeric type")
check(!same_integer(nil, nil), "nil outside domain")
puts "PASS alt-equality-eql"
