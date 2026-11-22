def check(condition, detail)
  unless condition
    puts "FAIL respond-to " + detail
    raise "assertion failed"
  end
end

check([].respond_to?(:size), "known method")
check([].respond_to?(:no_such_probe_method) == false, "unknown method")
check(nil.respond_to?(:nil?), "nil receiver")
puts "PASS respond-to"
