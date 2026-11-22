def check(condition, detail)
  unless condition
    puts "FAIL string-ljust " + detail
    raise "assertion failed"
  end
end

check("a".ljust(3, "-") == "a--", "padding")
check("".ljust(2, "-") == "--", "empty")
check("long".ljust(2) == "long", "no truncation")
puts "PASS string-ljust"
