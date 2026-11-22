def check(condition, detail)
  unless condition
    puts "FAIL public-send " + detail
    raise "assertion failed"
  end
end

check("abc".public_send(:size) == 3, "public send")
check("".public_send(:size) == 0, "empty")
check(nil.public_send(:nil?), "nil receiver")
puts "PASS public-send"
