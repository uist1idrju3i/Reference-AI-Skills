def check(condition, detail)
  unless condition
    puts "FAIL alt-group-by " + detail
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

def frequencies(items)
  raise ArgumentError, "nil items" if items.nil?
  groups = {}
  items.each do |value|
    groups[value] = [] unless groups.has_key?(value)
    groups[value] << value
  end
  groups
end
groups = frequencies(["a", nil, "a"])
check(groups["a"] == ["a", "a"] && groups[nil] == [nil], "group values")
counts = {}
groups.each { |key, values| counts[key] = values.size }
check(counts["a"] == 2 && counts[nil] == 1, "counts")
check(frequencies([]) == {}, "empty")
reject_nil { frequencies(nil) }
puts "PASS alt-group-by"
