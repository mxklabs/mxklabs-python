from mxklabs.expr import expr as ex
from mxklabs import utils

''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr, args=None):
    
    assert(isinstance(expr, ex.Expr))
    
    visit_method_name = 'visit_' + utils.Utils.camel_case_to_snake_case(expr.__class__.__name__)
    visit_method = getattr(self, visit_method_name)
    
    res = dict([(c, self.bottom_up_walk(c, args)) for c in expr.children()])
    
    return visit_method(expr=expr, res=res, args=args)
  