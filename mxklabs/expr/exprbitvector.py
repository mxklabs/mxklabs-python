import six

import mxklabs.utils

from mxklabs.expr import expr as e

@mxklabs.utils.Memoise
def BitVector(bits): return e.Type("uint%d" % bits, values=six.moves.range(2**bits), num_values=2**bits)

class Index(e.Expression):
  
  def __init__(self, indexee, index):
    e.Expression.__init__(self, type=indexee.type(), nodestr="index", children=[indexee, index], min_num_children=2, max_num_children=2)
    
  def evaluate(self, args):
    indexee = args[self.children()[0]]
    index = args[self.children()[1]] % self.type().num_values()
    return ((indexee & (1 << index)) != 0)