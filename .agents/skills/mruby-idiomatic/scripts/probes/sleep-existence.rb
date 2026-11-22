def check(condition, detail)
  unless condition
    puts "FAIL sleep-existence " + detail
    raise "assertion failed"
  end
end

check(respond_to?(:sleep), "sleep missing")
check(respond_to?(:sleep_ms), "sleep_ms missing")
puts "PASS sleep-existence"
