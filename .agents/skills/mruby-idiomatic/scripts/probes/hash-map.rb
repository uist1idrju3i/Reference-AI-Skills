def check(condition, detail)
  unless condition
    puts "FAIL hash-map " + detail
    raise "assertion failed"
  end
end

check({a: 1, b: nil}.map { |k, v| [k, v] } == [[:a, 1], [:b, nil]], "map pairs")
check({}.map { |k, v| k } == [], "empty")
puts "PASS hash-map"
