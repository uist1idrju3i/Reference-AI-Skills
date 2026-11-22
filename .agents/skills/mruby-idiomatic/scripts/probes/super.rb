def check(condition, detail)
  unless condition
    puts "FAIL super " + detail
    raise "assertion failed"
  end
end

class Parent
  def value(v)
    v.nil? ? 0 : v
  end
end
class Child < Parent
  def value(v)
    super(v) + 1
  end
end
check(Child.new.value(2) == 3, "explicit super")
check(Child.new.value(nil) == 1, "nil")
puts "PASS super"
