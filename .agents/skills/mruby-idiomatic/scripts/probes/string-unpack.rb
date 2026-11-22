def check(condition, detail)
  unless condition
    puts "FAIL string-unpack " + detail
    raise "assertion failed"
  end
end

check("AZ".unpack("C*") == [65, 90], "unpack")
check("".unpack("C*") == [], "empty")
puts "PASS string-unpack"
