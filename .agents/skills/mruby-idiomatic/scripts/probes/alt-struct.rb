def check(condition, detail)
  unless condition
    puts "FAIL alt-struct " + detail
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

class Reading
  attr_accessor :value
  def initialize(value = nil)
    @value = value
  end
end
check(Reading.new(2).value == 2, "explicit class")
check(Reading.new.value.nil?, "unset")
item = Reading.new("")
item.value = false
check(item.value == false, "setter")
puts "PASS alt-struct"
