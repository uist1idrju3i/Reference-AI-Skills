def check(condition, detail)
  unless condition
    puts "FAIL class-variable " + detail
    raise "assertion failed"
  end
end

class Counter
  @@count = 0
  def increment
    @@count += 1
  end
  def count
    @@count
  end
end
check(Counter.new.count == 0, "initial")
check(Counter.new.increment == 1 && Counter.new.count == 1, "shared across instances")
puts "PASS class-variable"
