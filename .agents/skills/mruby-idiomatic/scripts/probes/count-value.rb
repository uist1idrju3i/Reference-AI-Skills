def check(condition, detail)
  unless condition
    puts "FAIL count-value " + detail
    raise "assertion failed"
  end
end

check([1, nil, 1].count(1) == 2, "value matches")
check([1, nil].count(nil) == 1, "nil matches")
check([].count(1) == 0, "empty")
puts "PASS count-value"
