def check(condition, detail)
  unless condition
    puts "FAIL then " + detail
    raise "assertion failed"
  end
end

check(3.then { |v| v * 2 } == 6, "then value")
check(nil.then { |v| v.nil? }, "nil yielded")
check([].then { |v| v.size } == 0, "empty")
puts "PASS then"
