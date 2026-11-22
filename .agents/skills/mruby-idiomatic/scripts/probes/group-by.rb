def check(condition, detail)
  unless condition
    puts "FAIL group-by " + detail
    raise "assertion failed"
  end
end

check([1, 2, 3].group_by { |v| v % 2 } == {1 => [1, 3], 0 => [2]}, "groups")
check([].group_by { |v| v } == {}, "empty")
check([nil].group_by { |v| v } == {nil => [nil]}, "nil key")
puts "PASS group-by"
