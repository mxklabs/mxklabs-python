from .expr import Expr
from .module import Module

class ExprClassSet(Module):

  def __init__(self, ctx, proxy, identifier, module):
    Module.__init__(self, ctx, identifier, module)
    self._proxy = proxy
    self.expr_defs = {}
    self.input_validator = self.load_class(self.module.definition['inputValidator'], ctx=self.ctx)
    self.expr_simplifier = self.load_class(self.module.definition['exprSimplifier'], ctx=self.ctx)
    self.value_inference = self.load_class(self.module.definition['valueInference'], ctx=self.ctx)
    self.type_inference = self.load_class(self.module.definition['typeInference'], ctx=self.ctx)

    # TODO: Check expressions of type variable and constant exist and
    # have the attributes name and value.
    exprset_def = self.module.definition

    for expr_def in exprset_def['expressions']:
      exprid = expr_def['identifier']
      self.expr_defs[exprid] = expr_def
      fun = lambda *ops, exprid=exprid, **attrs : self._expr_fun(*ops, exprid=exprid, **attrs)
      setattr(self._proxy, exprid, fun)
      is_fun = lambda expr, exprid=exprid: self._is_expr_fun(expr, exprid)
      setattr(self._proxy, f"is_{exprid}", is_fun)

    for expr_def in self.module.definition['expressions']:
      if not hasattr(self.value_inference, expr_def['identifier']):
        raise RuntimeError(f"no value inference found for '{self.short_name}.{expr_def['identifier']}'")
      if not hasattr(self.type_inference, expr_def['identifier']):
        raise RuntimeError(f"no value inference found for '{self.short_name}.{expr_def['identifier']}'")

  def _is_expr_fun(self, expr, exprid):
    return expr.expr_class_set == self and expr.identifier == exprid

  def _expr_fun(self, *ops, exprid, **attrs):
    # Check operand and attribute validity.
    input_validator_fun = getattr(self.input_validator, exprid)
    input_validator_fun(*ops, **attrs)

    # See if we can simplify it.
    expr_simplifier_fun = getattr(self.expr_simplifier, exprid)
    simplifier_result = expr_simplifier_fun(*ops, **attrs)

    if simplifier_result is not None:
      return simplifier_result
    else:
      # Work out the type.
      type_infererence_fun = getattr(self.type_inference, exprid)
      valtype = type_infererence_fun(*ops, **attrs)

      # Create the expression.
      expr = Expr(ctx=self.ctx, expr_class_set=self, identifier=exprid, ops=ops, valtype=valtype, attrs=attrs)
      return self.ctx.exprpool.make_unique(expr)

  def get_cnf_mapping_class(self):
    return self.get_class(self.module.definition['cnfMapping'])

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



