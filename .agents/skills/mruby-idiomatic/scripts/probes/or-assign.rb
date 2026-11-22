def check(condition, detail)
  unless condition
    puts "FAIL or-assign " + detail
    raise "assertion failed"
  end
end

a = nil
a ||= 3
check(a == 3, "nil replaced")
a = false
a ||= 4
check(a == 4, "false replaced")
a = 0
a ||= 5
check(a == 0, "zero preserved")
a = ""
a ||= "x"
check(a == "", "empty preserved")
puts "PASS or-assign"
