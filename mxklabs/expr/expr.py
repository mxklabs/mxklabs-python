import abc
import functools

import six

from mxklabs.utils import Utils
from mxklabs.expr import exprtype as et


@six.add_metaclass(abc.ABCMeta)
class Expr(object):
    """
    Base class for all objects that represent an expression. This is an abstract
    base class. Derive from this class if you want to implement a custom type of
    expression; do not instantiate directly.
    """

    def __init__(self, expr_type, children=[], aux=[]):
        """
        Initialiser for Expr functions. Not normally called by end-users.
        :param expr_type: Either an object derived from ExprType, representing
        the type of this expression object or, preferably, a str that can be
        used to look-up this ExprType object using ExprTypeRepository.lookup().
        :param children: An iterable collection of Expr objects representing
        subexpressions.
        :param aux: An iterable collection of str objects, representing
        additional information like variable identifiers or constant values
        (normally empty)
        """
        if type(expr_type) == str:
          expr_type = et.ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(et.ExprType.is_exprtype(expr_type))
        Utils.check_precondition(Utils.is_iterable(children))
        Utils.check_precondition(all([Expr.is_expr(c) for c in children]))
        Utils.check_precondition(Utils.is_iterable(aux))
        Utils.check_precondition(all([type(a) == str for a in aux]))

        self._expr_type = expr_type
        self._children = children

        params = [self.node_str()] + [str(o) for o in children] + aux
        self._str_rep = "({})".format(" ".join(params))

    def node_str(self):
        """
        Get a string representing this expression node (e.g. 'logical-or' or
        'variable').
        :return: The string.
        """
        return Utils.camel_case_to_kebab_case(self.__class__.__name__)

    def expr_type(self):
        """
        Get the type of this expression (in the form of a ExprType object).
        :return: An ExprType object.
        """
        return self._expr_type
  
    def __lt__(self, other):
        """
        Implements an arbitrary total order on Expr objects based on a string
        representation of Expr objects. Returns true if this object is strictly
        less than other (another Expr object) in the total order.
        :param other: The Expr object to compare to.
        :return: True if strictly less than other.
        """
        Utils.check_precondition(isinstance(other, Expr))
        return self._str_rep < other._str_rep

    def __eq__(self, other):
        """
        Implements an equivalence on Expr objects based on a string
        representation of Expr objects. Returns true if this object is
        equivalent to other (another Expr object).
        :param other: The Expr object to compare to.
        :return: True if equal to other.
        """
        return self._str_rep == other._str_rep
  
    def __hash__(self):
        """
        Utility function to retrieve a hash value for this Expr object.
        :return: A hash value.
        """
        return hash(self._str_rep)

    def __str__(self):
        """
        Utility function to retrieve a string representation of an Expr object.
        :return: A string representation.
        """
        return self._str_rep

    def __repr__(self):
        """
        Return a string representation of this Expr object.
        :return: A string representation.
        """
        return self._str_rep

    def child(self, index=0):
        """
        Return child expression indexed by index.
        :param index: The index of the child to return (default=0, must be
        an int less then the number of children).
        :return: An Expr object representing a child expression.
        """
        Utils.check_precondition(type(index) == int)
        Utils.check_precondition(index < len(self._children))
        return self._children[index]

    def children(self):
        """
        Return a iterable container of all children.
        :return: An iterable container of all children.
        """
        return self._children

    def visit(self, visitor, **kwargs):
        """
        Call a method corresponding to our Expr class name on the visitor with
        **kwargs and return the value. For a class called SomeExpr we call the
        function visitor.visit_some_expr(self, **kwargs) and return the result.
        :param args: The parameter to pass to the visitor method.
        :return: The result of the visitor method.
        """
        visit_method_name = '_visit_' + Utils.camel_case_to_snake_case(
            self.__class__.__name__)
        visit_method = getattr(visitor, visit_method_name)

        return visit_method(self, **kwargs)

    def ensure_number_of_children(self, n):
        if len(self._children) != n:
            raise Exception("type \"{type}\" requires exactly {num_children} operand(s)".format(
                            type=str(type), num_children=n))

    def ensure_minimum_number_of_children(self, n):
        if len(self._children) < n:
            raise Exception("type \"{type}\" requires at least {min_num_children} operand(s)".format(
                            type=str(type), min_num_children=n))

    def ensure_maximum_number_of_children(self, n):
        if len(self._children) > n:
            raise Exception("type \"{type}\" requires at most {max_num_children} operand(s)".format(
                            type=str(type), max_num_children=n))

    def ensure_child_is_constant(self, index):
        if not isinstance(self._children[index], Const):
            raise Exception("type \"{type}\" requires subexpression '{childstr}' to be constant".format(
                            type=str(type), childstr=str(self._children[index])))

    def ensure_child_is_type(self, index, type):
        if self._children[index].expr_type() != type:
            raise Exception("type \"{type}\" requires subexpression '{childstr}' to be to be of type "
                            "'{exptype}' but it is of type '{childtype}')".format(
                            type=str(type), childstr=str(self._children[index]), exptype=type,
                            childtype=str(self._children[index].expr_type())))

    def ensure_children_types_match(self):
        for i in range(1,len(self.children())):
            if self._children[i].expr_type() != self._children[0].expr_type():
                raise Exception("expression '{expr}' requires the type of subexpression "
                                "'{childstr1}' to match the type of subexpression '{childstr2}' but "
                                "this is not the case (types are '{childtype1}' and '{childtype2}', "
                                "respectively)".format(expr=Utils.camel_case_to_snake_case(
                                                       self.__class__.__name__),
                                                       childstr1=self._children[i],
                                                       childstr2=self._children[0],
                                                       childtype1=self._children[i].expr_type(),
                                                       childtype2=self._children[0].expr_type()))


    @staticmethod
    def is_expr(obj):
        """
        Static method that can be used to check if an object is an Expr.
        :param obj: The object to check.
        :return: True if and only if expr is an instance of Expr.
        """
        try:
            return isinstance(obj, Expr)
        except:
            return False


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
            Utils.check_precondition(expr_type.is_valid_littup_value(littup_value))

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
