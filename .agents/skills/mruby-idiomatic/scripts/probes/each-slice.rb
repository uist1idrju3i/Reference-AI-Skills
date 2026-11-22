def check(condition, detail)
  unless condition
    puts "FAIL each-slice " + detail
    raise "assertion failed"
  end
end

seen = []
[1, nil, 3].each_slice(2) { |slice| seen << slice }
check(seen == [[1, nil], [3]], "partial last slice")
seen = []
[].each_slice(2) { |slice| seen << slice }
check(seen == [], "empty")
raised = false
begin
  [1].each_slice(0) { |slice| slice }
rescue ArgumentError
  raised = true
end
check(raised, "zero size rejected")
puts "PASS each-slice"
