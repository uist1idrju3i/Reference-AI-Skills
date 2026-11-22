def check(condition, detail)
  unless condition
    puts "FAIL hash-dig " + detail
    raise "assertion failed"
  end
end

check({a: {b: 3}}.dig(:a, :b) == 3, "nested")
check({}.dig(:a, :b).nil?, "missing")
check({a: nil}.dig(:a, :b).nil?, "nil intermediate")
puts "PASS hash-dig"
