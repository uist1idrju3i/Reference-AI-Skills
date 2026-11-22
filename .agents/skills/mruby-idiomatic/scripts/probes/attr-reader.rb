def check(condition, detail)
  unless condition
    puts "FAIL attr-reader " + detail
    raise "assertion failed"
  end
end

class Record
  attr_reader :value
  def initialize(value)
    @value = value
  end
end
check(Record.new(3).value == 3, "reader")
check(Record.new(nil).value.nil?, "nil reader")
puts "PASS attr-reader"
