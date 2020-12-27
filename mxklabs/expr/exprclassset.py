from .expr import Expr
from .module import Module

class ExprClassSet(Module):

  def __init__(self, ctx, identifier, module):
    Module.__init__(self, ctx, identifier, module)
    self.expr_defs = {}
    self.input_validator = self.load_class(self.module.definition['inputValidator'], ctx=self.ctx)
    self.value_inference = self.load_class(self.module.definition['valueInference'], ctx=self.ctx)
    self.type_inference = self.load_class(self.module.definition['typeInference'], ctx=self.ctx)

    # TODO: Check expressions of type variable and constant exist and
    # have the attributes name and value.
    exprset_def = self.module.definition

    for expr_def in exprset_def['expressions']:
      self.expr_defs[expr_def['identifier']] = expr_def
      fun = lambda *ops, expr_def=expr_def, **attrs : self._expr_fun(*ops, expr_def=expr_def, **attrs)
      setattr(self, expr_def['identifier'], fun)

    for expr_def in self.module.definition['expressions']:
      if not hasattr(self.value_inference, expr_def['identifier']):
        raise RuntimeError(f"no value inference found for '{self.short_name}.{expr_def['identifier']}'")
      if not hasattr(self.type_inference, expr_def['identifier']):
        raise RuntimeError(f"no value inference found for '{self.short_name}.{expr_def['identifier']}'")

  def variable(self, name, **attrs):
    return self.ctx.make_var(name=name, valtype_fun=getattr(self.ctx, self.module.definition['varType']), **attrs)

  def constant(self, value, **attrs):
    return self.ctx.make_constant(value=value, valtype_fun=getattr(self.ctx, self.module.definition['varType']), **attrs)

  def _expr_fun(self, *ops, expr_def, **attrs):
    # Check operand and attribute validity.
    input_validator_fun = getattr(self.input_validator, expr_def['identifier'])
    input_validator_fun(*ops, **attrs)

    # Work out the type.
    type_infererence_fun = getattr(self.type_inference, expr_def['identifier'])
    valtype = type_infererence_fun(*[op.valtype for op in ops], **attrs)

    # Create the expression.
    expr = Expr(ctx=self.ctx, expr_class_set=self, identifier=expr_def['identifier'], ops=ops, valtype=valtype, attrs=attrs)
    return self.ctx.exprpool.make_unique(expr)

  def get_class(self, name):
    symbol = self.module
    for attr in name.split('.'):
      if not hasattr(symbol, attr):
        raise RuntimeError(f"class '{self.identifier}.{name}' not found")
      else:
        symbol = getattr(symbol, attr)
    return symbol

  def load_class(self, name, **kwargs):
    symbol = self.get_class(name)
    return symbol(**kwargs)



