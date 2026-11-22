def check(condition, detail)
  unless condition
    puts "FAIL splat-multiple-assignment " + detail
    raise "assertion failed"
  end
end

def values(*items)
  items
end
check(values(1, nil, 3) == [1, nil, 3], "splat arguments")
check(values == [], "empty splat")
a, *middle, z = [1, 2, nil, 4]
check(a == 1 && middle == [2, nil] && z == 4, "multiple assignment")
a, b = []
check(a.nil? && b.nil?, "empty assignment")
puts "PASS splat-multiple-assignment"
