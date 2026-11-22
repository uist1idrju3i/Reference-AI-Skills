def check(condition, detail)
  unless condition
    puts "FAIL catch-throw " + detail
    raise "assertion failed"
  end
end

check(catch(:done) { throw :done, 7; 0 } == 7, "throw value")
check(catch(:done) { throw :done }.nil?, "nil throw")
check(catch(:done) { 3 } == 3, "normal result")
puts "PASS catch-throw"
