def check(condition, detail)
  unless condition
    puts "FAIL alt-partition " + detail
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

def partition_present(items)
  raise ArgumentError, "nil items" if items.nil?
  yes = []
  no = []
  items.each { |value| value.nil? ? no << value : yes << value }
  [yes, no]
end
check(partition_present([1, nil, false]) == [[1, false], [nil]], "partition")
check(partition_present([]) == [[], []], "empty")
reject_nil { partition_present(nil) }
puts "PASS alt-partition"
