def check(condition, detail)
  unless condition
    puts "FAIL safe-navigation " + detail
    raise "assertion failed"
  end
end

check(nil&.size == nil, "nil skips call")
check(""&.size == 0 && "abc"&.size == 3, "empty and normal")
raised = false
begin
  false&.no_such_probe_method
rescue NoMethodError
  raised = true
end
check(raised, "false does not skip call")
puts "PASS safe-navigation"
