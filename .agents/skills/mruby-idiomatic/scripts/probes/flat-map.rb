def check(condition, detail)
  unless condition
    puts "FAIL flat-map " + detail
    raise "assertion failed"
  end
end

check([1, nil].flat_map { |v| [v, v] } == [1, 1, nil, nil], "one level flatten")
check([].flat_map { |v| [v] } == [], "empty")
puts "PASS flat-map"
