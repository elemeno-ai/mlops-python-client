
from mlops_client.feature_store.feature_value_type import InvalidFeatureValueTypeError
from mlops_client.inference_server.feature_source_type import FeatureSourceType
from mlops_client.model.missing_field import MissingFieldError

class FeatureSource:
  """
  FeatureSource

  Object building functions:
    - with_source_type: The type of the feature source.
    - with_feature_table_id: The id of the feature table.
    - with_feature_name: The name of the feature.
    - with_body_json_path: The path to the feature in the request body.
    - build: Returns a complete instance of the object.

  Raises:
    - MissingFieldError: If a required field is not provided.
    - InvalidFeatureValueTypeError: If the provided source type is invalid.

  Returns:
   - A feature source.
  """

  @property
  def source_type(self):
    return self._source_type
  
  @property
  def feature_table_id(self):
    return self._feature_table_id
  
  @property
  def feature_name(self):
    return self._feature_name
  
  @property
  def body_json_path(self):
    return self._body_json_path

  def with_source_type(self, source_type: FeatureSourceType) -> 'FeatureSource':
    self._source_type = source_type
    return self
  
  def with_feature_name(self, feature_name: str) -> 'FeatureSource':
    self._feature_name = feature_name
    return self
  
  def with_body_json_path(self, body_json_path: str) -> 'FeatureSource':
    self._body_json_path = body_json_path
    return self
  
  def with_feature_table_id(self, feature_table_id: str) -> 'FeatureSource':
    self._feature_table_id = feature_table_id
    return self
  
  def build(self) -> 'FeatureSource':
    if not hasattr(self, f"_source_type"):
      raise MissingFieldError("source_type")
    required = []
    if self._source_type == FeatureSourceType.FEATURE_TABLE:
      required.extend(['feature_table_id', 'feature_name'])
    elif self._source_type == FeatureSourceType.REQUEST_BODY_KEY:
      required.append('body_json_path')
    else:
      raise InvalidFeatureValueTypeError(self._source_type)
    for r in required:
      if not hasattr(self, f"_{r}"):
        raise MissingFieldError(r)
    return self
    