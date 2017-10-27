import six

import mxklabs.utils

from mxklabs.expr import expr as e

@mxklabs.utils.Memoise
def BitVector(bits): return e.Type("uint%d" % bits, values=six.moves.range(2**bits), num_values=2**bits)

