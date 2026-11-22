def check(condition, detail)
  unless condition
    puts "FAIL alt-count-block " + detail
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

def count_present(items)
  raise ArgumentError, "nil items" if items.nil?
  count = 0
  items.each { |value| count += 1 unless value.nil? }
  count
end
check(count_present([1, nil, false]) == 2, "predicate")
check(count_present([]) == 0, "empty")
reject_nil { count_present(nil) }
puts "PASS alt-count-block"
