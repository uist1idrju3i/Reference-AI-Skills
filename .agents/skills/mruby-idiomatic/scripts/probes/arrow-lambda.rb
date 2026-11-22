def check(condition, detail)
  unless condition
    puts "FAIL arrow-lambda " + detail
    raise "assertion failed"
  end
end

fn = ->(v) { v.nil? ? "" : v * 2 }
check(fn.call(3) == 6 && fn.call(nil) == "", "arrow call")
raised = false
begin
  fn.call
rescue ArgumentError
  raised = true
end
check(raised, "strict arrow arity")
puts "PASS arrow-lambda"
