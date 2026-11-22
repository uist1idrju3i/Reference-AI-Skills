def check(condition, detail)
  unless condition
    puts "FAIL raise-class-message " + detail
    raise "assertion failed"
  end
end

message = nil
begin
  raise ArgumentError, "bad input"
rescue ArgumentError => error
  message = error.message
end
check(message == "bad input", "class and message")
puts "PASS raise-class-message"
