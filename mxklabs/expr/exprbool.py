from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et

class Bool(et.ExprType):
    """
    An object that represents a boolean expression type.
    """

    def __init__(self):
        """ Initialise Bool object. """
        self._values = [et.ExprValue(type=self, user_value=False),
                        et.ExprValue(type=self, user_value=True)]
        self._num_values = len(self._values)
        et.ExprType.__init__(self, "bool")

    def values(self):
        """ See ExprType.values. """
        return self._values

    def num_values(self):
        """ See ExprType.num_values. """
        return self._num_values

    def littup_size(self):
        """ See ExprType.littup_size. """
        return 1

    def is_valid_user_value(self, user_value):
        """ See ExprType.is_valid_user_value. """
        return type(user_value) == bool

    def is_valid_littup_value(self, littup_value):
        """ See ExprType.user_value_to_littup_value. """
        return type(littup_value) == tuple \
            and len(littup_value) == 1 \
            and type(littup_value[0]) == bool

    def user_value_to_littup_value(self, user_value):
        """ See ExprType.user_value_to_littup_value. """
        assert (self.is_valid_user_value(user_value))
        return (user_value,)

    def littup_value_to_user_value(self, littup_value):
        """ See ExprType.littup_value_to_user_value. """
        assert (self.is_valid_littup_value(littup_value))
        return littup_value[0]

class LogicalAnd(ex.Expr):
  
    def __init__(self, *args):
        ex.Expr.__init__(self, type=Bool(), nodestr="logical-and", children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, Bool())

class LogicalOr(ex.Expr):
  
    def __init__(self, *args):
        ex.Expr.__init__(self, type=Bool(), nodestr="logical-or", children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, Bool())

class LogicalNot(ex.Expr):
  
    def __init__(self, arg):
        ex.Expr.__init__(self, type=Bool(), nodestr="logical-not", children=[arg])

        self.ensure_number_of_children(1)
        self.ensure_child_is_type(0, Bool())
