from .exprevaluator import ExprEvaluator

import functools

class Expr:

  def __init__(self, ctx, exprset, id, ops, val_type, attrs):
    self.ctx = ctx
    self.exprset = exprset
    self.id = id
    self.ops = ops
    self.val_type = val_type
    self.attrs = attrs
    self._hash = None

    if self.exprset is not None and id in self.exprset.expr_defs:
      expr_def = self.exprset.expr_defs[id]

      # Check number of operands.
      min_ops = expr_def['minOps']
      max_ops = expr_def['maxOps']
      if (min_ops is not None and \
          max_ops is not None and \
          min_ops == max_ops):
        if (min_ops != len(ops)):
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects exactly {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
      else:
        if (min_ops is not None and len(ops) < min_ops):
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects at least {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
        if (max_ops is not None and len(ops) > max_ops):
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects at most {max_ops} operand{'s' if max_ops > 1 else ''} (got {len(ops)})")

      # Check operands are actually expression objects.
      for op_index, op in zip(range(len(ops)), ops):
        if not isinstance(op, Expr):
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

      # Check operands are from the same context.
      for op_index, op in zip(range(len(ops)), ops):
        if not isinstance(op, Expr):
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")


      # TODO: Check operand validity.
      # TODO: Check all operands are from the same context.

      # Check attributes.
      exp_attrs = set(expr_def['attrs'])
      act_attrs = set(attrs.keys())

      for actAttr in act_attrs:
        if actAttr not in exp_attrs:
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' does not expect attribute '{actAttr}'")
      for expAttr in exp_attrs:
        if expAttr not in act_attrs:
          raise RuntimeError(f"'{self.exprset.short_name}.{self.id}' expects attribute '{expAttr}'")


  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self.exprset)
    hash_items.append(self.id)
    hash_items += self.ops
    hash_items.append(self.val_type)
    hash_items += self.attrs.keys()
    hash_items += self.attrs.values()
    print(f'self.attrs={self.attrs} self.attrs.values={self.attrs.values()}')
    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  @functools.lru_cache(maxsize=1000)
  def __eq__(self, rhs):
    return self.exprset == rhs.exprset and \
           self.id == rhs.id and \
           self.ops == rhs.ops and \
           self.val_type == rhs.val_type and \
           self.attrs == rhs.attrs

  def evaluate(self, varmap):
    """
    Return the value of this expression under a given dictionary mapping
    variables to values.
    """
    evaluator = ExprEvaluator(self.ctx, varmap)
    return evaluator.eval(self)

