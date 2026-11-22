def check(condition, detail)
  unless condition
    puts "FAIL alt-symbol-to-proc " + detail
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

def strings(items)
  raise ArgumentError, "nil items" if items.nil?
  items.map { |value| value.to_s }
end
check(strings([1, nil]) == ["1", ""], "explicit block")
check(strings([]) == [], "empty")
reject_nil { strings(nil) }
puts "PASS alt-symbol-to-proc"
