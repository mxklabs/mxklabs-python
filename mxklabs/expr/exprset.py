from .expr import Expr

class ExprSet:

  def __init__(self, module):
    self._module = module
    self._load_exprs()

  def _load_exprs(self):
    for exprdef in self._module.exprdefs['exprDefs']:
      def fun(*args):
        return self._expr_fun(*args, exprdef=exprdef)
      setattr(self, exprdef['id'], fun)

  def variable(self, name=None):
    return name

  def _expr_fun(self, *args, exprdef):
    assert(exprdef['minOps'] is None or len(args) >= exprdef['minOps'])
    assert(exprdef['maxOps'] is None or len(args) <= exprdef['maxOps'])
    return Expr()