def check(condition, detail)
  unless condition
    puts "FAIL alt-hash-fetch-key-error " + detail
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

class MissingKey < StandardError
end
def fetch_required(hash, key)
  raise MissingKey, "missing key" unless hash.has_key?(key)
  hash[key]
end
check(fetch_required({a: nil}, :a).nil?, "present nil")
begin
  fetch_required({}, :a)
  check(false, "missing accepted")
rescue MissingKey => error
  check(error.message == "missing key", "message")
end
puts "PASS alt-hash-fetch-key-error"
