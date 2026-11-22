def check(condition, detail)
  unless condition
    puts "FAIL alt-tap " + detail
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

def normalize(value)
  return "" if value.nil?
  value.to_s
end
value = normalize(2)
observed = []
observed << value
check(value == "2" && observed == ["2"], "named intermediate")
check(normalize("") == "" && normalize(nil) == "", "empty and nil")
puts "PASS alt-tap"
