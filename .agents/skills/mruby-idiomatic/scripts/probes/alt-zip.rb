def check(condition, detail)
  unless condition
    puts "FAIL alt-zip " + detail
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

def pair(left, right)
  raise ArgumentError, "nil items" if left.nil? || right.nil?
  result = []
  left.each_with_index { |value, index| result << [value, right[index]] }
  result
end
check(pair([1, 2], ["a"]) == [[1, "a"], [2, nil]], "padding")
check(pair([], []) == [], "empty")
reject_nil { pair(nil, []) }
puts "PASS alt-zip"
