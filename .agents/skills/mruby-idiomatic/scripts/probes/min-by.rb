def check(condition, detail)
  unless condition
    puts "FAIL min-by " + detail
    raise "assertion failed"
  end
end

check(["bbb", "", "aa"].min_by { |v| v.size } == "", "minimum")
check([].min_by { |v| v }.nil?, "empty")
puts "PASS min-by"
