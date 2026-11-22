def check(condition, detail)
  unless condition
    puts "FAIL partition " + detail
    raise "assertion failed"
  end
end

check([1, nil, 2].partition { |v| v.nil? } == [[nil], [1, 2]], "two partitions")
check([].partition { true } == [[], []], "empty")
puts "PASS partition"
