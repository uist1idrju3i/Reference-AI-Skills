def check(condition, detail)
  unless condition
    puts "FAIL array-dig " + detail
    raise "assertion failed"
  end
end

check([[3]].dig(0, 0) == 3, "nested")
check([].dig(0, 0).nil?, "empty")
check([nil].dig(0, 0).nil?, "nil intermediate")
puts "PASS array-dig"
