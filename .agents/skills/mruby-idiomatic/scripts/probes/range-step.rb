def check(condition, detail)
  unless condition
    puts "FAIL range-step " + detail
    raise "assertion failed"
  end
end

seen = []
(1..5).step(2) { |v| seen << v }
check(seen == [1, 3, 5], "stepped")
seen = []
(1...1).step(2) { |v| seen << v }
check(seen == [], "empty")
puts "PASS range-step"
