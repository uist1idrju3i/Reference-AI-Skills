def check(condition, detail)
  unless condition
    puts "FAIL integer-digits " + detail
    raise "assertion failed"
  end
end

check(123.digits == [3, 2, 1], "decimal digits")
check(0.digits == [0], "zero")
check(10.digits(2) == [0, 1, 0, 1], "base two")
puts "PASS integer-digits"
