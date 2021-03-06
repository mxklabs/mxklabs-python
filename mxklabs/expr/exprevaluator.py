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
      if expr.identifier == 'variable':
        if expr not in self.varmap:
          raise RuntimeError(f'evaluation depends on value for variable \'{expr.attrs["name"]}\', which is not available')
        return self.varmap[expr]
      else:
        # Evaluate expr's ops.
        opvals = [self.eval(op) for op in expr.ops]
        # Get the function to evaluate op.
        value_inference_fun = getattr(expr.expr_class_set.value_inference, expr.identifier)
        # Evaluate it.
        return value_inference_fun(expr, *opvals)
