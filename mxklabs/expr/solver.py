#from .exprcontext import ExprContext

class SolverResult:

  def __init__(self, varmap=None, unsat_proof=None):
    self.varmap = varmap
    self.unsat_proof = unsat_proof

  def __nonzero__(self):
    return self.varmap is not None

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
      self.cnfctx.add_constraint(self.map_expr(constraint))

    

    print(f"variables={self.cnfctx.vars}")
    print(f"constraints={self.cnfctx.constraints}")

class Solver:

  def __init__(self, ctx, cnfctx):
    self.ctx = ctx
    self.cnfctx = cnfctx

  def solve(self):
    solve_ctx = SolveContext(self.ctx, self.cnfctx)
    return solve_ctx.solve()
