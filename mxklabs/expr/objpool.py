class ObjPool:

  def __init__(self):
    self._pool = {}

  def make_unique(self, obj):
    if obj in self._pool:
      return self._pool[obj]
    else:
      self._pool[obj] = obj
      return obj

