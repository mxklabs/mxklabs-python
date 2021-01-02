#from .exprcontext import ExprContext
from pysat.solvers import Glucose3

class SolveResult:

  def __init__(self, varmap=None):
    self.varmap = varmap

  def __bool__(self):
    return self.varmap is not None

  def __nonzero__(self):
    return self.__bool__()

  def get_varmap(self):
    return self.varmap

class SolveContext:

  def __init__(self, ctx, cnfctx):
    self.ctx = ctx
    self.cnfctx = cnfctx

    self.mappers = {}
    self.mapping = {}

    for expr_class_set_id, expr_class_set in self.ctx.exprclasssets.items():
      cnf_mapping_class = expr_class_set.get_cnf_mapping_class()
      self.mappers[expr_class_set_id] = cnf_mapping_class(self.cnfctx)

  def map_expr(self, expr):
    if expr in self.mapping:
      return self.mapping[expr]
    else:
      if self.ctx.is_variable(expr):
        # TODO: move this to valtype code.
        if expr.valtype == self.ctx.valtypes.bool():
          mapped_expr = self.cnfctx.cnf.variable(expr.name)
        else:
          raise RuntimeError(f"No implementation for lowering type {expr.valtype}")
      else:
        #print(f'expr={expr}')
        mapped_expr_ops = [self.map_expr(expr_op) for expr_op in expr.ops]
        #print(f'mapped_expr_ops={mapped_expr_ops}')
        #print(self.mappers[expr.expr_class_set.identifier])
        mapper_fun = getattr(self.mappers[expr.expr_class_set.identifier], expr.identifier)
        mapped_expr = mapper_fun(expr, *mapped_expr_ops)

      self.mapping[expr] = mapped_expr
      return mapped_expr

  def solve(self):
    for constraint in self.ctx.constraints:
      self.cnfctx.add_constraint(
        self.cnfctx.cnf.logical_or(self.map_expr(constraint)))

    print(f"variables={self.cnfctx.vars}")
    print('-'*80)
    print(f"constraints=")
    for c in self.cnfctx.constraints:
      print(f"- {c}")
    print('-'*80)

    var_num = 1
    var_num_mapping = {}
    var_num_mapping_inv = {}

    # TODO: Don't hard code use of glucose.
    g = Glucose3()

    for c in self.cnfctx.constraints:
      assert(self.cnfctx.cnf.is_logical_or(c))
      clause = []
      for op in c.ops:
        if self.cnfctx.is_variable(op):
          if op not in var_num_mapping:
            var_num_mapping[op] = var_num
            var_num_mapping_inv[var_num] = op
            var_num += 1
          clause.append(var_num_mapping[op])
        else:
          assert(self.cnfctx.cnf.is_logical_not(op))
          assert(self.cnfctx.is_variable(op.ops[0]))
          if op.ops[0] not in var_num_mapping:
            var_num_mapping[op.ops[0]] = var_num
            var_num_mapping_inv[var_num] = op.ops[0]
            var_num += 1
          clause.append(-var_num_mapping[op.ops[0]])
      g.add_clause(clause)

    print(f"var_num_mapping={var_num_mapping}")

    if g.solve():
      # SAT
      cnf_varmap = {}
      model = g.get_model()
      for i in model:
        if i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[i]] = True
        if -i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[-i]] = False

      varmap = {}
      for _,v in self.ctx.vars.items():
        # TODO: generalise
        varmap[v] = cnf_varmap[self.map_expr(v)]
        return SolveResult(varmap=varmap)
    else:
      # UNSAT
      print("UNSAT")
      return SolveResult()

class Solver:

  def __init__(self, ctx, cnfctx):
    self.ctx = ctx
    self.cnfctx = cnfctx

  def solve(self):
    solve_ctx = SolveContext(self.ctx, self.cnfctx)
    return solve_ctx.solve()
