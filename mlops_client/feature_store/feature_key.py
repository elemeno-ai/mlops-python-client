from mlops_client.feature_store.feature_value_type import FeatureValueType
from mlops_client.model.missing_field import MissingFieldError
class FeatureKey:
  """
    This class is used to build a feature key.

    Object building functions:
      - with_key_name (str): The name of the feature key.
      - with_key_value_type (FeatureValueType): The type of the feature key.
      - build: Returns a complete instance of the object.

    Returns:
      FeatureKey: A feature key.
    """
    
  @property
  def key_name(self) -> str:
    return self._key_name
  
  @property
  def key_value_type(self) -> FeatureValueType:
    return self._key_value_type

  def with_key_name(self, key_name: str) -> 'FeatureKey':
    self._key_name = key_name
    return self

  def with_key_value_type(self, key_value_type: FeatureValueType) -> 'FeatureKey':
    self._key_value_type = key_value_type
    return self

  def build(self) -> 'FeatureKey':
    if not hasattr(self, '_key_name'):
      raise MissingFieldError('key_name')
    if not hasattr(self, '_key_value_type'):
      raise MissingFieldError('key_value_type')
    return self
      

  def to_dict(self):
    return {
      'key_name': self._key_name,
      'key_value_type': self._key_value_type
    }