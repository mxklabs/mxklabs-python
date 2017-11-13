import abc
import functools
import itertools
import operator

import six

import mxklabs.utils

class ExprValue(object):
    """
    A container that holds the value of an Expr object. This class is used by
    the mxklabs module in various places but this type is not normally relevant
    to end users of this module.

    Values are represented by both a 'user value' and a 'littup value'. We rely
    on a ExprType object between these representations and to tell us what
    are valid representations. Note that the user value is typically a Python
    object that naturally represents the type (e.g. True for a boolean type or
    12 for an integer type) whereas the littup value must be a tuple of booleans
    (e.g. (True,) and (False, False, True, True)).
    """

    def __init__(self, type, user_value=None, littup_value=None):
        """
        To construct a ExprValue you need to provide exactly one value
        representation:

        v1 = mxklabs.ExprValue(mxklabs.Bool(), user_value=False)
        v1 = mxklabs.ExprValue(mxklabs.Bool(), littup_value=(False,))
        """
        assert(isinstance(type, ExprType))
        assert((user_value == None) != (littup_value == None))

        if user_value != None:
            assert(type.is_valid_user_value(user_value=user_value))
            self._type = type
            self._user_value = user_value
            self._littup_value = self._type.user_value_to_littup_value(self._user_value)

        if littup_value != None:
            assert(type.is_valid_littup_value(littup_value=littup_value))
            self._type = type
            self._littup_value = littup_value
            self._user_value = self._type.littup_value_to_user_value(self._littup_value)

    def __eq__(self, other):
        assert(isinstance(other, ExprValue))
        return self._littup_value == other._littup_value

    def __hash__(self):
        return hash(self._littup_value)

    def __str__(self):
        return str(self._user_value)

    def __repr__(self):
        return repr(self._user_value)

    def user_value(self):
        """ Return the 'user value' representation of this value. """
        return self._user_value

    def littup_value(self):
        """ Return the 'user value' representation of this value. """
        return self._littup_value
    
@six.add_metaclass(abc.ABCMeta)
class ExprType(object):
    """
    A class representing a type of an Expr object. One of the most important
    functions of an ExprType is to tell other classes what values an Expr is
    allowed to have. Values come in the form of ExprValue objects and they have
    two representations, a user_value and a littup_value. ExprType objects are
    expected to have various utility functions to help other classes establish
    what are valid such values and to convert between them.
    """

    def __init__(self, typestr):
        self._typestr = typestr

    def __eq__(self, other):
        assert (isinstance(other, ExprType))
        return self._typestr == other._typestr

    def __ne__(self, other):
        assert (isinstance(other, ExprType))
        return self._typestr != other._typestr

    def __hash__(self):
        return hash(self._typestr)

    def __str__(self):
        return self._typestr

    def __repr__(self):
        return self._typestr

    @abc.abstractmethod
    def values(self):
        """
        :return: Derived classes should return an iterable container of ExprValue
        objects. For example, a type for booleans could return a list of two
        ExprValue objects, one representing True and one representing False.

        Note that for types with a large numbers of values it is better not to
        explicitly construct a list of values.
        """
        pass

    @abc.abstractmethod
    def num_values(self):
        """
        :return: Derived classes should return the result of len(values()) here. This is
        primarily used to calculate the number possible variable assignments
        without actually iterating over them.
        """
        pass

    @abc.abstractmethod
    def littup_size(self):
        """
        :return: Derived classes should return the number of booleans required to encode
        a value. This is normally the smallest integer n such that 2^n >=
        num_values() although this is not a requirement.
        """
        pass

    @abc.abstractmethod
    def is_valid_user_value(self, user_value):
        """
        :param user_value: The user value representation to consider.
        :return: True if and only if the user_value parameter is a valid
        user value representation of this ExprType.
        """
        pass

    @abc.abstractmethod
    def is_valid_littup_value(self, littup_value):
        """
        :param littup_value: The littup value representation to consider.
        :return: True if and only if the littup_value parameter is a valid
        littup value representation of this ExprType.
        """
        pass
        return type(littup_value) == tuple and len(littup_value) == 1 and type(
        littup_value[0]) == bool

    @abc.abstractmethod
    def user_value_to_littup_value(self, user_value):
        """
        :param user_value: The user value to convert to a littup value.
        :return: A littup value representing the same value as user_value.
        """
        pass

    @abc.abstractmethod
    def littup_value_to_user_value(self, littup_value):
        """
        :param littup_value: The littup value to convert to a user value.
        :return: A user value representing the same value as littup_value.
        """

    @staticmethod
    def is_exprtype(type):
        """
        Call to see if type derives from ExprType.
        :param type: The python object to consider.
        :return: Return True if and only if type derives from ExprType.
        """
        try:
            return isinstance(type, ExprType)
        except Exception as e:
            return False




''' Class for product of types. '''

#class Product(ExprType):
#  
#  def __init__(self, subtypes, typestr=None):
#
#    if len(subtypes) < 1:
#      raise Exception("a product type must have at least one subtype")
#    for subtype in subtypes:
#      if not isinstance(subtype, ExprType):
#        raise Exception("the 'subtype' parameter of type 'Product' must be an interable over 'ExprType' (found '{type}' subtype)".format(
#                        type=subtype))
#
#    super().__init__(
#        # Use the given typestr if there is one. If not, use something like "(Bool,Bool)".
#        typestr="(" + ",".join([t._typestr for t in subtypes]) + ")" if typestr==None else typestr,
#        # Produce a values iterator (don't be explicit due to combinatorial explosions).
#        values=itertools.product(*([t.values() for t in subtypes])),
#        # Compute number of values.
#        num_values=functools.reduce(operator.mul, [s.num_values() for s in subtypes]))
#    
#    self._subtypes = subtypes
#    
#    
#    def is_valid_value(self, value):
#      if len(value) != len(self._subtypes):
#        return False
#      else:
#        return all([self._subtypes[s].is_valid_value(value[s]) for s in range(len(self._subtypes))])
#
#''' Parameterised types. '''
#
#class BitVector(Product):
#    
#  def __init__(self, bits):
#    super().__init__(subtypes=([Bool()] * bits), typestr=("uint%d" % bits))
#
#  @staticmethod
#  def int_to_value(bits, n):
#    return tuple([(((1 << b) & n) != 0,) for b in range(bits)])
#
#  @staticmethod
#  def value_to_int(bits, value):
#    return sum([(1 << b) if value[b][0] else 0 for b in range(len(value))])

