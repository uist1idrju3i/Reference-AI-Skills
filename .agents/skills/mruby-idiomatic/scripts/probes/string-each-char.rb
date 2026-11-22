def check(condition, detail)
  unless condition
    puts "FAIL string-each-char " + detail
    raise "assertion failed"
  end
end

seen = []
"ab".each_char { |v| seen << v }
check(seen == ["a", "b"], "characters")
seen = []
"".each_char { |v| seen << v }
check(seen == [], "empty")
seen = []
"あ".each_char { |v| seen << v }
check(seen == ["あ"], "UTF-8 character not bytes")
puts "PASS string-each-char"
