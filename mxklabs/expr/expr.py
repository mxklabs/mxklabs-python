from .exprevaluator import ExprEvaluator

import functools

class Expr:

  def __init__(self, ctx, valtype):
    self._ctx = ctx
    self._valtype = valtype
    self._hash = None
    self._hash_items = [self._ctx, self._valtype]

  def ctx(self):
    return self._ctx

  def valtype(self):
    return self._valtype

  def __str__(self):
    return self.get_compact_str()

  def __repr__(self):
    return self.get_compact_str()

  def __hash__(self):
    if self._hash is not None:
      return self._hash
    self._hash = hash(tuple(self._hash_items))
    return self._hash

  # TODO: Find a way to cache this.
  def __eq__(self, rhs):

    # If hash computed and doesn't match, the expressions are not equivalent.
    if self._hash is not None and rhs._hash is not None:
      if self._hash != rhs._hash:
        return False

    # Compare each member.
    return all([l == r for l, r in zip(self._hash_items, rhs._hash_items)])

class Constant(Expr):

  def __init__(self, ctx, value, valtype):
    Expr.__init__(self, ctx, valtype)
    self._value = value
    self._hash_items.append(self._value)

  def value(self):
    return self._value

  def get_compact_str(self):
    return self._valtype.valtype_def().convert_value_to_str(
      self._valtype, self._value)

class Variable(Expr):

  def __init__(self, ctx, name, valtype):
    Expr.__init__(self, ctx, valtype)
    self._name = name
    self._hash_items.append(self._name)

  def name(self):
    return self._name

  def get_compact_str(self):
    return self._name

class OpExpr(Expr):

  def __init__(self, ctx, expr_def_set, expr_def, ops, attrs, valtype):
    Expr.__init__(self, ctx, valtype)
    self._expr_def_set = expr_def_set
    self._expr_def = expr_def
    self._ops = ops
    self._attrs = attrs

    self._hash_items.append(self._expr_def_set)
    self._hash_items.append(self._expr_def)
    self._hash_items += self._ops
    self._hash_items += self._attrs.keys()
    self._hash_items += self._attrs.values()

  def expr_def_set(self):
    return self._expr_def_set

  def expr_def(self):
    return self._expr_def

  def ops(self):
    return self._ops

  def attrs(self):
    return self._attrs

  def evaluate(self, op_values):
    return self._expr_def.evaluate(self, op_values)

  def __getattr__(self, field):
    if field in self._attrs:
      return self._attrs[field]
    else:
      # Default behaviour
      raise AttributeError

  def get_compact_str(self):
    # TODO: Use valtype to string function here.
    # TODO: Add attributes.
    result = f"{self._expr_def.baseid()}("
    items = [f"{op}" for op in self._ops]
    items += [f"{k}={v}" for k, v in self._attrs.items()]
    result += ", ".join(items)
    result += ")"
    return result

  #def get_pretty_str(self):
  #  # TODO: Use valtype to string function here.
  #  if self._ctx.is_variable(self):
  #    return f"{self.name}"
  #  elif self._ctx.is_constant(self):
  #    return f"{self.value}"
  #  else:
  #    # TODO: Add attributes.
  #    result = self._expr_def.id()
  #    for op in self._ops:
  #      result += f"\n  - {op}"
  #    return result


