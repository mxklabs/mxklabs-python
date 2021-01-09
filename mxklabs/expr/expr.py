from .exprevaluator import ExprEvaluator

import functools

class Expr:

  def __init__(self, ctx, expr_def_set, expr_def, ops, attrs, valtype):
    self._ctx = ctx
    self._expr_def_set = expr_def_set
    self._expr_def = expr_def
    self._ops = ops
    self._attrs = attrs
    self._valtype = valtype
    self._hash = None

  def ctx(self):
    return self._ctx

  def expr_def_set(self):
    return self._expr_def_set

  def expr_def(self):
    return self._expr_def

  def ops(self):
    return self._ops

  def attrs(self):
    return self._attrs

  def valtype(self):
    return self._valtype

  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self._expr_def_set)
    hash_items.append(self._expr_def)
    hash_items += self._ops
    hash_items += self._attrs.keys()
    hash_items += self._attrs.values()
    hash_items.append(self._valtype)

    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  def __str__(self):
    return self.get_compact_str()

  def __repr__(self):
    return self.get_compact_str()

  def __getattr__(self, name):
    if name in self._attrs:
      return self._attrs[name]
    else:
      # Default behaviour
      raise AttributeError

  def get_compact_str(self):
    # TODO: Use valtype to string function here.
    if self._ctx.is_variable(self):
      return f"{self.name}"
    elif self._ctx.is_constant(self):
      return f"{self.value}"
    else:
      # TODO: Add attributes.
      result = f"{self._expr_def.id()}("
      result += ",".join([f"{op}" for op in self._ops])
      result += ")"
      return result

  def get_pretty_str(self):
    # TODO: Use valtype to string function here.
    if self._ctx.is_variable(self):
      return f"{self.name}"
    elif self._ctx.is_constant(self):
      return f"{self.value}"
    else:
      # TODO: Add attributes.
      result = self._expr_def.id()
      for op in self._ops:
        result += f"\n  - {op}"
      return result

  # TODO: Find a way to cache this.
  def __eq__(self, rhs):
    # If hash computed and doesn't match, the expressions are not equivalent.
    if self._hash is not None and rhs._hash is not None:
      if self._hash != rhs._hash:
        return False

    # Compare each member.
    result = self._ctx == rhs._ctx and \
           self._expr_def_set == rhs._expr_def_set and \
           self._expr_def == rhs._expr_def and \
           self._ops == rhs._ops and \
           self._attrs == rhs._attrs and \
           self._valtype == rhs._valtype

    return result


