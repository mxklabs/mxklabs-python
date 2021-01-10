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
    Return the fully qualified id, e.g. 'mxklabs.expr.exprdefset.cnf.logical_and'.
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
