def check(condition, detail)
  unless condition
    puts "FAIL alt-symbol " + detail
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

def nonempty_symbol(text)
  raise ArgumentError, "nonempty name required" if text.nil? || text.empty?
  text.to_sym
end
check(nonempty_symbol("ruby") == :ruby, "nonempty conversion")
check(nonempty_symbol("ruby").to_s == "ruby", "round trip")
reject_nil { nonempty_symbol("") }
reject_nil { nonempty_symbol(nil) }
puts "PASS alt-symbol"
