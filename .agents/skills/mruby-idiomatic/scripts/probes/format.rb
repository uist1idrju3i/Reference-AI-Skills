def check(condition, detail)
  unless condition
    puts "FAIL format " + detail
    raise "assertion failed"
  end
end

check(format("%s:%02d", "x", 3) == "x:03", "formatted")
check(format("%s", "") == "", "empty")
check(format("%s", nil) == "", "nil")
puts "PASS format"
