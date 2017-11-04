import mxklabs as mxk

if __name__ == '__main__':
  
  x_ = mxk.Variable(type=mxk.Bool(), id='x')  
  y_ = mxk.Variable(type=mxk.Bool(), id='y')
  
  x_or_y_ = mxk.LogicalOr(x_, y_)
  not_x_ = mxk.LogicalNot(x_)

  solver = mxk.CryptoSatSolver()

  result = solver.sat([x_or_y_, not_x_])
  
  if result == mxk.Solver.RESULT_SAT:
    print("SAT")
    print("")
    print("Satisfying assignment:")
    for expr, value in solver.get_satisfying_assignment().items():
      print("  {expr} -> {value}".format(expr=expr, value=value))
    
  elif result == mxk.Solver.RESULT_UNSAT:
    print("UNSAT")
  elif result == mxk.Solver.RESULT_ERROR:
    print("ERROR")
  else:
    raise Exception("Unable to interpret result from solver")