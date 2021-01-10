import importlib
import inspect
import logging

from .expr import Constant, OpExpr, Variable
from .exprcontextnamespace import ExprContextNamespace
from .objpool import ObjPool
from .valtype_ import Valtype
from .valtypedef import ValtypeDef

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_defaults=True):
    self._expr_pool = ObjPool()
    self._namespaces = {}
    self._valtype_defs = {}
    self._valtype_pool = ObjPool()
    self._variables = {}

  def __getattr__(self, name):
    if name in self._namespaces:
      return self._namespaces[name]
    else:
      # Default behaviour
      raise AttributeError

  def load_valtype(self, valtypeid):
    if valtypeid in self._valtype_defs:
      raise RuntimeError(f"'{valtypeid}' already loaded")

    logger.info(f'Loading \'{valtypeid}\'')
    module = importlib.import_module(valtypeid)

    # Look for ValtypeDef classes.
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj) and issubclass(obj, ValtypeDef):
        valtype_def = obj(self)

        # Make it so we can call, e.g., ctx.valtype.bool() to get a type.
        def create_valtype(*sub_valtypes, **attrs):
          # Check sub_valtypes are valid valtypes.
          for index, sub_valtype in zip(range(len(sub_valtypes)), sub_valtypes):
            self._check_valtype(f"sub_valtype {index}", valtype)
          valtype_def.validate(sub_valtypes, attrs)
          valtype = Valtype(self, valtype_def, sub_valtypes, attrs)
          return self._valtype_pool.make_unique(valtype)
        self._add('valtype', valtype_def.baseid(), create_valtype)

        # Make it so we can call, e.g., ctx.valtype.is_bool() check for type.
        def is_valtype(valtype, *sub_valtypes, **valtype_attrs):
          return id(valtype) == id(create_valtype(*sub_valtypes, **valtype_attrs))
        self._add('valtype', f"is_{valtype_def.baseid()}", is_valtype)

        self._valtype_defs[valtype_def.id()] = valtype_def

  def variable(self, name, valtype):
    # Check valtype is valid.
    self._check_valtype(f"valtype argument of variable '{name}'", valtype)
    # Check variable name is valid.
    if not isinstance(name, str):
      raise RuntimeError(f"name argument of variable is not a 'str'")
    # Check variable name is unique.
    if name in self._variables.keys():
      raise RuntimeError(f"variable with name '{name}' already exists in context")
    # Create variable.
    expr = Variable(ctx=self, name=name, valtype=valtype)
    expr = self._expr_pool.make_unique(expr)
    self._variables[name] = expr
    return expr

  def constant(self, value, valtype):
    # Check valtype is valid.
    self._check_valtype(f"valtype argument of constant", valtype)
    # Check and convert user's value.
    value = valtype.valtype_def().convert_userobj_to_value(valtype, value)
    # Create constant.
    expr = Constant(ctx=self, value=value, valtype=valtype)
    return self._expr_pool.make_unique(expr)

  #def constant(value, valtype):


  def _add(self, namespaceid, baseid, fun):
    if namespaceid not in self._namespaces:
      self._namespaces[namespaceid] = ExprContextNamespace(namespaceid)
    self._namespaces[namespaceid]._set_attr(baseid, fun)

  def _check_valtype(self, descr, valtype):
    if not isinstance(valtype, Valtype):
      raise RuntimeError(f"{descr} is not a mxklabs.expr.Valtype object")
    if valtype.ctx() != self:
      raise RuntimeError(f"{descr} was created in a different context")
    if not self._valtype_pool.contains(valtype):
      raise RuntimeError(f"{descr} not found in context")
    


