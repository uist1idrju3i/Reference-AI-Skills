def check(condition, detail)
  unless condition
    puts "FAIL to-enum " + detail
    raise "assertion failed"
  end
end

check([1, nil].to_enum.to_a == [1, nil], "Enumerator values")
check([].to_enum.to_a == [], "empty")
puts "PASS to-enum"
