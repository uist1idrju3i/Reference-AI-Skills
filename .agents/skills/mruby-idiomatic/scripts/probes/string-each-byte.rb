def check(condition, detail)
  unless condition
    puts "FAIL string-each-byte " + detail
    raise "assertion failed"
  end
end

seen = []
"AZ".each_byte { |v| seen << v }
check(seen == [65, 90], "bytes")
"".each_byte { seen << 99 }
check(seen == [65, 90], "empty")
puts "PASS string-each-byte"
