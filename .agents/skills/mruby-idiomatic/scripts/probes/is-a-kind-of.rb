def check(condition, detail)
  unless condition
    puts "FAIL is-a-kind-of " + detail
    raise "assertion failed"
  end
end

check([].is_a?(Array) && [].kind_of?(Array), "Array")
check(nil.is_a?(NilClass) && nil.kind_of?(NilClass), "nil")
check([].is_a?(String) == false && [].kind_of?(String) == false, "unrelated")
puts "PASS is-a-kind-of"
