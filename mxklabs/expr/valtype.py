import functools

class ValType:

  def __init__(self, ctx, val_type_class, **attrs):
    self.ctx = ctx
    self.val_type_class = val_type_class
    self.attrs = attrs
    self._hash = None

    for act_attr in attrs:
      if act_attr not in val_type_class.attrs:
        raise RuntimeError(f"{val_type_class.id}' does not expect attribute '{act_attr}'")
    for exp_attr in val_type_class.attrs:
      if exp_attr not in attrs:
        raise RuntimeError(f"'{val_type_class.id}' expects attribute '{exp_attr}'")

  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self.val_type_class)
    hash_items += self.attrs.keys()
    hash_items += self.attrs.values()
    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  def __str__(self):
    result = f'{self.val_type_class.id}'
    if len(self.attrs) > 0:
      result += '{'
      result += ','.join([f'{k}:{v}' for k, v in self.attrs])
      result += '}'
    return result

  def __eq__(self, rhs):
    return self.val_type_class == rhs.val_type_class and \
           self.attrs == rhs.attrs