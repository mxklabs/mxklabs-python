import functools

from .expr import OpExpr

class ExprWalker:
    """
    This class can be used to apply a 'feature' to an expression in either
    a top-down or bottom-up fashion.
    """

    def __init__(self, ctx):
      self._ctx = ctx

    @functools.lru_cache(maxsize=None)
    def _bottom_up(self, expr, exprfun):
      assert(id(self._ctx) == id(expr.ctx()))
      if self._ctx.is_variable(expr):
        return expr
      elif self._ctx.is_constant(expr):
        return expr
      else:
        walked_ops = [self._bottom_up(op, exprfun) for op in expr.ops()]
        expr = OpExpr(self._ctx, expr.expr_def_set(), expr.expr_def(), walked_ops, expr.attrs(), expr.valtype())
        expr = self._ctx._expr_pool.make_unique(expr)
        expr = exprfun(expr)
        return expr

    @functools.lru_cache(maxsize=None)
    def _top_down(self, expr, exprfun):
      assert(id(self._ctx) == id(expr.ctx()))
      if self._ctx.is_variable(expr):
        return expr
      elif self._ctx.is_constant(expr):
        return expr
      else:
        expr = exprfun(expr)
        walked_ops = [self._top_down(op, exprfun) for op in expr.ops()]
        expr = OpExpr(self._ctx, expr.expr_def_set(), expr.expr_def(), walked_ops, expr.attrs(), expr.valtype())
        expr = self._ctx._expr_pool.make_unique(expr)
        return expr

    def simplify(self, expr):
      """ Bottom-up simplify. """
      def exprfun(expr):
        if expr.expr_def().has_feature('simplify'):
          return expr.expr_def().simplify(expr)
        else:
          return expr
      return self._bottom_up(expr, exprfun)

    def pushnot(self, expr):
      """  Top-down pushnot. """
      def exprfun(expr):
        if expr.expr_def().has_feature('pushnot'):
          return expr.expr_def().pushnot(expr)
        else:
          return expr
      return self._top_down(expr, exprfun)

    def canonicalize(self, expr):
      """ Bottom-up canonicalize. """
      def exprfun(expr):
        if expr.expr_def().has_feature('canonicalize'):
          return expr.expr_def().canonicalize(expr)
        else:
          return expr
      return self._bottom_up(expr, exprfun)

    @functools.lru_cache(maxsize=None)
    def decompose(self, expr):
      """ Top-down decompose until no longer decomposable. """
      assert(id(self._ctx) == id(expr.ctx()))
      if self._ctx.is_variable(expr):
        return expr
      elif self._ctx.is_constant(expr):
        return expr
      else:
        while expr.expr_def().has_feature('decompose'):
          decomposed_expr = expr.expr_def().decompose(expr)
          if decomposed_expr == expr:
            break
          else:
            expr = decomposed_expr
            walked_ops = [self.decompose(op) for op in expr.ops()]
            expr = OpExpr(self._ctx, expr.expr_def_set(), expr.expr_def(), walked_ops, expr.attrs(), expr.valtype())
            expr = self._ctx._expr_pool.make_unique(expr)
        return expr



