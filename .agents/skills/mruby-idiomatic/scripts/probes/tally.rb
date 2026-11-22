def check(condition, detail)
  unless condition
    puts "FAIL tally " + detail
    raise "assertion failed"
  end
end

check([1, nil, 1].tally == {1 => 2, nil => 1}, "counts")
check([].tally == {}, "empty")
puts "PASS tally"
