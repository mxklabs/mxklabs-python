import inspect
import unittest

import mxklabs as mxk

class Test_ExprVisitor(unittest.TestCase):

    def test_exprvisitor_expr_visitor_functions(self):

        # For all classes, visitor_type, that derive from mxk.ExprWalker...
        for visitor_type in mxk.Utils.get_derived_classes(mxk,
                                                          mxk.ExprVisitor):
            # For all classes, expr_type, that derive from mxk.Expr...
            for expr_type in mxk.Utils.get_derived_classes(mxk, mxk.Expr):
                # Test that visitor_type handles expr_type.
                visit_method_name = '_visit_' + mxk.Utils.camel_case_to_snake_case(
                    expr_type.__name__)

                self.assertTrue(
                    mxk.utils.Utils.class_has_function(visitor_type,
                                                     visit_method_name),
                    "expected '{}' to have a function '{}'".format(
                        visitor_type.__name__, visit_method_name))



