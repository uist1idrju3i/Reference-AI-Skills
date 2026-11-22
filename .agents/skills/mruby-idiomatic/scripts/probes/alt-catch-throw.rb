def check(condition, detail)
  unless condition
    puts "FAIL alt-catch-throw " + detail
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

def first_match(items)
  raise ArgumentError, "nil items" if items.nil?
  items.each { |value| return value if value == 2 }
  nil
end
check(first_match([1, 2, 3]) == 2, "early return")
check(first_match([]).nil? && first_match([nil]).nil?, "no match")
reject_nil { first_match(nil) }
puts "PASS alt-catch-throw"
