def check(condition, detail)
  unless condition
    puts "FAIL yield " + detail
    raise "assertion failed"
  end
end

def forward(value)
  yield value
end
check(forward(3) { |v| v * 2 } == 6, "yield result")
check(forward(nil) { |v| v }.nil?, "nil")
puts "PASS yield"
