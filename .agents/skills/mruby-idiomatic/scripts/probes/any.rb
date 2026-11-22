def check(condition, detail)
  unless condition
    puts "FAIL any " + detail
    raise "assertion failed"
  end
end

check([nil, false, 0].any? { |v| v }, "zero truthy")
check([nil, false].any? { |v| v } == false, "falsey")
check([].any? { true } == false, "empty")
puts "PASS any"
