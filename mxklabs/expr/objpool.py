class ObjPool:

  def __init__(self):
    self._pool = {}

  def contains(self, obj):
    return obj in self._pool

  def values(self):
    return self._pool.values()

  def make_unique(self, obj):
    if obj in self._pool:
      return self._pool[obj]
    else:
      self._pool[obj] = obj
      return obj

  def clear(self):
    self._pool = {}

