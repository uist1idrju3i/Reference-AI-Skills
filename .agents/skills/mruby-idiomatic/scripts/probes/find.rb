def check(condition, detail)
  unless condition
    puts "FAIL find " + detail
    raise "assertion failed"
  end
end

check([nil, 2, 3].find { |v| !v.nil? } == 2, "first match")
check([].find { true }.nil?, "empty")
check([1].find { false }.nil?, "no match")
puts "PASS find"
