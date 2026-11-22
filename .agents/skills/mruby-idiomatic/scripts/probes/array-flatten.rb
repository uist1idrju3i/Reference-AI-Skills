def check(condition, detail)
  unless condition
    puts "FAIL array-flatten " + detail
    raise "assertion failed"
  end
end

check([1, [nil, [2]]].flatten == [1, nil, 2], "recursive")
check([].flatten == [], "empty")
check([1, [2, [3]]].flatten(1) == [1, 2, [3]], "depth")
puts "PASS array-flatten"
