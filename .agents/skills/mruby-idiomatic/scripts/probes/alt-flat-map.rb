def check(condition, detail)
  unless condition
    puts "FAIL alt-flat-map " + detail
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

def flatten_one(items)
  raise ArgumentError, "nil items" if items.nil?
  result = []
  items.each do |value|
    if value.is_a?(Array)
      value.each { |nested| result << nested }
    else
      result << value
    end
  end
  result
end
check(flatten_one([[1], [], nil, [2]]) == [1, nil, 2], "one level")
check(flatten_one([]) == [], "empty")
reject_nil { flatten_one(nil) }
puts "PASS alt-flat-map"
