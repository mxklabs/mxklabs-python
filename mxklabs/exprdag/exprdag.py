import collections

from mxklabs.utils import Utils
from mxklabs.expr.exprbase import Expr
import mxklabs as mxk

# A node is class string plus aux?
# Does end-user input dags? Probably not, current format works OK, stick with
# constraints. But perhaps it's useful as an internal data structure?
#

ExprDagNode = collections.namedtuple("ExprDagNode", ["expr", "is_root"])



class ExprDag(object):
    """
    A representation of a directed acyclic graph in which
    """
    VALID_LABELS = [Utils.camel_case_to_kebab_case(e.__name__)
        for e in Utils.get_derived_classes(mxk, Expr)]

    def __init__(self):
        self._node_map = {}

    def add_node(self, label, **kwargs):
        ExprDag.check_label(label)

    @staticmethod
    def check_label(label):
        """
        Check if 'label' matches a expression object.
        :param label: A kebab-case label of an expression type.
        :return: True if such an expression exists.
        """
        if label not in ExprDag.VALID_LABELS:
            valid_label_strs = ["'{}'".format(l) for l in ExprDag.VALID_LABELS]
            raise Exception("expected label ('{}') to be one of {}".format(
                label, ", ".join(valid_label_strs)))



