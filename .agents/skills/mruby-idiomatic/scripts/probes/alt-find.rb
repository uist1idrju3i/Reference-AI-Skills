def check(condition, detail)
  unless condition
    puts "FAIL alt-find " + detail
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

def first_present(items)
  raise ArgumentError, "nil items" if items.nil?
  result = nil
  items.each do |value|
    unless value.nil?
      result = value
      break
    end
  end
  result
end
check(first_present([nil, false, 2]) == false, "false value")
check(first_present([]).nil?, "empty")
reject_nil { first_present(nil) }
puts "PASS alt-find"
