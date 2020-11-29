import functools

class ExprEvaluator:
    """
    This class can be used to 'compute' the value of an expression under a
    specific assignment of values to variables in said expression.
    """

    def __init__(self, ctx, varmap):
      self.ctx = ctx
      self.varmap = varmap

    @functools.lru_cache(maxsize=None)
    def eval(self, expr):
      if expr.id == 'variable':
        return self.varmap[expr]
      else:
        # Evaluate expr's ops.
        opvals = [self.eval(op) for op in expr.ops]
        # Get the function to evaluate op.
        semantics_fun = getattr(expr.exprset.semantics, expr.id)
        # Evaluate it.
        return semantics_fun(opvals)
