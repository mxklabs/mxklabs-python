import importlib
import logging
import os

from .expr import Expr
from .exprset import ExprSet
from .exprpool import ExprPool
from .valtype import ValType

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_mxklabs_exprsets=True):
    self.exprsets = {}
    self.exprpool = ExprPool()
    self.valtypes = {}
    self.vars = {}
    if load_mxklabs_exprsets:
      exprsets = self._get_mxklabs_exprsets()
      for exprset in exprsets:
        exprset = self.load_exprset(exprset)
        self.exprsets[exprset.ident] = exprset

  def load_valtype(self, ident):
    if ident not in self.valtypes:
      logger.info(f'Loading valtype \'{ident}\'')
      module = importlib.import_module(ident)
      valtype = ValType(ctx=self,
        ident=ident,
        short_name=self._id_to_short_name(ident),
        module=module)
      self.valtypes[ident] = valtype

  def load_exprset(self, id_):
    """
        Load an expression set via a module name.
        For example:

        ```
        from mxklabs.expr import ExprBuilder

        builder = ExprBuilder()
        builder.load_exprset("mxklabs.expr.exprsets.bitvector")

        # Now use the bitvector exprset.
        x = builder.bitvector.variable(width=10)
        ```
    """
    logger.info(f'Loading exprset \'{id_}\'')
    module = importlib.import_module(id_)
    short_name = self._id_to_short_name(id_)
    exprset = ExprSet(
      ctx=self,
      ident=id_,
      short_name=short_name,
      module=module)

    # This is where we set the exprset attribute so that they can be
    # accessed with, e.g., builder.prop.
    setattr(self, short_name, exprset)

    # Load valtypes.
    for valtype in module.exprdescrs["valTypes"]:
      self.load_valtype(valtype)

    return exprset

  def make_var(self, name, valtype):
    if valtype not in self.valtypes.keys():
      raise RuntimeError(f"variable with name '{name}' has unknown type {valtype}")

    # TODO: Use an expression pool to avoid duplicate values.
    if name in self.vars.keys():
      raise RuntimeError(f"variable with name '{name}' already exists in this context")
    else:
      expr = Expr(ctx=self, exprset=None, ident="variable", ops=[], attrs={"name":name})
      self.vars[name] = valtype
      return self.exprpool.make_unique(expr)

  def make_expr(self, **kwargs):
    expr = Expr(ctx=self, **kwargs)
    # TODO: Use an expression pool to avoid duplicate values.
    return self.exprpool.make_unique(expr)

  def _id_to_short_name(self, ident):
    if '.' in ident:
      return ident[ident.rfind('.')+1:]
    else:
      return ident

  def _get_mxklabs_exprsets(self):
    exprsets_dir = os.path.join(os.path.dirname(__file__), "exprsets")
    ids = [e for e in os.listdir(exprsets_dir)
        if os.path.isdir(os.path.join(exprsets_dir, e)) and not e.startswith('_')]
    return [f"mxklabs.expr.exprsets.{ident}" for ident in ids]

