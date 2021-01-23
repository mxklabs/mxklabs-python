import itertools

class ExprTester:

  def __init__(self, ctx, expr_fun, op_valtypes, attrs, semantics):
    """
    ctx         - context.
    expr_fun    - a callable to generate the expression, e.g., ctx.expr.logical_and
    op_valtypes - a list of valtypes for expr's inputs
    attrs       - the attributes for the expr
    semantics   - a callable that maps a list of input values to an expected output value
    """
    self._ctx = ctx
    self._expr_fun = expr_fun
    self._op_valtypes = op_valtypes
    self._attrs = attrs
    self._semantics = semantics
    self._num_ops = len(self._op_valtypes)

    self._ctx.clear()

    self._test_evaluate_varops()
    self._test_evaluate_constops()

  def _test_evaluate_varops(self):
    # Create a list of variables for the operands.
    varlist = []
    for i in range(self._num_ops):
      varlist.append(self._ctx.variable(name=f"op_{i}", valtype=self._op_valtypes[i]))

    # Create the expression with variables for inputs.
    varexpr = self._expr_fun(*varlist, **self._attrs)

    # Iterate over all possible input values and check evaluate for varexpr is correct.
    for valtup in itertools.product(*[self._op_valtypes[i].values() for i in range(self._num_ops)]):
      varmap = { varlist[i] : valtup[i] for i in range(self._num_ops)}
      expected_val = self._semantics(*valtup)
      actual_val = self._ctx.util.evaluate(varexpr, varmap)
      assert(expected_val == actual_val), f"expected '{varexpr}' with {varmap} to evaluate to {expected_val} (got {actual_val})"

  def _test_evaluate_constops(self):

    # Iterate over all possible input values.
    for valtup in itertools.product(*[self._op_valtypes[i].values() for i in range(self._num_ops)]):

      # Create a list of variables for the operands.
      constlist = []
      for i in range(self._num_ops):
        constlist.append(self._ctx.constant(value=valtup[i], valtype=self._op_valtypes[i]))

      # Create the expression with constant for inputs.
      constexpr = self._expr_fun(*constlist, **self._attrs)

      # Evaluate it and check against expectation.
      expected_val = self._semantics(*valtup)
      actual_val = self._ctx.util.evaluate(constexpr, {})

      assert(expected_val == actual_val), f"expected '{constexpr}' to evaluate to {expected_val} (got {actual_val})"

      # Decompose and simplify.
      decompose_expr = self._ctx.util.decompose(constexpr)
      simplified_expr = self._ctx.util.simplify(decompose_expr)

      # Expect it to have simplified to a const. If not, we're not really doing
      # a great job in propagating constants.
      assert(self._ctx.is_constant(simplified_expr)), f"expected '{constexpr}' to decompose/simplify to a constant (got {simplified_expr})"
      assert(simplified_expr.value() == expected_val), f"expected '{constexpr}' to decompose/simplify to a constant with value {expected_val} (got {simplified_expr})"