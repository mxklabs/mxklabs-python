import logging

#from .exprcontext import ExprContext
from pysat.solvers import Glucose3
from .exprutils import ExprUtils
from .cnftarget import CnfTarget


logger = logging.getLogger(f'mxklabs.expr.CnfSolver')

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

  def __init__(self, ctx, cnfctx):
    self._ctx = ctx
    self._cnfctx = cnfctx
    self._target = CnfTarget(ctx=self._cnfctx)

    # Mapping from ctx expr to mapped results.
    self._expr_map = {}

  def map_expr(self, expr):
    if expr in self._expr_map:
      return self._expr_map[expr]
    else:
      if self._ctx.is_variable(expr):
        # Lower a variable as a list of boolean variables.
        booltup_size = expr.valtype().valtype_def().booltup_size(expr.valtype())
        mapped_expr = [self._cnfctx.variable(
            name=ExprUtils.make_variable_name_from_expr(expr),
            valtype=self._cnfctx.valtype.bool())
          for b in range(booltup_size)]
      elif self._ctx.is_constant(expr):
        # Lower a constant as a combination of literals.
        booltup_value = expr.valtype().valtype_def().booltup_size(expr.valtype(), expr.value())
        mapped_expr = [self._target.true() if b else self._target.false() for b in booltup_value]
      else:
        #print(f'expr={expr}')
        op_target_mapping = [self.map_expr(expr_op) for expr_op in expr.ops()]
        mapped_expr = expr.expr_def().to_cnf(expr, op_target_mapping, self._target)

      self._expr_map[expr] = mapped_expr
      return mapped_expr

  def solve(self):

    # Add each constraint.
    for constraint in self._ctx.constraints():
      constraint_litvec = self.map_expr(constraint)
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
      for v in self._ctx.variables():
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
