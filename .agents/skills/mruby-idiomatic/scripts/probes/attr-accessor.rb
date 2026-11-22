def check(condition, detail)
  unless condition
    puts "FAIL attr-accessor " + detail
    raise "assertion failed"
  end
end

class Record
  attr_accessor :value
end
r = Record.new
check(r.value.nil?, "unset")
r.value = 3
check(r.value == 3, "write")
r.value = nil
check(r.value.nil?, "nil write")
puts "PASS attr-accessor"
