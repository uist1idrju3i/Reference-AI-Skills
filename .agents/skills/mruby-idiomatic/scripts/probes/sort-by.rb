def check(condition, detail)
  unless condition
    puts "FAIL sort-by " + detail
    raise "assertion failed"
  end
end

check(["bbb", "", "aa"].sort_by { |v| v.size } == ["", "aa", "bbb"], "key sort")
check([].sort_by { |v| v } == [], "empty")
puts "PASS sort-by"
