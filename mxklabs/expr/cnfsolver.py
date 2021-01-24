import logging
import random
import itertools

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
    self._name_map = {}
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
    if booltup_size == 1:
      mapped_expr = [self._cnfctx.variable(
          name=ExprUtils.make_variable_name_from_expr(expr),
          valtype=self._cnfctx.valtype.bool())]
    else:
      mapped_expr = [self._cnfctx.variable(
          name=ExprUtils.make_variable_name_from_expr(expr, bit=b),
          valtype=self._cnfctx.valtype.bool())
        for b in range(booltup_size)]
    self._name_map[expr] = [var.name() for var in mapped_expr]
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

  def map_bitvector_from_bool(self, expr, mapped_ops):
    oplits = [self._unpack(ol) for ol in mapped_ops]
    return oplits

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
        self._make_not(oplit),
        lit))

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

  def map_util_index(self, expr, mapped_ops):
    return self._pack(mapped_ops[0][expr.attrs()['index']])

  def map_util_equals(self, expr, mapped_ops):
    oplits0 = mapped_ops[0]
    oplits1 = mapped_ops[1]
    assert(len(oplits0) == len(oplits1))
    bits = len(oplits0)

    # TODO: there may be more optimal ways to do this. but we're basically
    # introducing literals for every bit, doitn bit-wise xnor, then doing
    # a logical and over the resulting lits.

    # NOTE: We may want to do something better for small numbers of bits as
    # it wouldn't be too expensive to avoid the intermediate literals.

    bit_lits = [self._make_lit(expr, bit=bit) for bit in range(bits)]

    for bit in range(bits):
      # oplits0[bit] and oplits1[bit] => bit_lits[bit]
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
          self._make_not(oplits0[bit]),
          self._make_not(oplits1[bit]),
          self._make_not(bit_lits[bit])))

      # not oplits0[bit] and not oplits1[bit] => bit_lits[bit]
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
          oplits0[bit],
          oplits1[bit],
          self._make_not(bit_lits[bit])))

      # oplits0[bit] and not oplits1[bit] => not bit_lits[bit]
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
          self._make_not(oplits0[bit]),
          oplits1[bit],
          bit_lits[bit]))

      # not oplits0[bit] and oplits1[bit] => not bit_lits[bit]
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
          oplits0[bit],
          self._make_not(oplits1[bit]),
          bit_lits[bit]))

    expr_lit = self._make_lit(expr)

    # For each bit: expr_lit => bit_lits[bit]
    for bit in range(bits):
      self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        bit_lits[bit],
        self._make_not(expr_lit)))

    # bit_lits[0] and ... and bit_lits[bits-1] => expr_lit
    self._cnfctx.add_constraint(self._cnfctx.expr.logical_or(
        *[self._make_not(bit_lit) for bit_lit in bit_lits],
        expr_lit))

    return self._pack(expr_lit)

  #  for lit0, lit1 in zip(mapped_ops[0], mapped_ops[0])
  #
  #  return self._pack(mapped_ops[0][expr.attrs()['index']])

  def _pack(self, lit):
    return [lit]

  def _unpack(self, booltup):
    return booltup[0]

  def _make_lit(self, expr, bit=None):
    lit = self._cnfctx.variable(
        name=ExprUtils.make_variable_name_from_expr(expr, bit),
        valtype=self._cnfctx.valtype.bool())
    self._name_map[expr] = lit.name()
    return lit

  def _make_not(self, lit):
    # All literals are either variables or negations of variables. If we
    # are asked to negate a negation, return the variable.
    if self._cnfctx.expr.is_logical_not(lit):
      return lit.ops()[0]
    else:
      return self._cnfctx.expr.logical_not(lit)

class CnfSolveResult:

  def __init__(self, varmap=None, varmap_gen=None, varmap_expr=None):
    self._varmap = varmap
    self._varmap_gen = varmap_gen
    self._varmap_expr = varmap_expr

  def __bool__(self):
    return self._varmap is not None

  def __nonzero__(self):
    return self.__bool__()

  def get_varmap(self):
    return self._varmap

  def get_varmap_gen(self):
    return self._varmap_gen

  def get_varmap_expr(self):
    return self._varmap_expr

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
      #print(f"self._expr_map[{expr}] = {mapped_expr}")
      return mapped_expr

  def solve(self):
    # Add each constraint.
    for constraint in self._srcctx.constraints():
      c = constraint
      c = self._decomposer.decompose(c)
      c = self._srcctx.util.pushnot(c)
      c = self._srcctx.util.simplify(c)
      c = self._srcctx.util.canonicalize(c)
      #print(f"Simplifying {constraint} to {c} ")
      constraint_litvec = self.map_expr(c)
      self._cnfctx.add_constraint(
        self._cnfctx.expr.logical_or(constraint_litvec[0]))

    
    #print('-'*80)
    #print(f"ctx_constraints=")
    #for c in self._srcctx.constraints():
    #  print(f"- {c}")
    #print('-'*80)
    #print(f"cnf_variables=")
    #for var in self._cnfctx.variables():
    #  print(f"- {var}")
    #print('-'*80)
    #print(f'cnf_name_map=')
    #for k, v in self._proxy._name_map.items():
    #  print(f'- {k} -> {v}')
    #print('-'*80)
    #print(f"cnf_constraints=")
    #for c in self._cnfctx.constraints():
    #  print(f"- {c}")
    #print('-'*80)


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

    #print(f"var_num_mapping={var_num_mapping}")

    if g.solve():
      # SAT
      logger.info(f"SAT")

      # Get mapping for cnfctx literals.
      cnf_varmap = {}
      model = g.get_model()
      for i in model:
        if i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[i]] = True
        elif -i in var_num_mapping_inv:
          cnf_varmap[var_num_mapping_inv[-i]] = False

      # Get mapping for srcctx variables.
      varmap = {}
      varmap_gen = {}

      varmap_subexprs = []

      for v in self._srcctx.variables():
        valtype = v.valtype()
        valtype_def = valtype.valtype_def()

        mapped_v = self.map_expr(v)

        have_cnf_vs = [cnf_v in cnf_varmap for cnf_v in mapped_v]

        booltup = []
        boolgen = []
        boolexprs = []

        for index, cnf_v in zip(range(len(mapped_v)), mapped_v):
          if cnf_v in cnf_varmap:
            booltup.append(cnf_varmap[cnf_v])
            boolgen.append([cnf_varmap[cnf_v]])
            boolexprs.append(
              self._srcctx.expr.util_equal(
                valtype_def.get_bool_expr(v, index=index),
                self._srcctx.constant(value=cnf_varmap[cnf_v], valtype=self._srcctx.valtype.bool())))
          else:
            # Apparently it doesn't matter...
            booltup.append(random.choice([True, False]))
            boolgen.append([True, False])

        value = valtype_def.convert_booltup_to_value(valtype, booltup)
        #print(f"value {value} FOR {v}")

        varmap[v] = value

        def gen(boolgen, valtype, v):
          #print(f"gen({boolgen}, {valtype}) FOR {v}")
          for booltup in itertools.product(*boolgen):
            yield valtype.valtype_def().convert_booltup_to_value(valtype, booltup)

        #for booltup in itertools.product(*boolgen):
        #  actvalue = valtype_def.convert_booltup_to_value(valtype, booltup)
        #  #print(f"FOUND {booltup} ({actvalue}) -> FOR {v}")

        varmap_gen[v] = lambda boolgen=boolgen, valtype=valtype, v=v: gen(boolgen, valtype, v)

        if len(boolexprs) == 0:
          # Don't do anything.
          pass
        elif len(boolexprs) == 1:
          # Add the singular expression.
          varmap_subexprs.append(boolexprs[0])
        else:
          varmap_subexprs.append(self._srcctx.expr.logical_and(*boolexprs))


        # We can use this to make up a conflict constraint.
        #if all(have_cnf_vs):
        #  # If we have all bits of the variable in the solver's map we
        #  # can construct a value expr for it.
        #  booltup = [cnf_varmap[cnf_v] for cnf_v in self.map_expr(v)]
        #  value = valtype_def.convert_booltup_to_value(valtype, booltup)
        #  varmap[v] = self._srcctx.expr.is_equal(
        #    v,
        #    constant(value, valtype))
        #elif not any(have_cnf_vs):
        #  # If we don't have any bits for a variable then it is unconstrained.
        #  varmap[v] = self._srcctx.constant(value=1, valtype=self._srcctx.valtype.bool())
        #else:
        #  # We have some bits, but not all bits. This is awkward.

      if len(varmap_subexprs) == 0:
        varmap_expr = self._srcctx.constant(value=1, valtype=self._srcctx.valtypel.bool())
      elif len(varmap_subexprs) == 1:
        varmap_expr = varmap_subexprs[0]
      else:
        varmap_expr = self._srcctx.expr.logical_and(*varmap_subexprs)

      varmap_expr = self._srcctx.util.simplify(varmap_expr)

      return CnfSolveResult(varmap=varmap, varmap_gen=varmap_gen, varmap_expr=varmap_expr)

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
