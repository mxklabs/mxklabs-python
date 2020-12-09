from .expr import Expr

class Semantics:
  pass

class ExprSet:

  def __init__(self, ctx, id, short_name, module):
    self.ctx = ctx
    self.id = id
    self.short_name = short_name
    self._module = module

    # TODO: Check expressions of type variable and constant exist and
    # have the attributes name and value.
    exprset_def = self._module.definition
    for expr_def in exprset_def['expressions']:
      fun = lambda *ops, expr_def=expr_def, **attrs : self._expr_fun(*ops, expr_def=expr_def, **attrs)
      setattr(self, expr_def['id'], fun)

    self.load_semantics()

  def variable(self, name):
    return self.ctx.make_var(name=name, valtype=self._module.definition['varType'])

  def constant(self, value):
    return self.ctx.make_constant(value=value, valtype=self._module.definition['varType'])

  def _expr_fun(self, *ops, expr_def, **attrs):
    # Check operators.
    if (expr_def['minOps'] is not None and \
        expr_def['minOps'] is not None and \
        expr_def['minOps'] == expr_def['maxOps']):
      if (expr_def['minOps'] != len(ops)):
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' expects exactly {expr_def['minOps']} operand{'s' if expr_def['minOps'] > 1 else ''} (got {len(ops)})")
    else:
      if (expr_def['minOps'] is not None and len(ops) < expr_def['minOps']):
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' expects at least {expr_def['minOps']} operand{'s' if expr_def['minOps'] > 1 else ''} (got {len(ops)})")
      if (expr_def['maxOps'] is not None and len(ops) > expr_def['maxOps']):
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' expects at most {expr_def['maxOps']} operand{'s' if expr_def['maxOps'] > 1 else ''} (got {len(ops)})")

    for op_index, op in zip(range(len(ops)), ops):
      if not isinstance(op, Expr):
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

    # TODO: Check operand validity.
    # TODO: Check all operands are from the same context.

    # Check attributes.
    expAttrs = set(expr_def['attrs'])
    actAttrs = set(attrs.keys())

    for actAttr in actAttrs:
      if actAttr not in expAttrs:
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' does not expect attribute '{actAttr}'")
    for expAttr in expAttrs:
      if expAttr not in actAttrs:
        raise RuntimeError(f"'{self.short_name}.{expr_def['id']}' expects attribute '{expAttr}'")

    # TODO: Check attribute validity.

    assert(expr_def['maxOps'] is None or len(ops) <= expr_def['maxOps'])
    return self.ctx.make_expr(exprset=self, id=expr_def['id'], ops=ops, attrs=attrs)

  def load_semantics(self):
    self.semantics = self.load_class(self._module.definition['semantics'], ctx=self)
    for expr_def in self._module.definition['expressions']:
      if not hasattr(self.semantics, expr_def['id']):
        raise RuntimeError(f"no semantics found for '{self.short_name}.{expr_def['id']}'")

  def get_class(self, name):
    symbol = self._module
    for attr in name.split('.'):
      if not hasattr(symbol, attr):
        raise RuntimeError(f"class '{self.id}.{name}' not found")
      else:
        symbol = getattr(symbol, attr)
    return symbol

  def load_class(self, name, **kwargs):
    symbol = self.get_class(name)
    return symbol(**kwargs)

