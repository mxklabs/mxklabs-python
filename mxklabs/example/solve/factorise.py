from __future__ import division
from __future__ import print_function

import mxklabs as mxk

def find_divisor(logger, n):

    constraints = []

    # We're looking for ANY non-trivial divisor of n (with non-trivial we mean
    # that it can't be 1 or n). A divisor is an integer d such that there's no
    # remainder in the division n/d.
    #
    # Note that if d is a divisor of n then n/d is also a divisor of n because
    # n = d * n/d. From this it follows that either divisor d or n/d is an
    # integers in the interval [2,sqrt(n)]. This is because it can't be the case
    # that both d and n/d are strictly greater than sqrt(n) because this would
    # imply d * n/d is strictly greater than n (and hence not n).
    #
    # Suppose n is a number representable with N bits. The question we want to
    # answer next is: how many bits do we need to use to represent a divisor of
    # n such that if there is a divisor one of those divisors is representable
    # with this number of bits. It turns out CEIL(N/2) bits is sufficient.
    #
    # To see this number of bits is sufficient, recall that we only need to be
    # able to represent up to the largest integer that is smaller or equal to
    # sqrt(n). Also, clearly, with i bits, we can represent numbers up to 2^i-1.
    # Hence it must be that n <= 2^N-1. Now consider that:
    #
    #   sqrt(n) <= sqrt(2^N-1)
    #           <  sqrt(2^N)
    #           <= sqrt((2^(N/2))^2)
    #           <= 2^(N/2) .
    #
    # Assume for the moment that N is even (and hence CEIL(N/2)=N/2).Recall that
    # if a divisor of n exists then one exists that is smaller or equal to
    # sqrt(n) and, because of the inequality above, it is *strictly* smaller
    # 2^(N/2). As 2^(N/2) is an integer and a divisor is guaranteed to be
    # strictly less than this integer, it must be at most 2^(N/2)-1 and hence
    # can be represented with CEIL(N/2)=N/2 bits.
    #
    # For odd N we can't use N/2 bits as N is not divisible by 2. However,
    # CEIL(N/2) for odd N is (N+1)/2 and the following holds
    #
    #   sqrt(n) <  2^(N/2)                   (see above)
    #           <= 2^(N/2) * 2^(1/2) - 1     (only for N>=3)
    #           <= 2^(N/2 + 1/2)-1
    #           <= 2^((N+1)/2)-1 .
    #
    # Again, if a divisor of n exists then one exists that is smaller or equal
    # to sqrt(n) and, hence, strictly smaller than 2^((N+1)/2)-1). As a result,
    # it can be represented with CEIL(N/2)=(N+1)/2 bits.
    #
    # As a side note, note that one of the inequalities above only holds for
    # N>=3. However, we've checked CEIL(N/2) is sufficient for N<3 manually.

    n_bit_length = n.bit_length()
    divisor_bit_length = (n_bit_length // 2) if (n_bit_length % 2) == 0 else (n_bit_length // 2) + 1

    logger("N={}".format(n_bit_length))
    logger("CEIL(N/2)={}".format(divisor_bit_length))

    # Const representing n and a variable for the divisor.
    n_typestr = 'uint%d' % n_bit_length
    divisor_typestr = 'uint%d' % divisor_bit_length

    n_ = mxk.Const(n_typestr, n)
    divisor = mxk.Var(divisor_typestr, 'divisor')

    # Make sure divisor is non-trivial.
    constraints.append(mxk.LogicalNot(
        mxk.Equals(divisor, mxk.Const(divisor_typestr, 0))))
    constraints.append(mxk.LogicalNot(
        mxk.Equals(divisor, mxk.Const(divisor_typestr, 1))))

    # Now all that remains is to formulate constraints on n_ and divisor_ that
    # ensure that if the constraints are met then divisor_ divides n_. This is
    # easier said than done. We basically have to calculate the remainder of
    # the integer division n_ / divisor_ and ensure there is no remainder.
    #
    # We're going to use a shift and subtract division.
    remainder = n_

    # Iterate over bitvector within n that are the same size as the
    # divisor, starting with the most significant such bitvector.
    for r in range(n_bit_length - divisor_bit_length + 1):

        # We're interested in the r-th most significant bitvector that is the
        # same size as the divisor's bit length.
        start = n_bit_length - divisor_bit_length - r
        end = n_bit_length - r

        remainder_part = mxk.Slice(remainder, start, end)

        #print("[{},{}[".format(start, end))

        # Work out what bits to replace remainder_part with.
        remainder_part_new = mxk.IfThenElse(
            # If divisor is less or equal to this remainder_part ...
            mxk.LessThanEquals(divisor, remainder_part),
            # ... then subtract divisor from remainder_part ...
            mxk.Subtract(remainder_part, divisor),
            # ... else leave it 'as is'.
            remainder_part)

        # Update the remainder.
        remainder = mxk.Concatenate(
            mxk.Slice(remainder, 0, start),
            remainder_part_new,
            mxk.Slice(remainder, end, n_bit_length))

    # Ensure the final remainder is 0!
    constr = mxk.Equals(remainder, mxk.Const(n_typestr, 0))
    constraints.append(constr)

    # We're done! We got all the constraints. Let's use a constraint solver
    # to find an assignment to variables under which all constraints hold.
    solver = mxk.TseitinConstraintSolver(logger=None)
    result = solver.solve(constraints)

    # See if the solver was able to find a satisfying assignment.
    if result == mxk.ConstraintSolver.RESULT_SAT:

        # We found a divisor, return it!
        assignment = solver.get_satisfying_assignment()
        divisor_value = assignment(divisor)
        logger("{} divides {}".format(divisor_value, n))
        return divisor_value

    elif result == mxk.ConstraintSolver.RESULT_UNSAT:
        logger("Unable to find a divisor.")
        return None

    elif result == mxk.ConstraintSolver.RESULT_ERROR:
        logger("Something went wrong, sorry.")
        return None

    else:
        raise Exception("Unable to interpret result from solver")

def find_prime_factors(logger, n):

    if n <= 0:
        raise("Unable to factorise {:d}".format(n))
    elif n == 1:
        return {}
    else:
        divisor = find_divisor(logger, n)
        if divisor == None:
            return { n : 1 }
        else:
            mapl = find_prime_factors(logger, divisor)
            mapr = find_prime_factors(logger, n // divisor)

            for n, val in mapr.items():
                if n in mapl.keys():
                    mapl[n] = mapl[n] + val
                else:
                    mapl[n] = val

            return mapl

def run_example(logger):
    """
    This example demonstrates how to factorise a 2048 bit number
    """
    #n = 22580116242535058188623517908541842633310092715854343846499796528769924223671807456607207419106621519588054730245966134358662000861657234814981687546213715297116993744190702405123601421779826894111197445944603613969124042229902202605182127458854328092374858429249966182880779471051954712334390750518196900438794893396809490213228123823764463452353363582030091984618564441824624833291389753934147982215735585974663924374055872463956337167613961791649759852314679564700205664568046040625039008367966025154382490947923562947778613745893443444809542921142924788398447884047063914104247152421812331793595144009461596199479
    n = 10

    find_divisor(logger, n)

if __name__ == '__main__':
    run_example(logger=print)

import unittest


class Test_Factorise(unittest.TestCase):

    def test_find_divisor(self):
        logger = lambda msg: None

        logger = lambda msg: None
        DIVISOR = lambda i: find_divisor(logger, i)

        #self.assertEqual(DIVISOR(1), None)
        #self.assertEqual(DIVISOR(2), None)
        #self.assertEqual(DIVISOR(3), None)
        self.assertIn(DIVISOR(4), [2])

    def test_find_prime_factors(self):

        logger = lambda msg: None
        FACTORS = lambda i: find_prime_factors(logger, i)

        self.assertEqual({}, FACTORS(1))
        self.assertEqual({2:1}, FACTORS(2))
        self.assertEqual({3:1}, FACTORS(3))
        self.assertEqual({2:2}, FACTORS(4))
