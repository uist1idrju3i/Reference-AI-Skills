def check(condition, detail)
  unless condition
    puts "FAIL map " + detail
    raise "assertion failed"
  end
end

check([1, nil, 3].map { |v| v.nil? ? 0 : v * 2 } == [2, 0, 6], "transform nil")
check([].map { |v| v } == [], "empty")
puts "PASS map"
