from mxklabs.expr import expranalyse as ea
from mxklabs.expr import exprtype as et

class ExpressionEvaluator(ea.ExprWalker):
    def _process(self, expr, variable_value_map):
        return self.bottom_up_walk(expr=expr, args=variable_value_map)

    def visit_const(self, expr, res, args):
        return expr.value()

    def visit_var(self, expr, res, args):
        return args[expr]

    def visit_logical_and(self, expr, res, args):
        return et.ExprValue(expr_type=et.ExprTypeRepository._BOOL,
                            user_value=all([res[child].user_value() for child in
                                            expr.children()]))

    def visit_logical_or(self, expr, res, args):
        return et.ExprValue(expr_type=et.ExprTypeRepository._BOOL,
                            user_value=any([res[child].user_value() for child in
                                            expr.children()]))

    def visit_logical_not(self, expr, res, args):
        return et.ExprValue(expr_type='bool',
                            user_value=not res[expr.child()].user_value())

    def visit_equals(self, expr, res, args):
        return et.ExprValue(expr_type='bool',
                            user_value=(res[child(0)] == res[child(1)]))

    ''' Quick version (avoid creating VarHarvester). '''

    @staticmethod
    def process(expr, variable_value_map):
        ee = ExpressionEvaluator()
        return ee._process(expr, variable_value_map)