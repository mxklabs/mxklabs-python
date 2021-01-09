class ExprContextNamespace:

  def __init__(self, namespaceid):
    self._namespaceid = namespaceid
    self._callable = None

  def _set_callable(self, callable):
    self._callable = callable

  def _set_attr(self, attribute_name, obj):
    setattr(self, attribute_name, obj)

  def __call__(self, **kwargs):
    if self._callable is None:
      raise RuntimeError(f"'{self._namespaceid}' is not callable'")
    else:
      return self._callable(**kwargs)