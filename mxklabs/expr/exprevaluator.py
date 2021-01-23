import functools

class ExprEvaluator:
    """
    This class can be used to 'compute' the value of an expression under a
    specific assignment of values to variables in said expression.
    """

    def __init__(self, ctx, varmap):
      self._ctx = ctx
      self._varmap = varmap

    @functools.lru_cache(maxsize=None)
    def eval(self, expr):
      if self._ctx.is_variable(expr):
        if expr not in self._varmap:
          raise RuntimeError(f'evaluation depends on value for variable \'{expr.name()}\', which is not available')
        return self._varmap[expr]
      if self._ctx.is_constant(expr):
        return expr.value()
      else:
        # Evaluate expr's ops.
        opvals = [self.eval(op) for op in expr.ops()]
        # Determine the value.
        return expr.evaluate(opvals)
