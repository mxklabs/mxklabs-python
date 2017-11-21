from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et


class LogicalAnd(ex.Expr):
    """ An object that represents a logical AND expression. """

    def __init__(self, *args):
        """
        Construct a LogicalAnd object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        ex.Expr.__init__(self, expr_type='bool', children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, et.ExprTypeRepository._BOOL)

class LogicalOr(ex.Expr):
    """ An object that represents a logical OR expression. """

    def __init__(self, *args):
        """
        Construct a LogicalOr object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        ex.Expr.__init__(self, expr_type='bool', children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, et.ExprTypeRepository._BOOL)

class LogicalNot(ex.Expr):
    """ An object that represents a logical NOT expression. """

    def __init__(self, arg):
        """
        Construct a LogicalNot object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        ex.Expr.__init__(self, expr_type='bool', children=[arg])

        self.ensure_number_of_children(1)
        self.ensure_child_is_type(0, et.ExprTypeRepository._BOOL)
