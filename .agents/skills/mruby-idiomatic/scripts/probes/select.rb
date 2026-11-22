def check(condition, detail)
  unless condition
    puts "FAIL select " + detail
    raise "assertion failed"
  end
end

check([1, nil, 2].select { |v| !v.nil? } == [1, 2], "select")
check([].select { true } == [], "empty")
check([nil].select { |v| v } == [], "nil falsey")
puts "PASS select"
