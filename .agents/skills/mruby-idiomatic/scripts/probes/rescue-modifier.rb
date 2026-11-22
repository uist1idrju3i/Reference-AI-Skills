def check(condition, detail)
  unless condition
    puts "FAIL rescue-modifier " + detail
    raise "assertion failed"
  end
end

def broken
  raise ArgumentError, "bad"
end
value = broken rescue :fallback
check(value == :fallback, "exception fallback")
value = nil rescue :fallback
check(value.nil?, "nil is not exception")
value = 3 rescue :fallback
check(value == 3, "normal")
puts "PASS rescue-modifier"
