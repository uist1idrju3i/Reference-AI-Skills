def check(condition, detail)
  unless condition
    puts "FAIL symbol-empty-conversion " + detail
    raise "assertion failed"
  end
end

"".to_sym
puts "PASS symbol-empty-conversion"
