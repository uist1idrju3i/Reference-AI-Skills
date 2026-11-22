def check(condition, detail)
  unless condition
    puts "FAIL alt-sort-by " + detail
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

def sorted(items)
  raise ArgumentError, "nil items" if items.nil?
  result = []
  items.each do |value|
    index = 0
    index += 1 while index < result.size && result[index].size <= value.size
    tail = result.size
    while tail > index
      result[tail] = result[tail - 1]
      tail -= 1
    end
    result[index] = value
  end
  result
end
check(sorted(["bbb", "a", "cc"]) == ["a", "cc", "bbb"], "length key")
check(sorted(["bbb", "a"])[0] == "a", "minimum")
check(sorted([]) == [], "empty")
reject_nil { sorted(nil) }
puts "PASS alt-sort-by"
