import six

import mxklabs.utils

from mxklabs.expr import expr as e

#''' Amalgamate one or mode product expressions into one. '''
#
#
#class Glue(Expression):
#  
#  def __init__(self, *children):
#    self.ensureMinChildren(1)
#    
#    super().__init__()
#
#''' From a product (first child) select the component indexed by the second child. If
#    the second child is non-constant the product must be homogenous (i.e. each child must
#    have the same type). '''
#
#class GetItem(Expression):
#
#  def __init__(self, indexee, index):
#    e.Expression.__init__(self, type=indexee.type(), nodestr="index", children=[indexee, index], min_num_children=2, max_num_children=2)
#    
#  def evaluate(self, args):
#    indexee = args[self.children()[0]]
#    index = args[self.children()[1]] % self.type().num_values()
#    return ((indexee & (1 << index)) != 0)
#  
#''' From a product (first child) select the components started from the component indexed
#    by the second child up to but not including the component indexed by the third child. '''
#
#class Break(Expression):
#  
#  def __init__(self, product, from, to):
#    self.ensureChildIsConst(from)
#    self.ensureConstantChild(to)
  

  