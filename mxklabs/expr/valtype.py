import functools

class Valtype:

  def __init__(self, ctx, valtype_class, **attrs):
    self.ctx = ctx
    self.valtype_class = valtype_class
    self.attrs = attrs
    self._hash = None

    for act_attr in attrs:
      if act_attr not in valtype_class.attrs:
        raise RuntimeError(f"{valtype_class.identifier}' does not expect attribute '{act_attr}'")
    for exp_attr in valtype_class.attrs:
      if exp_attr not in attrs:
        raise RuntimeError(f"'{valtype_class.identifier}' expects attribute '{exp_attr}'")

  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self.valtype_class)
    hash_items += self.attrs.keys()
    hash_items += self.attrs.values()
    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  def __str__(self):
    result = f'{self.valtype_class.identifier}'
    if len(self.attrs) > 0:
      result += '{'
      result += ','.join([f'{k}:{v}' for k, v in self.attrs])
      result += '}'
    return result

  def __eq__(self, rhs):
    return self.valtype_class == rhs.valtype_class and \
           self.attrs == rhs.attrs