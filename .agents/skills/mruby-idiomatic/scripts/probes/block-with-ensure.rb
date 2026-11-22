def check(condition, detail)
  unless condition
    puts "FAIL block-with-ensure " + detail
    raise "assertion failed"
  end
end

class Resource
  attr_reader :closed
  def initialize
    @closed = false
  end
  def close
    @closed = true
  end
  def open
    yield self
  ensure
    close
  end
end
r = Resource.new
check(r.open { |value| value == r ? 7 : 0 } == 7 && r.closed, "normal close")
r = Resource.new
begin
  r.open { raise ArgumentError, "bad" }
rescue ArgumentError
end
check(r.closed, "exception close")
r = Resource.new
check(r.open { nil }.nil? && r.closed, "nil result close")
puts "PASS block-with-ensure"
