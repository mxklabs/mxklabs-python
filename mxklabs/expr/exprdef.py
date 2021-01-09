import re

class ExprDef:

  id_regex = re.compile(r'(?<!^)(?=[A-Z])')

  def __init__(self, ctx):
    self._ctx = ctx

  def id(self):
    """
    Return the identifier used to construct and represent the function. By
    default we convert the class name to snake case (e.g. an ExprDef with class
    name LogicalAnd will return an id of 'logical_and').
    """
    return ExprDef.id_regex.sub('_', self.__class__.__name__).lower()

  def validate(self, ops, attrs):
    """
    This method is called prior to the construction of an expression.

    Determine whether a list of operands and a dictionary of attributes are valid
    for this type of expression in the provided context. Raise an exception if
    this is not the case.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.validate' has not been implemented")

  def replace(self, ops, attrs):
    """
    This method is called prior to the construction of an expression.

    If desired, return an expression to substitute an expression being
    considered for construction. This mechanism exists to allow for
    canonicalisation of expressions and constant propagation, etc., at
    construction time. Return None to construct the expression as-is or
    return an alternative expression constructed via ctx.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.replace' has not been implemented")

  def determine_valtype(self, ops, attrs, op_valtypes):
    """
    This method is called prior to the construction of an expression.

    This method is called to determine the valtype of an expression for a given
    list of operands and a dictionary of attributes and a list of valtypes for
    its operands.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.determine_valtype' has not been implemented")

  def determine_value(self, expr, op_values):
    """
    This method is called once an expression is constructed.

    This method is called to determine an expression's value for a given list
    of operands and a dictionary of attributes and a list of values for operands.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.determine_value' has not been implemented")

  def map_to_target(self, expr, op_target_mapping, target_ctx):
    """
    This method is called once an expression is constructed.

    This method is called to map the expression to a target context for a given
    list of operands and a dictionary of attributes and a list of return values
    returned by this function for the operands.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.map_to_target' has not been implemented")
