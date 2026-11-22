def check(condition, detail)
  unless condition
    puts "FAIL case-in-hash " + detail
    raise "assertion failed"
  end
end

def match(value)
  case value
  in {name: name} then name
  else :missing
  end
end
check(match({name: "ruby"}) == "ruby", "hash match")
check(match({name: nil}).nil?, "nil member")
check(match({}) == :missing, "empty nonmatch")
check(match(nil) == :missing, "nil nonmatch")
puts "PASS case-in-hash"
