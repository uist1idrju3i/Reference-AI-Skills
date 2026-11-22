def check(condition, detail)
  unless condition
    puts "FAIL alt-string-center " + detail
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

def center_ascii(text, width)
  raise ArgumentError, "nil text" if text.nil?
  padding = width - text.bytesize
  return text if padding <= 0
  left = padding / 2
  " " * left + text + " " * (padding - left)
end
check(center_ascii("a", 4) == " a  ", "ASCII center")
check(center_ascii("", 2) == "  ", "empty")
check(center_ascii("abc", 1) == "abc", "narrow")
reject_nil { center_ascii(nil, 2) }
puts "PASS alt-string-center"
