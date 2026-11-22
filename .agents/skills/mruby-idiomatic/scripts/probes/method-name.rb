def check(condition, detail)
  unless condition
    puts "FAIL method-name " + detail
    raise "assertion failed"
  end
end

def probe_name
  __method__
end
check(probe_name == :probe_name, "method name")
puts "PASS method-name"
