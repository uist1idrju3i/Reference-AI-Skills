def check(condition, detail)
  unless condition
    puts "FAIL fiber " + detail
    raise "assertion failed"
  end
end

f = Fiber.new do |v|
  Fiber.yield v * 2
  nil
end
check(f.resume(3) == 6, "yield")
check(f.resume.nil?, "completion")
puts "PASS fiber"
