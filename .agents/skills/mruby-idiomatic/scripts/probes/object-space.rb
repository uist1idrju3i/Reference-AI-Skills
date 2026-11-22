def check(condition, detail)
  unless condition
    puts "FAIL object-space " + detail
    raise "assertion failed"
  end
end

value = []
found = false
ObjectSpace.each_object(Array) { |object| found = true if object.equal?(value) }
check(found, "allocated array enumerated")
puts "PASS object-space"
