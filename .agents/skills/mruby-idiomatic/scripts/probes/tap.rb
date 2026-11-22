def check(condition, detail)
  unless condition
    puts "FAIL tap " + detail
    raise "assertion failed"
  end
end

seen = []
source = [1]
result = source.tap { |v| seen << v[0] }
check(result == source && seen == [1], "tap return and effect")
check(nil.tap { |v| check(v.nil?, "nil yielded") }.nil?, "nil return")
check([].tap { |v| check(v == [], "empty yielded") } == [], "empty return")
puts "PASS tap"
