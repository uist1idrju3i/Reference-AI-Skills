def check(condition, detail)
  unless condition
    puts "FAIL string-getbyte " + detail
    raise "assertion failed"
  end
end

check("AZ".getbyte(0) == 65 && "AZ".getbyte(-1) == 90, "indices")
check("".getbyte(0).nil? && "A".getbyte(9).nil?, "out of bounds")
puts "PASS string-getbyte"
