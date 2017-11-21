from __future__ import print_function

import mxklabs as mxk

def run_example(logger):
    """
    This example demonstrates how to use the mxklabs module to solve 
    'Einstein's Riddle' (see https://en.wikipedia.org/wiki/Zebra_Puzzle):
  
        Suppose there are five houses in a row, each painted a different 
        color, their inhabitants are of different national extractions, own 
        different pets, drink different beverages and smoke different brands 
        of American cigarets and:
  
        1.  The Englishman lives in the red house.
        2.  The Spaniard owns the dog.
        3.  Coffee is drunk in the green house.
        4.  The Ukrainian drinks tea.
        5.  The green house is immediately to the right of the ivory house.
        6.  The Old Gold smoker owns snails.
        7.  Kools are smoked in the yellow house.
        8.  Milk is drunk in the middle house.
        9.  The Norwegian lives in the first house.
        10. The man who smokes Chesterfields lives in the house next to the 
            man with the fox.
        11. Kools are smoked in the house next to the house where the horse 
            is kept.
        12. The Lucky Strike smoker drinks orange juice.
        13. The Japanese smokes Parliaments.
        14. The Norwegian lives next to the blue house.

        Now, who drinks water? Who owns the zebra?"
  
    In this example code we'll solve the riddle by encoding the problem using 
    only boolean variables and by placing logical constraints over those 
    variables using only logical AND, OR and NOT expressions.
    """
    # Use a Python dictionary to store variables (mxk.Var objects).
    vars = dict()
    # Use a Python list object to store constraints (mxk.Expr objects).
    constraints = list()

    # Define some lists for house locations, nations, colours, pets, brands
    # of cigarettes and drinks that we'll later on.
    locs = [1, 2, 3, 4, 5]
    nats = ['Englishman', 'Spaniard', 'Ukranian', 'Norwegian', 'Japanese']
    cols = ['red', 'green', 'ivory', 'yellow', 'blue']
    pets = ['dog', 'snail', 'fox', 'horse', 'zebra']
    cigs = ['Old Gold', 'Kools', 'Chesterfields', 'Lucy Strike', 'Parliaments']
    drks = ['coffee', 'tea', 'milk', 'orange juice', 'water']

    # For some definitions it's handy to have all properties other than house
    # locations in one single list.
    all_properties = nats + cols + pets + cigs + drks

    # It's time to think about what variables could be useful to 'encode' the
    # state space of this riddle. Our plan is to treat house location as a
    # special property that basically represents a house and we're going to
    # introduce a Boolean variable for every possible combination of 1) house
    # location and nation 2) house location and colour 3) house location and
    # pet 4) house location and cigarettes and 5) house location and drinks. The
    # idea is that this variable is true if and only if that pairing is correct.
    # Because of this representation it will be useful to define a list of list
    # of properties that excludes house locations.
    property_lists = [nats, cols, pets, cigs, drks]

    # We're now in a position to create our variables. We could create each
    # variables as a separate Python object like this:
    #
    #   house1_England = mxk.Var('bool', 'house1_England')
    #
    # but that would require 125 such definitions. Instead, well loop over the
    # lists we have just defined and put the generated variables in vars.

    # Iterate over each house location.
    for l in locs:
        # Iterate over properties in the property list.
        for a in all_properties:
            # A variable name.
            id = "house{}_{}".format(l, a)
            # Add variable to vars.
            vars[(l, a)] = mxk.Var('bool', id)

    # Print our list of variables.
    #print("Vars:");
    #for value in vars.values():
    #    print(" - {}".format(value))

    # Now we have created the variables that define the 'solution space' of our
    # riddle but we have to be explicit about what constitutes a valid solution.
    # First of all propery (whether it be nation, house colour, pet, branch of
    # cigarette or drink should be associated with at least one house location
    # (or more precisely *exactly one* house locations, but we'll get to that).

    for a in all_properties:
        # Ensure this property holds at at least one location by
        # constraining valid solutions to a logical OR over all locations.
        constraints.append(
            mxk.LogicalOr(
                *[vars[(l, a)] for l in locs]))

    # Now, make sure each property is subscribed to at most one house location
    # by adding a constraint for every property and every pair of distinct
    # locations ensure this property is never associated with both locations
    # at the same time.
    for p in all_properties:
        for l1 in locs:
            for l2 in locs:
                if l1 != l2:
                    # Ensure this property doesn't both hold at location l1 and
                    # l2 at the same time using a logical NOT.
                    constraints.append(
                        mxk.LogicalNot(
                            mxk.LogicalAnd(
                              vars[(l1, p)],
                              vars[(l2, p)])))

    # Now ensure that every house location has at least one nation, colour,
    # pet, cigarette brand and drink associated with it.
    for property_list in property_lists:
        for l in locs:
            # For every property list and location ensure at least one property
            # in the list holds.
            constraints.append(
                mxk.LogicalOr(
                    *[vars[(l, p)] for p in property_list]))

    # The constrains above are sufficient to encode the general rules of the
    # riddle. All that remains is to enforce the 'hints'.
    #
    # Let's start with two easy hints:
    #
    # 8.  Milk is drunk in the middle house.
    #
    # This hint is easy! The vars[(3, 'milk')] variable must be true!
    constraints.append(vars[(3, 'milk')])

    # 9.  The Norwegian lives in the first house.
    #
    # This hint is easy! The vars[(1, 'Norwegian')] variable must be true!
    constraints.append(vars[(1, 'Norwegian')])

    # Upon inspection, quite a few of the hints are of the same format,
    # effectively saying 'the house with property A also has property B. As an
    # example:
    #
    #   1.  The Englishman lives in the red house.
    #
    # Or, in other words, the house location which is associated with
    # 'Englishman' is also associated with 'red'. This means that for all
    # locations, l, the variable A = vars([l,'Englishman']) implies
    # B=vars([l,'red']). A logical implication like this can be encoded using
    # OR and NOT as follows:
    #
    #    (not A) or B
    #
    # We will add a constraint like this for every hint in this format:

    #   1.  The Englishman lives in the red house.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Englishman')]),
                vars[(l, 'red')]))

    # 2.  The Spaniard owns the dog.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Spaniard')]),
                vars[(l, 'dog')]))

    # 3.  Coffee is drunk in the green house.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'coffee')]),
                vars[(l, 'green')]))

    # 4.  The Ukrainian drinks tea.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Ukranian')]),
                vars[(l, 'tea')]))

    # 6.  The Old Gold smoker owns snails.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Old Gold')]),
                vars[(l, 'snail')]))

    # 7.  Kools are smoked in the yellow house.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Kools')]),
                vars[(l, 'yellow')]))

    # 12. The Lucky Strike smoker drinks orange juice.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Lucy Strike')]),
                vars[(l, 'orange juice')]))

    # 13. The Japanese smokes Parliaments.
    for l in locs:
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'Japanese')]),
                vars[(l, 'Parliaments')]))

    # Hint 5. is slightly more difficult:
    #
    # 5.  The green house is immediately to the right of the ivory house.
    #
    # This is again an equivalence but now between variables in adjacent
    # locations. That is, for all l we have A = vars([l,'ivory']) implies
    # B = vars([l + 1,'green']). There is also the implication that the
    # right-most location can't be ivory.
    for l in locs[:-1]:
        # 5.  The green house is immediately to the right of the ivory house.
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l, 'ivory')]),
                vars[(l + 1, 'green')]))

    # The right-most location can't be ivory.
    constraints.append(mxk.LogicalNot(vars[5,'ivory']))

    # 10. The man who smokes Chesterfields lives in the house next to the
    #     man with the fox.
    #
    # This is quite similar to hint 5. except that we're not quite sure which
    # house is left or right, so we need to cover both cases. To accomplish this
    # we again do a logical implication but this time we conside all possible
    # neighbouring locations.
    for l1 in locs:
        neighbouring_locs = [l2 for l2 in locs if abs(l1 - l2) == 1]
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l1, 'Chesterfields')]),
                *[vars[(l2, 'fox')] for l2 in neighbouring_locs]))

    # 11. Kools are smoked in the house next to the house where the horse
    #     is kept.
    for l1 in locs:
        neighbouring_locs = [l2 for l2 in locs if abs(l1 - l2) == 1]
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l1, 'Kools')]),
                *[vars[(l2, 'horse')] for l2 in neighbouring_locs]))

    # 14. The Norwegian lives next to the blue house.
    for l1 in locs:
        neighbouring_locs = [l2 for l2 in locs if abs(l1 - l2) == 1]
        constraints.append(
            mxk.LogicalOr(
                mxk.LogicalNot(vars[(l1, 'Norwegian')]),
                *[vars[(l2, 'blue')] for l2 in neighbouring_locs]))

    # We're done! We got all the constraints. Let's use a constraint solver
    # to find an assignment to variables under which all constraints hold.
    solver = mxk.TseitinConstraintSolver(logger=None)
    result = solver.solve(constraints)

    # See if the solver was able to find a satisfying assignment.
    if result == mxk.ConstraintSolver.RESULT_SAT:

        # Get the assignment of values to variables.
        assignment = solver.get_satisfying_assignment()

        # To answer 'who drinks the water?' we first lookup the house location
        # at which water is drunk and then the nationality associated with
        # that house location.
        l_water = next(l for l in locs if assignment(vars[(l, 'water')]))
        n_water = next(n for n in nats if assignment(vars[(l_water, n)]))

        # To answer 'who owns the zebra?' we first look up the house location
        # at which the zebra is kept and then the nationality associated with
        # that house location.
        l_zebra = next(l for l in locs if assignment(vars[(l, 'zebra')]))
        n_zebra = next(n for n in nats if assignment(vars[(l_zebra, n)]))

        logger("Solution: {n_water} drinks the water, {n_zebra} owns the "
               "zebra!".format(n_water=n_water, n_zebra=n_zebra))

    elif result == mxk.ConstraintSolver.RESULT_UNSAT:
      logger("Unable to find a solution, sorry.")
    elif result == mxk.ConstraintSolver.RESULT_ERROR:
      logger("Something went wrong, sorry.")
    else:
      raise Exception("Unable to interpret result from solver")

if __name__ == '__main__':
    run_example(logger=print)

import unittest

class Test_EinsteinsRiddle(unittest.TestCase):

    def test_example_solve_einsteins_riddle(self):

        logs = []
        logger = lambda msg : logs.append(msg)

        run_example(logger=logger)

        self.assertEqual(['Solution: Norwegian drinks the water, Japanese owns '
                          'the zebra!'], logs)