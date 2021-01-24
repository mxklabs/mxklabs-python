from .exprdef import BitvectorExprDef
from ...exprutils import ExprUtils

class BitvectorMult(BitvectorExprDef):

  def __init__(self, **kwargs):
    BitvectorExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting as many bool ops as width bits, all boolean.
    ExprUtils.basic_attrs_check(self.id(), {'width':int}, attrs)
    valtype_checker = lambda valtype, index: self._ctx.valtype.is_bitvector(valtype)
    ExprUtils.basic_ops_check(self.id(), 2, 2, valtype_checker, ops)

    if (attrs['width'] < 0):
      raise RuntimeError(f"'{self.id}' expected attribute 'width' to be non-negative integer (got {attrs['width']})")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bitvector(width=attrs['width'])

  def evaluate(self, expr, op_values):
    return (op_values[0] * op_values[1]) % (2**expr.attrs()['width'])

  def has_feature(self, featurestr):
    if featurestr == 'decompose':
      return True
    if featurestr == 'simplify':
      return True
    return False

  def simplify(self, expr):

    # TODO: this is not expr-specific, could put in base class

    # if all ops are constant, propagate.
    if all([self._ctx.is_constant(op) for op in expr.ops()]):
      value = self.evaluate(expr, [op.value() for op in expr.ops()])
      return self._ctx.constant(value=value, valtype=expr.valtype())

    # Can't simplify.
    return expr

  def decompose(self, expr):

    def half_adder(bit0, bit1):
      return {
        "sum" : self._ctx.expr.logical_xor(bit0, bit1),
        "carry" : self._ctx.expr.logical_and(bit0, bit1)
      }

    def full_adder(bit0, bit1, carry):
      return {
        "sum" : self._ctx.expr.logical_xor(
                  self._ctx.expr.logical_xor(bit0, bit1),
                  carry),
        "carry" : self._ctx.expr.logical_or(
                    self._ctx.expr.logical_and(bit0, bit1),
                    self._ctx.expr.logical_and(
                      self._ctx.expr.logical_or(bit0, bit1),
                      carry))
      }

    def zipadd(bits0, bits1):
      result = []
      carry = None
      if len(bits0) == len(bits1):
        for bit0, bit1 in zip(bits0, bits1):
          if carry is None:
            res = half_adder(bit0, bit1)
          else:
            res = full_adder(bit0, bit1, carry)
          result.append(res['sum'])
          carry = res['carry']
        result.append(carry)
      elif len(bits0) + 1 == len(bits1):
        for bit0, bit1 in zip(bits0, bits1):
          if carry is None:
            res = half_adder(bit0, bit1)
          else:
            res = full_adder(bit0, bit1, carry)
          result.append(res['sum'])
          carry = res['carry']
        # We still have one bit in bits1!
        res = half_adder(bits1[-1], carry)
        result.append(res['sum'])
        result.append(res['carry'])
      else:
        raise RuntimeError("This shouldn't happen")
      return result

    op0 = expr.ops()[0]
    op1 = expr.ops()[1]
    op0_width = op0.valtype().attrs()['width']
    op1_width = op1.valtype().attrs()['width']
    expr_width = expr.attrs()['width']

    op0_bits = [self._ctx.expr.util_index(op0, index=bit) for bit in range(op0_width)]
    op1_bits = [self._ctx.expr.util_index(op1, index=bit) for bit in range(op1_width)]

    ands = [[self._ctx.expr.logical_and(op0_bits[bit0], op1_bits[bit1]) for bit1 in range(op1_width)] for bit0 in range(op0_width)]

    expr_bits = []
    carry_term = []

    for bit in range(expr_width):

      if bit == 0:
        expr_bits.append(ands[0][0])
        carry_term = [ands[i0][0] for i0 in range(1, op0_width)]
      else:
        if bit < op1_width:
          incoming = [ands[i0][bit] for i0 in range(0, op0_width)]
          res = zipadd(carry_term, incoming)
          expr_bits.append(res[0])
          carry_term = res[1:]
        else:
          expr_bits.append(carry_term[0])
          carry_term = carry_term[1:]

    return self._ctx.expr.bitvector_from_bool(*expr_bits, width=expr_width)



