def check(condition, detail)
  unless condition
    puts "FAIL hash-fetch-default " + detail
    raise "assertion failed"
  end
end

h = {a: nil, b: 3}
check(h.fetch(:b, 7) == 3, "existing")
check(h.fetch(:a, 7).nil?, "stored nil")
check({}.fetch(:missing, 7) == 7, "default")
puts "PASS hash-fetch-default"
