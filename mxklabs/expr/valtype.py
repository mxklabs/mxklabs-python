class ValType:

  def __init__(self, ctx, ident, short_name, module):
    self.ctx = ctx
    self.ident = ident
    self.short_name = short_name
    self._module = module
    self.ident = ident