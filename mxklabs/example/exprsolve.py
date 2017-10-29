import mxklabs.expr as e
import mxklabs.solve as s

if __name__ == '__main__':
  
  x = e.Variable(type=e.Bool(), id='x')  
  y = e.Variable(type=e.Bool(), id='y')
  
  x_or_y = e.LogicalOr(x, y)
  not_x = e.LogicalNot(x)

  solver = s.Solver()
  
  solver.solve([x_or_y, not_x])