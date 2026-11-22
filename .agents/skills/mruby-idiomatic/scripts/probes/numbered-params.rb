def check(condition, detail)
  unless condition
    puts "FAIL numbered-params " + detail
    raise "assertion failed"
  end
end

check([1, nil].map { _1.nil? ? 0 : _1 * 2 } == [2, 0], "numbered param")
check([].map { _1 } == [], "empty")
puts "PASS numbered-params"
