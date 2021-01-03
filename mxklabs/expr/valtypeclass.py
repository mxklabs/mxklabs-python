from .module import Module

class CnfMappingWrapper:

  def __init__(self, cnf_mapping_class, valtype_attrs):
    self._cnf_mapping_class = cnf_mapping_class
    self._valtype_attrs = valtype_attrs

  def __call__(self, ctx):
    return self._cnf_mapping_class(ctx, **self._valtype_attrs)

class ValtypeClass(Module):

  def __init__(self, ctx, identifier, module):
    Module.__init__(self, ctx, identifier, module)
    self.attrs = module.definition['attrs']

  def get_cnf_mapping_class(self, **valtype_attrs):
    return CnfMappingWrapper(self.get_class(self.module.definition['cnfMapping']), valtype_attrs)

