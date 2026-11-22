def check(condition, detail)
  unless condition
    puts "FAIL case-in-pin " + detail
    raise "assertion failed"
  end
end

wanted = 2
result = case [2]
in [^wanted] then true
else false
end
check(result, "pin equality")
result = case [3]
in [^wanted] then true
else false
end
check(result == false, "pin mismatch")
result = case nil
in [^wanted] then true
else false
end
check(result == false, "nil mismatch")
puts "PASS case-in-pin"
