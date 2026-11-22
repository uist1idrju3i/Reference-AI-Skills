def check(condition, detail)
  unless condition
    puts "FAIL all " + detail
    raise "assertion failed"
  end
end

check([1, 0].all? { |v| v }, "truthy")
check([1, nil].all? { |v| v } == false, "nil")
check([].all? { false }, "empty")
puts "PASS all"
