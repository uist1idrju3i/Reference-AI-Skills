def check(condition, detail)
  unless condition
    puts "FAIL default-args " + detail
    raise "assertion failed"
  end
end

def value(a = 7, b = 2)
  [a, b]
end
check(value == [7, 2], "defaults")
check(value(nil) == [nil, 2], "explicit nil")
check(value(3, 4) == [3, 4], "override")
puts "PASS default-args"
