#include <assert.h>
#include <stdio.h>
#include "mrubyc.h"

void value_contract_init(mrbc_class *binding);

#ifdef NDEBUG
#error "binding contract requires enabled assertions"
#endif

static mrbc_value saved;
static mrbc_class *error_class;
static mrbc_class *data_class;
static int destructor_calls, after_raise, detected, guarded_side_effects;
static int keyword_side_effects;

static void destroy_data(mrbc_value *value)
{
  assert(*(int *)value->instance->data == 123);
  destructor_calls++;
}

static void macro_test(mrbc_vm *vm, mrbc_value v[], int argc)
{
  mrbc_value old = v[0];
  mrbc_incref(&old);
  mrbc_value replacement = mrbc_string_new_cstr(vm, "new");
  assert(old.obj->ref_count == 2 && replacement.obj->ref_count == 1);
  SET_RETURN(replacement);
  assert(old.obj->ref_count == 1 && v[0].obj->ref_count == 1);
  mrbc_decref(&old);
  puts("PASS SET_RETURN decrefs old self, does not incref result");
}

static void unsafe_alias_test(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int before = destructor_calls;
  SET_RETURN(v[0]);
  assert(destructor_calls == before + 1);
  v[0] = mrbc_nil_value();
  puts("PASS SET_RETURN(self) destroyed sole reference; freed value not dereferenced");
}

static void retained_alias_test(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int before = destructor_calls;
  mrbc_value retained = v[0];
  mrbc_incref(&retained);
  SET_RETURN(retained);
  assert(destructor_calls == before && v[0].obj->ref_count == 1);
  mrbc_decref_empty(&v[0]);
  assert(destructor_calls == before + 1);
  puts("PASS retaining self before SET_RETURN preserves object until caller release");
}

static void replace_self(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int before = destructor_calls;
  SET_RETURN(mrbc_string_new_cstr(vm, "replacement"));
  assert(destructor_calls == before + 1 && v[0].obj->ref_count == 1);
  mrbc_decref_empty(&v[0]);
  assert(destructor_calls == before + 1);
  puts("PASS SET_RETURN releases old object exactly once");
}

static void destructor_ownership(mrbc_vm *vm)
{
  mrbc_value local[1] = {mrbc_instance_new(vm, data_class, sizeof(int))};
  *(int *)local[0].instance->data = 123;
  replace_self(vm, local, 0);
  int before = destructor_calls;
  mrbc_value array = mrbc_array_new(vm, 1);
  mrbc_value element = mrbc_instance_new(vm, data_class, sizeof(int));
  *(int *)element.instance->data = 123;
  assert(mrbc_array_set(&array, 0, &element) == 0);
  mrbc_value retained = mrbc_array_get(&array, 0);
  assert(retained.obj->ref_count == 1);
  mrbc_incref(&retained);
  mrbc_decref(&array);
  assert(destructor_calls == before && retained.obj->ref_count == 1);
  mrbc_decref_empty(&retained);
  assert(destructor_calls == before + 1);
  puts("PASS retained array element destroyed only after last owner");
}

static void ownership(mrbc_vm *vm, mrbc_value v[], int argc)
{
  mrbc_value local[2] = {mrbc_string_new_cstr(vm, "old"), mrbc_nil_value()};
  macro_test(vm, local, 0);
  mrbc_decref(&local[0]);

  mrbc_value array = mrbc_array_new(vm, 1);
  mrbc_value string = mrbc_string_new_cstr(vm, "element");
  assert(mrbc_array_set(&array, 0, &string) == 0);
  assert(string.obj->ref_count == 1);
  mrbc_value borrowed = mrbc_array_get(&array, 0);
  assert(borrowed.obj->ref_count == 1);
  mrbc_incref(&borrowed);
  assert(string.obj->ref_count == 2);
  mrbc_decref(&borrowed);
  mrbc_decref(&array);
  puts("PASS array_set transfers; array_get borrows");

  mrbc_value object = mrbc_instance_new(vm, data_class, sizeof(int));
  *(int *)object.instance->data = 123;
  string = mrbc_string_new_cstr(vm, "ivar");
  mrbc_sym key = mrbc_str_to_symid("@value");
  mrbc_instance_setiv(&object, key, &string);
  assert(string.obj->ref_count == 2);
  mrbc_value owned = mrbc_instance_getiv(&object, key);
  assert(string.obj->ref_count == 3);
  mrbc_decref(&owned);
  mrbc_decref(&string);
  mrbc_decref(&object);
  assert(destructor_calls == 1);
  puts("PASS ivar setter/getter retain; instance-data destructor runs");

  local[0] = mrbc_instance_new(vm, data_class, sizeof(int));
  *(int *)local[0].instance->data = 123;
  unsafe_alias_test(vm, local, 0);
  local[0] = mrbc_instance_new(vm, data_class, sizeof(int));
  *(int *)local[0].instance->data = 123;
  retained_alias_test(vm, local, 0);

  string = mrbc_string_new_cstr(vm, "const");
  key = mrbc_str_to_symid("BINDING_CONTRACT_CONSTANT");
  assert(mrbc_set_const(key, &string) == 0);
  assert(string.obj->ref_count == 1);
  assert(mrbc_get_const(key)->string == string.string);
  puts("PASS set_const transfers; get_const borrows");
  destructor_ownership(vm);
  SET_TRUE_RETURN();
}

static void layout(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int keyword = mrbc_type(v[argc + 1]) == MRBC_TT_HASH;
  int block = mrbc_type(v[argc + 1 + keyword]) == MRBC_TT_PROC;
  SET_INT_RETURN(argc * 100 + keyword * 10 + block);
}

static void keyword(mrbc_vm *vm, mrbc_value v[], int argc)
{
  MRBC_KW_ARG(required, optional);
  if (argc != 1) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "one positional argument required");
    goto done;
  }
  if (!MRBC_KW_MANDATORY(required) || !MRBC_KW_END()) goto done;
  if (mrbc_type(required) != MRBC_TT_STRING ||
      (MRBC_KW_ISVALID(optional) && mrbc_type(optional) != MRBC_TT_INTEGER)) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "wrong keyword type");
    goto done;
  }
  mrbc_value result = mrbc_array_new(vm, 3);
  mrbc_incref(&required);
  mrbc_array_set(&result, 0, &required);
  mrbc_value option = MRBC_KW_ISVALID(optional) ? optional : mrbc_integer_value(4);
  mrbc_array_set(&result, 1, &option);
  mrbc_array_set(&result, 2, &v[1]);
  SET_RETURN(result);
done:
  MRBC_KW_DELETE(required, optional);
}

static void dict(mrbc_vm *vm, mrbc_value v[], int argc)
{
  MRBC_KW_ARG(required);
  MRBC_KW_DICT(rest);
  if (!MRBC_KW_MANDATORY(required)) {
    MRBC_KW_DELETE(required, rest);
    return;
  }
  SET_RETURN(rest);
  MRBC_KW_DELETE(required);
}

static void keyword_guard(mrbc_vm *vm, mrbc_value v[], int argc)
{
  MRBC_KW_ARG(mode);
  if (!MRBC_KW_MANDATORY(mode)) goto RETURN;
  if (!MRBC_KW_END()) goto RETURN;
  if (mrbc_type(mode) != MRBC_TT_SYMBOL) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "mode must be Symbol");
    goto RETURN;
  }
  keyword_side_effects++;
  SET_TRUE_RETURN();
RETURN:
  MRBC_KW_DELETE(mode);
}

static void keyword_effects(mrbc_vm *vm, mrbc_value v[], int argc)
{
  SET_INT_RETURN(keyword_side_effects);
}

static void save_block(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int index = argc + 1 + (mrbc_type(v[argc + 1]) == MRBC_TT_HASH);
  if (mrbc_type(v[index]) != MRBC_TT_PROC) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "block required");
    return;
  }
  mrbc_value next = v[index];
  mrbc_incref(&next);
  mrbc_decref(&saved);
  saved = next;
  SET_NIL_RETURN();
}

static void saved_block(mrbc_vm *vm, mrbc_value v[], int argc)
{
  assert(mrbc_type(saved) == MRBC_TT_NIL || mrbc_type(saved) == MRBC_TT_PROC);
  mrbc_incref(&saved);
  SET_RETURN(saved);
}

static void clear_block(mrbc_vm *vm, mrbc_value v[], int argc)
{
  mrbc_decref(&saved);
  saved = mrbc_nil_value();
  SET_NIL_RETURN();
}

static void send_c(mrbc_vm *vm, mrbc_value v[], int argc)
{
  int refs = v[2].obj->ref_count;
  mrbc_value result = mrbc_send(vm, v, argc, &v[1], "+", 1, &v[2]);
  assert(!mrbc_israised(vm));
  assert(refs == v[2].obj->ref_count);
  SET_RETURN(result);
}

static void send_method(mrbc_vm *vm, mrbc_value v[], int argc)
{
  const char *name = mrbc_string_cstr(&v[2]);
  mrbc_value result = mrbc_send(vm, v, argc, &v[1], name, 0);
  if (mrbc_israised(vm)) {
    detected++;
    mrbc_decref(&result);
    return;
  }
  SET_RETURN(result);
}

static void fail_method(mrbc_vm *vm, mrbc_value v[], int argc)
{
  mrbc_raise(vm, error_class, "from C");
  after_raise++;
}

static void statistics(mrbc_vm *vm, mrbc_value v[], int argc)
{
  SET_INT_RETURN(detected * 10 + after_raise);
}

static void numeric(mrbc_vm *vm, mrbc_value v[], int argc)
{
  mrbc_int_t result = MRBC_ARG_I(1);
  if (mrbc_israised(vm)) return;
  SET_INT_RETURN(result);
}

static void guarded(mrbc_vm *vm, mrbc_value v[], int argc)
{
  if (argc != 1) {
    mrbc_raise(vm, MRBC_CLASS(ArgumentError), "one argument required");
    return;
  }
  if (mrbc_type(v[1]) != MRBC_TT_INTEGER) {
    mrbc_raise(vm, MRBC_CLASS(TypeError), "Integer required");
    return;
  }
  guarded_side_effects++;
  SET_INT_RETURN(mrbc_integer(v[1]));
}

static void guarded_count(mrbc_vm *vm, mrbc_value v[], int argc)
{
  SET_INT_RETURN(guarded_side_effects);
}

void binding_contract_init(void)
{
  saved = mrbc_nil_value();
  mrbc_class *cls = mrbc_define_class(NULL, "BindingContract", NULL);
  data_class = mrbc_define_class_under(NULL, cls, "Data", NULL);
  mrbc_define_destructor(data_class, destroy_data);
  error_class = mrbc_define_class(NULL, "BindingContractError", MRBC_CLASS(StandardError));
  mrbc_define_method(NULL, cls, "ownership", ownership);
  mrbc_define_method(NULL, cls, "layout", layout);
  mrbc_define_method(NULL, cls, "keyword", keyword);
  mrbc_define_method(NULL, cls, "keyword_guard", keyword_guard);
  mrbc_define_method(NULL, cls, "keyword_effects", keyword_effects);
  mrbc_define_method(NULL, cls, "dict", dict);
  mrbc_define_method(NULL, cls, "save_block", save_block);
  mrbc_define_method(NULL, cls, "saved", saved_block);
  mrbc_define_method(NULL, cls, "clear_block", clear_block);
  mrbc_define_method(NULL, cls, "send_c", send_c);
  mrbc_define_method(NULL, cls, "send_method", send_method);
  mrbc_define_method(NULL, cls, "fail_method", fail_method);
  mrbc_define_method(NULL, cls, "statistics", statistics);
  mrbc_define_method(NULL, cls, "numeric", numeric);
  mrbc_define_method(NULL, cls, "guarded", guarded);
  mrbc_define_method(NULL, cls, "guarded_count", guarded_count);
  value_contract_init(cls);
}
