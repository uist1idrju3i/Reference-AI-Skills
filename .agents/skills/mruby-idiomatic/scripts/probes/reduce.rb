def check(condition, detail)
  unless condition
    puts "FAIL reduce " + detail
    raise "assertion failed"
  end
end

check([1, 2, 3].reduce(0) { |acc, v| acc + v } == 6, "sum")
check([].reduce(7) { |acc, v| acc + v } == 7, "initial")
check([].reduce { |acc, v| acc + v }.nil?, "empty without initial")
puts "PASS reduce"
