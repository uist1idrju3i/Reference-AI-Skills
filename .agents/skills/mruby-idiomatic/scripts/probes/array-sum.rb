def check(condition, detail)
  unless condition
    puts "FAIL array-sum " + detail
    raise "assertion failed"
  end
end

check([1, 2, 3].sum == 6, "sum")
check([].sum == 0, "empty")
check([nil, 2].sum(1) { |v| v.nil? ? 0 : v } == 3, "initial and nil transform")
puts "PASS array-sum"
