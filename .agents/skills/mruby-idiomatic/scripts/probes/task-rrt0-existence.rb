def check(condition, detail)
  unless condition
    puts "FAIL task-rrt0-existence " + detail
    raise "assertion failed"
  end
end

check(Task.respond_to?(:current), "Task.current missing")
check(Task.respond_to?(:create), "Task.create missing")
check(Task.respond_to?(:suspend), "rrt0 task suspend missing")
check(Task.respond_to?(:pass), "rrt0 Task.pass missing")
check(VM.respond_to?(:tick), "rrt0 VM.tick missing")
puts "PASS task-rrt0-existence"
