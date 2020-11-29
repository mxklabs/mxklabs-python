class ValType:

  def __init__(self, ctx, id, short_name, module):
    self.ctx = ctx
    self.id = id
    self.short_name = short_name
    self._module = module
    self.id = id