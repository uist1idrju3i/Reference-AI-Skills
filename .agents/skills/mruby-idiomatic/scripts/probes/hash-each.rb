def check(condition, detail)
  unless condition
    puts "FAIL hash-each " + detail
    raise "assertion failed"
  end
end

seen = []
source = {a: 1, b: nil}
result = source.each { |k, v| seen << [k, v] }
check(seen == [[:a, 1], [:b, nil]] && result == source, "pairs and return")
{}.each { seen << 99 }
check(seen.size == 2, "empty")
puts "PASS hash-each"
