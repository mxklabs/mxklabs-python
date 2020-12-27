class Bool:

  def __init__(self, ctx):
    self.ctx = ctx

  def is_valid_value(self, valtype_instance, value):
    return valtype_instance == True or valtype_instance == False

  def assert_valid_value(self, valtype_instance, value):
    if not self.is_valid_value(valtype_instance, value):
      raise RuntimeError(f"invalid value for type '{valtype_instance}' (got {value})")

  def is_valid_user_value(self, valtype_instance, user_value):
    if type(user_value) == int:
      return user_value == 0 or user_value == 1
    if type(user_value) == bool:
      return True

  def assert_valid_user_value(self, valtype_instance, user_value):
    if not self.is_valid_value(valtype_instance, user_value):
      raise RuntimeError(f"invalid value for type '{valtype_instance}' (got {user_value}, expecting False, True, 0 or 1)")

  def values(self, valtype_instance):
    yield False
    yield True

  def num_values(self, valtype_instance):
    return 2

  def value_to_str(self, valtype_instance, value):
    return 'False' if not value else 'True'

  def user_value_to_str(self, valtype_instance, user_value):
    return self.value_to_str(valtype_instance,
      self.user_value_to_value(valtype_instance, user_value))

  def value_to_user_value(self, valtype_instance, value):
    return value

  def user_value_to_value(self, valtype_instance, user_value):
    if user_value:
      return True
    else:
      return False