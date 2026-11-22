def check(condition, detail)
  unless condition
    puts "FAIL alt-sum " + detail
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

def total(items, initial = 0)
  raise ArgumentError, "nil items" if items.nil?
  result = initial
  items.each { |value| result += value }
  result
end
check(total([1, 2, 3]) == 6, "array")
check(total(1..3, 5) == 11, "range and initial")
check(total([]) == 0 && total(1...1) == 0, "empty")
reject_nil { total(nil) }
puts "PASS alt-sum"
