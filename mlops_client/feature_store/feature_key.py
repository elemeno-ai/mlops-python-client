from mlops_client.feature_store.feature_value_type import FeatureValueType

class FeatureKey:

  def __init__(self, key_name: str, key_value_type: FeatureValueType):
    self._key_name = key_name
    self._key_value_type = key_value_type

  @property
  def key_name(self) -> str:
    return self._key_name
  
  @property
  def key_value_type(self) -> FeatureValueType:
    return self._key_value_type

  @key_name.setter
  def key_name(self, key_name):
    self._key_name = key_name

  @key_value_type.setter
  def key_value_type(self, key_value_type):
    self._key_value_type = key_value_type

  def to_dict(self):
    return {
      'key_name': self._key_name,
      'key_value_type': self._key_value_type
    }