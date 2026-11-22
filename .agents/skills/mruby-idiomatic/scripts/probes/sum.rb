def check(condition, detail)
  unless condition
    puts "FAIL sum " + detail
    raise "assertion failed"
  end
end

check((1..3).sum == 6, "range sum")
check((1...1).sum == 0, "empty sum")
check((1..2).sum(5) { |v| v * 2 } == 11, "initial and transform")
puts "PASS sum"
