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
    divisor_ = mxk.Var(divisor_typestr, 'd')

    # Make sure divisor is non-trivial.
    constraints.append(mxk.LogicalNot(
        mxk.Equals(n_, mxk.Const(divisor_typestr, 0))))
    constraints.append(mxk.LogicalNot(
        mxk.Equals(n_, mxk.Const(divisor_typestr, 1))))

    # Now all that remains is to formulate constraints on n_ and divisor_ that
    # ensure that if the constraints are met then divisor_ divides n_. This is
    # easier said than done. We basically have to calculate the remainder of
    # the integer division n_ / divisor_ and ensure there is no remainder.
    #
    # We're going to use a shift and subtract division.
    rng = n_bit_length - divisor_bit_length
    remainder_ = n_

    for r in range(rng+1):
        remainder_part_start = rng - r
        remainder_part_end = remainder_part_start + divisor_bit_length

        print("[{},{}[".format(remainder_part_start, remainder_part_end))

        remainder_part_ =  mxk.Extract(remainder_,
                           mxk.Const('int', remainder_part_start),
                           mxk.Const('int', remainder_part_end))

        # See if subtraction is possible.
        can_subtract_ = mxk.LessThanEquals(divisor_, remainder_part_)

        # Work out what n_part_ looks like after subtraction.
        remainder_part_new_ = mxk.IfThenElse(can_subtract_,
                                             mxk.Subtract(remainder_part_,
                                                          divisor_),
                                             remainder_part_)

        # Update n_ with the revised n_part_new_.
        remainder_ = mxk.Insert(remainder_,
                                remainder_part_new_,
                                mxk.Const('int', remainder_part_start),
                                mxk.Const('int', remainder_part_end))

    # Ensure the remainder is 0!
    constraints.append(mxk.Equals(remainder_, mxk.Const(divisor_typestr, 0)))

    # TODO(mkkt): Extract, Insert, LessThanEquals, Equals, IfThenElse, Subtract.


    # We're done! We got all the constraints. Let's use a constraint solver
    # to find an assignment to variables under which all constraints hold.
    solver = mxk.TseitinConstraintSolver(logger=None)
    result = solver.solve(constraints)

    # See if the solver was able to find a satisfying assignment.
    if result == mxk.ConstraintSolver.RESULT_SAT:

        # We found a divisor, return it!
        assignment = solver.get_satisfying_assignment()
        return assignment(divisor_)

    elif result == mxk.ConstraintSolver.RESULT_UNSAT:
        logger("Unable to find a divisor.")
        return None

    elif result == mxk.ConstraintSolver.RESULT_ERROR:
        logger("Something went wrong, sorry.")
        return None

    else:
        raise Exception("Unable to interpret result from solver")


def run_example(logger):
    """
    This example demonstrates how to factorise a 2048 bit number
    """
    #n = 22580116242535058188623517908541842633310092715854343846499796528769924223671807456607207419106621519588054730245966134358662000861657234814981687546213715297116993744190702405123601421779826894111197445944603613969124042229902202605182127458854328092374858429249966182880779471051954712334390750518196900438794893396809490213228123823764463452353363582030091984618564441824624833291389753934147982215735585974663924374055872463956337167613961791649759852314679564700205664568046040625039008367966025154382490947923562947778613745893443444809542921142924788398447884047063914104247152421812331793595144009461596199479
    n = 1234

    find_divisor(logger, n)

if __name__ == '__main__':
    run_example(logger=print)

import unittest


class Test_EinsteinsRiddle(unittest.TestCase):
    def test_example_solve_einsteins_riddle(self):
        logs = []
        logger = lambda msg: logs.append(msg)

        run_example(logger=logger)

        self.assertEqual(['Solution: Norwegian drinks the water, Japanese owns '
                          'the zebra!'], logs)