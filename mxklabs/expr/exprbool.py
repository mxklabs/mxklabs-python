from mxklabs.expr import expr as e

'''  operations. '''

class And(e.Expression):
  
  def __init__(self, args):
    e.Expression.__init__(self, type=e.Bool, nodestr="and", children=args, min_num_children=1)
    
  def evaluate(self, args):
    return all([args[c] for c in self.children()])
    
class Or(e.Expression):
  
  def __init__(self, args):
    e.Expression.__init__(self, type=e.Bool, nodestr="or", children=args, min_num_children=1)
    
  def evaluate(self, args):
    return any([args[c] for c in self.children()])

class Not(e.Expression):
  
  def __init__(self, arg):
    e.Expression.__init__(self, type=e.Bool, nodestr="not", children=[arg], num_children=1)
    
  def evaluate(self, args):
    return not args[self.children()[0]]
