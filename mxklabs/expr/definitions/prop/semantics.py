from ...exprutils import ExprUtils

class InputValidator:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_not', 1, 1, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_and(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_and', 2, None, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_nand(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_nand', 2, None, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_or(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_or', 2, None, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_nor(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_nor', 2, None, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_xor(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_xor', 2, 2, self.ctx.valtypes.bool(), ops, [], attrs)

  def logical_xnor(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_xnor', 2, 2, self.ctx.valtypes.bool(), ops, [], attrs)

  def implies(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('implies', 2, 2, self.ctx.valtypes.bool(), ops, [], attrs)

class ExprSimplifier:
  """ Responsible for simplifying and canonicalising expressions. Return
      an expression object to replace the about-to-be-constructed expression
      to replace it with something simpler. Take care not to create infinite
      recursion. Return None to construct the expression as-is.
  """
  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, op0):
    # not(1) => 0
    # not(0) => 1
    if self.ctx.prop.is_constant(op0):
      return self.ctx.prop.constant(not op0.value)

    # not(not(e)) => e
    if self.ctx.prop.is_logical_not(op0):
      return op0.ops[0]

    # not(and(e_0,...,e_n)) => or(not(e_0),...,not(e_n)))
    if self.ctx.prop.is_logical_and(op0):
      return self.ctx.prop.logical_or(*[self.ctx.prop.logical_not(op) for op in op0.ops])

    # not(or(e_0,...,e_n)) => and(not(e_0),...,not(e_n)))
    if self.ctx.prop.is_logical_or(op0):
      return self.ctx.prop.logical_and(*[self.ctx.prop.logical_not(op) for op in op0.ops])

    return None

  def logical_and(self, *ops):
    # and(..., 0, ...) => 0
    if any([self.ctx.prop.is_constant(op) and not op.value for op in ops]):
      return self.ctx.prop.constant(False)

    # and(1, ..., 1) => 1
    if all([self.ctx.prop.is_constant(op) and op.value for op in ops]):
      return self.ctx.prop.constant(True)

    # Sort by operand hash.
    ops = list(ops)
    new_ops = sorted(ops, key=hash)
    if new_ops != ops:
      return self.ctx.prop.logical_and(*new_ops)

    return None

  def logical_nand(self, *ops):
    return self.ctx.logical_not(self.ctx.logical_and(*ops))

  def logical_or(self, *ops):
    # or(..., 1, ...) => 1
    if any([self.ctx.prop.is_constant(op) and op.value for op in ops]):
      return self.ctx.prop.constant(True)

    # or(0, ..., 0) => 0
    if all([self.ctx.prop.is_constant(op) and not op.value for op in ops]):
      return self.ctx.prop.constant(False)

    # Sort by operand hash.
    ops = list(ops)
    new_ops = sorted(ops, key=hash)
    if new_ops != ops:
      return self.ctx.prop.logical_or(*new_ops)

    return None

  def logical_nor(self, *ops):
    return self.ctx.logical_not(self.ctx.logical_or(*ops))

  def logical_xor(self, *ops):
    # If xor(0,1) => 1
    # If xor(1,0) => 1
    # If xor(1,1) => 0
    # If xor(0,0) => 0
    if all([self.ctx.prop.is_constant(op) for op in ops]):
      return self.ctx.prop.constant(ops[0].value != ops[1].value)

    # Sort by operand hash.
    if hash(ops[1]) < hash(ops[0]):
      return self.ctx.prop.logical_xor(ops[1], ops[0])

    return None

  def logical_xnor(self, *ops):
    return self.ctx.logical_not(self.ctx.logical_xor(*ops))

  def implies(self, *ops):
    return self.ctx.prop.logical_or(self.ctx.prop.logical_not(ops[0]), ops[1])

class TypeInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_and(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_nand(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_or(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_nor(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_xor(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def logical_xnor(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

  def implies(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

class ValueInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, op_value):
    return not op_value

  def logical_and(self, expr, *op_values):
    return all(op_values)

  def logical_nand(self, expr, *op_values):
    return not(all(op_values))

  def logical_or(self, expr, *op_values):
    return any(op_values)

  def logical_nor(self, expr, *op_values):
    return not(any(op_values))

  def logical_xor(self, expr, op_value0, op_value1):
    return op_value0 != op_value1

  def logical_xnor(self, expr,  op_value0, op_value1):
    return op_value0 == op_value1

  def implies(self, expr, op_value0, op_value1):
    return op_value1 or not op_value0

class CnfMapping:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, oplit):
    print(f"oplit={oplit}")
    return self._make_not(oplit)

  def logical_and(self, expr, *oplits):
    lit = self.ctx.make_var(f'{expr}', self.ctx.valtypes.bool())

    # For each op: lit => oplit
    for oplit in oplits:
      self.ctx.add_constraint(self.ctx.cnf.logical_or(
        oplit,
        self._make_not(lit)))

    # oplit_0 and ... and oplit_n => lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        *[self._make_not(oplit) for oplit in oplits],
        lit))

    return lit

  def logical_nand(self, expr, *oplits):
    raise RuntimeError(f"Unexpected call to create CNF mapping for '{expr}'")

  def logical_or(self, expr, *oplits):
    lit = self.ctx.make_var(f'{expr}', self.ctx.valtypes.bool())

    # For each op: lit => oplit
    for oplit in oplits:
      self.ctx.add_constraint(self.ctx.cnf.logical_or(
        oplit,
        self._make_not(lit)))

    # not oplit_0 and ... and not oplit_n => not lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        *[oplit for oplit in oplits],
        self._make_not(lit)))

    return lit

  def logical_nor(self, expr, *oplits):
    raise RuntimeError(f"Unexpected call to create CNF mapping for '{expr}'")

  def logical_xor(self, expr, oplit0, oplit1):
    lit = self.ctx.make_var(f'{expr}', self.ctx.valtypes.bool())

    # oplit0 and not oplit1 => lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        self._make_not(oplit0),
        oplit1,
        lit))

    # not oplit0 and oplit1 => lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        oplit0,
        self._make_not(oplit1),
        lit))

    # oplit0 and oplit1 => not lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        self._make_not(oplit0),
        self._make_not(oplit1),
        self._make_not(lit)))

    # not oplit0 and not oplit1 => not lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        oplit0,
        oplit1,
        self._make_not(lit)))

    return lit

  def logical_xnor(self, expr, op_cnf_expr_tup0, op_cnf_expr_tup1):
    raise RuntimeError(f"Unexpected call to create CNF mapping for '{expr}'")

  def implies(self, expr, op_cnf_expr_tup0, op_cnf_expr_tup1):
    raise RuntimeError(f"Unexpected call to create CNF mapping for '{expr}'")

  def _make_not(self, oplit):
    if self.ctx.cnf.is_logical_not(oplit):
      return oplit.ops[0]
    else:
      return self.ctx.cnf.logical_not(oplit)
