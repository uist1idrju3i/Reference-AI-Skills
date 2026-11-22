def check(condition, detail)
  unless condition
    puts "FAIL while-until " + detail
    raise "assertion failed"
  end
end

n = 0
while n < 3
  n += 1
end
check(n == 3, "while")
until n == 0
  n -= 1
end
check(n == 0, "until")
while false
  n = 9
end
until true
  n = 9
end
check(n == 0, "zero iterations")
puts "PASS while-until"
