def check(condition, detail)
  unless condition
    puts "FAIL string-rjust " + detail
    raise "assertion failed"
  end
end

check("a".rjust(3, "-") == "--a", "padding")
check("".rjust(2, "-") == "--", "empty")
check("long".rjust(2) == "long", "no truncation")
puts "PASS string-rjust"
