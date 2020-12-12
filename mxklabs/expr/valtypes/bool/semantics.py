class Bool:

  def __init__(self, ctx):
    self.ctx = ctx

  def is_valid_value(self, val_type_instance, value):
    return val_type_instance == True or val_type_instance == False

  def assert_valid_value(self, val_type_instance, value):
    if not self.is_valid_value(val_type_instance, value):
      raise RuntimeError(f"invalid value for type '{val_type_instance}' (got {value})")

  def is_valid_user_value(self, val_type_instance, user_value):
    if type(user_value) == int:
      return user_value == 0 or user_value == 1
    if type(user_value) == bool:
      return True

  def assert_valid_user_value(self, val_type_instance, user_value):
    if not self.is_valid_value(val_type_instance, user_value):
      raise RuntimeError(f"invalid value for type '{val_type_instance}' (got {user_value}, expecting False, True, 0 or 1)")

  def values(self, val_type_instance):
    yield False
    yield True

  def num_values(self, val_type_instance):
    return 2

  def value_to_str(self, val_type_instance, value):
    return 'False' if not value else 'True'

  def user_value_to_str(self, val_type_instance, user_value):
    return self.value_to_str(val_type_instance,
      self.user_value_to_value(val_type_instance, user_value))

  def value_to_user_value(self, val_type_instance, value):
    return value

  def user_value_to_value(self, val_type_instance, user_value):
    if user_value:
      return True
    else:
      return False