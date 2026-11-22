def check(condition, detail)
  unless condition
    puts "FAIL keyword-rest " + detail
    raise "assertion failed"
  end
end

def keyword(**opts)
  opts
end
check(keyword(a: 1, b: nil) == {a: 1, b: nil}, "keyword rest")
check(keyword == {}, "empty")
puts "PASS keyword-rest"
