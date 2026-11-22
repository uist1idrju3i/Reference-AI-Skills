def check(condition, detail)
  unless condition
    puts "FAIL hash-fetch-key-error " + detail
    raise "assertion failed"
  end
end

check({a: 3}.fetch(:a) == 3, "existing")
raised = false
begin
  {}.fetch(:missing)
rescue KeyError
  raised = true
end
check(raised, "missing raises KeyError")
puts "PASS hash-fetch-key-error"
