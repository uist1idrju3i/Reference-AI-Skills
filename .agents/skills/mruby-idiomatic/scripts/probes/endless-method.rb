def check(condition, detail)
  unless condition
    puts "FAIL endless-method " + detail
    raise "assertion failed"
  end
end

def twice(v) = v.nil? ? 0 : v * 2
check(twice(3) == 6, "endless method")
check(twice(nil) == 0, "nil")
puts "PASS endless-method"
