def check(condition, detail)
  unless condition
    puts "FAIL time " + detail
    raise "assertion failed"
  end
end

t = Time.at(0)
check(t.to_i == 0, "epoch")
check((t + 3).to_i == 3, "addition")
puts "PASS time"
