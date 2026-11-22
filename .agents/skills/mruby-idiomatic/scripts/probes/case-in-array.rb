def check(condition, detail)
  unless condition
    puts "FAIL case-in-array " + detail
    raise "assertion failed"
  end
end

def match(value)
  case value
  in [a, b] then [b, a]
  else nil
  end
end
check(match([1, 2]) == [2, 1], "array destructuring")
check(match([]).nil?, "empty nonmatch")
check(match(nil).nil?, "nil nonmatch")
puts "PASS case-in-array"
