def check(condition, detail)
  unless condition
    puts "FAIL gpio-contract " + detail
    raise "assertion failed"
  end
end

def rejects(error)
  rejected = false
  begin
    yield
  rescue => exception
    check(exception.is_a?(error), "wrong exception")
    rejected = true
  end
  check(rejected, "invalid input accepted")
end

gpio = GPIO.new(0, GPIO::OUT)
check(gpio.read == 0 && gpio.low? && !gpio.high?, "initial low")
check(gpio.write(1).nil?, "write return policy")
check(gpio.read == 1 && gpio.high? && !gpio.low?, "instance high")
check(GPIO.read_at(0) == 1 && GPIO.high_at?(0) && !GPIO.low_at?(0), "class high")
check(GPIO.write_at(0, 0).nil?, "class write")
check(GPIO.low_at?(0) && !GPIO.high_at?(0) && gpio.low?, "class low")
check(GPIO.setmode(1, GPIO::IN | GPIO::PULL_UP).nil?, "class mode")
FakeGPIO.input_at(1, 1)
check(GPIO.read_at(1) == 1 && GPIO.high_at?(1), "injected input high")
input = GPIO.new(2, GPIO::IN | GPIO::PULL_DOWN)
FakeGPIO.input_at(2, 0)
check(input.read == 0 && input.low? && !input.high?, "injected input low")
check(FakeGPIO.mode(2) == (GPIO::IN | GPIO::PULL_DOWN), "input flags")
check(input.setmode(GPIO::OUT).nil? && FakeGPIO.mode(2) == GPIO::OUT, "direction resets pulls")
input.setmode(GPIO::PULL_UP)
check(FakeGPIO.mode(2) == (GPIO::OUT | GPIO::PULL_UP), "partial instance mode")
GPIO.new(3, GPIO::HIGH_Z)
check(FakeGPIO.mode(3) == GPIO::HIGH_Z, "high impedance")
GPIO.new(4, GPIO::OUT | GPIO::OPEN_DRAIN)
check(FakeGPIO.mode(4) == (GPIO::OUT | GPIO::OPEN_DRAIN), "open drain")

before_mode = FakeGPIO.mode(0)
before_writes = FakeGPIO.writes
rejects(ArgumentError) { GPIO.new(0, 0) }
rejects(ArgumentError) { GPIO.new(0, GPIO::PULL_UP) }
rejects(ArgumentError) { GPIO.setmode(0, GPIO::PULL_UP) }
[GPIO::IN | GPIO::OUT, GPIO::IN | GPIO::HIGH_Z, GPIO::OUT | GPIO::HIGH_Z].each do |flags|
  rejects(ArgumentError) { GPIO.new(0, flags) }
  rejects(ArgumentError) { gpio.setmode(flags) }
end
rejects(ArgumentError) { GPIO.new(0, GPIO::OUT | GPIO::PULL_UP | GPIO::PULL_DOWN) }
rejects(ArgumentError) { gpio.setmode(GPIO::PULL_UP | GPIO::PULL_DOWN) }
rejects(ArgumentError) { GPIO.new(0, GPIO::OUT | 64) }
rejects(ArgumentError) { GPIO.new(0) }
rejects(ArgumentError) { gpio.read(1) }
rejects(ArgumentError) { GPIO.write_at(0) }
rejects(ArgumentError) { gpio.write(1, unknown: true) }
rejects(TypeError) { GPIO.new(nil, GPIO::OUT) }
rejects(TypeError) { GPIO.new("", GPIO::OUT) }
rejects(TypeError) { GPIO.new(0, nil) }
rejects(RangeError) { GPIO.new(-1, GPIO::IN) }
rejects(RangeError) { GPIO.read_at(8) }
[2, -1, 2147483647].each do |value|
  rejects(RangeError) { gpio.write(value) }
  rejects(RangeError) { GPIO.write_at(0, value) }
end
rejects(TypeError) { gpio.write(nil) }
rejects(TypeError) { GPIO.write_at(0, "1") }
check(FakeGPIO.mode(0) == before_mode, "rejected mode has no side effect")
check(FakeGPIO.writes == before_writes && gpio.read == 0, "rejected write has no side effect")

check(BindingProbe.keyword(7, required: 2, optional: 3) == 123, "C keyword slot and argc")
check(BindingProbe.keyword(7, required: 2) == 124, "C keyword default")
rejects(ArgumentError) { BindingProbe.keyword(7) }
rejects(ArgumentError) { BindingProbe.keyword(7, required: 2, unknown: 1) }
rejects(ArgumentError) { BindingProbe.keyword(7, {required: 2}) }
rejects(TypeError) { BindingProbe.keyword(7, required: nil) }
check(BindingProbe.keyword(7, **{required: 2}) == 124, "C keyword splat")
puts "PASS gpio-contract"
