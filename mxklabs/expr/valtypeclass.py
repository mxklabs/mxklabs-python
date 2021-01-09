from .module import Module

class ValtypeClass(Module):

  def __init__(self, ctx, identifier, module):
    Module.__init__(self, ctx, identifier, module)
    self.attrs = module.definition['attrs']

  

