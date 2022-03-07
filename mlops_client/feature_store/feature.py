
from model.missing_field import MissingFieldError
from mlops_client.feature_store.feature_value_type import FeatureValueType


class Feature:
  """
  Builds a Feature object.

  Object building functions:
    - with_feature_name: The name of the feature.
    - with_feature_value_type: The type of the feature value.
    - build: Returns a complete instance of the object.

  Returns:
    A Feature object.
  """
  
  @property
  def feature_name(self) -> str:
    return self._feature_name
  
  @property
  def feature_value_type(self) -> FeatureValueType:
    return self._feature_value_type

  def with_feature_name(self, feature_name: str) -> 'Feature':
    self._feature_name = feature_name
    return self
  
  def with_feature_value_type(self, feature_value_type: FeatureValueType) -> 'Feature':
    self._feature_value_type = feature_value_type
    return self
  
  def build(self) -> 'Feature':
    if not hasattr(self, '_feature_name'):
      raise MissingFieldError('feature_name')
    if not hasattr(self, '_feature_value_type'):
      raise MissingFieldError('feature_value_type')
    return self

  def to_dict(self):
    return {
      'feature_name': self._feature_name,
      'feature_value_type': self._feature_value_type
    }