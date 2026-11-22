def check(condition, detail)
  unless condition
    puts "FAIL hash-to-a " + detail
    raise "assertion failed"
  end
end

check({a: 1, b: nil}.to_a == [[:a, 1], [:b, nil]], "pairs")
check({}.to_a == [], "empty")
puts "PASS hash-to-a"
