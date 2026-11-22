def check(condition, detail)
  unless condition
    puts "FAIL heredoc " + detail
    raise "assertion failed"
  end
end

value = 3
text = <<~TEXT
  value=#{value}
    more
TEXT
check(text == "value=3\n  more\n", "dedent and interpolate")
empty = <<~TEXT
TEXT
check(empty == "", "empty heredoc")
puts "PASS heredoc"
