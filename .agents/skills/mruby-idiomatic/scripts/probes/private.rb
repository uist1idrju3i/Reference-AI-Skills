def check(condition, detail)
  unless condition
    puts "FAIL private " + detail
    raise "assertion failed"
  end
end

class Secret
  def public_value
    secret
  end
  private
  def secret
    7
  end
end
check(Secret.new.public_value == 7, "internal private call")
raised = false
begin
  Secret.new.secret
rescue NoMethodError
  raised = true
end
check(raised, "private method callable from outside")
puts "PASS private"
