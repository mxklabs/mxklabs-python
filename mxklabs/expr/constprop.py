from mxklabs.expr import expr as ex
from mxklabs.expr import expranalyse as ea
from mxklabs.expr import exprbool as eb
from mxklabs.expr import exprcomp as ec
from mxklabs.expr import exprtype as et

from mxklabs import utils

class ConstPropagator(ea.ExprVisitor):

    @staticmethod
    def propagate(expr):
        cp = ConstPropagator()
        return expr.visit(cp)

    @utils.memoise
    def _visit_const(self, expr):
        return expr

    @utils.memoise
    def _visit_var(self, expr):
        return expr

    @utils.memoise
    def _visit_logical_and(self, expr):

        ops = [child.visit(self) for child in expr.children()]

        # If ANY operand is false, return false.
        if any([self._is_value(op, False) for op in ops]):
            return ex.Const('bool', False)

        # If ALL operands are true, return true.
        if all([self._is_value(op, True) for op in ops]):
            return ex.Const('bool', True)

        return eb.LogicalAnd(*ops)

    @utils.memoise
    def _visit_logical_or(self, expr):
        ops = [child.visit(self) for child in expr.children()]

        # If ALL operand are false, return false.
        if all([self._is_value(op, False) for op in ops]):
            return ex.Const('bool', False)

        # If ANY operand is true, return true.
        if any([self._is_value(op, True) for op in ops]):
            return ex.Const('bool', True)

        return eb.LogicalOr(*ops)

    @utils.memoise
    def _visit_logical_not(self, expr):
        op = expr.child().visit(self)

        if isinstance(op, ex.Const):
            return ex.Const('bool', not op.expr_value().user_value())
        else:
            return eb.LogicalNot(op)

    @utils.memoise
    def _visit_equals(self, expr):
        ops = [child.visit(self) for child in expr.children()]

        if ops[0] == ops[1]:
            # Comparing an expression against itself?
            return ex.Const('bool', True)

        elif isinstance(ops[0], ex.Const) and isinstance(ops[1], ex.Const):
            # When comparing two Const objects we can work out the result.
            is_equal = (ops[0].expr_value() == ops[1].expr_value())
            return ex.Const('bool', is_equal)

        return ec.Equals(*ops)

    @utils.memoise
    def _is_value(self, expr, user_value):
        '''
        Internal helper function which returns True iff expr is a Const with
        ExprValue that matches user_value.
        :param expr: The expression to check.
        :param user_value: The value to consider.
        :return: True iff expr is a Const with ExprValue that matches
        user_value.
        '''
        if isinstance(expr, ex.Const):
            return expr.expr_value() == et.ExprValue(expr.expr_type(), user_value)
        else:
            return False
