import importlib
import logging
import os

from .expr import Expr
from .exprset import ExprSet
from .exprpool import ExprPool
from .valtypeclass import ValTypeClass
from .valtype import ValType

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_mxklabs_exprsets=True):
    self.exprsets = {}
    self.exprpool = ExprPool()
    self.val_type_pool = ExprPool()
    self.val_type_classes = {}
    self.vars = {}
    if load_mxklabs_exprsets:
      exprsets = self._get_mxklabs_exprsets()
      for exprset in exprsets:
        exprset = self.load_exprset(exprset)
        self.exprsets[exprset.id] = exprset

  def load_val_type(self, id):
    if id not in self.val_type_classes:
      logger.info(f'Loading \'{id}\'')
      module = importlib.import_module(id)
      val_type_class = ValTypeClass(ctx=self,
        id=id,
        module=module)
      self.val_type_classes[id] = val_type_class

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

    short_name = module.definition['shortName']

    if hasattr(self, short_name):
      logger.error(f"'{id}' cannot be loaded (name '{short_name}' is already in use)")
      raise RuntimeError(f"'{id}' cannot be loaded (name '{short_name}' is already in use)")

    # Load dependencies.
    for val_type_class in module.definition["dependencies"]["valTypes"]:
      self.load_val_type(val_type_class)

    # Create expression set.
    exprset = ExprSet(ctx=self, id=id, module=module)

    # This is where we set the exprset attribute so that they can be
    # accessed with, e.g., context.prop.
    setattr(self, short_name, exprset)

    return exprset

  def get_unique_val_type(self, val_type_class_id, **val_type_attrs):
    if val_type_class_id not in self.val_type_classes.keys():
      raise RuntimeError(f"unknown type '{val_type_class_id}'")

    val_type_class = self.val_type_classes[val_type_class_id]
    val_type = ValType(self, val_type_class, **val_type_attrs)
    print(f'val_type={val_type}')
    return self.val_type_pool.make_unique(val_type)

  def make_var(self, name, val_type_class_id, **val_type_attrs):
    val_type = self.get_unique_val_type(val_type_class_id, **val_type_attrs)

    if name in self.vars.keys():
      raise RuntimeError(f"variable with name '{name}' already exists in this context")
    else:
      expr = Expr(ctx=self, exprset=None, id="variable", ops=[], val_type=val_type, attrs={"name":name})
      self.vars[name] = val_type
      return self.exprpool.make_unique(expr)

  def make_expr(self, exprset, id, ops, attrs):
    val_type = self.get_unique_val_type('mxklabs.expr.valtypes.bool')
    expr = Expr(ctx=self, exprset=exprset, id=id, ops=ops, val_type=val_type, attrs=attrs)
    return self.exprpool.make_unique(expr)

  def _get_mxklabs_exprsets(self):
    exprsets_dir = os.path.join(os.path.dirname(__file__), "exprsets")
    ids = [e for e in os.listdir(exprsets_dir)
        if os.path.isdir(os.path.join(exprsets_dir, e)) and not e.startswith('_')]
    return [f"mxklabs.expr.exprsets.{id}" for id in ids]

