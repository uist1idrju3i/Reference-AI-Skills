def check(condition, detail)
  unless condition
    puts "FAIL it-block-param " + detail
    raise "assertion failed"
  end
end

check([1, nil].map { it.nil? ? 0 : it * 2 } == [2, 0], "implicit it")
check([].map { it } == [], "empty")
puts "PASS it-block-param"
