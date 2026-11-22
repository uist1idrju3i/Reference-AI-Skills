def check(condition, detail)
  unless condition
    puts "FAIL alt-class-variable " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

class Counter
  attr_reader :value
  def initialize
    @value = 0
  end
  def increment
    @value += 1
  end
end
shared = Counter.new
check(shared.value == 0, "initial")
a = shared
b = shared
a.increment
check(b.value == 1, "explicit shared owner")
check(Counter.new.value == 0, "independent owner")
puts "PASS alt-class-variable"
