def check(condition, detail)
  unless condition
    puts "FAIL case-when " + detail
    raise "assertion failed"
  end
end

def label(value)
  case value
  when nil then :missing
  when 1, 2 then :small
  when String then :text
  else :other
  end
end
check(label(nil) == :missing, "nil")
check(label(2) == :small, "alternatives")
check(label("") == :text, "class match")
check(label([]) == :other, "else")
puts "PASS case-when"
