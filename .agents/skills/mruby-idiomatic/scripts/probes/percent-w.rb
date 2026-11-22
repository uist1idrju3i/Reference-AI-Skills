def check(condition, detail)
  unless condition
    puts "FAIL percent-w " + detail
    raise "assertion failed"
  end
end

check(%w[one two] == ["one", "two"], "word array")
check(%w[] == [], "empty")
puts "PASS percent-w"
