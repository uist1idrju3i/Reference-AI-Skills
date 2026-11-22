def check(condition, detail)
  unless condition
    puts "FAIL alt-it-block-param " + detail
    raise "assertion failed"
  end
end

check([1, nil].map { |value| value.nil? ? 0 : value * 2 } == [2, 0], "explicit parameter")
check([].map { |value| value } == [], "empty")
puts "PASS alt-it-block-param"
