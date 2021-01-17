import re

class ExprDef:

  id_regex = re.compile(r'(?<!^)(?=[A-Z])')

  def __init__(self, ctx, expr_def_set):
    self._ctx = ctx
    self._expr_def_set = expr_def_set
    self._baseid = ExprDef.id_regex.sub('_', self.__class__.__name__).lower()
    self._id = f"{self._expr_def_set.id()}.{self._baseid}"

  def id(self):
    """
    Return the fully qualified id, e.g. 'mxklabs.expr.logical_and'.
    """
    return self._id

  def baseid(self):
    """
    Return the last part of the id, e.g. 'logical_and', defaults to snake case of
    the class' name.
    """
    return self._baseid

  def validate(self, ops, attrs):
    """
    This method is called prior to the construction of an expression.

    Determine whether a list of operands and a dictionary of attributes are valid
    for this type of expression in the provided context. Raise an exception if
    this is not the case.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.validate' has not been implemented")

  def valtype(self, ops, attrs, op_valtypes):
    """
    This method is called prior to the construction of an expression.

    This method is called to determine the valtype of an expression for a given
    list of operands and a dictionary of attributes and a list of valtypes for
    its operands.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.valtype' has not been implemented")

  def evaluate(self, expr, op_values):
    """
    This method is called once an expression is constructed.

    This method is called to determine an expression's value for a given list
    of operands and a dictionary of attributes and a list of values for operands.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.evaluate' has not been implemented")

  def has_feature(self, featurestr):
    """
    Check whether the op supports a specific 'feature'. Features are optional. This function should
    be overloaded by each expression and should return true only for features they support.
    Currently known features are:

    * 'simplify'
    * 'pushnot'
    * 'canonicalize'
    * 'decompose'

    """
    return False

  def simplify(self, expr):
    """
    This method is called once an expression is constructed.

    Return a logically equivalent expression that is no more
    complex than expr. This is a good place to apply, e.g.,
    constant propagation.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.simplify' has not been implemented")

  def pushnot(self, expr):
    """
    This method is called once an expression is constructed.

    Push logical_not expressions down to leaf nodes.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.pushnot' has not been implemented")

  def canonicalize(self, expr):
    """
    This method is called once an expression is constructed.

    Obtain a 'more canonicalized' version of the expr. That is, two expressions
    that are logically equivalent but previously not identical, may become
    identical after canonicalisation.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.simplify' has not been implemented")

  def decompose(self, expr):
    """
    This method is called once an expression is constructed.

    Return an alternative composition of expressions that is logically
    equivalent.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.replace' has not been implemented")

