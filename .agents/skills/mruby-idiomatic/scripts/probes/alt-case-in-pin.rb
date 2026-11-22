def check(condition, detail)
  unless condition
    puts "FAIL alt-case-in-pin " + detail
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

def extract(value)
  return nil if value.nil?
  if value.is_a?(Array)
    return value[1] if value.size == 2 && value[0] == :tag
  elsif value.is_a?(Hash)
    return value[:value] if value.has_key?(:value)
  end
  nil
end
check(extract([:tag, 3]) == 3, "array tag")
check(extract({value: false}) == false, "hash false")
check(extract(nil).nil? && extract([]).nil? && extract({}).nil?, "nonmatch")
check(extract([:other, 3]).nil?, "pin-like comparison")
puts "PASS alt-case-in-pin"
