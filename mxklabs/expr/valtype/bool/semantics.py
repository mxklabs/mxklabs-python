class ValtypeSemantics:

  def __init__(self, ctx):
    self.ctx = ctx

  def is_valid_value(self, valtype, value):
    if type(value) == int:
      return value == 0 or value == 1
    if type(value) == bool:
      return True

  def values(self, valtype):
    yield False
    yield True

  def num_values(self, valtype):
    return 2

  def value_to_str(self, valtype, value):
    return 'False' if not value else 'True'
