def check(condition, detail)
  unless condition
    puts "FAIL begin-rescue-else-ensure " + detail
    raise "assertion failed"
  end
end

seen = []
begin
  seen << :body
rescue StandardError
  seen << :rescue
else
  seen << :else
ensure
  seen << :ensure
end
check(seen == [:body, :else, :ensure], "normal path")
seen = []
begin
  raise ArgumentError, "bad"
rescue ArgumentError
  seen << :rescue
else
  seen << :else
ensure
  seen << :ensure
end
check(seen == [:rescue, :ensure], "exception path")
puts "PASS begin-rescue-else-ensure"
