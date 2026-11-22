def check(condition, detail)
  unless condition
    puts "FAIL alt-string-each-char " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

def protocol_bytes(text)
  raise ArgumentError, "nil text" if text.nil?
  result = []
  text.each_byte { |value| result << value }
  result
end
check(protocol_bytes("あ") == [227, 129, 130], "UTF-8 bytes, not characters")
check(protocol_bytes("") == [], "empty")
reject_nil { protocol_bytes(nil) }
puts "PASS alt-string-each-char"
