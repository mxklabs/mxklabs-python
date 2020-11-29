from .exprevaluator import ExprEvaluator

class Expr:

  def __init__(self, ctx, exprset, id, ops, attrs):
    self.ctx = ctx
    self.exprset = exprset
    self.id = id
    self.ops = ops
    self.attrs = attrs

  def evaluate(self, varmap):
    """
    Return the value of this expression under a given dictionary mapping
    variables to values.
    """
    evaluator = ExprEvaluator(self.ctx, varmap)
    return evaluator.eval(self)

