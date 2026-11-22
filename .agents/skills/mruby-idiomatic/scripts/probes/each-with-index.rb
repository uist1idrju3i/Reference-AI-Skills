def check(condition, detail)
  unless condition
    puts "FAIL each-with-index " + detail
    raise "assertion failed"
  end
end

seen = []
source = [nil, 4]
result = source.each_with_index { |v, i| seen << [v, i] }
check(seen == [[nil, 0], [4, 1]] && result == source, "values indices return")
[].each_with_index { seen << 99 }
check(seen.size == 2, "empty")
puts "PASS each-with-index"
