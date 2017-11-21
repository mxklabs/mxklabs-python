from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et


class Equals(ex.Expr):
    def __init__(self, op0, op1):

        ex.Expr.__init__(self, expr_type=et.ExprTypeRepository._BOOL, children=[op0, op1])

        self.ensure_minimum_number_of_children(2)
        self.ensure_children_types_match()



#class NotEquals(ex.Expr):
#    def __init__(self, args):
#        pass
#
#
#class LessThanEquals(ex.Expr):
#
#    def __init__(self, #args):
#        pass

