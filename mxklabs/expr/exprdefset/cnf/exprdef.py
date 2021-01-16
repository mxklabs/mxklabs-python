from ...exprdef import ExprDef

class CnfExprDef(ExprDef):

  def __init__(self, **kwargs):
    ExprDef.__init__(self, **kwargs)

  def _pack(self, lit):
    return [lit]

  def _unpack(self, booltup):
    return booltup[0]