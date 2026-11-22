def check(condition, detail)
  unless condition
    puts "FAIL retry " + detail
    raise "assertion failed"
  end
end

attempts = 0
begin
  attempts += 1
  raise ArgumentError, "again" if attempts < 2
rescue ArgumentError
  retry
end
check(attempts == 2, "bounded retry")
puts "PASS retry"
