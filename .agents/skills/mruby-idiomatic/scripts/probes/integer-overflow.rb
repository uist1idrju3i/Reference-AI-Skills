def check(condition, detail)
  unless condition
    puts "FAIL integer-overflow " + detail
    raise "assertion failed"
  end
end

n = 2147483647
result = n + 1
check(result.to_s == "2147483648", "int32 overflow lost precision: " + result.to_s)
check((0 + 0) == 0, "zero")
puts "PASS integer-overflow"
