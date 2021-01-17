import logging

#from .exprcontext import ExprContext
from pysat.solvers import Glucose3
from .expr import OpExpr
from .exprutils import ExprUtils

logger = logging.getLogger(f'mxklabs.expr.CnfSolver')

class CnfDecomposer:

  """ Ensures expression can be mapped to CNF. """

  def __init__(self, srcctx, proxy):
    self._srcctx = srcctx
    self._proxy = proxy

  def decompose(self, expr):
    if self._srcctx.is_variable(expr):
      return expr
    elif self._srcctx.is_constant(expr):
      return expr
    else:
      while not self._proxy.can_map(expr):
        if expr.expr_def().has_feature('decompose'):
          expr = expr.expr_def().decompose(expr)
        else:
          raise RuntimeError(f"cannot map '{expr}' to CNF")
      if self._srcctx.is_variable(expr):
        return expr
      elif self._srcctx.is_constant(expr):
        return expr
      else:
        walked_ops = [self.decompose(op) for op in expr.ops()]
        expr = OpExpr(self._srcctx, expr.expr_def_set(), expr.expr_def(), walked_ops, expr.attrs(), expr.valtype())
        expr = self._srcctx._expr_pool.make_unique(expr)
        return expr

class CnfProxy:

  def __init__(self, srcctx, cnfctx):
    self._srcctx = srcctx
    self._cnfctx = cnfctx
    self._true = self._cnfctx.variable(name='__true', valtype=self._cnfctx.valtype.bool())
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(self._true))
    self._false = self._cnfctx.expr.logical_not(self._true)

  def can_map(self, expr):
    return hasattr(self, f"map_{expr.expr_def().baseid()}")

  def map_variable(self, expr):
    # Lower a variable as a list of boolean variables.
    booltup_size = expr.valtype().valtype_def().booltup_size(expr.valtype())
    mapped_expr = [self._cnfctx.variable(
        name=ExprUtils.make_variable_name_from_expr(expr),
        valtype=self._cnfctx.valtype.bool())
      for b in range(booltup_size)]
    return mapped_expr

  def map_constant(self, expr):
    # Lower a constant as a combination of literals.
    booltup_value = expr.valtype().valtype_def().convert_value_to_booltup(expr.valtype(), expr.value())
    mapped_expr = [self._true if b else self._false for b in booltup_value]
    return mapped_expr

  def map_opexpr(self, expr, mapped_ops):
    if hasattr(self, f"map_{expr.expr_def().baseid()}"):
      fun = getattr(self, f"map_{expr.expr_def().baseid()}")
      return fun(expr, mapped_ops)
    else:
      raise RuntimeError(f"unable to convert '{expr}' to CNF")

  def map_logical_and(self, expr, mapped_ops):
    oplits = [self._unpack(ol) for ol in mapped_ops]

    lit = self._make_lit(expr)

    # For each op: lit => oplit
    for oplit in oplits:
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        oplit,
        self._make_not(lit)))

    # oplit_0 and ... and oplit_n => lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        *[self._make_not(oplit) for oplit in oplits],
        lit))

    return self._pack(lit)

  def map_logical_not(self, expr, mapped_ops):
    oplits = [self._unpack(ol) for ol in mapped_ops]
    return self._pack(self._make_not(oplits[0]))

  def map_logical_or(self, expr, mapped_ops):
    oplits = [self._unpack(ol) for ol in mapped_ops]

    lit = self._make_lit(expr)

    # For each op: lit => oplit
    for oplit in oplits:
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        oplit,
        self._make_not(lit)))

    # not oplit_0 and ... and not oplit_n => not lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        *[oplit for oplit in oplits],
        self._make_not(lit)))

    return self._pack(lit)

  def map_logical_xor(self, expr, mapped_ops):
    oplits = [self._unpack(ol) for ol in mapped_ops]
    oplit0 = oplits[0]
    oplit1 = oplits[1]

    lit = self._make_lit(expr)

    # oplit0 and not oplit1 => lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        self._make_not(oplit0),
        oplit1,
        lit))

    # not oplit0 and oplit1 => lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        oplit0,
        self._make_not(oplit1),
        lit))

    # oplit0 and oplit1 => not lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        self._make_not(oplit0),
        self._make_not(oplit1),
        self._make_not(lit)))

    # not oplit0 and not oplit1 => not lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        oplit0,
        oplit1,
        self._make_not(lit)))

    return self._pack(lit)

  def _pack(self, lit):
    return [lit]

  def _unpack(self, booltup):
    return booltup[0]

  def _make_lit(self, expr, bit=None):
    return self._cnfctx.variable(
        name=ExprUtils.make_variable_name_from_expr(expr, bit),
        valtype=self._cnfctx.valtype.bool())

  def _make_not(self, lit):
    # All literals are either variables or negations of variables. If we
    # are asked to negate a negation, return the variable.
    if self._cnfctx.expr.is_logical_not(lit):
      return lit.ops()[0]
    else:
      return self._cnfctx.expr.logical_not(lit)

class CnfSolveResult:

  def __init__(self, varmap=None):
    self.varmap = varmap

  def __bool__(self):
    return self.varmap is not None

  def __nonzero__(self):
    return self.__bool__()

  def get_varmap(self):
    return self.varmap

class CnfSolveContext:

  def __init__(self, srcctx, cnfctx):
    self._srcctx = srcctx
    self._cnfctx = cnfctx
    self._proxy = CnfProxy(srcctx=srcctx, cnfctx=cnfctx)
    self._decomposer = CnfDecomposer(srcctx=srcctx, proxy=self._proxy)

    # Mapping from ctx expr to mapped results.
    self._expr_map = {}

  def map_expr(self, expr):
    if expr in self._expr_map:
      return self._expr_map[expr]
    else:
      if self._srcctx.is_variable(expr):
        mapped_expr = self._proxy.map_variable(expr)
      elif self._srcctx.is_constant(expr):
        mapped_expr = self._proxy.map_constant(expr)
      else:
        #print(f'expr={expr}')
        mapped_ops = [self.map_expr(expr_op) for expr_op in expr.ops()]
        mapped_expr = self._proxy.map_opexpr(expr, mapped_ops)

      self._expr_map[expr] = mapped_expr
      return mapped_expr

  def solve(self):
    # Add each constraint.
    for c in self._srcctx.constraints():
      c = self._decomposer.decompose(c)
      c = self._srcctx.util.pushnot(c)
      c = self._srcctx.util.simplify(c)
      c = self._srcctx.util.canonicalize(c)
      constraint_litvec = self.map_expr(c)
      self._cnfctx.add_constraint(
        self._cnfctx.expr.logical_or(constraint_litvec[0]))

    print(f"variables={self._cnfctx.variables()}")
    print('-'*80)
    print(f"constraints=")
    for c in self._cnfctx.constraints():
      print(f"- {c}")
    print('-'*80)

    var_num = 1
    var_num_mapping = {}
    var_num_mapping_inv = {}

    # TODO: Don't hard code use of glucose.
    g = Glucose3()

    for c in self._cnfctx.constraints():
      assert(self._cnfctx.expr.is_logical_or(c))
      clause = []
      for op in c.ops():
        if self._cnfctx.is_variable(op):
          if op not in var_num_mapping:
            var_num_mapping[op] = var_num
            var_num_mapping_inv[var_num] = op
            var_num += 1
          clause.append(var_num_mapping[op])
        else:
          assert(self._cnfctx.expr.is_logical_not(op))
          assert(self._cnfctx.is_variable(op.ops()[0]))
          if op.ops()[0] not in var_num_mapping:
            var_num_mapping[op.ops()[0]] = var_num
            var_num_mapping_inv[var_num] = op.ops()[0]
            var_num += 1
          clause.append(-var_num_mapping[op.ops()[0]])
      g.add_clause(clause)

    print(f"var_num_mapping={var_num_mapping}")

    if g.solve():
      # SAT
      logger.info(f"SAT")

      # Get mapping for CNF literals.
      cnf_varmap = {}
      model = g.get_model()
      for i in model:
        if i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[i]] = True
        if -i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[-i]] = False

      # Get mapping for valtype variables.
      varmap = {}
      for v in self._srcctx.variables():
        valtype = v.valtype()
        valtype_def = valtype.valtype_def()
        booltup = [cnf_varmap[cnf_v] for cnf_v in self.map_expr(v)]
        value = valtype_def.convert_booltup_to_value(valtype, booltup)
        varmap[v] = value
      return CnfSolveResult(varmap=varmap)

    else:
      # UNSAT
      logger.info(f"UNSAT")
      return CnfSolveResult()

class CnfSolver:

  def __init__(self, ctx, cnfctx):
    self._ctx = ctx
    self._cnfctx = cnfctx

  def solve(self):
    solve_ctx = CnfSolveContext(self._ctx, self._cnfctx)
    return solve_ctx.solve()
