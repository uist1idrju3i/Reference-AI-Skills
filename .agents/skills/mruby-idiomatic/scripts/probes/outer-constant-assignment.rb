def check(condition, detail)
  unless condition
    puts "FAIL outer-constant-assignment " + detail
    raise "assertion failed"
  end
end

class Namespace
end
Namespace::VALUE = 7
Namespace::EMPTY = nil
check(Namespace::VALUE == 7, "qualified assignment")
check(Namespace::EMPTY.nil?, "nil constant")
puts "PASS outer-constant-assignment"
