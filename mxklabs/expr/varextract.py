from six.moves import reduce

from mxklabs.expr.exprbase import Expr
from mxklabs.expr.exprvisitor import ExprVisitor
from mxklabs.utils import memoise, Utils


class VarExtractor(ExprVisitor):
    """
    This class can be used to find all variables used in an expression.
    """

    @staticmethod
    def extract(expr):
        """
        Return the variables used in an expression (or list of expressions).
        :param expr: The Expr object to evaluate or an iterable collection
           of such Expr objects.
        :return: A set object containing Var objects.
        """
        is_expr = isinstance(expr, Expr)
        is_iterable_exprs = Utils.is_iterable(expr) and \
            all([isinstance(e, Expr) for e in expr])

        assert(is_expr or is_iterable_exprs)

        ee = VarExtractor()
        if is_expr:
            return expr.visit(ee)
        if is_iterable_exprs:
            return reduce(lambda x,y: x.union(y),
                          [e.visit(ee) for e in expr],
                          set())

    def __init__(self):
        """
        There is no need to instantiate this class manually. Use the extract
        method instead. This constructor is called internally.
        """
        ExprVisitor.__init__(self)

    @memoise
    def _visit_const(self, expr):
        '''
        Internal method for working the variables used in a Const object.
        :param expr: A Const object.
        :return: A empty set object.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_var(self, expr):
        '''
        Internal method for working the variables used in a Var object.
        :param expr: A Var object.
        :return: A set object containing just expr.
        '''
        return set([expr])

    @memoise
    def _visit_logical_and(self, expr):
        '''
        Internal method for working the variables used in a LogicalAnd object.
        :param expr: A LogicalAnd object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_logical_or(self, expr):
        '''
        Internal method for working the variables used in a LogicalOr object.
        :param expr: A LogicalOr object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_logical_not(self, expr):
        '''
        Internal method for working the variables used in a LogicalNot object.
        :param expr: A LogicalNot object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_less_than_equals(self, expr):
        '''
        Internal method for working the variables used in a LessThanEquals
        object.
        :param expr: An LessThanEquals object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_equals(self, expr):
        '''
        Internal method for working the variables used in a Equals object.
        :param expr: An Equals object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_if_then_else(self, expr):
        '''
        Internal method for working the variables used in a IfThenElse object.
        :param expr: An IfThenElse object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_subtract(self, expr):
        '''
        Internal method for working the variables used in a Subtract object.
        :param expr: An Subtract object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_concatenate(self, expr):
        '''
        Internal method for working the variables used in a Concatenate object.
        :param expr: An Concatenate object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_slice(self, expr):
        '''
        Internal method for working the variables used in a Slice object.
        :param expr: An Slice object.
        :return: A set object containing variables used in expr.
        '''
        return self._visit_default(expr)

    @memoise
    def _visit_default(self, expr):
        '''
        Internal method for working out the variables used in an expression.
        :param expr: An Expr object.
        :return: A set object containing variables used in expr.
        '''
        return reduce(lambda x,y: x.union(y),
                      [child.visit(self) for child in expr.children()],
                      set())
