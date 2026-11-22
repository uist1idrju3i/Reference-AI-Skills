def check(condition, detail)
  unless condition
    puts "FAIL string-interpolation " + detail
    raise "assertion failed"
  end
end

value = 3
check("v=#{value}" == "v=3", "integer interpolation")
value = nil
check("v=#{value}" == "v=", "nil interpolation")
value = ""
check("v=#{value}" == "v=", "empty interpolation")
puts "PASS string-interpolation"
