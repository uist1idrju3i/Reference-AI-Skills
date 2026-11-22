def check(condition, detail)
  unless condition
    puts "FAIL loop-break " + detail
    raise "assertion failed"
  end
end

n = 0
result = loop do
  n += 1
  break :done if n == 3
end
check(n == 3 && result == :done, "loop break result")
check(loop { break nil }.nil?, "nil break")
puts "PASS loop-break"
