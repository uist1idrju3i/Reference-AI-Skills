def check(condition, detail)
  unless condition
    puts "FAIL alt-integer-digits " + detail
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

def decimal_digits(value)
  raise ArgumentError, "negative integer" if value < 0
  return [0] if value == 0
  digits = []
  while value > 0
    digits << value % 10
    value /= 10
  end
  digits
end
check(decimal_digits(120) == [0, 2, 1], "digits")
check(decimal_digits(0) == [0], "zero")
reject_nil { decimal_digits(-1) }
puts "PASS alt-integer-digits"
