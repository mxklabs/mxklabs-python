import sys
import string
import unittest

import six

class Dimacs(object):
  
  def __init__(self, clauses):
    self.clauses = clauses
    self.num_clauses = len(self.clauses)
    self.num_vars = max([0] + [max([0] + [abs(l) for l in c]) for c in self.clauses])

class DimacsParser(object):

  def __init__(self, filename=None, file=None, string=None):
    self.in_filename = filename
    self.in_file = file
    self.in_string = string
    self.line_no = None
    self.num_vars = 0
    self.num_clauses = 0
    self.problem_statement_line = 0
    self.problem_statement_num_vars_column = 0
    self.problem_statement_num_clauses_column = 0
    self.seen_clause = False
    self.seen_problem_statement = False
    self.clauses = []
    self.max_var = 0
    self._parse()
 
  def get_num_vars(self):
    return self.num_vars

  def get_num_clauses(self):
    return len(self.clauses)

  def get_clauses(self):
    return self.clauses
  
  def _process_problem_statement(self, num_vars, num_clauses):
    self.num_vars = num_vars
    self.num_clauses = num_clauses
    self.seen_problem_statement = True

  def _process_start_of_clause(self):
    self.clauses.append([])

  def _process_clause_literal(self, literal):
    self.clauses[-1].append(literal)
    abs_literal = abs(literal)
    if abs_literal > self.max_var:
      self.max_var = abs_literal

  def _process_end_of_clause(self ):
    pass

  def _parse(self):
    self.line_no = 1

    if self.in_filename is not None:
      file = open(self.in_filename, 'r')
      for line in file:
        self._process_line(line)
      file.close()
    if self.in_file is not None:
      for line in self.in_file:
        self._process_line(line)
    if self.in_string is not None:
      for line in self.in_string.split('\n'):
        self._process_line(line)

    #max_var = max([max([abs(l) for l in c]) for c in self.clauses])
    
    if self.num_vars < self.max_var:
      self._process_error_with_location("the declared number of variables (%d) is smaller than the actual number of variables (%d)" % (
        self.num_vars,
        self.max_var),
        self.problem_statement_line,
        self.problem_statement_num_vars_column)

    if self.num_clauses != len(self.clauses):
      self._process_error_with_location("the declared number of clauses (%d) does not match the actual number of clauses (%d)" % (
        self.num_clauses,
        len(self.clauses)),
        self.problem_statement_line,
        self.problem_statement_num_clauses_column)

    if not self.seen_problem_statement:
      self._process_error("missing problem statement")

  def _process_line(self, line):
    if len(line) > 0:
      if line[0] == 'c':
        pass
      elif not self.seen_problem_statement and line[0] == 'p':
        #tokens = line.split()
        line_frags = self._split_string(line)
        if len(line_frags) != 4:
           self._raise_syntax_error(self.line_no, 1)
        elif line_frags[0][0] != 'p':
           self._raise_syntax_error(self.line_no, line_frags[0][1][0]+1)
        elif line_frags[1][0] != 'cnf':
           self._raise_syntax_error(self.line_no, line_frags[1][1][0]+1)
        else:
          self.problem_statement_line = self.line_no
          self.problem_statement_num_vars_column = line_frags[2][1][0]+1
          self.problem_statement_num_clauses_column = line_frags[3][1][0]+1
          try:
            num_vars = int(line_frags[2][0])
            try:
              num_clauses = int(line_frags[3][0])
              self._process_problem_statement(num_vars, num_clauses)
            except ValueError:
              self._raise_syntax_error(self.line_no, line_frags[3][1][0]+1)
          except ValueError:
            self._raise_syntax_error(self.line_no, line_frags[2][1][0]+1)
      elif self.seen_problem_statement:
        line_frags = self._split_string(line)
        for token, (col_start, _) in line_frags:
          try:
            literal = int(token)
            if literal == 0:
              if self.seen_clause:
                self._process_end_of_clause()
                self.seen_clause = False
            else: # literal != 0
              if not self.seen_clause:
                self._process_start_of_clause()
                self.seen_clause = True
              self._process_clause_literal(literal)
          except ValueError:
            self._raise_syntax_error(self.line_no, col_start+1)
      else:
        self._process_error_with_location("expected a problem statement or comment on this line", self.line_no, 1)
    self.line_no += 1
 
  def _process_error(self, error_msg):
    raise Exception("error: %s" % error_msg)

  def _process_error_with_location(self, msg, line, col):
    self._process_error("%s (line %d, column %d)" % (msg, line, col))
 
  def _raise_syntax_error(self, line, col):
    self._process_error_with_location("invalid syntax", line, col)

  ''' Tokenise tokens in a string as seperated by whitespace. Return 
      list of tuples of words and the column that word starts. '''
  @staticmethod
  def _split_string(s):
    result = []
    was_in_token = False
    token_start = None
    for i in six.moves.range(len(s)):
      is_in_token = s[i] not in string.whitespace
      if not was_in_token and is_in_token:
        token_start = i
      elif was_in_token and not is_in_token:
        result.append((s[token_start:i], (token_start,i)))
      was_in_token = is_in_token
    if was_in_token:
      result.append((s[token_start], (token_start,len(s))))
    return result

def read(filename=None, file=None, string=None):
  dimacs_parser = DimacsParser(filename=filename, file=file, string=string)
  return Dimacs(clauses=dimacs_parser.clauses)
