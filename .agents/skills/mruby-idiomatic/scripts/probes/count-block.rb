def check(condition, detail)
  unless condition
    puts "FAIL count-block " + detail
    raise "assertion failed"
  end
end

check([1, nil, 2].count { |v| !v.nil? } == 2, "predicate")
check([nil].count { |v| v } == 0, "falsey")
check([].count { true } == 0, "empty")
puts "PASS count-block"
