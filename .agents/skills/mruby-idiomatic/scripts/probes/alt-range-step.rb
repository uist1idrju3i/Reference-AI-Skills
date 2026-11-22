def check(condition, detail)
  unless condition
    puts "FAIL alt-range-step " + detail
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

def stepped(first, last, step)
  raise ArgumentError, "invalid step" if step <= 0
  result = []
  value = first
  while value <= last
    result << value
    break if last - value < step
    value += step
  end
  result
end
check(stepped(1, 6, 2) == [1, 3, 5], "step")
check(stepped(2, 1, 1) == [], "empty")
reject_nil { stepped(1, 3, 0) }
puts "PASS alt-range-step"
