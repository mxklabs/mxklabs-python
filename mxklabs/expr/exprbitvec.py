#


#class Subtract(ex.Expr):
#    """
#    An object that represents a bit vector subtraction modulo 2^n where both op0
#    and op1 must be Expr objects with type 'uint<n>' for some n.
#    """
#
#    def __init__(self, op0, op1):
#        """
#        Construct a LogicalAnd object.
#        :param args: One or more Expr objects of type Bool (operands).
#        """
#        ex.Expr.__init__(self, type=op0.expr_type(), nodestr="subtract", children=[op0, op1])
#
#        self.ensure_number_of_children(2)
#        //self.ensure_child_is_type(i, et.ExprTypeRepository._)
#
#class Extract(ex.Expr):
#    """
#    An object representing an extraction expression. An extraction expression
#    has three operands: a bitvector an index
#    """
#    def __init(self, args):
#        pass
#
#class Insert(ex.Expr):
#    """
#    An object that represets a bitvector expression that is the result of insert
#    """