def check(condition, detail)
  unless condition
    puts "FAIL comparable " + detail
    raise "assertion failed"
  end
end

class Score
  include Comparable
  def initialize(value)
    @value = value
  end
  attr_reader :value
  def <=>(other)
    return nil unless other.is_a?(Score)
    @value <=> other.value
  end
end
check(Score.new(1) < Score.new(2), "less")
check(Score.new(2) == Score.new(2), "equal")
check((Score.new(2) == nil) == false, "unrelated")
puts "PASS comparable"
