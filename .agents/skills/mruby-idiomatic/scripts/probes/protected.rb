def check(condition, detail)
  unless condition
    puts "FAIL protected " + detail
    raise "assertion failed"
  end
end

class Secret
  def internal(other)
    other.secret
  end
  protected
  def secret
    7
  end
end
check(Secret.new.internal(Secret.new) == 7, "same class call")
raised = false
begin
  Secret.new.secret
rescue NoMethodError
  raised = true
end
check(raised, "protected method callable from outside")
puts "PASS protected"
