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

    for exprdescr in self._module.exprdescrs['exprDescrs']:
      fun = lambda *ops, exprdescr=exprdescr, **attrs : self._expr_fun(*ops, exprdescr=exprdescr, **attrs)
      setattr(self, exprdescr['id'], fun)

    self.load_semantics()

  def variable(self, name):
    return self.ctx.make_var(name=name, valtype=self._module.exprdescrs['varType'])

  def constant(self, value):
    return self.ctx.make_constant(value=value, valtype=self._module.exprdescrs['varType'])

  def _expr_fun(self, *ops, exprdescr, **attrs):
    # Check operators.
    if (exprdescr['minOps'] is not None and len(ops) < exprdescr['minOps']):
      raise RuntimeError(f"'{self.short_name}.{exprdescr['id']}' expect at least {exprdescr['minOps']} operands (got {len(ops)})")
    if (exprdescr['maxOps'] is not None and len(ops) > exprdescr['maxOps']):
      raise RuntimeError(f"'{self.short_name}.{exprdescr['id']}' expect at most {exprdescr['maxOps']} operands (got {len(ops)})")

    for op_index, op in zip(range(len(ops)), ops):
      if not isinstance(op, Expr):
        raise RuntimeError(f"'{self.short_name}.{exprdescr['id']}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

    # TODO: Check operand validity.
    # TODO: Check all operands are from the same context.

    # Check attributes.
    expAttrs = set(exprdescr['attrs'])
    actAttrs = set(attrs.keys())

    for actAttr in actAttrs:
      if actAttr not in expAttrs:
        raise RuntimeError(f"'{self.short_name}.{exprdescr['id']}' does not expect attribute '{actAttr}'")
    for expAttr in expAttrs:
      if expAttr not in actAttrs:
        raise RuntimeError(f"'{self.short_name}.{exprdescr['id']}' expects attribute '{expAttr}'")

    # TODO: Check attribute validity.

    assert(exprdescr['maxOps'] is None or len(ops) <= exprdescr['maxOps'])
    return self.ctx.make_expr(exprset=self, id=exprdescr['id'], ops=ops, attrs=attrs)

  def load_semantics(self):
    self.semantics = Semantics()
    print(f'DIR={dir(self._module.semantics)}')
    for exprdescr in self._module.exprdescrs['exprDescrs']:
      fun = getattr(self._module.semantics, exprdescr['id'])
      setattr(self.semantics, exprdescr['id'], lambda *opvals, fun=fun : fun(*opvals))
