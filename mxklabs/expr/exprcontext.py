import importlib
import logging
import os

from .expr import Expr
from .exprset import ExprSet
from .valtype import ValType

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_mxklabs_exprsets=True):
    self.exprsets = {}
    self.valtypes = {}
    self.vars = {}
    if load_mxklabs_exprsets:
      exprsets = self._get_mxklabs_exprsets()
      for exprset in exprsets:
        exprset = self.load_exprset(exprset)
        self.exprsets[exprset.id] = exprset

  def load_valtype(self, id):
    if id not in self.valtypes:
      logger.info(f'Loading valtype \'{id}\'')
      module = importlib.import_module(id)
      valtype = ValType(ctx=self,
        id=id,
        short_name=self._id_to_short_name(id),
        module=module)
      self.valtypes[id] = valtype

  def load_exprset(self, id):
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
    logger.info(f'Loading exprset \'{id}\'')
    module = importlib.import_module(id)
    short_name = self._id_to_short_name(id)
    exprset = ExprSet(ctx=self,
      id=id,
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
      expr = Expr(ctx=self, exprset=None, id="variable", ops=[], attrs={"name":name})
      self.vars[name] = valtype
      return expr

  def make_expr(self, **kwargs):
    expr = Expr(ctx=self, **kwargs)
    # TODO: Use an expression pool to avoid duplicate values.
    return expr

  def _id_to_short_name(self, id):
    if '.' in id:
      return id[id.rfind('.')+1:]
    else:
      return id

  def _get_mxklabs_exprsets(self):
    exprsets_dir = os.path.join(os.path.dirname(__file__), "exprsets")
    ids = [e for e in os.listdir(exprsets_dir)
        if os.path.isdir(os.path.join(exprsets_dir, e)) and not e.startswith('_')]
    return [f"mxklabs.expr.exprsets.{id}" for id in ids]

