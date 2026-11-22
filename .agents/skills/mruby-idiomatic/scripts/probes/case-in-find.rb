def check(condition, detail)
  unless condition
    puts "FAIL case-in-find " + detail
    raise "assertion failed"
  end
end

def match(value)
  case value
  in [*, 2, a, *] then a
  else nil
  end
end
check(match([0, 2, 3, 4]) == 3, "find middle")
check(match([]).nil?, "empty")
check(match(nil).nil?, "nil")
puts "PASS case-in-find"
