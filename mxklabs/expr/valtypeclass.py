from .module import Module

class ValTypeClass(Module):

  def __init__(self, ctx, id, module):
    Module.__init__(self, ctx, id, module)
    self.attrs = module.definition['attrs']

