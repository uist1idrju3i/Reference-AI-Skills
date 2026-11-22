def check(condition, detail)
  unless condition
    puts "FAIL string-bytes " + detail
    raise "assertion failed"
  end
end

check("AZ".bytes == [65, 90], "byte array")
check("".bytes == [], "empty")
puts "PASS string-bytes"
