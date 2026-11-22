def check(condition, detail)
  unless condition
    puts "FAIL string-append " + detail
    raise "assertion failed"
  end
end

s = ""
result = s << "ab"
check(s == "ab" && result == s, "append and return")
s << ""
check(s == "ab", "empty append")
raised = false
begin
  s << nil
rescue TypeError
  raised = true
end
check(raised, "nil rejected")
puts "PASS string-append"
