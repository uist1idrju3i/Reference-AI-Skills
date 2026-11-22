def check(condition, detail)
  unless condition
    puts "FAIL array-pack " + detail
    raise "assertion failed"
  end
end

check([65, 90].pack("C*") == "AZ", "pack")
check([].pack("C*") == "", "empty")
puts "PASS array-pack"
