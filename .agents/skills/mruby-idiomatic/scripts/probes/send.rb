def check(condition, detail)
  unless condition
    puts "FAIL send " + detail
    raise "assertion failed"
  end
end

check("abc".send(:size) == 3, "dynamic send")
check("".send(:size) == 0, "empty")
check(nil.send(:nil?), "nil receiver")
puts "PASS send"
