import mxklabs.expr
import pytest

#def test_solve1():
ctx = mxklabs.expr.ExprContext()


a = ctx.prop.variable(name="a")

ctx.prop.logical_not(a)

ctx.add_constraint(ctx.prop.logical_and(a, ctx.prop.logical_not(a)))

result = ctx.solve()

# Must be satisfiable.
assert(result)

# Must have a=False
varmap = result.get_variable_values()
assert(False == varmap[a])

