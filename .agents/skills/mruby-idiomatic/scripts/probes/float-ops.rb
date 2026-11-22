def check(condition, detail)
  unless condition
    puts "FAIL float-ops " + detail
    raise "assertion failed"
  end
end

check((1.5 + 2.25) == 3.75, "addition")
check((3.0 / 2.0) == 1.5, "division")
check((0.0 * 1.5) == 0.0, "zero")
puts "PASS float-ops"
