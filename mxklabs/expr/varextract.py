from mxklabs.expr import expranalyse as ea
from mxklabs import utils

class VarExtractor(ea.ExprVisitor):
    """
    This class can be used to find all variables used in an expression.
    """

    @staticmethod
    def extract(expr):
        """
        Return the variables used in an expression.
        :param expr: The Expr object to evaluate.
        :return: A set object containing Var objects.
        """
        ee = VarExtractor()
        return expr.visit(ee)

    @utils.memoise
    def _visit_const(self, expr):
        return self._visit_default(expr)

    @utils.memoise
    def _visit_var(self, expr):
        return set([expr])

    @utils.memoise
    def _visit_logical_and(self, expr):
        return self._visit_default(expr)

    @utils.memoise
    def _visit_logical_or(self, expr):
        return self._visit_default(expr)

    @utils.memoise
    def _visit_logical_not(self, expr):
        return self._visit_default(expr)

    @utils.memoise
    def _visit_equals(self, expr):
        return self._visit_default(expr)

    @utils.memoise
    def _visit_default(self, expr):
        result = set()

        for child in expr.children():
            result = result.union(child.visit(self))

        return result
