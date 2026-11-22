def check(condition, detail)
  unless condition
    puts "FAIL sprintf " + detail
    raise "assertion failed"
  end
end

check(sprintf("%s:%02d", "x", 3) == "x:03", "formatted")
check(sprintf("%s", "") == "", "empty")
check(sprintf("%s", nil) == "", "nil")
puts "PASS sprintf"
