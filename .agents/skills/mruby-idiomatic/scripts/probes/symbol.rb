def check(condition, detail)
  unless condition
    puts "FAIL symbol " + detail
    raise "assertion failed"
  end
end

check(:ruby == "ruby".to_sym, "symbol conversion")
check(:ruby.to_s == "ruby", "symbol string")
check("".to_sym.to_s == "", "empty symbol")
puts "PASS symbol"
