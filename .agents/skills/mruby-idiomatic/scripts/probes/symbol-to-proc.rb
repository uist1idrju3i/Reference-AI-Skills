def check(condition, detail)
  unless condition
    puts "FAIL symbol-to-proc " + detail
    raise "assertion failed"
  end
end

check([1, nil].map(&:to_s) == ["1", ""], "symbol block conversion")
check([].map(&:to_s) == [], "empty")
puts "PASS symbol-to-proc"
