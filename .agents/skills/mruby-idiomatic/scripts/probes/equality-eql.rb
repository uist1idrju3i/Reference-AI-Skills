def check(condition, detail)
  unless condition
    puts "FAIL equality-eql " + detail
    raise "assertion failed"
  end
end

check(1 == 1.0, "numeric equality")
check(1.eql?(1.0) == false, "strict equality")
check(nil.eql?(nil) && ([] == []), "nil and empty")
puts "PASS equality-eql"
