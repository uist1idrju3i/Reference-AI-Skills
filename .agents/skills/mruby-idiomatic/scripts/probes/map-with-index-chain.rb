def check(condition, detail)
  unless condition
    puts "FAIL map-with-index-chain " + detail
    raise "assertion failed"
  end
end

check([8, nil].map.with_index { |v, i| [v, i] } == [[8, 0], [nil, 1]], "Enumerator chain")
check([].map.with_index { |v, i| [v, i] } == [], "empty")
puts "PASS map-with-index-chain"
