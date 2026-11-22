def check(condition, detail)
  unless condition
    puts "FAIL struct " + detail
    raise "assertion failed"
  end
end

Record = Struct.new(:name, :value)
r = Record.new("ruby", 3)
check(r.name == "ruby" && r.value == 3, "members")
check(Record.new.name.nil? && Record.new.value.nil?, "unset members")
puts "PASS struct"
