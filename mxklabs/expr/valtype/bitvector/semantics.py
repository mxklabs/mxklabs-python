class ValtypeSemantics:

  def __init__(self, ctx):
    self.ctx = ctx

  def is_valid_value(self, valtype, value):
    if type(value) == int:
      return value >= 0 and value < 2**valtype.width
    else:
      return False

  def values(self, valtype):
    return range(2**valtype.width)

  def num_values(self, valtype):
    return 2**valtype.width

  def value_to_str(self, valtype, value):
    return f'{value:d}'