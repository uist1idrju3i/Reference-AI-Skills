def check(condition, detail)
  unless condition
    puts "FAIL keyword-required " + detail
    raise "assertion failed"
  end
end

def keyword(value:)
  value
end
check(keyword(value: 3) == 3 && keyword(value: nil).nil?, "required keyword")
raised = false
begin
  keyword
rescue ArgumentError
  raised = true
end
check(raised, "missing required rejected")
puts "PASS keyword-required"
