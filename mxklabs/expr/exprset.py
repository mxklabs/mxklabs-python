from .expr import Expr
from .module import Module

class Semantics:
  pass

class ExprSet(Module):

  def __init__(self, ctx, id, module):
    Module.__init__(self, ctx, id, module)
    self.expr_defs = {}

    # TODO: Check expressions of type variable and constant exist and
    # have the attributes name and value.
    exprset_def = self.module.definition

    for expr_def in exprset_def['expressions']:
      self.expr_defs[expr_def['id']] = expr_def
      fun = lambda *ops, expr_def=expr_def, **attrs : self._expr_fun(*ops, expr_def=expr_def, **attrs)
      setattr(self, expr_def['id'], fun)

    self.semantics = self.load_class(self.module.definition['semantics'], ctx=self)
    for expr_def in self.module.definition['expressions']:
      if not hasattr(self.semantics, expr_def['id']):
        raise RuntimeError(f"no semantics found for '{self.short_name}.{expr_def['id']}'")

  def variable(self, name, **attrs):
    return self.ctx.make_var(name=name, val_type_class_id=self.module.definition['varType'], **attrs)

  def constant(self, value, **attrs):
    return self.ctx.make_constant(value=value, val_type_class_id=self.module.definition['varType'], **attrs)

  def _expr_fun(self, *ops, expr_def, **attrs):
    # Check operators.

    # TODO: Check attribute validity.
    return self.ctx.make_expr(exprset=self, id=expr_def['id'], ops=ops, attrs=attrs)

  def get_class(self, name):
    symbol = self.module
    for attr in name.split('.'):
      if not hasattr(symbol, attr):
        raise RuntimeError(f"class '{self.id}.{name}' not found")
      else:
        symbol = getattr(symbol, attr)
    return symbol

  def load_class(self, name, **kwargs):
    symbol = self.get_class(name)
    return symbol(**kwargs)

