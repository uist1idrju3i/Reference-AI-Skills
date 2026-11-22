def check(condition, detail)
  unless condition
    puts "FAIL alt-outer-constant-assignment " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

module Settings
  LIMIT = 3
  EMPTY = ""
end
check(Settings::LIMIT == 3, "defined inside owner")
check(Settings::EMPTY == "", "empty constant")
puts "PASS alt-outer-constant-assignment"
