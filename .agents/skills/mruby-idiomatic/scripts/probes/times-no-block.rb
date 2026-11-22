def check(condition, detail)
  unless condition
    puts "FAIL times-no-block " + detail
    raise "assertion failed"
  end
end

check(3.times.to_a == [0, 1, 2], "blockless Enumerator")
check(0.times.to_a == [], "empty Enumerator")
puts "PASS times-no-block"
