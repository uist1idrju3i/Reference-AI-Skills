#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "mrubyc.h"

static mrbc_class *value_class, *value_module;
static mrbc_value native;
static int effects, created, destroyed;

static int reject(mrbc_vm *vm, mrbc_class *error, const char *message)
{
  mrbc_raise(vm, error, message);
  return 0;
}

static void destroy_value(mrbc_value *value)
{
  assert(*(int *)value->instance->data == 123);
  destroyed++;
}

static mrbc_value new_data(mrbc_vm *vm)
{
  mrbc_value result = mrbc_instance_new(vm, value_class, sizeof(int));
  *(int *)result.instance->data = 123;
  created++;
  return result;
}

static void data_new(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc || mrbc_type(v[0]) != MRBC_TT_CLASS || v[0].cls != value_class) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "ValueData class constructor required");
    return;
  }
  SET_RETURN(new_data(vm));
}

static int short_value(mrbc_vm *vm, mrbc_value value)
{
  if (mrbc_type(value) != MRBC_TT_INTEGER)
    return reject(vm, MRBC_CLASS(TypeError), "Integer required");
  if (mrbc_integer(value) < INT16_MIN || mrbc_integer(value) > INT16_MAX)
    return reject(vm, MRBC_CLASS(RangeError), "int16 range required");
  return 1;
}

static int array_values(mrbc_vm *vm, const mrbc_value *array)
{
  if (mrbc_type(*array) != MRBC_TT_ARRAY)
    return reject(vm, MRBC_CLASS(TypeError), "Array required");
  if (mrbc_array_size(array) > 4)
    return reject(vm, MRBC_CLASS(RangeError), "at most four elements");
  for (int i = 0; i < mrbc_array_size(array); i++) {
    if (!short_value(vm, mrbc_array_get(array, i))) return 0;
  }
  return 1;
}

static int hash_values(mrbc_vm *vm, const mrbc_value *hash)
{
  if (mrbc_hash_size(hash) > 4)
    return reject(vm, MRBC_CLASS(RangeError), "at most four pairs");
  mrbc_hash_iterator iterator = mrbc_hash_iterator_new(hash);
  while (mrbc_hash_i_has_next(&iterator)) {
    mrbc_value *pair = mrbc_hash_i_next(&iterator);
    if (mrbc_type(pair[0]) != MRBC_TT_SYMBOL)
      return reject(vm, MRBC_CLASS(TypeError), "Symbol key required");
    mrbc_sym key = mrbc_symbol(pair[0]);
    if (key != mrbc_str_to_symid("value") && key != mrbc_str_to_symid("other"))
      return reject(vm, MRBC_CLASS(ArgumentError), "unknown key");
    if (!short_value(vm, pair[1])) return 0;
  }
  return 1;
}

static void typed(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 2 || mrbc_type(v[1]) != MRBC_TT_INTEGER) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "tag and value required");
    return;
  }
  mrbc_int_t tag = mrbc_integer(v[1]);
  if (tag < MRBC_TT_NIL || tag > MRBC_TT_EXCEPTION) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "public value tag required");
    return;
  }
  if (mrbc_type(v[2]) != tag) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "wrong value type");
    return;
  }
  switch (tag) {
  case MRBC_TT_INTEGER:
    if (!short_value(vm, v[2])) return;
    break;
  case MRBC_TT_FLOAT: {
    mrbc_float_t number = mrbc_float(v[2]);
    if (!isfinite(number) || number < INT16_MIN || number > INT16_MAX || trunc(number) != number) {
      mrbc_raise(vm, MRBC_CLASS(RangeError), "finite integral int16 Float required");
      return;
    }
    break;
  }
  case MRBC_TT_SYMBOL:
    if (mrbc_symbol(v[2]) != mrbc_str_to_symid("write") &&
        mrbc_symbol(v[2]) != mrbc_str_to_symid("read")) {
      mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unknown Symbol");
      return;
    }
    break;
  case MRBC_TT_CLASS:
  case MRBC_TT_MODULE:
    if (v[2].cls != (tag == MRBC_TT_CLASS ? value_class : value_module)) {
      mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unexpected class/module identity");
      return;
    }
    break;
  case MRBC_TT_OBJECT:
    if (mrbc_type(native) != MRBC_TT_OBJECT ||
        find_class_by_object(&v[2]) != value_class || v[2].instance != native.instance) {
      mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unregistered native instance");
      return;
    }
    assert(*(int *)v[2].instance->data == 123);
    break;
  case MRBC_TT_ARRAY: {
    if (!array_values(vm, &v[2])) return;
    int16_t buffer[4];
    int total = 0;
    for (int i = 0; i < mrbc_array_size(&v[2]); i++) {
      mrbc_value item = mrbc_array_get(&v[2], i);
      buffer[i] = (int16_t)mrbc_integer(item);
      total += buffer[i];
    }
    assert(total >= 4 * INT16_MIN && total <= 4 * INT16_MAX);
    break;
  }
  case MRBC_TT_STRING:
    if (mrbc_string_size(&v[2]) > 8) {
      mrbc_raise(vm, MRBC_CLASS(RangeError), "at most eight bytes");
      return;
    }
    if (memchr(mrbc_string_cstr(&v[2]), 0, mrbc_string_size(&v[2]))) {
      mrbc_raise(vm, MRBC_CLASS(ArgumentError), "embedded NUL rejected");
      return;
    }
    break;
  case MRBC_TT_RANGE: {
    mrbc_value first = mrbc_range_first(&v[2]), last = mrbc_range_last(&v[2]);
    if (!short_value(vm, first) || !short_value(vm, last)) return;
    if (mrbc_integer(first) > mrbc_integer(last)) {
      mrbc_raise(vm, MRBC_CLASS(RangeError), "ascending Range required");
      return;
    }
    assert(mrbc_range_exclude_end(&v[2]) == 0 || mrbc_range_exclude_end(&v[2]) == 1);
    break;
  }
  case MRBC_TT_HASH:
    if (!hash_values(vm, &v[2])) return;
    break;
  case MRBC_TT_EXCEPTION:
    if (!mrbc_obj_is_kind_of(&v[2], MRBC_CLASS(StandardError))) {
      mrbc_raise(vm, MRBC_CLASS(ArgumentError), "StandardError required");
      return;
    }
    if ((v[2].exception->message_size ? v[2].exception->message_size :
         (v[2].exception->message ? strlen((const char *)v[2].exception->message) : 0)) > 8) {
      mrbc_raise(vm, MRBC_CLASS(RangeError), "at most eight message bytes");
      return;
    }
    break;
  }
  effects++;
  mrbc_value result = v[2];
  mrbc_incref(&result);
  SET_RETURN(result);
}

static void value_make(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 1 || mrbc_type(v[1]) != MRBC_TT_INTEGER) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "one tag required");
    return;
  }
  mrbc_value result;
  switch (mrbc_integer(v[1])) {
  case MRBC_TT_NIL: result = mrbc_nil_value(); break;
  case MRBC_TT_FALSE: result = mrbc_false_value(); break;
  case MRBC_TT_TRUE: result = mrbc_true_value(); break;
  case MRBC_TT_INTEGER: result = mrbc_integer_value(7); break;
  case MRBC_TT_FLOAT: result = mrbc_float_value(vm, 3.0); break;
  case MRBC_TT_SYMBOL: result = mrbc_symbol_new(vm, "write"); break;
  case MRBC_TT_CLASS: result = mrbc_immediate_value(MRBC_TT_CLASS, .cls = value_class); break;
  case MRBC_TT_MODULE: result = mrbc_immediate_value(MRBC_TT_MODULE, .cls = value_module); break;
  case MRBC_TT_OBJECT:
    if (mrbc_type(native) != MRBC_TT_OBJECT) {
      mrbc_raise(vm, MRBC_CLASS(RuntimeError), "native registry closed"); return;
    }
    result = native; mrbc_incref(&result); break;
  case MRBC_TT_ARRAY: result = mrbc_array_new(vm, 0); break;
  case MRBC_TT_STRING: result = mrbc_string_new(vm, "text", 4); break;
  case MRBC_TT_RANGE: {
    mrbc_value first = mrbc_integer_value(1), last = mrbc_integer_value(2);
    result = mrbc_range_new(vm, &first, &last, 0);
    break;
  }
  case MRBC_TT_HASH: result = mrbc_hash_new(vm, 0); break;
  case MRBC_TT_EXCEPTION: result = mrbc_exception_new(vm, MRBC_CLASS(RuntimeError), "ok", 2); break;
  default:
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unsupported factory tag");
    return;
  }
  if (mrbc_israised(vm)) { mrbc_decref(&result); return; }
  SET_RETURN(result);
}

static void nested(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 1) { mrbc_raise(vm, MRBC_CLASS(ArgumentError), "one Array required"); return; }
  if (mrbc_type(v[1]) != MRBC_TT_ARRAY) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "nested Array required"); return;
  }
  if (mrbc_array_size(&v[1]) > 4) {
    mrbc_raise(vm, MRBC_CLASS(RangeError), "at most four rows"); return;
  }
  for (int i = 0; i < mrbc_array_size(&v[1]); i++) {
    mrbc_value row = mrbc_array_get(&v[1], i);
    if (!array_values(vm, &row)) return;
  }
  int16_t buffer[16];
  int size = 0, total = 0;
  for (int i = 0; i < mrbc_array_size(&v[1]); i++) {
    mrbc_value row = mrbc_array_get(&v[1], i);
    for (int j = 0; j < mrbc_array_size(&row); j++) {
      mrbc_value item = mrbc_array_get(&row, j);
      buffer[size] = (int16_t)mrbc_integer(item);
      total += buffer[size++];
    }
  }
  effects++;
  SET_INT_RETURN(total);
}

static void build_pair(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 1) { mrbc_raise(vm, MRBC_CLASS(ArgumentError), "failure flag required"); return; }
  int fail = MRBC_ARG_B(1);
  if (mrbc_israised(vm)) return;
  int before = destroyed;
  mrbc_value array = mrbc_array_new(vm, 1), hash = mrbc_hash_new(vm, 1);
  mrbc_value item = new_data(vm);
  int status = mrbc_array_set(&array, 0, &item);
  assert(status == 0);
  if (fail) { mrbc_raise(vm, MRBC_CLASS(RuntimeError), "injected partial build failure"); goto RETURN; }
  mrbc_value key = mrbc_symbol_new(vm, "value");
  status = mrbc_hash_set(&hash, &key, &array);
  assert(status == 0);
  array = mrbc_nil_value();
  effects++;
  SET_RETURN(hash);
  hash = mrbc_nil_value();
RETURN:
  mrbc_decref(&array);
  mrbc_decref(&hash);
  assert(!fail || destroyed == before + 1);
}

static void value_reset(mrbc_vm *vm, mrbc_value v[], int argc) { effects = 0; SET_NIL_RETURN(); }
static void value_effects(mrbc_vm *vm, mrbc_value v[], int argc) { SET_INT_RETURN(effects); }

static void value_equal(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 2) { mrbc_raise(vm, MRBC_CLASS(ArgumentError), "two values required"); return; }
  int equal = mrbc_type(v[1]) == mrbc_type(v[2]);
  if (equal) equal = mrbc_type(v[1]) == MRBC_TT_EXCEPTION ?
    v[1].exception == v[2].exception : mrbc_compare(&v[1], &v[2]) == 0;
  SET_BOOL_RETURN(equal);
}

static void helper(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc < 1 || argc > 2 || mrbc_type(v[1]) != MRBC_TT_INTEGER) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "helper selector required"); return;
  }
  mrbc_value *value = argc == 2 ? &v[2] : NULL;
  mrbc_value result = mrbc_nil_value();
  mrbc_int_t integer = 0;
  mrbc_float_t number = 0;
  const char *string = NULL;
  mrbc_int_t selector = mrbc_integer(v[1]);
  switch (selector) {
  case 0: value = MRBC_ARG(2); break;
  case 1: integer = MRBC_ARG_I(2); break;
  case 2: integer = MRBC_ARG_I(2, 7); break;
  case 3: number = MRBC_ARG_F(2); break;
  case 4: number = MRBC_ARG_F(2, 2.0); break;
  case 5: string = MRBC_ARG_S(2); break;
  case 6: string = MRBC_ARG_S(2, "d"); break;
  case 7: integer = MRBC_ARG_B(2); break;
  case 8: integer = MRBC_ARG_B(2, 1); break;
  case 9: integer = MRBC_VAL_I(value); break;
  case 10: integer = MRBC_VAL_I(value, 7); break;
  case 11: number = MRBC_VAL_F(value); break;
  case 12: number = MRBC_VAL_F(value, 2.0); break;
  case 13: string = MRBC_VAL_S(value); break;
  case 14: string = MRBC_VAL_S(value, "d"); break;
  case 15: integer = MRBC_TO_I(value); break;
  case 16: number = MRBC_TO_F(value); break;
  case 17: string = MRBC_TO_S(value); break;
  default: mrbc_raise(vm, MRBC_CLASS(ArgumentError), "unknown helper"); return;
  }
  if (mrbc_israised(vm)) return;
  switch (selector) {
  case 0: result = *value; mrbc_incref(&result); break;
  case 3: case 4: case 11: case 12: case 16: result = mrbc_float_value(vm, number); break;
  case 5: case 6: case 13: case 14: case 17:
    if (string) result = mrbc_string_new_cstr(vm, string);
    break;
  default: result = mrbc_integer_value(integer); break;
  }
  effects++;
  SET_RETURN(result);
}

static void value_ownership(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int before = destroyed;
  mrbc_value first = new_data(vm), last = new_data(vm);
  mrbc_value range = mrbc_range_new(vm, &first, &last, 1);
  assert(first.obj->ref_count == 1 && last.obj->ref_count == 1);
  mrbc_value borrowed = mrbc_range_first(&range);
  assert(borrowed.obj->ref_count == 1);
  mrbc_incref(&borrowed);
  mrbc_decref(&range);
  assert(destroyed == before + 1 && borrowed.obj->ref_count == 1);
  mrbc_decref(&borrowed);
  assert(destroyed == before + 2);
  puts("PASS range endpoints transfer and getters borrow");
  assert(native.obj->ref_count == 1 && created == destroyed + 1);
  mrbc_decref_empty(&native);
  assert(created == destroyed);
  puts("PASS value refcounts and destructors balanced");
  SET_NIL_RETURN();
}

void value_contract_init(mrbc_class *binding)
{
  value_class = mrbc_define_class_under(NULL, binding, "ValueData", NULL);
  value_module = mrbc_define_module_under(NULL, binding, "ValueModule");
  mrbc_define_destructor(value_class, destroy_value);
  mrbc_define_method(NULL, value_class, "new", data_new);
  native = new_data(NULL);
  mrbc_define_method(NULL, binding, "typed", typed);
  mrbc_define_method(NULL, binding, "value_make", value_make);
  mrbc_define_method(NULL, binding, "nested", nested);
  mrbc_define_method(NULL, binding, "build_pair", build_pair);
  mrbc_define_method(NULL, binding, "value_reset", value_reset);
  mrbc_define_method(NULL, binding, "value_effects", value_effects);
  mrbc_define_method(NULL, binding, "value_ownership", value_ownership);
  mrbc_define_method(NULL, binding, "helper", helper);
  mrbc_define_method(NULL, binding, "value_equal", value_equal);
}
