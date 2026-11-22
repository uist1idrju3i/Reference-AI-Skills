def check(condition, detail)
  unless condition
    puts "FAIL large-integer-literal " + detail
    raise "assertion failed"
  end
end

check(2147483648.to_s == "2147483648", "literal beyond int32")
check(0.to_s == "0", "zero literal")
puts "PASS large-integer-literal"
