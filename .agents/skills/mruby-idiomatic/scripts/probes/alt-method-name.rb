def check(condition, detail)
  unless condition
    puts "FAIL alt-method-name " + detail
    raise "assertion failed"
  end
end

def probe_name
  :probe_name
end
check(probe_name == :probe_name, "explicit label")
check([].map { probe_name } == [], "empty")
puts "PASS alt-method-name"
