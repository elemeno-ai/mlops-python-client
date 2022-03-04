
from sqlalchemy import desc

from mlops_client.model.missing_field import MissingFieldError


class RedshiftAuthentication:

  @property
  def api_key(self):
    return self._api_key

  @property
  def api_secret_key(self):
    return self._api_secret_key
  
  @property
  def cluster_id(self):
    return self._cluster_id
  
  @property
  def aws_region(self):
    return self._aws_region
  
  @property
  def database(self):
    return self._database

  def with_api_key(self, api_key: str) -> 'RedshiftAuthentication':
    self._api_key = api_key
    return self
  
  def with_api_secret_key(self, api_secret_key: str) -> 'RedshiftAuthentication':
    self._api_secret_key = api_secret_key
    return self
  
  def with_cluster_id(self, cluster_id: str) -> 'RedshiftAuthentication':
    self._cluster_id = cluster_id
    return self
  
  def with_aws_region(self, aws_region: str) -> 'RedshiftAuthentication':
    self._aws_region = aws_region
    return self
  
  def with_database(self, database: str) -> 'RedshiftAuthentication':
    self._database = database
    return self
  
  def build(self) -> 'RedshiftAuthentication':
    required_fields = ["api_key", "api_secret_key", "cluster_id", "aws_region", "database"]
    for r in required_fields:
      if self.__getattribute__(f"_{r}") == None:
        raise MissingFieldError(r)
    return self