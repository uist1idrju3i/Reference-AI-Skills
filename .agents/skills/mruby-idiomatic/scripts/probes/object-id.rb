def check(condition, detail)
  unless condition
    puts "FAIL object-id " + detail
    raise "assertion failed"
  end
end

a = []
b = []
check(a.object_id == a.object_id, "stable identity")
check(a.object_id != b.object_id, "distinct arrays")
check(nil.object_id == nil.object_id, "nil stable")
puts "PASS object-id"
