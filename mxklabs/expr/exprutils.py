import string

from .expr import Expr
from .valtype_ import Valtype

class ExprUtils:

  expr_name_counter = 0

  @staticmethod
  def basic_ops_check(exprid, min_ops, max_ops, valtype_checker, ops):

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

    # Check op_valtypes matches static type for all ops.
    if isinstance(valtype_checker, Valtype):
      for op_index, op in zip(range(len(ops)), ops):
        if op.valtype() != valtype_checker:
          raise RuntimeError(f"'{exprid}' expects operands of valtype '{valtype_checker}' (operand {op_index} has valtype '{op.valtype()}')")
    # Check expr_op_valtype is a custom type checker
    if callable(valtype_checker):
      for op_index, op in zip(range(len(ops)), ops):
        if not valtype_checker(op.valtype(), op_index):
          raise RuntimeError(f"'{exprid}' operand {op_index} has an invalid valtype ('{op.valtype()}')")


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
        raise RuntimeError(f"'{valtype_id}' expects sub_valtypes of valtype mxklabs.expr.Valtype (sub_valtypes {index} has valtype {type(sub_valtype)})")

    # Check sub_valtypes match.
    if exp_sub_valtype is not None:
      for index, sub_valtype in zip(range(len(sub_valtypes)), sub_valtypes):
        if sub_valtype != exp_sub_valtype:
          raise RuntimeError(f"'{valtype_id}' expects sub_valtypes of valtype '{exp_sub_valtype}' (sub_valtypes {index} has valtype {sub_valtype})")

  @staticmethod
  def basic_attrs_check(objid, exp_attrs, act_attrs):
    # Check attributes.
    for act_attr in act_attrs:
      if act_attr not in exp_attrs:
        raise RuntimeError(f"'{objid}' does not expect attribute '{act_attr}'")
    for exp_attr in exp_attrs:
      if exp_attr not in act_attrs:
        raise RuntimeError(f"'{objid}' expects attribute '{exp_attr}'")
    for exp_attr in exp_attrs:
      if type(act_attrs[exp_attr]) != exp_attrs[exp_attr]:
        raise RuntimeError(f"'{objid}' expects attribute '{exp_attr}' to be of type '{exp_attrs[exp_attr]}' (got '{type(act_attrs[exp_attr])}')")

  @staticmethod
  def make_variable_name_from_expr(expr, bit=None):

    if not expr.ctx().is_variable(expr):
      result = f"__expr{ExprUtils.expr_name_counter}"
      ExprUtils.expr_name_counter += 1
    else:
      result = expr.name()
  
    if bit is not None:
      result += f"[{bit}]"
    return result

    #result = "$"
    #if not expr.ctx().is_variable(expr):
    #  result += "<"
    #result += f"{repr(expr)}"
    #if bit is not None:
    #  result += f":{bit}"
    #result += ""
    #if not expr.ctx().is_variable(expr):
    #  result += ">"
    #result = result.replace("_", "_")
    #result = result.replace("(", "~L~")
    #result = result.replace(")", "~R~")
    #result = result.replace(" ", "")
    #result = result.replace(",", "~")
    #return result

