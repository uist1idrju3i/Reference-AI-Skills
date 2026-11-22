def check(condition, detail)
  unless condition
    puts "FAIL alt-each-slice " + detail
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

def slices(items, width)
  raise ArgumentError, "invalid slice" if items.nil? || width <= 0
  result = []
  current = []
  items.each do |value|
    current << value
    if current.size == width
      result << current
      current = []
    end
  end
  result << current unless current.empty?
  result
end
check(slices([1, nil, 3], 2) == [[1, nil], [3]], "partial slice")
check(slices([], 2) == [], "empty")
reject_nil { slices([], 0) }
reject_nil { slices(nil, 2) }
puts "PASS alt-each-slice"
