def check(condition, detail)
  unless condition
    puts "FAIL proc-new " + detail
    raise "assertion failed"
  end
end

fn = Proc.new { |v| v.nil? ? :missing : v * 2 }
check(fn.call(3) == 6, "Proc call")
check(fn.call(nil) == :missing && fn.call == :missing, "nil and lenient arity")
puts "PASS proc-new"
