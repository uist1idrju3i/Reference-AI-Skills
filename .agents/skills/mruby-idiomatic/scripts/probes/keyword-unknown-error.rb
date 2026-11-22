def check(condition, detail)
  unless condition
    puts "FAIL keyword-unknown-error " + detail
    raise "assertion failed"
  end
end

def keyword(value: 7)
  value
end
check(keyword(value: 3) == 3, "known keyword")
raised = false
begin
  keyword(unknown: 1)
rescue ArgumentError
  raised = true
end
check(raised, "unknown keyword must raise ArgumentError")
puts "PASS keyword-unknown-error"
