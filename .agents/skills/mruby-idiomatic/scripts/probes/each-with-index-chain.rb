def check(condition, detail)
  unless condition
    puts "FAIL each-with-index-chain " + detail
    raise "assertion failed"
  end
end

seen = []
[8, nil].each.with_index { |v, i| seen << [v, i] }
check(seen == [[8, 0], [nil, 1]], "Enumerator chain")
check([].each.with_index.to_a == [], "empty")
puts "PASS each-with-index-chain"
