def check(condition, detail)
  unless condition
    puts "FAIL block-given " + detail
    raise "assertion failed"
  end
end

def supplied
  block_given?
end
check(supplied { nil } == true, "with block")
check(supplied == false, "without block")
puts "PASS block-given"
