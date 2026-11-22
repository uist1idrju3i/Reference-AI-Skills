def check(condition, detail)
  unless condition
    puts "FAIL alt-large-integer-literal " + detail
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

MAX_INT = 2147483647
MIN_INT = -2147483647 - 1
def checked_add(left, right)
  sum = left.to_f + right.to_f
  if sum > MAX_INT.to_f || sum < MIN_INT.to_f
    raise ArgumentError, "int32 overflow"
  end
  left + right
end
check(checked_add(2, -2) == 0, "zero")
check(checked_add(MAX_INT, 0) == MAX_INT, "upper bound")
check(checked_add(MIN_INT, 0) == MIN_INT, "lower bound")
check(checked_add(MAX_INT, MIN_INT) == -1, "opposite extremes")
reject_nil { checked_add(MAX_INT, 1) }
reject_nil { checked_add(MIN_INT, -1) }
puts "PASS alt-large-integer-literal"
