def check(condition, detail)
  unless condition
    puts "FAIL symbol-empty-string " + detail
    raise "assertion failed"
  end
end

value = "".to_sym
check(value.to_s == "", "empty symbol string")
puts "PASS symbol-empty-string"
