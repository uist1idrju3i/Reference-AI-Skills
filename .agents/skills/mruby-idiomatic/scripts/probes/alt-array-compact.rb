def check(condition, detail)
  unless condition
    puts "FAIL alt-array-compact " + detail
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

def compact(items)
  raise ArgumentError, "nil items" if items.nil?
  items.reject { |value| value.nil? }
end
check(compact([nil, false, 0]) == [false, 0], "nil only")
check(compact([]) == [], "empty")
reject_nil { compact(nil) }
puts "PASS alt-array-compact"
