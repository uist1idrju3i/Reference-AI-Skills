def check(condition, detail)
  unless condition
    puts "FAIL alt-string-append " + detail
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

def append_text(target, value)
  raise ArgumentError, "text required" unless value.is_a?(String)
  target << value
end
text = ""
check(append_text(text, "ab") == "ab" && text == "ab", "append")
check(append_text(text, "") == "ab", "empty")
reject_nil { append_text(text, nil) }
puts "PASS alt-string-append"
