def check(condition, detail)
  unless condition
    puts "FAIL freeze-frozen " + detail
    raise "assertion failed"
  end
end

a = [1]
check(a.frozen? == false, "initial")
check(a.freeze == a && a.frozen?, "freeze")
raised = false
begin
  a << 2
rescue StandardError
  raised = true
end
check(raised && a == [1], "frozen array rejects mutation")
puts "PASS freeze-frozen"
