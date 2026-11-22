def check(condition, detail)
  unless condition
    puts "FAIL alt-send " + detail
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

def dispatch(name, value)
  case name
  when :text
    value.to_s
  when :present
    !value.nil?
  else
    raise ArgumentError, "unknown operation"
  end
end
check(dispatch(:text, 2) == "2", "dispatch")
check(dispatch(:text, "") == "", "empty")
check(dispatch(:present, nil) == false, "nil")
reject_nil { dispatch(:unknown, 1) }
puts "PASS alt-send"
