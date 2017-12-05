import abc
from functools import reduce
from itertools import product
from operator import add, mul
import re
import six

from mxklabs.utils import Utils, memoise

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

    def __init__(self, expr_type, user_value=None, littup_value=None):
        """
        To construct a ExprValue you need to provide exactly one value
        representation (not neither and not both). For example:

        v1 = mxklabs.ExprValue('bool', user_value=False)
        v1 = mxklabs.ExprValue('bool', littup_value=(False,))

        :param expr_type: Either an object derived from ExprType, representing
        the type of this value or, preferably, a str that can be used to look-up
        this ExprType object using ExprTypeRepository.lookup().
        :param user_value: The user value (optional).
        :param littup_value: The littup value (optional).
        """
        if type(expr_type) == str:
            expr_type = ExprTypeRepository.lookup(expr_type)

        Utils.check_precondition(isinstance(expr_type, ExprType))
        Utils.check_precondition((user_value is None) != (littup_value is None))

        if user_value is not None:
            Utils.check_precondition(
                expr_type.is_valid_user_value(user_value))
            self._expr_type = expr_type
            self._user_value = user_value
            self._littup_value = \
                self._expr_type.user_value_to_littup_value(user_value)

        if littup_value is not None:
            Utils.check_precondition(
                expr_type.is_valid_littup_value(littup_value))

            self._expr_type = expr_type
            self._user_value = \
                self._expr_type.littup_value_to_user_value(littup_value)
            self._littup_value = littup_value

    def type(self):
        """
        Return the ExprType object representing the type of this value.
        :return: The ExprType object representing the type of this value.
        """
        return self._expr_type

    def __eq__(self, other):
        """
        Implements an equivalence on ExprValue objects based on their littup
        values.
        :param other: The ExprValue object to compare to.
        :return: True if equal to other.
        """
        Utils.check_precondition(isinstance(other, ExprValue))
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
        Utils.check_precondition(isinstance(other, ExprType))
        return self._typestr == other._typestr

    def __ne__(self, other):
        Utils.check_precondition(isinstance(other, ExprType))
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


class Bool(ExprType):
    """ An object that represents a boolean expression type. """

    def __init__(self):
        """ Initialise Bool object. """
        self._values = [ExprValue(expr_type=self, user_value=False),
                        ExprValue(expr_type=self, user_value=True)]
        self._num_values = len(self._values)
        ExprType.__init__(self, "bool")

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
        Utils.check_precondition(self.is_valid_user_value(user_value))
        return (user_value,)

    def littup_value_to_user_value(self, littup_value):
        """ See ExprType.littup_value_to_user_value. """
        Utils.check_precondition(self.is_valid_littup_value(littup_value))
        return littup_value[0]


class BitVec(ExprType):
    """ An object that represents a bit vector type. """

    def __init__(self, number_of_bits):
        """ Initialise object. """
        self._littup_size = number_of_bits
        self._num_values = 2 ** number_of_bits

        littup_values_rev = product(*[[False, True] for b in
            range(number_of_bits)])
        littup_values = six.moves.map(lambda v : v[::-1], littup_values_rev)
        self._values = six.moves.map(lambda v: ExprValue(expr_type=self,
            littup_value=v), littup_values)

        ExprType.__init__(self, "uint{:d}".format(number_of_bits))

    def values(self):
        """ See ExprType.values. """
        return self._values

    def num_values(self):
        """ See ExprType.num_values. """
        return self._num_values

    def littup_size(self):
        """ See ExprType.littup_size. """
        return self._littup_size

    def is_valid_user_value(self, user_value):
        """ See ExprType.is_valid_user_value. """
        return (type(user_value) == int) and (0 <= user_value < self._num_values)

    def is_valid_littup_value(self, littup_value):
        """ See ExprType.user_value_to_littup_value. """
        return type(littup_value) == tuple \
            and len(littup_value) == self._littup_size \
            and all([type(lit_value) == bool for lit_value in littup_value])

    def user_value_to_littup_value(self, user_value):
        """ See ExprType.user_value_to_littup_value. """
        Utils.check_precondition(self.is_valid_user_value(user_value))
        return tuple([(((1 << b) & user_value) != 0) for b in range(self._littup_size)])

    def littup_value_to_user_value(self, littup_value):
        """ See ExprType.littup_value_to_user_value. """
        Utils.check_precondition(self.is_valid_littup_value(littup_value))
        return sum([(1 << b) if littup_value[b] else 0 for b in range(self._littup_size)])


class Product(ExprType):
    """ An object that represents a product of types. """

    def __init__(self, subtypes):
        assert(all([isinstance(subtype, ExprType) for subtype in subtypes]))

        self._subtypes = tuple(subtypes)
        self._littup_size = sum([s.littup_size() for s in subtypes])
        self._num_values = reduce(mul, [s.num_values() for s in subtypes], 1)
        value_iters = [s.values() for s in subtypes]

        # We can't use itertools.product here because it explicitly creates
        # tuples from the subtype's values iterable, which in some cases
        # is too big to create.
        self._values = Utils.product(*value_iters)

        subtype_strs = [str(s) for s in subtypes]
        ExprType.__init__(self, "({})".format(",".join(subtype_strs)))

    def subtypes(self):
        return self._subtypes

    def values(self):
        """ See ExprType.values. """
        return self._values

    def num_values(self):
        """ See ExprType.num_values. """
        return self._num_values

    def littup_size(self):
        """ See ExprType.littup_size. """
        return self._littup_size

    def is_valid_user_value(self, user_value):
        """ See ExprType.is_valid_user_value. """
        return (type(user_value) == tuple) and \
               (len(user_value) == len(self._subtypes)) and \
               (all(s.is_valid_user_value(v) for v, s in
                    zip(user_value, self._subtypes)))

    def is_valid_littup_value(self, littup_value):
        """ See ExprType.user_value_to_littup_value. """
        if type(littup_value) != tuple or len(littup_value) \
                != self._littup_size:
            return False
        else:
            i = 0
            for s in self._subtype:
                assert(len(littup_value) >= i + s.littup_size())
                s_littup_value = littup_value[i:i + s.littup_size()]
                if not s.is_valid_user_value(s_littup_value):
                    return False
                i += s.littup_size()
            return True

    def user_value_to_littup_value(self, user_value):
        """ See ExprType.user_value_to_littup_value. """
        Utils.check_precondition(self.is_valid_user_value(user_value))
        return reduce(add, [s.user_value_to_littup_value(v) \
            for s,v in zip(self._subtypes, user_value)])

    def littup_value_to_user_value(self, littup_value):
        """ See ExprType.littup_value_to_user_value. """
        Utils.check_precondition(self.is_valid_littup_value(littup_value))

        i = 0
        user_value_list = []
        for s in self._subtype:
            assert (len(littup_value) >= i + s.littup_size())
            s_littup_value = littup_value[i:i + s.littup_size()]
            user_value_list.append(s.littup_value_to_user_value(s_littup_value))

        return tuple(user_value_list)


class ExprTypeRepository(object):
    """
    A utility class that maps string like 'bool' into ExprType objects like
    an instance of Bool. This serves two purposes. Firstly, it stops lots of
    of representation of the same type being created (there's no need to have
    more than one object to represent a boolean type). Secondly, it's more
    convenient to the end-user to type 'bool' than mxklabs.Bool().
    """
    # Create one Bool object.
    _BOOL = Bool()

    @staticmethod
    @memoise
    def _get_type_str_regex():
        # Type string tokens.
        type_str_tokens = ['bool', 'uint(\d)+', '\(', '\)', '\,']
        type_str_regex_str = '(' + '|'.join([t for t in type_str_tokens]) + ')'
        return re.compile(type_str_regex_str)

    @staticmethod
    @memoise
    def _get_type_str_tokens(type_str):
        regex = ExprTypeRepository._get_type_str_regex()
        tokens = [m[0] for m in regex.findall(type_str)]

        if "".join(tokens) == type_str:
            return tokens
        else:
            # Some characters unused.
            return []

    @staticmethod
    @memoise
    def _BITVEC(number_of_bits):
        return BitVec(number_of_bits=number_of_bits)

    @staticmethod
    @memoise
    def _PRODUCT(*subtypes):
        return Product(subtypes=subtypes)

    @staticmethod
    @memoise
    def lookup(type_str):
        """
        Get a type using a name like 'bool'
        :param type_str: A type string (as recognised by ExprType implementations).
        :return: A ExprType object.
        """
        Utils.check_precondition(type(type_str) == str)
        tokens = ExprTypeRepository._get_type_str_tokens(type_str)
        return ExprTypeRepository._parse(tokens)

    @staticmethod
    def _parse(tokens):
        if len(tokens) > 0:
            token = tokens.pop(0)

            if token == 'bool':
                return ExprTypeRepository._BOOL
            elif token.startswith('uint'):
                return ExprTypeRepository._BITVEC(int(token[4:]))
            elif token == '(':
                subtypes = []
                while True:
                    subtypes.append(ExprTypeRepository._parse(tokens))
                    if len(tokens) > 0:
                        next = tokens.pop(0)
                        if next == ')':
                            return Product(subtypes)
                        elif next == ',':
                            continue
                        else:
                            raise("Expected ',' or ')'")
                    else:
                        raise ("Expected ',' or ')'")
                pass
            else:
                raise Exception("Expected '(', 'bool' or 'uint\d' (got '{}')"
                    .format(token))
        else:
            raise Exception("Expected '(', 'bool' or 'uint\d' (got '')")


