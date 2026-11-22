def check(condition, detail)
  unless condition
    puts "FAIL array-join " + detail
    raise "assertion failed"
  end
end

check([1, nil, 3].join("-") == "1--3", "join nil")
check([].join("-") == "", "empty")
check(["a", "b"].join == "ab", "default separator")
puts "PASS array-join"
