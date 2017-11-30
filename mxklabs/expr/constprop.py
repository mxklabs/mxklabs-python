from mxklabs.expr.expr import LogicalAnd, LogicalOr, LogicalNot, Equals, \
    Const, Var
from mxklabs.expr.exprtype import ExprValue
from mxklabs.expr.exprvisitor import ExprVisitor
from mxklabs.utils import memoise

class ConstPropagator(ExprVisitor):
    """
    This class can be used to propagate constants in an expression.
    """

    @staticmethod
    def propagate(expr):
        """
        Return an equivalent expression (with constants propagated).
        :param expr: The Expr object to consider.
        :return: An Expr object equivalent to expr.
        """
        cp = ConstPropagator()
        return expr.visit(cp)

    @memoise
    def _visit_const(self, expr):
        '''
        Internal method for propagating constant in a Const object.
        :param expr: A Const object.
        :return: expr.
        '''
        return expr

    @memoise
    def _visit_var(self, expr):
        '''
        Internal method for propagating constant in a Var object.
        :param expr: A Var object.
        :return: expr.
        '''
        return expr

    @memoise
    def _visit_logical_and(self, expr):
        '''
        Internal method for propagating constant in a LogicalAnd object.
        :param expr: A LogicalAnd object.
        :return: An expression equi-satisfiable to expr.
        '''
        ops = [child.visit(self) for child in expr.children()]

        # If ANY operand is false, return false.
        if any([self._is_value(op, False) for op in ops]):
            return Const('bool', False)

        # If ALL operands are true, return true.
        if all([self._is_value(op, True) for op in ops]):
            return Const('bool', True)

        return LogicalAnd(*ops)

    @memoise
    def _visit_logical_or(self, expr):
        '''
        Internal method for propagating constant in a LogicalOr object.
        :param expr: A LogicalOr object.
        :return: An expression equi-satisfiable to expr.
        '''
        ops = [child.visit(self) for child in expr.children()]

        # If ALL operand are false, return false.
        if all([self._is_value(op, False) for op in ops]):
            return Const('bool', False)

        # If ANY operand is true, return true.
        if any([self._is_value(op, True) for op in ops]):
            return Const('bool', True)

        return LogicalOr(*ops)

    @memoise
    def _visit_logical_not(self, expr):
        '''
        Internal method for propagating constant in a LogicalNot object.
        :param expr: A LogicalNot object.
        :return: An expression equi-satisfiable to expr.
        '''

        op = expr.child().visit(self)

        if isinstance(op, Const):
            return Const('bool', not op.expr_value().user_value())
        else:
            return LogicalNot(op)

    @memoise
    def _visit_equals(self, expr):
        '''
        Internal method for propagating constant in a Equals object.
        :param expr: A Equals object.
        :return: An expression equi-satisfiable to expr.
        '''

        ops = [child.visit(self) for child in expr.children()]

        if ops[0] == ops[1]:
            # Comparing an expression against itself?
            return Const('bool', True)

        elif isinstance(ops[0], Const) and isinstance(ops[1], Const):
            # When comparing two Const objects we can work out the result.
            is_equal = (ops[0].expr_value() == ops[1].expr_value())
            return Const('bool', is_equal)

        return Equals(*ops)

    @memoise
    def _is_value(self, expr, user_value):
        '''
        Internal helper function which returns True iff expr is a Const with
        ExprValue that matches user_value.
        :param expr: The expression to check.
        :param user_value: The value to consider.
        :return: True iff expr is a Const with ExprValue that matches
        user_value.
        '''
        if isinstance(expr, Const):
            return expr.expr_value() == ExprValue(expr.expr_type(), user_value)
        else:
            return False
