def check(condition, detail)
  unless condition
    puts "FAIL array-compact " + detail
    raise "assertion failed"
  end
end

check([1, nil, false].compact == [1, false], "remove only nil")
check([].compact == [], "empty")
puts "PASS array-compact"
