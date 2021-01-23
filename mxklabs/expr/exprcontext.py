import importlib
import inspect
import logging

from .cnfsolver import CnfSolver
from .expr import Constant, Expr, OpExpr, Variable
from .exprcontextnamespace import ExprContextNamespace
from .exprdefset_ import ExprDefSet
from .exprevaluator import ExprEvaluator
from .exprwalker import ExprWalker
from .objpool import ObjPool
from .valtype_ import Valtype
from .valtypedef import ValtypeDef

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_defaults=True):
    self._constraint_pool = ObjPool()
    self._expr_pool = ObjPool()
    self._expr_def_sets = {}
    self._namespaces = {}
    self._valtype_defs = {}
    self._valtype_pool = ObjPool()
    self._variables = {}
    self._walker = ExprWalker(self)

    def solve():
      cnfctx = ExprContext(load_defaults=False)
      cnfctx.load_expr_def_set('mxklabs.expr.exprdefset.cnf')
      solver = CnfSolver(self, cnfctx)
      return solver.solve()

    def evaluate(expr, varmap):
      evaluator = ExprEvaluator(self, varmap)
      return evaluator.eval(expr)

    self._add('util', 'solve', solve)
    self._add('util', 'evaluate', evaluate)
    self._add('util', 'simplify', lambda expr: self._walker.simplify(expr))
    self._add('util', 'pushnot', lambda expr: self._walker.pushnot(expr))
    self._add('util', 'canonicalize', lambda expr: self._walker.canonicalize(expr))
    self._add('util', 'decompose', lambda expr: self._walker.decompose(expr))

    if load_defaults:
      self.load_valtype('mxklabs.expr.valtype.bool')
      self.load_valtype('mxklabs.expr.valtype.bitvector')
      self.load_expr_def_set('mxklabs.expr.exprdefset.logical')
      self.load_expr_def_set('mxklabs.expr.exprdefset.bitvector')
      self.load_expr_def_set('mxklabs.expr.exprdefset.util')

  def __getattr__(self, name):
    if name in self._namespaces:
      return self._namespaces[name]
    else:
      # User is accessing ctx.<something> where <something> doesn't exist.
      if len(self._namespaces) > 0:
        namespaces = ", ".join([f"'{n}'" for n in self._namespaces.keys()])
        raise AttributeError(f"'{name}' is not a valid attribute for this context (try, e.g., {namespaces})")
      else:
        raise AttributeError(f"'{name}' is not a valid attribute (also, no valid attributes exist; did you forget to load valtypes and/or expression definitions)")

  def load_valtype(self, valtype_id):
    if valtype_id in self._valtype_defs:
      logger.info(f"Skipping loading of '{valtype_id}' (already loaded)")
    else:
      logger.info(f'Loading \'{valtype_id}\'')
      module = importlib.import_module(valtype_id)

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
          # Make it callable.
          self._add('valtype', valtype_def.baseid(), create_valtype)

          # Make it so we can call, e.g., ctx.valtype.is_bool() check for type.
          def is_valtype(valtype, *sub_valtypes, **valtype_attrs):
            # Error if it's not a valtype.
            self._check_valtype(f"'is_{valtype_def.baseid()}' argument", valtype)

            if valtype.ctx() != self:
              return False
            if valtype.valtype_def() != valtype_def:
              return False
            if valtype.sub_valtypes() != sub_valtypes:
              return False
            for attr in valtype.attrs():
              if attr in valtype_attrs and valtype_attrs[attr] != None:
                if valtype.attrs()[attr] != valtype_attrs[attr]:
                  return False

            return True

            # Check by id (this doesn't work when we don't pass some attrs).
            #return id(valtype) == id(create_valtype(*sub_valtypes, **valtype_attrs))
          self._add('valtype', f"is_{valtype_def.baseid()}", is_valtype)

          self._valtype_defs[valtype_def.id()] = valtype_def

  def load_expr_def_set(self, expr_def_set_id):
    if expr_def_set_id in self._expr_def_sets:
      logger.info(f"Skipping loading of '{expr_def_set_id}' (already loaded)")
    else:
      logger.info(f'Loading \'{expr_def_set_id}\'')
      module = importlib.import_module(expr_def_set_id)

      # Look for ExprDefSet classes.
      for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, ExprDefSet):
          expr_def_set = obj(self)

          # Iterate over expression definitions.
          for expr_def in expr_def_set.expr_defs():

            # Make it so we can call, e.g., ctx.expr.logical_and(...).
            def create_expr(expr_def_set, expr_def, ops, attrs):
              # Check ops are valid expressions.
              for index, op in zip(range(len(ops)), ops):
                self._check_expr(f"op {index}", op)
              # Check ops and attrs are valid.
              expr_def.validate(ops, attrs)
              # Optionally do a substitution.
              #if expr_def.has_feature('simplify'):
              #  replacement = expr_def.simplify(ops, attrs)
              #  if replacement is not None:
              #    return replacement
              # Work out the valtype.
              op_valtypes = [op.valtype() for op in ops]
              valtype = expr_def.valtype(ops, attrs, op_valtypes)
              # Create expression.
              expr = OpExpr(self, expr_def_set, expr_def, ops, attrs, valtype)
              return self._expr_pool.make_unique(expr)

            # Make it callable (must use lambda to avoid issues).
            self._add('expr', expr_def.baseid(),
                lambda *ops, expr_def_set=expr_def_set, expr_def=expr_def, **attrs: create_expr(expr_def_set, expr_def, ops, attrs))

            # Make it so we can call, e.g., ctx.expr.is_logical_and(...).
            def is_expr(expr_def_set, expr_def, expr):
              # Check it's a valid expression in this context.
              self._check_expr(f"'is_{expr_def.baseid()}' argument", expr)
              # If it's a variable or a constant, it's not one of our exprs.
              if not isinstance(expr, OpExpr):
                return False
              # Check our expr_def matches.
              return (id(expr.expr_def()) == id(expr_def))

            # Make it callable (must use lambda to avoid issues).
            self._add('expr', f"is_{expr_def.baseid()}",
                lambda expr, expr_def_set=expr_def_set, expr_def=expr_def: is_expr(expr_def_set, expr_def, expr))

          self._expr_def_sets[expr_def_set.id()] = expr_def_set

          # Load dependencies.
          for valtype_id in expr_def_set.valtype_ids():
            self.load_valtype(valtype_id)

          # Load dependencies.
          for expr_def_set_id in expr_def_set.expr_def_set_ids():
            self.load_expr_def_set(expr_def_set_id)

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

  def is_variable(self, expr):
    # Check it's a valid expression in this context.
    self._check_expr("'is_variable' argument", expr)
    # Check it's a variable.
    return isinstance(expr, Variable)

  def constant(self, value, valtype):
    # Check valtype is valid.
    self._check_valtype(f"valtype argument of constant", valtype)
    # Check and convert user's value.
    value = valtype.valtype_def().convert_userobj_to_value(valtype, value)
    # Create constant.
    expr = Constant(ctx=self, value=value, valtype=valtype)
    return self._expr_pool.make_unique(expr)

  def is_constant(self, expr):
    # Check it's a valid expression in this context.
    self._check_expr("'is_constant' argument", expr)
    # Check it's a variable.
    return isinstance(expr, Constant)

  def add_constraint(self, expr):
    # Check expression.
    self._check_expr("constraint", expr)
    # Check we have booleans loaded.
    if 'mxklabs.expr.valtype.bool' not in self._valtype_defs:
      raise RuntimeError("constraint expressions must be of valtype 'bool', but this valtype is not loaded in this context")
    # Check the expression is bool
    if not self.valtype.is_bool(expr.valtype()):
      raise RuntimeError(f"constraint expressions must be of valtype '{self.valtype.bool()}' (got {expr.valtype()})")
    self._constraint_pool.make_unique(expr)

  def clear(self):
    self._variables = {}
    self._constraint_pool.clear()
    self._expr_pool.clear()

  def variables(self):
    return self._variables.values()

  def constraints(self):
    return self._constraint_pool.values()

  def _add(self, namespaceid, baseid, fun):
    # Add an attribute to a namespace.
    if namespaceid not in self._namespaces:
      self._namespaces[namespaceid] = ExprContextNamespace(namespaceid)
    self._namespaces[namespaceid]._set_attr(baseid, fun)

  def _check_expr(self, descr, expr):
    # Check if an expression is sane.
    if not isinstance(expr, Expr):
      raise RuntimeError(f"{descr} ('{expr}') is not a mxklabs.expr.Expr object")
    if expr.ctx() != self:
      raise RuntimeError(f"{descr} ('{expr}') was created in a different context")
    if not self._expr_pool.contains(expr):
      raise RuntimeError(f"{descr} ('{expr}') not found in context")

  def _check_valtype(self, descr, valtype):
    # Check if a valtype is sane.
    if not isinstance(valtype, Valtype):
      raise RuntimeError(f"{descr} ('{valtype}') is not a mxklabs.expr.Valtype object")
    if valtype.ctx() != self:
      raise RuntimeError(f"{descr} ('{valtype}') was created in a different context")
    if not self._valtype_pool.contains(valtype):
      raise RuntimeError(f"{descr} ('{valtype}') not found in context")


