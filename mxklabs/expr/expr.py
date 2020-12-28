from .exprevaluator import ExprEvaluator

import functools

class Expr:

  def __init__(self, **kwargs):
    self.ctx = kwargs['ctx']
    self.expr_class_set = kwargs['expr_class_set']
    self.identifier = kwargs['identifier']
    self.ops = kwargs['ops']
    self.valtype = kwargs['valtype']
    self.attrs = kwargs['attrs']
    self._hash = None

  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self.expr_class_set)
    hash_items.append(self.identifier)
    hash_items += self.ops
    hash_items.append(self.valtype)
    hash_items += self.attrs.keys()
    hash_items += self.attrs.values()
    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  def __str__(self):
    return self.get_compact_str()

  def __getattr__(self, name):
    if name in self.attrs:
      return self.attrs[name]
    else:
      # Default behaviour
      raise AttributeError

  def get_compact_str(self):
    if self.ctx.is_variable(self):
      return f"{self.name}"
    elif self.ctx.is_constant(self):
      return f"{self.value}"
    else:
      result = f"{self.identifier}("
      result += ",".join([f"{op}" for op in self.ops])
      result += ")"
      return result

  def get_pretty_str(self):
    if self.expr_class_set.is_variable(self):
      return f"{self.name}"
    elif self.expr_class_set.is_constant(self):
      return f"{self.value}"
    else:
      result = f"{self.expr_class_set.identifier}.{self.identifier}"
      for op in self.ops:
        result += f"\n  - {op}"
      return result

  #@functools.lru_cache(maxsize=1000)
  # Find a way to cache this.
  def __eq__(self, rhs):
    # TODO: Could optimise and use hash if already computed.
    result = self.ctx == rhs.ctx and \
           self.expr_class_set == rhs.expr_class_set and \
           self.identifier == rhs.identifier and \
           self.ops == rhs.ops and \
           self.valtype == rhs.valtype and \
           self.attrs == rhs.attrs
    print(f"{self} == {rhs} ==> {result}")
    return result
      

  def evaluate(self, varmap):
    """
    Return the value of this expression under a given dictionary mapping
    variables to values.
    """
    evaluator = ExprEvaluator(self.ctx, varmap)
    return evaluator.eval(self)
