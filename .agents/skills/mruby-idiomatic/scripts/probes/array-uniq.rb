def check(condition, detail)
  unless condition
    puts "FAIL array-uniq " + detail
    raise "assertion failed"
  end
end

check([1, nil, 1, nil, false].uniq == [1, nil, false], "stable unique")
check([].uniq == [], "empty")
puts "PASS array-uniq"
