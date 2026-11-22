def check(condition, detail)
  unless condition
    puts "FAIL alt-hash-dig " + detail
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

def nested_value(container)
  return nil if container.nil? || container.empty?
  child = container[0]
  return nil if child.nil?
  raise ArgumentError, "invalid child" unless child.is_a?(Hash)
  child[:name]
end
check(nested_value([{name: "a"}]) == "a", "nested")
check(nested_value([]).nil? && nested_value([nil]).nil?, "empty and nil")
check(nested_value(nil).nil?, "nil container")
reject_nil { nested_value([2]) }
puts "PASS alt-hash-dig"
