from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex

class LogicalAnd(ex.Expression):
  
  def __init__(self, *args):
    super().__init__(type=et.Bool(), nodestr="logical-and", children=args)
    
    self.ensureMinimumNumberOfChildren(1)
    for i in range(len(self.children())):
      self.ensureChildIsType(i, et.Bool())
    
  def evaluate(self, args):
    return all([args[c] for c in self.children()])
    
class LogicalOr(ex.Expression):
  
  def __init__(self, *args):
    super().__init__(type=et.Bool(), nodestr="logical-or", children=args)
    
    self.ensureMinimumNumberOfChildren(1)
    for i in range(len(self.children())):
      self.ensureChildIsType(i, et.Bool())
    
  def evaluate(self, args):
    return any([args[c] for c in self.children()])

class LogicalNot(ex.Expression):
  
  def __init__(self, arg):
    super().__init__(type=et.Bool(), nodestr="logical-not", children=[arg])
    
    self.ensureNumberOfChildren(1)
    self.ensureChildIsType(0, et.Bool())
    
  def evaluate(self, args):
    return not args[self.children()[0]]
