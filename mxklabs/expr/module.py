class Module:

  def __init__(self, ctx, id, module):
    self.ctx = ctx
    self.id = id
    self.short_name = module.definition['shortName']
    self.module = module
