#include "mrubyc.h"
#include "fake_hal.h"

enum { GPIO_IN = 1, GPIO_OUT = 2, GPIO_HIGH_Z = 4,
       GPIO_PULL_UP = 8, GPIO_PULL_DOWN = 16, GPIO_OPEN_DRAIN = 32 };

static int exact_args(mrbc_vm *vm, mrbc_value v[], int argc, int expected)
{
  if (argc != expected ||
      (mrbc_type(v[argc + 1]) == MRBC_TT_HASH && mrbc_hash_size(&v[argc + 1]))) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unexpected arguments");
    return 0;
  }
  return 1;
}

static int integer_arg(mrbc_vm *vm, mrbc_value value)
{
  if (mrbc_type(value) != MRBC_TT_INTEGER) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "Integer required");
    return 0;
  }
  return 1;
}

static int pin_arg(mrbc_vm *vm, mrbc_value value)
{
  if (!integer_arg(vm, value)) return -1;
  int pin = mrbc_integer(value);
  if (pin < 0 || pin >= FAKE_PIN_COUNT) {
    mrbc_raise(vm, MRBC_CLASS(RangeError), "pin outside fake range");
    return -1;
  }
  return pin;
}

static int object_pin(mrbc_vm *vm, mrbc_value *self)
{
  if (mrbc_type(*self) != MRBC_TT_OBJECT) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "GPIO instance required");
    return -1;
  }
  return pin_arg(vm, mrbc_instance_getiv(self, mrbc_str_to_symid("pin")));
}

static int apply_mode(mrbc_vm *vm, int pin, mrbc_value flags, int require_direction)
{
  if (!integer_arg(vm, flags)) return 0;
  int mode = mrbc_integer(flags);
  int direction = mode & 7;
  if (mode < 0 || (mode & ~63) ||
      (require_direction && direction == 0) ||
      (direction && (direction & (direction - 1))) || (mode & 24) == 24) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "invalid or exclusive GPIO flags");
    return 0;
  }
  int next = mode;
  if (!direction) {
    next = fake_mode(pin);
    if (mode & 24) next &= ~24;
    next |= mode;
  }
  fake_setmode(pin, next);
  return 1;
}

static void gpio_initialize(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (!exact_args(vm, v, argc, 2)) return;
  int pin = pin_arg(vm, v[1]);
  if (pin < 0 || !apply_mode(vm, pin, v[2], 1)) return;
  mrbc_instance_setiv(&v[0], mrbc_str_to_symid("pin"), &v[1]);
}

static void gpio_setmode(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int class_call = mrbc_type(v[0]) == MRBC_TT_CLASS;
  if (!exact_args(vm, v, argc, class_call ? 2 : 1)) return;
  int pin = class_call ? pin_arg(vm, v[1]) : object_pin(vm, &v[0]);
  if (pin < 0 || !apply_mode(vm, pin, v[class_call ? 2 : 1], class_call)) return;
  SET_NIL_RETURN();
}

static void read_pin(mrbc_vm *vm, mrbc_value v[], int argc, int at, int predicate)
{
  if (!exact_args(vm, v, argc, at ? 1 : 0)) return;
  int pin = at ? pin_arg(vm, v[1]) : object_pin(vm, &v[0]);
  if (pin < 0) return;
  int level = fake_read(pin);
  if (predicate < 0) { SET_INT_RETURN(level); }
  else { SET_BOOL_RETURN(level == predicate); }
}

static void gpio_read(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 0, -1); }
static void gpio_high(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 0, 1); }
static void gpio_low(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 0, 0); }
static void gpio_read_at(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 1, -1); }
static void gpio_high_at(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 1, 1); }
static void gpio_low_at(mrbc_vm *vm, mrbc_value v[], int argc) { read_pin(vm, v, argc, 1, 0); }

static void write_pin(mrbc_vm *vm, mrbc_value v[], int argc, int at)
{
  if (!exact_args(vm, v, argc, at ? 2 : 1)) return;
  int pin = at ? pin_arg(vm, v[1]) : object_pin(vm, &v[0]);
  if (pin < 0) return;
  mrbc_value value = v[at ? 2 : 1];
  if (!integer_arg(vm, value)) return;
  int level = mrbc_integer(value);
  if (level != 0 && level != 1) {
    mrbc_raise(vm, MRBC_CLASS(RangeError), "write value must be 0 or 1");
    return;
  }
  fake_write(pin, level);
  SET_NIL_RETURN();
}

static void gpio_write(mrbc_vm *vm, mrbc_value v[], int argc) { write_pin(vm, v, argc, 0); }
static void gpio_write_at(mrbc_vm *vm, mrbc_value v[], int argc) { write_pin(vm, v, argc, 1); }

static void fake_get_mode(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (!exact_args(vm, v, argc, 1)) return;
  int pin = pin_arg(vm, v[1]);
  if (pin >= 0) { SET_INT_RETURN(fake_mode(pin)); }
}

static void fake_get_writes(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (exact_args(vm, v, argc, 0)) { SET_INT_RETURN(fake_write_count()); }
}

static void keyword_probe(mrbc_vm *vm, mrbc_value v[], int argc)
{
  MRBC_KW_ARG(required, optional);
  if (argc != 1) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "one positional argument required");
    goto done;
  }
  if (!MRBC_KW_MANDATORY(required) || !MRBC_KW_END()) goto done;
  if (!integer_arg(vm, v[1]) || !integer_arg(vm, required)) goto done;
  if (MRBC_KW_ISVALID(optional) && !integer_arg(vm, optional)) goto done;
  int option = MRBC_KW_ISVALID(optional) ? mrbc_integer(optional) : 4;
  SET_INT_RETURN(argc * 100 + mrbc_integer(required) * 10 + option);
done:
  MRBC_KW_DELETE(required, optional);
}

void gpio_example_init(void)
{
  fake_reset();
  mrbc_class *gpio = mrbc_define_class(0, "GPIO", 0);
  const char *names[] = { "IN", "OUT", "HIGH_Z", "PULL_UP", "PULL_DOWN", "OPEN_DRAIN" };
  for (int i = 0; i < 6; i++) {
    mrbc_value value = mrbc_integer_value(1 << i);
    mrbc_set_class_const(gpio, mrbc_str_to_symid(names[i]), &value);
  }
  mrbc_define_method(0, gpio, "initialize", gpio_initialize);
  mrbc_define_method(0, gpio, "setmode", gpio_setmode);
  mrbc_define_method(0, gpio, "read", gpio_read);
  mrbc_define_method(0, gpio, "write", gpio_write);
  mrbc_define_method(0, gpio, "high?", gpio_high);
  mrbc_define_method(0, gpio, "low?", gpio_low);
  mrbc_define_method(0, gpio, "read_at", gpio_read_at);
  mrbc_define_method(0, gpio, "write_at", gpio_write_at);
  mrbc_define_method(0, gpio, "high_at?", gpio_high_at);
  mrbc_define_method(0, gpio, "low_at?", gpio_low_at);
  mrbc_class *fake = mrbc_define_class(0, "FakeGPIO", 0);
  mrbc_define_method(0, fake, "mode", fake_get_mode);
  mrbc_define_method(0, fake, "writes", fake_get_writes);
  mrbc_define_method(0, fake, "input_at", gpio_write_at);
  mrbc_class *probe = mrbc_define_class(0, "BindingProbe", 0);
  mrbc_define_method(0, probe, "keyword", keyword_probe);
}
