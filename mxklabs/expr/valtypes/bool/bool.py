from ..valtype import ValType

class Bool(ValType):

  def __init__(self):
    ValType.__init__(self, ident='bool')

  def value_to_str(self, value):
    if value:
      return '0'
    else:
      return '1'

  def values(self):
    yield False
    yield True
