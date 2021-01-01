from .expr import Expr

class ExprUtils:

  @staticmethod
  def basicOpsAndAttrsCheck(opid, min_ops, max_ops, exp_op_valtype, ops, exp_attrs, act_attrs):

    # Check number of operands.
    if (min_ops is not None and \
        max_ops is not None and \
        min_ops == max_ops):
      if (min_ops != len(ops)):
        raise RuntimeError(f"'{opid}' expects exactly {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
    else:
      if (min_ops is not None and len(ops) < min_ops):
        raise RuntimeError(f"'{opid}' expects at least {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
      if (max_ops is not None and len(ops) > max_ops):
        raise RuntimeError(f"'{opid}' expects at most {max_ops} operand{'s' if max_ops > 1 else ''} (got {len(ops)})")

    # Check optypes match.
    if exp_op_valtype is not None:
      for op_index, op in zip(range(len(ops)), ops):
        if op.valtype != exp_op_valtype:
          raise RuntimeError(f"'{opid}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

    # Check operands are actually expression objects.
    for op_index, op in zip(range(len(ops)), ops):
      if not isinstance(op, Expr):
        raise RuntimeError(f"'{opid}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

    # Check operands are from the same context.
    for op_index, op in zip(range(len(ops)), ops):
      if not isinstance(op, Expr):
        raise RuntimeError(f"'{opid}' expects operands of type mxklabs.expr.Expr (operand {op_index} has type {type(op)})")

    # Check attributes.
    for actAttr in act_attrs:
      if actAttr not in exp_attrs:
        raise RuntimeError(f"'{opid}' does not expect attribute '{actAttr}'")
    for expAttr in exp_attrs:
      if expAttr not in act_attrs:
        raise RuntimeError(f"'{opid}' expects attribute '{expAttr}'")

