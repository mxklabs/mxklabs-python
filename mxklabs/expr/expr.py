from mxklabs.expr.exprbase import Expr
from mxklabs.expr.exprtype import ExprType, ExprTypeRepository, ExprValue, \
    Product
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
            expr_type = ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(isinstance(expr_type, ExprType))
        Utils.check_precondition((user_value is None) != (littup_value is None))

        if user_value is not None:
            Utils.check_precondition(expr_type.is_valid_user_value(user_value))
        if littup_value is not None:
            Utils.check_precondition(
                expr_type.is_valid_littup_value(littup_value))

        self._expr_value = ExprValue(expr_type=expr_type,
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
            expr_type = ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(isinstance(expr_type, ExprType))
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

    def __init__(self, *ops):
        """
        Construct a LogicalAnd object.
        :param ops: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=ops)

        self.ensure_minimum_number_of_children(1)
        self.ensure_all_children_are_type('bool')


class LogicalOr(Expr):
    """ An object that represents a logical OR expression. """

    def __init__(self, *ops):
        """
        Construct a LogicalOr object.
        :param ops: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=ops)

        self.ensure_minimum_number_of_children(1)
        self.ensure_all_children_are_type('bool')


class LogicalNot(Expr):
    """ An object that represents a logical NOT expression. """

    def __init__(self, op):
        """
        Construct a LogicalNot object.
        :param ops: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, expr_type='bool', children=[op])

        self.ensure_number_of_children(1)
        self.ensure_child_is_type(0, 'bool')


class Equals(Expr):
    """ An object that represents an equivalence expression. """

    def __init__(self, op0, op1):
        Expr.__init__(self, expr_type='bool', children=[op0, op1])

        self.ensure_number_of_children(2)
        self.ensure_children_types_match([0,1])


class IfThenElse(Expr):
    """ An object that represents an equivalence expression. """

    def __init__(self, op0, op1, op2):
        Expr.__init__(self, expr_type=op1.expr_type(), children=[op0, op1])

        self.ensure_number_of_children(3)
        self.ensure_children_types_match([1,2])


class Subtract(Expr):
    """
    An object that represents a bit vector subtraction modulo 2^n where both op0
    and op1 must be Expr objects with type 'uint<n>' for some n.
    """
    def __init__(self, op0, op1):
        """
        Construct a LogicalAnd object.
        :param ops: One or more Expr objects of type Bool (operands).
        """
        Expr.__init__(self, type=op0.expr_type(), nodestr="subtract", children=[op0, op1])

        self.ensure_number_of_children(2)
        self.ensure_child_is_bitvec(0)
        self.ensure_children_types_match([0,1])

class Concatenate(Expr):
    """
    Take one or more expressions of type 'uint<n1>', 'uint<n2>', ... and
    concatenate the expressions into one bitvector of type 'uint<m>' where m
    is n1 + n2 + ...
    """

    def __init__(self, *ops):
        Expr.__init__(self, expr_type='uint{:d}'.format(len(ops)), children=ops)

        self.ensure_all_children_are_bitvecs()
        self.ensure_minimum_number_of_children(1)

class Slice(Expr):
    """
    Take an expression of type 'uintN', integers start_bit and end_bit and
    return a sliced version of the operand.
    """
    def __init__(self, op, start_bit, end_bit):
        self._start_bit = start_bit
        self._end_bit = end_bit

        Expr.__init__(self, expr_type='uint{:d}'.format(end_bit - start_bit),
                      children=[op], aux=[str(start_bit), str(end_bit)])

        self.ensure_child_is_bitvec(0)
        self.ensure_number_of_children(1)

        if start_bit > end_bit:
            raise Exception("Parameter start_bit (={}) must not exceed end_bit "
                            "(={})".format(start_bit, end_bit))

        if end_bit > op.littup_size():
            raise Exception("Parameter end_bit (={}) must not exceed {} when "
                            "operand is of type '{}'"
                            "(={})".format(end_bit, op.littup_size(), op))
