
from datasource.datasource_client import Datasource
from feature_store.featuretable_client import FeatureTable
from inference_server.inferenceserver_client import InferenceServer
from model.headers import Headers
from model.missing_field import MissingFieldError


class MLOpsClient:
  """
  MLOpsClient

  A client for the Elemeno MLOps REST API.

  Usage:
    client = MLOpsClient().with_api_key(api_key).with_api_secret(api_secret).build()
    client.datasource.create(datasource)
    client.datasource.remove(datasource_id)
    client.datasource.list()
    client.featuretable.create_mapping(featuretable)
    client.inferenceserver.create_rest(inferenceserver)
    client.inferenceserver.list()
  """

  def with_api_key(self, api_key: str) -> 'MLOpsClient':
    self._api_key = api_key
    return self
  
  def with_api_secret(self, api_secret: str) -> 'MLOpsClient':
    self._api_secret = api_secret
    return self

  def use_staging(self) -> 'MLOpsClient':
    self._use_staging = True
    self._host = 'http://localhost:8080'
    return self

  @property
  def host(self) -> str:
    if not hasattr(self, '_use_staging') or not self._use_staging:
      self._host = 'https://c3p0.elemeno.ai'
    return self._host
  
  @property
  def datasource(self) -> Datasource:
    if not hasattr(self, '_datasource'):
      raise ClientNotBuiltError()
    return self._datasource
  
  @property
  def featuretable(self) -> FeatureTable:
    if not hasattr(self, '_featuretable'):
      raise ClientNotBuiltError()
    return self._featuretable

  @property
  def inferenceserver(self) -> InferenceServer:
    if not hasattr(self, '_inferenceserver'):
      raise ClientNotBuiltError()
    return self._inferenceserver

  def build(self) -> 'MLOpsClient':
    if not hasattr(self,'_api_key'):
      raise MissingFieldError('api_key')
    if not hasattr(self, '_api_secret'):
      raise MissingFieldError('api_secret')
    headers = Headers(). \
      with_api_key(self._api_key). \
      with_api_secret(self._api_secret). \
      build()
    
    self._datasource = Datasource(headers, self.host)
    headersft = Headers(). \
      from_dict_with_header(headers, 'Content-Type', 'application/json'). \
      build()
    self._featuretable = FeatureTable(headersft, self.host)

    self._inferenceserver = InferenceServer(headers, self.host)
    return self
class ClientNotBuiltError(ValueError):
  
  def __str__(self):
    return "Not able to use the client yet. First call the build() method."