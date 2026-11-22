def check(condition, detail)
  unless condition
    puts "FAIL alt-lambda " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

callback = Proc.new { |value| value.nil? ? 0 : value + 1 }
check(callback.call(2) == 3, "callback")
check(callback.call(nil) == 0, "nil value")
check([].map { |value| callback.call(value) } == [], "empty")
puts "PASS alt-lambda"
