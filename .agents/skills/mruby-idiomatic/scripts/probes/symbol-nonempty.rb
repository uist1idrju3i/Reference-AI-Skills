def check(condition, detail)
  unless condition
    puts "FAIL symbol-nonempty " + detail
    raise "assertion failed"
  end
end

check(:ruby == "ruby".to_sym, "symbol conversion")
check(:ruby.to_s == "ruby", "symbol string")
puts "PASS symbol-nonempty"
