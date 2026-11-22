def check(condition, detail)
  unless condition
    puts "FAIL range-each " + detail
    raise "assertion failed"
  end
end

seen = []
(1..3).each { |v| seen << v }
check(seen == [1, 2, 3], "inclusive")
seen = []
(1...1).each { |v| seen << v }
check(seen == [], "empty")
puts "PASS range-each"
