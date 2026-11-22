def check(condition, detail)
  unless condition
    puts "FAIL lambda " + detail
    raise "assertion failed"
  end
end

fn = lambda { |v| v.nil? ? "" : v * 2 }
check(fn.call(3) == 6 && fn.call(nil) == "", "lambda call")
raised = false
begin
  fn.call
rescue ArgumentError
  raised = true
end
check(raised, "strict lambda arity")
puts "PASS lambda"
