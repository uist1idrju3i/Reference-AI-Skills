def check(condition, detail)
  unless condition
    puts "FAIL times-block " + detail
    raise "assertion failed"
  end
end

values = []
result = 3.times { |n| values << n }
check(values == [0, 1, 2] && result == 3, "times values and return")
0.times { values << 99 }
(-1).times { values << 99 }
check(values == [0, 1, 2], "zero and negative")
puts "PASS times-block"
