def check(condition, detail)
  unless condition
    puts "FAIL define-method " + detail
    raise "assertion failed"
  end
end

class Dynamic
  define_method(:twice) { |v| v.nil? ? 0 : v * 2 }
end
check(Dynamic.new.twice(3) == 6, "defined method")
check(Dynamic.new.twice(nil) == 0, "nil")
puts "PASS define-method"
