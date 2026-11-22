def check(condition, detail)
  unless condition
    puts "FAIL zip " + detail
    raise "assertion failed"
  end
end

check([1, 2].zip([3]) == [[1, 3], [2, nil]], "padding")
check([].zip([1]) == [], "empty receiver")
check([nil].zip([]) == [[nil, nil]], "nil")
puts "PASS zip"
