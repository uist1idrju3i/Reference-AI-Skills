def check(condition, detail)
  unless condition
    puts "FAIL alt-count-value " + detail
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

def occurrences(items, target)
  raise ArgumentError, "nil items" if items.nil?
  count = 0
  items.each { |value| count += 1 if value == target }
  count
end
check(occurrences([1, nil, 1], 1) == 2, "matches")
check(occurrences([nil, 1], nil) == 1, "nil value")
check(occurrences([], 1) == 0, "empty")
reject_nil { occurrences(nil, 1) }
puts "PASS alt-count-value"
