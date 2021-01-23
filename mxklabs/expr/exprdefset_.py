class ExprDefSet:

  def __init__(self, ctx, baseid, package):
    self._package = package
    self._baseid = baseid
    self._id = f"{package}.{baseid}"
    self._ctx = ctx

  def id(self):
    return self._id

  def baseid(self):
    return self._baseid

  def expr_defs(self):
    """
    Return the set of ExprDef objects associated with this ExprDefSet.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_expr_defs' has not been implemented")

  def valtype_ids(self):
    """
    Return the set of valtype defs used by this ExprDefSet.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_valtypes' has not been implemented")

  def expr_def_set_ids(self):
    """
    Return the set of expr def sets used by this ExprDefSet.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.expr_def_sets_ids' has not been implemented")

  def targets(self):
    """
    Return target ExprDefSets that these expressions can be lowered to.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_targets' has not been implemented")
