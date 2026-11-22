def check(condition, detail)
  unless condition
    puts "FAIL and-assign " + detail
    raise "assertion failed"
  end
end

a = nil
a &&= 3
check(a.nil?, "nil preserved")
a = false
a &&= 4
check(a == false, "false preserved")
a = 0
a &&= 5
check(a == 5, "zero truthy")
a = ""
a &&= "x"
check(a == "x", "empty truthy")
puts "PASS and-assign"
