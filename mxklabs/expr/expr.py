from mxklabs.expr.exprbase import Expr
from mxklabs.expr import exprtype as et
from mxklabs.utils import Utils

class Const(Expr):
    """
    A class whose objects represent constant expressions like integer literals
    or boolean values such as true and false.
    """

    def __init__(self, expr_type, user_value=None, littup_value=None):
        """
        Construct an object that represents a constant value. Note that exactly
        one of user_value or littup_value must be None.
        :param expr_type: Either an object derived from ExprType, representing
        the type of this expression object or, preferably, a str that can be
        used to look-up this ExprType object using ExprTypeRepository.lookup().
        :param user_value: A valid 'user_value' representation of the constant
        for this ExprType (see ExprValue for more details).
        :param littup_value: A valid 'littup_value' representation of the
        constant for this ExprType (see ExprValue for more details).
        """
        if type(expr_type) == str:
            expr_type = et.ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(isinstance(expr_type, et.ExprType))
        Utils.check_precondition((user_value is None) != (littup_value is None))

        if user_value is not None:
            Utils.check_precondition(expr_type.is_valid_user_value(user_value))
        if littup_value is not None:
            Utils.check_precondition(
                expr_type.is_valid_littup_value(littup_value))

        self._expr_value = et.ExprValue(expr_type=expr_type,
                                        user_value=user_value,
                                        littup_value=littup_value)

        aux = [str(expr_type), str(self._expr_value).lower()]
        Expr.__init__(self, expr_type=expr_type, aux=aux)

    def expr_value(self):
        """
        Return the constant's value as an ExprValue object.
        :return: The constant's value as an ExprValue object.
        """
        return self._expr_value


class Var(Expr):
    """
    A class whose objects represent variables.
    """

    def __init__(self, expr_type, id):
        """
        Construct an object that represents a variable. Note that exactly one
        of user_value or littup_value must be None.
        :param expr_type: Either an object derived from ExprType, representing
        the type of this expression object or, preferably, a str that can be
        used to look-up this ExprType object using ExprTypeRepository.lookup().
        :param id: A str object representing the variable's identifier.
        """
        if type(expr_type) == str:
            expr_type = et.ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(isinstance(expr_type, et.ExprType))
        Utils.check_precondition(type(id) == str)

        self.id_ = id

        aux = [str(expr_type), id]
        Expr.__init__(self, expr_type=expr_type, aux=aux)

    def id(self):
        """
        Return the variable's identifier.
        :return: The variable's identifier as a str object.
        """
        return self.id_


class LogicalAnd(Expr):
    """ An object that represents a logical AND expression. """

    def __init__(self, *args):
        """
        Construct a LogicalAnd object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, et.ExprTypeRepository._BOOL)


class LogicalOr(Expr):
    """ An object that represents a logical OR expression. """

    def __init__(self, *args):
        """
        Construct a LogicalOr object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=args)

        self.ensure_minimum_number_of_children(1)
        for i in range(len(self.children())):
            self.ensure_child_is_type(i, et.ExprTypeRepository._BOOL)


class LogicalNot(Expr):
    """ An object that represents a logical NOT expression. """

    def __init__(self, arg):
        """
        Construct a LogicalNot object.
        :param args: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=[arg])

        self.ensure_number_of_children(1)
        self.ensure_child_is_type(0, et.ExprTypeRepository._BOOL)


class Equals(Expr):
    """ An object that represents an equivalence expression. """

    def __init__(self, op0, op1):
        Expr.__init__(self, expr_type='bool', children=[op0, op1])

        self.ensure_number_of_children(2)
        self.ensure_children_types_match()


class IfThenElse(Expr):
    """ An object that represents an equivalence expression. """

    def __init__(self, op0, op1):
        Expr.__init__(self, expr_type='bool', children=[op0, op1])

        self.ensure_number_of_children(3)
        self.ensure_children_types_match([1,2])

            #class IfThenElse(Expr):
#
#    def __init__(self, args):
#        pass


#class Subtract(Expr):
#    """
#    An object that represents a bit vector subtraction modulo 2^n where both op0
#    and op1 must be Expr objects with type 'uint<n>' for some n.
#    """
#
#    def __init__(self, op0, op1):
#        """
#        Construct a LogicalAnd object.
#        :param args: One or more Expr objects of type Bool (operands).
#        """
#        Expr.__init__(self, type=op0.expr_type(), nodestr="subtract", children=[op0, op1])
#
#        self.ensure_number_of_children(2)
#        //self.ensure_child_is_type(i, et.ExprTypeRepository._)
#
#class Extract(Expr):
#    """
#    An object representing an extraction expression. An extraction expression
#    has three operands: a bitvector an index
#    """
#    def __init(self, args):
#        pass
#
#class Insert(Expr):
#    """
#    An object that represets a bitvector expression that is the result of insert
#    """