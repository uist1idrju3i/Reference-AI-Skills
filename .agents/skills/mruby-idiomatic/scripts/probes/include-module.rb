def check(condition, detail)
  unless condition
    puts "FAIL include-module " + detail
    raise "assertion failed"
  end
end

module Label
  def label
    :included
  end
end
class Record
  include Label
end
check(Record.new.label == :included, "included instance method")
check(Record.new.is_a?(Label), "module ancestry")
puts "PASS include-module"
