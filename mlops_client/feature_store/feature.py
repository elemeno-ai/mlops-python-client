
from mlops_client.feature_store.feature_value_type import FeatureValueType


class Feature:

  def __init__(self, feature_name: str, feature_value_type: FeatureValueType):
    self._feature_name = feature_name
    self._feature_value_type = feature_value_type
  
  @property
  def feature_name(self) -> str:
    return self._feature_name
  
  @property
  def feature_value_type(self) -> FeatureValueType:
    return self._feature_value_type

  def to_dict(self):
    return {
      'feature_name': self._feature_name,
      'feature_value_type': self._feature_value_type
    }