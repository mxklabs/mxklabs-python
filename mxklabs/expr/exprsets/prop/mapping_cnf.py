class Mapping:

  def __init__(self, src_ctx, tgt_ctx):
    self.src_ctx = src_ctx
    self.tgt_ctx = tgt_ctx

  def map_value(self, val):
    pass

  def map_value_inv(self, val):
    pass

  def map_valtype(self, valtype):
    assert(valtype.ident == 'mxklabs.expr.valtypes.bool')


  def logical_not(self, expr, mapped_op):
    return (self.tgt_ctx.cnf.logical_not(mapped_op),)

  def logical_and(self, expr, *mapped_ops):
    return (self.tgt_ctx.cnf.logical_and(*mapped_ops),)

  def logical_nand(self, expr, *mapped_ops):
    return (self.tgt_ctx.cnf.logical_not(
      self.tgt_ctx.cnf.logical_and(*mapped_ops)),)

  def logical_or(self, expr, *mapped_ops):
    return (self.tgt_ctx.cnf.logical_or(*mapped_ops),)

  def logical_nor(self, expr, *mapped_ops):
    return (self.tgt_ctx.cnf.logical_not(
      self.tgt_ctx.cnf.logical_or(*mapped_ops)),)

  def logical_xor(self, expr, mapped_op0, mapped_op1):
    return (self.tgt_ctx.cnf.logical_or(
      self.tgt_ctx.cnf.logical_and(
        mapped_op0,
        self.tgt_ctx.cnf.logical_not(mapped_op1)),
      self.tgt_ctx.cnf.logical_and(
        self.tgt_ctx.cnf.logical_not(mapped_op0),
        mapped_op1)
    ),)

  def logical_nxor(self, expr, mapped_op0, mapped_op1):
    return (self.tgt_ctx.cnf.logical_or(
      self.tgt_ctx.cnf.logical_and(
        mapped_op0,
        mapped_op1),
      self.tgt_ctx.cnf.logical_and(
        self.tgt_ctx.cnf.logical_not(mapped_op0),
        self.tgt_ctx.cnf.logical_not(mapped_op1))
    ),)

  def implies(self, expr, mapped_op0, mapped_op1):
    return (self.tgt_ctx.cnf.logical_or(
      mapped_op1,
      self.tgt_ctx.cnf.logical_not(mapped_op0)
    ),)