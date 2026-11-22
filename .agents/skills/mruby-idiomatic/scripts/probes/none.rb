def check(condition, detail)
  unless condition
    puts "FAIL none " + detail
    raise "assertion failed"
  end
end

check([nil, false].none? { |v| v }, "falsey")
check([0].none? { |v| v } == false, "zero truthy")
check([].none? { true }, "empty")
puts "PASS none"
