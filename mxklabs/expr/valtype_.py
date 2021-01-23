import functools

class Valtype:

  def __init__(self, ctx, valtype_def, sub_valtypes, attrs):
    self._ctx = ctx
    self._valtype_def = valtype_def
    self._sub_valtypes = sub_valtypes
    self._attrs = attrs
    self._hash = None

  def ctx(self):
    return self._ctx

  def valtype_def(self):
    return self._valtype_def

  def sub_valtypes(self):
    return self._sub_valtypes

  def attrs(self):
    return self._attrs

  def values(self):
    return self._valtype_def.values(self)

  def __hash__(self):
    if self._hash is not None:
      return self._hash

    hash_items = []
    hash_items.append(self._ctx)
    hash_items.append(self._valtype_def)
    hash_items.append(self._sub_valtypes)
    hash_items += self._attrs.keys()
    hash_items += self._attrs.values()

    _hash = hash(tuple(hash_items))
    self._hash = _hash
    return _hash

  def __str__(self):
    result = f'{self._valtype_def.baseid()}'

    items = [v.__str__() for v in self._sub_valtypes]
    items += [f'{k}={v}' for k, v in self._attrs.items()]
    if len(items) > 0:
      result += '('
      result += ','.join(items)
      result += ')'
    return result

  def __repr__(self):
    return self.__str__()

  def __eq__(self, rhs):
    if not isinstance(rhs, Valtype):
      return False
    return self._ctx == rhs._ctx and \
           self._valtype_def == rhs._valtype_def and \
           self._sub_valtypes == rhs._sub_valtypes and \
           self._attrs == rhs._attrs
