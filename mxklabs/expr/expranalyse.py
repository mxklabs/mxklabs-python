import collections

from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et
from mxklabs import utils


class ExprVisitor(object):
  pass


''' Walker object. '''
class ExprWalker(object):
  def __init__(self):
    pass
  
  def bottom_up_walk(self, expr, args=None):

    assert (isinstance(expr, ex.Expr))

    visit_method_name = 'visit_' + utils.Utils.camel_case_to_snake_case(
      expr.__class__.__name__)
    visit_method = getattr(self, visit_method_name)

    res = dict([(c, self.bottom_up_walk(c, args)) for c in expr.children()])

    return visit_method(expr=expr, res=res, args=args)

  def simple_bottom_up_walk(self, expr):

    assert (isinstance(expr, ex.Expr))

    visit_method_name = 'visit_' + utils.Utils.camel_case_to_snake_case(
      expr.__class__.__name__)
    visit_method = getattr(self, visit_method_name)

    res = dict([(c, self.bottom_up_walk(c)) for c in expr.children()])

    return visit_method(expr=expr, children_res=res)

''' Help eliminate constants in expressions. '''



''' Evaluate the value of an expressions. '''


  
  