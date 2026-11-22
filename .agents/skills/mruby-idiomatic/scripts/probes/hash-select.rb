def check(condition, detail)
  unless condition
    puts "FAIL hash-select " + detail
    raise "assertion failed"
  end
end

check({a: 1, b: nil}.select { |k, v| !v.nil? } == {a: 1}, "select pairs")
check({}.select { true } == {}, "empty")
puts "PASS hash-select"
