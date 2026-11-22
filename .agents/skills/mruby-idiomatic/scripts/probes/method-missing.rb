def check(condition, detail)
  unless condition
    puts "FAIL method-missing " + detail
    raise "assertion failed"
  end
end

class Dynamic
  def method_missing(name, *args)
    [name, args]
  end
end
check(Dynamic.new.unknown(3) == [:unknown, [3]], "missing method dispatch")
check(Dynamic.new.empty == [:empty, []], "empty args")
check(Dynamic.new.unknown(nil) == [:unknown, [nil]], "nil arg")
puts "PASS method-missing"
