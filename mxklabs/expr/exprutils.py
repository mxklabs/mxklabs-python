import string

from .expr import Expr

class ExprUtils:

  @staticmethod
  def basic_ops_check(exprid, min_ops, max_ops, exp_op_valtype, ops):

    # Check number of operands.
    if (min_ops is not None and \
        max_ops is not None and \
        min_ops == max_ops):
      if (min_ops != len(ops)):
        raise RuntimeError(f"'{exprid}' expects exactly {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
    else:
      if (min_ops is not None and len(ops) < min_ops):
        raise RuntimeError(f"'{exprid}' expects at least {min_ops} operand{'s' if min_ops > 1 else ''} (got {len(ops)})")
      if (max_ops is not None and len(ops) > max_ops):
        raise RuntimeError(f"'{exprid}' expects at most {max_ops} operand{'s' if max_ops > 1 else ''} (got {len(ops)})")

    # Check op_valtypes matches expectation.
    if exp_op_valtype is not None:
      for op_index, op in zip(range(len(ops)), ops):
        if op.valtype != exp_op_valtype:
          raise RuntimeError(f"'{exprid}' expects operands of type '{exp_op_valtype}' (operand {op_index} has type '{op.valtype()}')")

  @staticmethod
  def basic_sub_valtypes_check(valtype_id, min_sub_valtypes, max_sub_valtypes, exp_sub_valtype, sub_valtypes):

    # Check number of operands.
    if (min_sub_valtypes is not None and \
        max_sub_valtypes is not None and \
        min_sub_valtypes == max_sub_valtypes):
      if (min_sub_valtypes != len(sub_valtypes)):
        raise RuntimeError(f"'{valtype_id}' expects exactly {min_sub_valtypes} sub_valtypes{'s' if min_sub_valtypes > 1 else ''} (got {len(sub_valtypes)})")
    else:
      if (min_sub_valtypes is not None and len(sub_valtypes) < min_sub_valtypes):
        raise RuntimeError(f"'{valtype_id}' expects at least {min_sub_valtypes} sub_valtypes{'s' if min_sub_valtypes > 1 else ''} (got {len(sub_valtypes)})")
      if (max_sub_valtypes is not None and len(sub_valtypes) > max_sub_valtypes):
        raise RuntimeError(f"'{valtype_id}' expects at most {max_sub_valtypes} sub_valtypes{'s' if max_sub_valtypes > 1 else ''} (got {len(sub_valtypes)})")

    # Check sub_valtypes are actually valtype objects.
    for index, sub_valtype in zip(range(len(sub_valtypes)), sub_valtypes):
      if not isinstance(op, Valtype):
        raise RuntimeError(f"'{valtype_id}' expects sub_valtypes of type mxklabs.expr.Valtype (sub_valtypes {index} has type {type(sub_valtype)})")

    # Check sub_valtypes match.
    if exp_sub_valtype is not None:
      for index, sub_valtype in zip(range(len(sub_valtypes)), sub_valtypes):
        if sub_valtype != exp_sub_valtype:
          raise RuntimeError(f"'{valtype_id}' expects sub_valtypes of type '{exp_sub_valtype}' (sub_valtypes {index} has type {sub_valtype})")

  @staticmethod
  def basic_attrs_check(objid, exp_attrs, act_attrs):
    # Check attributes.
    for actAttr in act_attrs:
      if actAttr not in exp_attrs:
        raise RuntimeError(f"'{objid}' does not expect attribute '{actAttr}'")
    for expAttr in exp_attrs:
      if expAttr not in act_attrs:
        raise RuntimeError(f"'{objid}' expects attribute '{expAttr}'")

  @staticmethod
  def make_variable_name_from_expr(expr, bit=None):
    result = f"[{repr(expr)}"
    if bit is not None:
      result += f":{bit}"
    result += "]"
    return result

