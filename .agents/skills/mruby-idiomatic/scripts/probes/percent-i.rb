def check(condition, detail)
  unless condition
    puts "FAIL percent-i " + detail
    raise "assertion failed"
  end
end

check(%i[one two] == [:one, :two], "symbol array")
check(%i[] == [], "empty")
puts "PASS percent-i"
