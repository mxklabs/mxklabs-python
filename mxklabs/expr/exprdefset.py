class ExprDefSet:

  def __init__(self, ctx):
    self._ctx = ctx

  def get_namespace(self):
    """
    Return the 'namespace' string in which expressions in this set should reside.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_namespace' has not been implemented")

  def get_expr_defs(self):
    """
    Return the set of ExprDef objects associated with this ExprDefSet.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_expr_defs' has not been implemented")

  def get_valtypes(self):
    """
    Return the set of valtype defs used by this ExprDefSet.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_valtypes' has not been implemented")

  def get_targets(self):
    """
    Return target ExprDefSets that these expressions can be lowered to.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_targets' has not been implemented")
