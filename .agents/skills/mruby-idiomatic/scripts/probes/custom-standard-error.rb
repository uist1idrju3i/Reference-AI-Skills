def check(condition, detail)
  unless condition
    puts "FAIL custom-standard-error " + detail
    raise "assertion failed"
  end
end

class ProbeError < StandardError
end
message = nil
begin
  raise ProbeError.new("bad input")
rescue ProbeError => error
  message = error.message
end
check(message == "bad input", "subclass message")
puts "PASS custom-standard-error"
