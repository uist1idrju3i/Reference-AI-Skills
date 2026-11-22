def check(condition, detail)
  unless condition
    puts "FAIL alt-format " + detail
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

check(sprintf("%s:%02d", "x", 3) == "x:03", "format")
check(sprintf("%s", "") == "", "empty")
check(sprintf("%s", nil) == "", "nil conversion")
puts "PASS alt-format"
