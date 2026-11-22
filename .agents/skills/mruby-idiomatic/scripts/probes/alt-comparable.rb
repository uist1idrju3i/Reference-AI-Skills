def check(condition, detail)
  unless condition
    puts "FAIL alt-comparable " + detail
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

module OrderedValue
  def <(other)
    @value < other.value
  end
  def ==(other)
    other.is_a?(Score) && @value == other.value
  end
  def bounded_value(low, high)
    raise ArgumentError, "invalid bounds" if low > high
    return low if @value < low
    return high if @value > high
    @value
  end
end
class Score
  include OrderedValue
  attr_reader :value
  def initialize(value)
    @value = value
  end
end
check(Score.new(1) < Score.new(2), "less")
check(Score.new(2) == Score.new(2), "equal")
check(!(Score.new(2) == nil), "nil")
check(Score.new(0).bounded_value(1, 3) == 1, "lower")
check(Score.new(4).bounded_value(1, 3) == 3, "upper")
check(Score.new(2).bounded_value(1, 3) == 2, "inside")
reject_nil { Score.new(2).bounded_value(3, 1) }
puts "PASS alt-comparable"
