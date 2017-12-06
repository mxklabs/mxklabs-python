from __future__ import print_function

from mxklabs.dimacs import Dimacs
from mxklabs.expr.expr import LogicalAnd, Const
from mxklabs.expr.exprvisitor import ExprVisitor
from mxklabs.expr.exprtype import ExprTypeRepository, ExprValue
from mxklabs.utils import memoise

class Tseitin(ExprVisitor):
    """

    """

    class _Cache(object):

        """
        Internal class.
        """

        # Literal corresponding to true.
        TRUE_LIT = 1
        # Literal corresponding to false.
        FALSE_LIT = -1

        def __init__(self):
            # Map tuple of expression and bit to literal.
            self._cache = {
                Const('bool', True): {0: Tseitin._Cache.TRUE_LIT},
                Const('bool', False): {0: Tseitin._Cache.FALSE_LIT}
            }
            self._dimacs = Dimacs(
                clauses=set([frozenset([Tseitin._Cache.TRUE_LIT])]))

        def dimacs(self):
            return self._dimacs

        ''' Test to see if bit is cached. '''

        def is_cached(self, expr, bit=None):
            if bit is not None:
                return expr in self._cache.keys() and bit in self._cache[expr].keys()
            else:
                return all(self.is_cached(expr, bit) for bit in
                                     range(expr.expr_type().littup_size()))

        def make_lit(self):
            self._dimacs.num_vars += 1
            return self._dimacs.num_vars

        def make_lits(self, bits):
            return tuple([self.make_lit() for b in range(bits)])

        def lookup_lit(self, expr, bit):
            if expr not in self._cache.keys():
                lit = self.make_lit()
                self._cache[expr] = { bit: lit }
                return lit
            elif bit not in self._cache[expr]:
                lit = self.make_lit()
                self._cache[expr][bit] = lit
            else:
                return self._cache[expr][bit]

        def lookup_littup(self, expr):
            return tuple(self.lookup_lit(expr, bit) for bit in
                                     range(expr.expr_type().littup_size()))

        ''' Add a CNF clause. '''

        def add_clause(self, clause):
            self._dimacs.clauses.add(clause)

        ''' Print cache. '''

        def print(self):
            for exprstr, lit in self._cache.items():
                print("'{exprstr}:{bit}' -> {lit}".format(exprstr=exprstr, lit=lit))

    def __init__(self):
        self._cache = Tseitin._Cache()
        self._true_lit, = self.cache_lookup(Const('bool', True))
        self._false_lit, = self.cache_lookup(Const('bool', False))

        ExprVisitor.__init__(self)
    
    def dimacs(self):
        return self._cache.dimacs()

    ''' Evaluate a number of boolean expressions and ensure they are asserted. '''
    def add_constraints(self, exprs):
        for expr in exprs:
            self.add_constraint(expr)

    ''' Evaluate a boolean expression and ensure it is asserted to hold. '''
    def add_constraint(self, expr):
        if isinstance(expr, LogicalAnd):
            # This is a small optimisation to avoid additional literals.
            for child in expr.children():
                self.add_constraint(child)
        elif expr.expr_type() == ExprTypeRepository._BOOL:
            littup = expr.visit(self)
            lit, = littup
            self._cache.add_clause(frozenset([lit]))
        else:
            raise("Cannot add an expression with type '{expr_type}' as a "
                  "constraint".format(expr_type=expr.expr_type()))

    ''' Can be used to established what literals belong to an expression. '''    
    def cache_lookup(self, expr):
        return self._cache.lookup_littup(expr)


    @memoise
    def _visit_var(self, expr):
        return self._cache.lookup_littup(expr)

    @memoise
    def _visit_const(self, expr):
        return tuple(self._true_lit if b else self._false_lit for b \
                in expr.expr_value().littup_value())

    @memoise
    def _visit_logical_and(self, expr):

        ops = [child.visit(self) for child in expr.children()]

        littup = self._cache.lookup_littup(expr)
        lit, = littup

        # Ensure when the logical and is true, exprlit is true.
        self._cache.add_clause(frozenset([lit]+[-op for op, in ops]))

        # Ensure when any child causes the logical and to be false, exprlit is false, too.
        for op, in ops:
            self._cache.add_clause(frozenset([-lit, op]))

        return littup

    @memoise
    def _visit_logical_or(self, expr):

        ops = [child.visit(self) for child in expr.children()]

        littup = self._cache.lookup_littup(expr)
        lit, = littup

        # Ensure when the logical or is false, exprlit is false.
        self._cache.add_clause(frozenset([-lit]+[op for op, in ops]))

        # Ensure when any child causes the logical and to be true, exprlit is true, too.
        for op, in ops:
            self._cache.add_clause(frozenset([lit, -op]))

        return littup

    @memoise
    def _visit_logical_not(self, expr):

        op, = expr.child().visit(self)
        return (-op,)

    @memoise
    def _visit_equals(self, expr):

        ops = [child.visit(self) for child in expr.children()]

        littup = self._cache.lookup_littup(expr)

        assert(len(littup) == 1)
        assert(len(ops)==2)
        assert(len(ops[0]) == len(ops[1]))

        lit, = littup

        bits = len(ops[0])

        # TODO: Cache these somehow. The tmp_lits are one literal per bit
        # and is true if and only if this bit of the operands agree.
        tmp_lits = self._cache.make_lits(bits)

        for b in range(bits):
            # For each bit, if operands disagree this implies -lit.
            self._cache.add_clause(frozenset([ ops[0][b], -ops[1][b], -tmp_lits[b]]))
            self._cache.add_clause(frozenset([-ops[0][b],  ops[1][b], -tmp_lits[b]]))
            self._cache.add_clause(frozenset([ ops[0][b],  ops[1][b],  tmp_lits[b]]))
            self._cache.add_clause(frozenset([-ops[0][b], -ops[1][b],  tmp_lits[b]]))

        # Ensure when the every bit agrees, exprlit is true.
        self._cache.add_clause(
            frozenset([-tmp_lits[b] for b in range(bits)] + [lit]))

        # Ensure when any child causes the logical and to be false, exprlit is false, too.
        for b in range(bits):
            self._cache.add_clause(frozenset([tmp_lits[b], -lit]))

        return littup

    @memoise
    def _visit_if_then_else(self, expr):

        ops = [child.visit(self) for child in expr.children()]

        littup = self._cache.lookup_littup(expr)

        assert(len(ops)==3)
        assert(len(ops[0]) == 1)
        assert(len(ops[1]) == len(ops[2]) == len(littup))

        cond, = ops[0]
        bits = len(littup)

        for b in range(bits):
            # Literal cond implies littup[b] == ops[1][b]
            self._cache.add_clause(frozenset([-cond, -littup[b], ops[1][b]]))
            self._cache.add_clause(frozenset([-cond, littup[b], -ops[1][b]]))

            # Literal -cond implies littup[b] != ops[1][b]
            self._cache.add_clause(frozenset([cond, littup[b], ops[1][b]]))
            self._cache.add_clause(frozenset([cond, -littup[b], -ops[1][b]]))

        return littup

    @memoise
    def _visit_subtract(self, expr):

        littup = self._cache.lookup_littup(expr)

        return littup

    @memoise
    def _visit_concatenate(self, expr):

        littup = self._cache.lookup_littup(expr)

        return littup

    @memoise
    def _visit_slice(self, expr):

        littup = self._cache.lookup_littup(expr)

        return littup
