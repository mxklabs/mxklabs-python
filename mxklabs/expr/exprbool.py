from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex

class LogicalAnd(ex.Expr):
  
  def __init__(self, *args):
    super().__init__(type=et.Bool(), nodestr="logical-and", children=args)
    
    self.ensure_minimum_number_of_children(1)
    for i in range(len(self.children())):
      self.ensure_child_is_type(i, et.Bool())
    
  def evaluate(self, args):
    return (all([args[c][0] for c in self.children()]),)
    
class LogicalOr(ex.Expr):
  
  def __init__(self, *args):
    super().__init__(type=et.Bool(), nodestr="logical-or", children=args)
    
    self.ensure_minimum_number_of_children(1)
    for i in range(len(self.children())):
      self.ensure_child_is_type(i, et.Bool())
    
  def evaluate(self, args):
    return (any([args[c][0] for c in self.children()]),)

class LogicalNot(ex.Expr):
  
  def __init__(self, arg):
    super().__init__(type=et.Bool(), nodestr="logical-not", children=[arg])
    
    self.ensure_number_of_children(1)
    self.ensure_child_is_type(0, et.Bool())
    
  def evaluate(self, args):
    return (not args[self.children()[0]][0],)
