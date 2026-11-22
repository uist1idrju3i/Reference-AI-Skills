def check(condition, detail)
  unless condition
    puts "FAIL regexp " + detail
    raise "assertion failed"
  end
end

check(/ab/ =~ "zab", "match")
check((/ab/ =~ "").nil?, "empty nonmatch")
check((/ab/ =~ nil).nil?, "nil nonmatch")
puts "PASS regexp"
