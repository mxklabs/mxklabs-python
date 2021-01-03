import importlib
import logging
import os

from .expr import Expr
from .exprclassset import ExprClassSet
from .exprevaluator import ExprEvaluator
from .exprpool import ExprPool
from .valtypeclass import ValtypeClass
from .valtype import Valtype
from .solver import Solver

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class Proxy:

  def __init__(self, short_name):
    self.short_name = short_name

  def __call__(self, **kwargs):
    if not hasattr(self, "callable"):
      raise RuntimeError(f"'{self.short_name}' is not callable'")
    else:
      return self.callable(**kwargs)

class ExprContext:

  def __init__(self, load_default_expr_class_sets=True):
    self.exprclasssets = {}
    self.exprpool = ExprPool()
    self.valtype_pool = ExprPool()
    self.valtype_classes = {}
    self.vars = {}
    self._proxies = {}
    self.constraints = []

    if load_default_expr_class_sets:
      exprsets = self._get_default_expr_class_sets()
      for exprset in exprsets:
        exprset = self.load_expr_class_set(exprset)
        self.exprclasssets[exprset.identifier] = exprset

  def get_proxy(self, short_name):
    """ Create and return a proxy object as an attribute for a given short_name (e.g. ctx.bool). """
    if short_name not in self._proxies:
      self._proxies[short_name] = Proxy(short_name)
      setattr(self, short_name, self._proxies[short_name])
    return self._proxies[short_name]

  def set_proxy_attr(self, identifier, short_name, attr_name, attr):
    proxy = self.get_proxy(short_name)
    if hasattr(proxy, attr_name):
      raise RuntimeError(f"'{identifier}' cannot be loaded (name '{short_name}.{attr_name}' is already in use)")
    else:
      setattr(proxy, attr_name, attr)

  def load_valtype_class(self, identifier):
    if identifier not in self.valtype_classes:
      logger.info(f'Loading \'{identifier}\'')
      module = importlib.import_module(identifier)
      valtype_class = ValtypeClass(ctx=self,
        identifier=identifier,
        module=module)
      self.valtype_classes[identifier] = valtype_class
      short_name = module.definition['shortName']

      # Make it so we can call, e.g., ctx.bool() to get a type.
      def call_fun(**valtype_attrs):
        valtype = Valtype(self, valtype_class, **valtype_attrs)
        return self.valtype_pool.make_unique(valtype)
      self.set_proxy_attr(identifier, short_name, "callable", call_fun)

      # Make it so we can call, e.g., ctx.is_bool() check for type.
      def is_call_fun(valtype, **valtype_attrs):
        return valtype == call_fun(**valtype_attrs)
      setattr(self, f"is_{short_name}", is_call_fun)

      # Make it so we can call, e.g., ctx.bool.variable(name="a") to create a variable.
      def variable_fun(name, **valtype_attrs):
        valtype = call_fun(**valtype_attrs)
        if name in self.vars.keys():
          raise RuntimeError(f"variable with name '{name}' already exists in this context")
        else:
          expr = Expr(ctx=self, expr_class_set=None, identifier="variable", ops=[], valtype=valtype, attrs={"name":name})
          expr = self.exprpool.make_unique(expr)
          self.vars[name] = expr
          return expr
      self.set_proxy_attr(identifier, short_name, "variable", variable_fun)

      # Make it so we can call, e.g., ctx.bool.constant(value=1) to create a constant.
      def constant_fun(value, **valtype_attrs):
        valtype = call_fun(**valtype_attrs)
        expr = Expr(ctx=self, expr_class_set=None, identifier="constant", ops=[], valtype=valtype, attrs={"value":value})
        return self.exprpool.make_unique(expr)
      self.set_proxy_attr(identifier, short_name, "constant", constant_fun)

  def is_variable(self, expr):
    return expr.identifier == "variable"

  def is_constant(self, expr):
    return expr.identifier == "constant"

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

  def add_constraint(self, expr):
    if expr.valtype == self.bool():
      self.constraints.append(expr)
    else:
      raise RuntimeError(f"constraints must be of type '{self.bool()}' (got {expr.valtype})")

  def evaluate(self, expr, varmap):
    """
    Return the value of this expression under a given dictionary mapping
    variables to values.
    """
    evaluator = ExprEvaluator(self, varmap)
    return evaluator.eval(expr)

  def solve(self):
    cnfctx = ExprContext(load_default_expr_class_sets=False)
    cnfctx.load_expr_class_set("mxklabs.expr.definitions.cnf")
    solver = Solver(self, cnfctx)
    return solver.solve()

  def _get_default_expr_class_sets(self):
    expr_class_sets_dir = os.path.join(os.path.dirname(__file__), "definitions")
    ids = [e for e in os.listdir(expr_class_sets_dir)
        if os.path.isdir(os.path.join(expr_class_sets_dir, e)) and not e.startswith('_')]
    return [f"mxklabs.expr.definitions.{identifier}" for identifier in ids]

