def check(condition, detail)
  unless condition
    puts "FAIL keyword-default " + detail
    raise "assertion failed"
  end
end

def keyword(value: 7)
  value
end
check(keyword == 7, "default")
check(keyword(value: 2) == 2, "override")
check(keyword(value: nil).nil?, "explicit nil")
puts "PASS keyword-default"
