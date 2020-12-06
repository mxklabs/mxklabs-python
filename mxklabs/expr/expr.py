from .exprevaluator import ExprEvaluator

import functools

class Expr:

  def __init__(self, ctx, exprset, ident, ops, attrs):
    self.ctx = ctx
    self.exprset = exprset
    self.ident = ident
    self.ops = ops
    self.attrs = attrs
    self._hash = None

  def __hash__(self):
    if self._hash:
      return self._hash

    hash_items = []
    hash_items.append(self.exprset)
    hash_items.append(self.ident)
    hash_items += self.ops
    hash_items += self.attrs.keys()
    hash_items += self.attrs.values()
    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  @functools.lru_cache(maxsize=1000)
  def __eq__(self, rhs):
    return self.exprset == rhs.exprset and \
           self.ident == rhs.ident and \
           self.ops == rhs.ops and \
           self.attrs == rhs.attrs

  def evaluate(self, varmap):
    """
    Return the value of this expression under a given dictionary mapping
    variables to values.
    """
    evaluator = ExprEvaluator(self.ctx, varmap)
    return evaluator.eval(self)

