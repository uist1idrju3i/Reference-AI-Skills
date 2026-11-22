def check(condition, detail)
  unless condition
    puts "FAIL integer-clamp " + detail
    raise "assertion failed"
  end
end

check(0.clamp(1, 3) == 1, "lower")
check(2.clamp(1, 3) == 2, "inside")
check(4.clamp(1, 3) == 3, "upper")
raised = false
begin
  2.clamp(3, 1)
rescue ArgumentError
  raised = true
end
check(raised, "invalid bounds")
puts "PASS integer-clamp"
