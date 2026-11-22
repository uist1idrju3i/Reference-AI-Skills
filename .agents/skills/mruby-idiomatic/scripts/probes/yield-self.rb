def check(condition, detail)
  unless condition
    puts "FAIL yield-self " + detail
    raise "assertion failed"
  end
end

check(3.yield_self { |v| v * 2 } == 6, "yield_self value")
check(nil.yield_self { |v| v.nil? }, "nil yielded")
check([].yield_self { |v| v.size } == 0, "empty")
puts "PASS yield-self"
