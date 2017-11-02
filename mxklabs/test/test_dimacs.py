import unittest

import mxklabs as mxk

class Test_DimacsParser(unittest.TestCase):

  ''' Check a good instance parses without problems. '''
  def test_dimacs_pos1(self):
    string = \
      "c  simple_v3_c2.cnf\n" + \
      "p cnf 3 2\n" + \
      "1 -3 0\n" + \
      "2 3 -1 0\n" 
    sat = mxk.DimacsParser(string=string)
    self.assertEqual(3, sat.get_num_vars())
    self.assertEqual(2, sat.get_num_clauses())
    self.assertEqual([[1,-3],[2,3,-1]], sat.get_clauses())

  ''' Invalid first token. '''
  def test_dimacs_invalid_problem_statement_1(self):
    string = "pt cnf 3 1\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 1, column 1)", str(c.exception))
  
  ''' Invalid second token. '''
  def test_dimacs_invalid_problem_statement_2(self):
    string = "p dnf 3 1\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 1, column 3)", str(c.exception))
  
  ''' Letter instead of num_vars. '''
  def test_dimacs_invalid_problem_statement_3(self):
    string = "p cnf a 1\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 1, column 7)", str(c.exception))
   
  ''' Letter instead of num_clauses. '''
  def test_dimacs_invalid_problem_statement_4(self):
    string = "p cnf 3 a\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 1, column 9)", str(c.exception))
  
  ''' Too many tokens. '''
  def test_dimacs_invalid_problem_statement_5(self):
    string = "p cnf 3 1 4\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 1, column 1)", str(c.exception))
  
  ''' Using letters. '''
  def test_dimacs_invalid_syntax_3(self):
    string = "p cnf 3 1\n2 a -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 2, column 3)", str(c.exception))

  ''' Num clauses mismatch. '''
  def test_dimacs_invalid_num_clauses(self):
    string = "p cnf 3 7\n2 3 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: the declared number of clauses (7) does not match the actual number of clauses (1) (line 1, column 9)", str(c.exception))

  ''' Invalid variable number. '''
  def test_dimacs_invalid_variable_num(self):
    string = "p cnf 3 2\n2 4 -1 0\n2 5 -8 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: the declared number of variables (3) is smaller than the actual number of variables (8) (line 1, column 7)", str(c.exception))

  ''' Clause before problem statement. '''
  def test_dimacs_clause_before_problem_statement(self):
    string = "c comment\n2 -1 0\np cnf 1 2\n1 -2 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: expected a problem statement or comment on this line (line 2, column 1)", str(c.exception))

  ''' Too many problem statements. '''
  def test_dimacs_too_many_problem_statements(self):
    string = "p cnf 3 2\np cnf 3 2\n2 4 -1 0\n2 5 -1 0\n"
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: invalid syntax (line 2, column 1)", str(c.exception))

  ''' Empty. '''
  def test_dimacs_missing_problem_statement(self):
    string = ""
    
    with self.assertRaises(Exception) as c:
      sat = mxk.DimacsParser(string=string)
    self.assertEqual("error: missing problem statement", str(c.exception))

  ''' From web site. '''
  def test_dimacs_website_instance(self):
    string = \
      "c This is an example Boolean Satisfiability instance with 3 variables ('1', '2' and '3') consisting of a\n" + \
      "c logical AND of 4 clauses ('1 OR NOT 2', '2 OR NOT 1', '1 OR 3' and '1 OR NOT 3'). A line starting with 'c'\n" + \
      "c indicates a comment line whereas the line starting with 'p' declares the size of the Boolean Satisifiability\n" + \
      "c problem by stating number of variables (3) and clauses (4) involved. The remaining lines each specify a\n" + \
      "c clause (terminated with a '0' character).\n" + \
      "p cnf 3 4\n" + \
      "1 -2 0\n" + \
      "2 -1 0\n" + \
      "1 3 0\n" + \
      "1 -3 0\n"

    sat = mxk.DimacsParser(string=string)

    self.assertEqual(3, sat.get_num_vars())
    self.assertEqual(4, sat.get_num_clauses())
    self.assertEqual([[1,-2],[2, -1],[1, 3],[1,-3]], sat.get_clauses())

