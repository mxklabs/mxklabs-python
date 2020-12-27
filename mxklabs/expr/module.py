class Module:

  def __init__(self, ctx, identifier, module):
    self.ctx = ctx
    self.identifier = identifier
    self.short_name = module.definition['shortName']
    self.module = module
