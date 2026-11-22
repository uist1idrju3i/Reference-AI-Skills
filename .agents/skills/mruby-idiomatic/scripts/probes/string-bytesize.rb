def check(condition, detail)
  unless condition
    puts "FAIL string-bytesize " + detail
    raise "assertion failed"
  end
end

check("abc".bytesize == 3, "ASCII")
check("".bytesize == 0, "empty")
check("あ".bytesize == 3, "UTF-8 byte count")
puts "PASS string-bytesize"
