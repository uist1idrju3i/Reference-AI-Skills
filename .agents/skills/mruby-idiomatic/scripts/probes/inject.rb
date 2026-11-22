def check(condition, detail)
  unless condition
    puts "FAIL inject " + detail
    raise "assertion failed"
  end
end

check([1, 2, 3].inject(0) { |acc, v| acc + v } == 6, "sum")
check([].inject(7) { |acc, v| acc + v } == 7, "initial")
check([].inject { |acc, v| acc + v }.nil?, "empty without initial")
puts "PASS inject"
