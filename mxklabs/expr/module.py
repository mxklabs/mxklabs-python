class Module:

  def __init__(self, ctx, identifier, module):
    self.ctx = ctx
    self.identifier = identifier
    self.short_name = module.definition['shortName']
    self.module = module

  def get_class(self, name):
    symbol = self.module
    for attr in name.split('.'):
      if not hasattr(symbol, attr):
        raise RuntimeError(f"class '{self.identifier}.{name}' not found")
      else:
        symbol = getattr(symbol, attr)
    return symbol

  def load_class(self, name, **kwargs):
    symbol = self.get_class(name)
    return symbol(**kwargs)