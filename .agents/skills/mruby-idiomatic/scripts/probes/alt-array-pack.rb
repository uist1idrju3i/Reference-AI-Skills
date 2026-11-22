def check(condition, detail)
  unless condition
    puts "FAIL alt-array-pack " + detail
    raise "assertion failed"
  end
end

def reject_nil
  rejected = false
  begin
    yield
  rescue ArgumentError
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

def encode_u16(value)
  raise ArgumentError, "u16 required" if value.nil? || value < 0 || value > 65535
  (value / 256).chr + (value % 256).chr
end
def decode_u16(text)
  raise ArgumentError, "two bytes required" if text.nil? || text.bytesize != 2
  text.getbyte(0) * 256 + text.getbyte(1)
end
check(encode_u16(258).bytes == [1, 2], "big endian")
check(decode_u16(encode_u16(65535)) == 65535, "round trip")
check(decode_u16(encode_u16(0)) == 0, "zero")
reject_nil { decode_u16("") }
reject_nil { encode_u16(nil) }
reject_nil { encode_u16(65536) }
puts "PASS alt-array-pack"
