def check(condition, detail)
  unless condition
    puts "FAIL alt-map-with-index-chain " + detail
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

def indexed(items)
  raise ArgumentError, "nil items" if items.nil?
  result = []
  items.each_with_index { |value, index| result << [value, index] }
  result
end
check(indexed([nil, "a"]) == [[nil, 0], ["a", 1]], "indexed")
check(indexed([]) == [], "empty")
reject_nil { indexed(nil) }
puts "PASS alt-map-with-index-chain"
