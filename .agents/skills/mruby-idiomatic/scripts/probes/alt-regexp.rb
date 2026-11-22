def check(condition, detail)
  unless condition
    puts "FAIL alt-regexp " + detail
    raise "assertion failed"
  end
end

def literal_ab_index(text)
  return nil if text.nil?
  text.index("ab")
end
check(literal_ab_index("zab") == 1, "literal substring")
check(literal_ab_index("").nil?, "empty")
check(literal_ab_index(nil).nil?, "nil")
check(literal_ab_index("zzz").nil?, "nonmatch")
puts "PASS alt-regexp"
