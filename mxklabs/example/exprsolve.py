from __future__ import print_function

import mxklabs as mxk

if __name__ == '__main__':
  
  x_ = mxk.Variable(type=mxk.Bool(), id='x')  
  y_ = mxk.Variable(type=mxk.Bool(), id='y')
  
  x_or_y_ = mxk.LogicalOr(x_, y_)
  not_x_ = mxk.LogicalNot(x_)

  solver = mxk.TseitinConstraintSolver()

  result = solver.solve([x_or_y_, not_x_])
  
  if result == mxk.ConstraintSolver.RESULT_SAT:
    print("SAT")
    print("")
    print("Satisfying assignment:")
    
    assignment = solver.get_satisfying_assignment()
    
    print("  {expr} -> {value}".format(expr=x_, value=assignment(x_)))
    print("  {expr} -> {value}".format(expr=y_, value=assignment(y_)))
    
  elif result == mxk.ConstraintSolver.RESULT_UNSAT:
    print("UNSAT")
  elif result == mxk.ConstraintSolver.RESULT_ERROR:
    print("ERROR")
  else:
    raise Exception("Unable to interpret result from solver")