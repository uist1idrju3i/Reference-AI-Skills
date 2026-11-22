def check(condition, detail)
  unless condition
    puts "FAIL guard-clause " + detail
    raise "assertion failed"
  end
end

def label(value)
  return :missing if value.nil?
  return :empty unless value != ""
  :present
end
check(label(nil) == :missing, "nil guard")
check(label("") == :empty, "unless guard")
check(label("x") == :present, "normal value")
value = 0
value = 1 if false
value = 2 unless true
check(value == 0, "modifier conditions")
puts "PASS guard-clause"
