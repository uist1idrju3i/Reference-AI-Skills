def check(condition, detail)
  unless condition
    puts "FAIL explicit-block-param " + detail
    raise "assertion failed"
  end
end

def forward(value, &block)
  return :missing if block.nil?
  block.call(value)
end
check(forward(3) { |v| v * 2 } == 6, "explicit block call")
check(forward(nil) { |v| v }.nil?, "nil")
check(forward(3) == :missing, "no block")
puts "PASS explicit-block-param"
