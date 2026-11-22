def check(condition, detail)
  unless condition
    puts "FAIL comparable-clamp " + detail
    raise "assertion failed"
  end
end

class Score
  include Comparable
  attr_reader :value
  def initialize(value)
    @value = value
  end
  def <=>(other)
    @value <=> other.value
  end
end
low = Score.new(1)
high = Score.new(3)
check(Score.new(0).clamp(low, high).value == 1, "lower")
check(Score.new(2).clamp(low, high).value == 2, "inside")
check(Score.new(4).clamp(low, high).value == 3, "upper")
puts "PASS comparable-clamp"
