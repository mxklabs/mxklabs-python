from mxklabs.expr import expranalyse as ea
from mxklabs.expr import exprtype as et
from mxklabs import utils

class ExprEvaluator(ea.ExprVisitor):
    """
    This class can be used to 'compute' the value of an expression under a
    specific assignment of values to variables in said expression.
    """
    def __init__(self, variable_assignment):
        self._variable_assignment = variable_assignment
        ea.ExprVisitor.__init__(self)

    @utils.memoise
    def visit_const(self, expr):
        return expr.expr_value()

    @utils.memoise
    def visit_var(self, expr):
        return self._variable_assignment(expr)

    @utils.memoise
    def visit_logical_and(self, expr):
        children_res = [c.visit(self).user_value() for c in expr.children()]
        return et.ExprValue(expr_type='bool', user_value=all(children_res))

    @utils.memoise
    def visit_logical_or(self, expr):
        children_res = [c.visit(self).user_value() for c in expr.children()]
        return et.ExprValue(expr_type='bool', user_value=any(children_res))

    @utils.memoise
    def visit_logical_not(self, expr):
        child0_res = expr.child(0).visit(self).user_value()
        return et.ExprValue(expr_type='bool', user_value=not child0_res)

    @utils.memoise
    def visit_equals(self, expr):
        child0_res = expr.child(0).visit(self).user_value()
        child1_res = expr.child(1).visit(self).user_value()
        return et.ExprValue(expr_type='bool',
                            user_value=(child0_res == child1_res))

    ''' Quick version (avoid creating VarHarvester). '''

    @staticmethod
    def eval(expr, variable_assignment):
        """
        Return the value of this expression under a given assignment of values
        to variables.
        :param expr: The Expr object to evaluate.
        :param variable_assignment: The variable assignment to consider. This
        must be a callable object that takes Var objects as parameters and
        returns ExprValue objects to indicate their value.
        :return: The ExprValue representing the value of this Expr.
        """
        ee = ExprEvaluator(variable_assignment)
        return expr.visit(ee)

