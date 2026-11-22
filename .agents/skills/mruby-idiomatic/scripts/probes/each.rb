def check(condition, detail)
  unless condition
    puts "FAIL each " + detail
    raise "assertion failed"
  end
end

seen = []
source = [1, nil, 3]
result = source.each { |v| seen << v }
check(seen == source && result == source, "values and return")
[].each { seen << 99 }
check(seen == [1, nil, 3], "empty")
puts "PASS each"
