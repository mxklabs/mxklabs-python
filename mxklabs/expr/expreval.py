from mxklabs.expr.exprvisitor import ExprVisitor
from mxklabs.expr.exprtype import ExprValue
from mxklabs.utils import memoise

class ExprEvaluator(ExprVisitor):
    """
    This class can be used to 'compute' the value of an expression under a
    specific assignment of values to variables in said expression.
    """

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

    def __init__(self, variable_assignment):
        """
        There is no need to instantiate this class manually. Use the eval method
        instead. This constructor is called internally.
        :param variable_assignment: A callable object that takes a Var parameter
        and produces a ExprValue of the same ExprType representing the
        variable's value.
        """
        self._variable_assignment = variable_assignment
        ExprVisitor.__init__(self)

    @memoise
    def _visit_const(self, expr):
        '''
        Internal method for working out the value of a constant.
        :param expr: A Const object.
        :return: An ExprValue object.
        '''
        return expr.expr_value()

    @memoise
    def _visit_var(self, expr):
        '''
        Internal method for working out the value of a variable.
        :param expr: A Var object.
        :return: An ExprValue object.
        '''
        return self._variable_assignment(expr)

    @memoise
    def _visit_logical_and(self, expr):
        '''
        Internal method for working out the value of a logical AND expression.
        :param expr: A LogicalAnd object.
        :return: An ExprValue object.
        '''
        children_res = [c.visit(self).user_value() for c in expr.children()]
        return ExprValue(expr_type='bool', user_value=all(children_res))

    @memoise
    def _visit_logical_or(self, expr):
        '''
        Internal method for working out the value of a logical OR expression.
        :param expr: A LogicalOr object.
        :return: An ExprValue object.
        '''
        children_res = [c.visit(self).user_value() for c in expr.children()]
        return ExprValue(expr_type='bool', user_value=any(children_res))

    @memoise
    def _visit_logical_not(self, expr):
        '''
        Internal method for working out the value of a logical NOT expression.
        :param expr: A LogicalNot object.
        :return: An ExprValue object.
        '''
        child0_res = expr.child(0).visit(self).user_value()
        return ExprValue(expr_type='bool', user_value=not child0_res)

    @memoise
    def _visit_equals(self, expr):
        '''
        Internal method for working out the value of an equivalence expression.
        :param expr: A Equals object.
        :return: An ExprValue object.
        '''
        child0_res = expr.child(0).visit(self).user_value()
        child1_res = expr.child(1).visit(self).user_value()
        return ExprValue(expr_type='bool',
            user_value=(child0_res == child1_res))



