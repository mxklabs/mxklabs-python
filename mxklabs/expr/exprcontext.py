import importlib
import logging
import os

from .expr import Expr
from .exprclassset import ExprClassSet
from .exprpool import ExprPool
from .valtypeclass import ValtypeClass
from .valtype import Valtype

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class AttrHolder:
  pass

class ExprContext:

  def __init__(self, load_default_expr_class_sets=True):
    self.exprclasssets = {}
    self.exprpool = ExprPool()
    self.valtype_pool = ExprPool()
    self.valtype_classes = {}
    self.vars = {}
    self.valtypes = AttrHolder()

    if load_default_expr_class_sets:
      exprsets = self._get_default_expr_class_sets()
      for exprset in exprsets:
        exprset = self.load_expr_class_set(exprset)
        self.exprclasssets[exprset.identifier] = exprset

  def load_valtype_class(self, identifier):
    if identifier not in self.valtype_classes:
      logger.info(f'Loading \'{identifier}\'')
      module = importlib.import_module(identifier)
      valtype_class = ValtypeClass(ctx=self,
        identifier=identifier,
        module=module)
      self.valtype_classes[identifier] = valtype_class

      fun = lambda **attrs : self._valtype_fun(valtype_class, **attrs)
      setattr(self.valtypes, module.definition['shortName'], fun)

  def _valtype_fun(self, valtype_class, **valtype_attrs):
    valtype = Valtype(self, valtype_class, **valtype_attrs)
    return self.valtype_pool.make_unique(valtype)

  def load_expr_class_set(self, identifier):
    """
        Load an expression set via a module name.
        For example:

        ```
        from mxklabs.expr import ExprBuilder

        builder = ExprBuilder()
        builder.load_expr_class_set("mxklabs.expr.definitions.bitvector")

        # Now use the bitvector exprset.
        x = builder.bitvector.variable(width=10)
        ```
    """
    logger.info(f'Loading exprset \'{identifier}\'')
    module = importlib.import_module(identifier)

    short_name = module.definition['shortName']

    if hasattr(self, short_name):
      logger.error(f"'{identifier}' cannot be loaded (name '{short_name}' is already in use)")
      raise RuntimeError(f"'{identifier}' cannot be loaded (name '{short_name}' is already in use)")

    # Load dependencies.
    for valtype_class in module.definition["dependencies"]["valTypes"]:
      self.load_valtype_class(valtype_class)

    # Create expression set.
    exprset = ExprClassSet(ctx=self, identifier=identifier, module=module)

    # This is where we set the exprset attribute so that they can be
    # accessed with, e.g., context.prop.
    setattr(self, short_name, exprset)

    return exprset

  def make_var(self, name, valtype_fun, **valtype_attrs):
    valtype = valtype_fun(**valtype_attrs)

    if name in self.vars.keys():
      raise RuntimeError(f"variable with name '{name}' already exists in this context")
    else:
      expr = Expr(ctx=self, expr_class_set=None, identifier="variable", ops=[], valtype=valtype, attrs={"name":name})
      self.vars[name] = valtype
      return self.exprpool.make_unique(expr)

  def _get_default_expr_class_sets(self):
    expr_class_sets_dir = os.path.join(os.path.dirname(__file__), "definitions")
    ids = [e for e in os.listdir(expr_class_sets_dir)
        if os.path.isdir(os.path.join(expr_class_sets_dir, e)) and not e.startswith('_')]
    return [f"mxklabs.expr.definitions.{identifier}" for identifier in ids]

