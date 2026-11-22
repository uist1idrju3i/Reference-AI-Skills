def check(condition, detail)
  unless condition
    puts "FAIL reject " + detail
    raise "assertion failed"
  end
end

check([1, nil, 2].reject { |v| v.nil? } == [1, 2], "reject")
check([].reject { true } == [], "empty")
check([nil].reject { |v| v } == [nil], "nil falsey")
puts "PASS reject"
