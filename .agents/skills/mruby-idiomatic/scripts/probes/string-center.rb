def check(condition, detail)
  unless condition
    puts "FAIL string-center " + detail
    raise "assertion failed"
  end
end

check("a".center(3, "-") == "-a-", "padding")
check("".center(2, "-") == "--", "empty")
check("long".center(2) == "long", "no truncation")
puts "PASS string-center"
