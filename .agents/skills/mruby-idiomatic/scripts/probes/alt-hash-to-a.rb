def check(condition, detail)
  unless condition
    puts "FAIL alt-hash-to-a " + detail
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

def pairs_present(hash)
  raise ArgumentError, "nil hash" if hash.nil?
  selected = {}
  pairs = []
  hash.each do |key, value|
    selected[key] = value unless value.nil?
    pairs << [key, value]
  end
  [selected, pairs]
end
check(pairs_present({a: 1, b: nil}) == [{a: 1}, [[:a, 1], [:b, nil]]], "pairs")
check(pairs_present({}) == [{}, []], "empty")
reject_nil { pairs_present(nil) }
puts "PASS alt-hash-to-a"
