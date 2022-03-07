from genericpath import exists
import os
from typing import Any, Dict, Optional, Union, cast
import aiohttp
from py import process
from mlops_client.datasource.datasource_type import DatasourceType, InvalidTypeError
from mlops_client.datasource.gcp_authentication import GCPAuthentication
from mlops_client.datasource.redshift_authentication import RedshiftAuthentication
from mlops_client.model.failed_api_call import FailedAPICallError
from mlops_client.model.missing_path import MissingPathError

from mlops_client.service_client import ServiceClient

class Datasource(ServiceClient):

  def __init__(self, headers: Dict[str, str], host: str, 
      client: Optional[aiohttp.ClientSession] = None):
    """Datasource is the client for interacting with the /datasource endpoint on
    Elemeno MLOps API.

    Paramaters:
      - headers: A dictionary with the headers to be used in the call. Consider using mlops_client.model.headers.Headers which already contain the default required headers
      - client: An optional parameter in case you think it's useful to specify your own aiohttp.ClientSession, if not specified this class creates one
    
    Returns:
      An instance of Datasource
    """

    self._endpoint = "/datasource"
    self._headers = headers
    self._host = host
    self._client = client

  def _get_client(self) -> aiohttp.ClientSession:
    if self._client == None:
      return aiohttp.ClientSession()
    return self._client
  
  async def create(self, 
      dstype: DatasourceType, 
      authentication: Union[GCPAuthentication, RedshiftAuthentication, None],
      description: str,
      csv_file_path: Optional[str] = None) -> Any:
    """Creates a new datasource object on your account at Elemeno MLOps
    
    Parameters:
      - dstype: The type of data source you want to use
      - authentication: The credentials that will allow the platform to handle your data. Should be None when the type is CSV
      - description: A short description of your datasource, so that you can find it later
      - csv_file_path: Only required when type is CSV
    
    Returns:
      The json object with the result. If it fails, this method will raise an Exception
    """

    async with self._get_client() as client:
      with aiohttp.MultipartWriter('text') as mpwriter:
        form = aiohttp.FormData()
        form.add_field("description", description)
        if dstype == DatasourceType.BIGQUERY:
          gcp: GCPAuthentication = cast(GCPAuthentication, authentication)
          if gcp.path == None or not exists(gcp.path):
            raise MissingPathError(gcp.path)
          form.add_field("gcpProjectId", gcp.project_id)
          with open(gcp.path) as file:
            mpwriter.append(file)
            form.add_field("gcpCredentials", mpwriter)
            return await self._post(client, self._endpoint, form=form, headers=self._headers)
        elif dstype == DatasourceType.REDSHIFT:
          rs: RedshiftAuthentication = cast(RedshiftAuthentication, authentication)
          form.add_field("awsAccessKeyId", rs.api_key)
          form.add_field("awsSecretAccessKey", rs.api_secret_key)
          form.add_field("awsRegion", rs.aws_region)
          form.add_field("redshiftClusterIdentifier", rs.cluster_id)
          form.add_field("redshiftDatabase", rs.database)
          return await self._post(client, self._endpoint, form=form, headers=self._headers)
        elif dstype == DatasourceType.CSV:
          if csv_file_path == None or not exists(csv_file_path):
            raise MissingPathError(csv_file_path)
          with open(csv_file_path) as file:
            mpwriter.append(file)
            form.add_field('file', mpwriter)
            return await self._post(client, self._endpoint, form=form, headers=self._headers)
        else:
          raise InvalidTypeError(dstype)
  
  async def remove(self, id: str) -> Any:
    """
    Removes a datasource.

    Parameters:
      - id: The datasource id.

    Returns:
      The datasource.
    """

    async with self._get_client() as client:
      endpoint = "/".join([self._endpoint, id])
      return await self._delete(client, endpoint, self._headers)
  
  async def list(self, offset: Optional[str] = None, limit: Optional[int] = None) -> Any:
    """
    Lists all datasources.

    Parameters:
      - offset: An optional string that is used for pagination. It indicates the
        first element that should be returned (0-based).
      - limit: An optional integer that is used for pagination. It indicates the
        maximum number of elements to return.

    Returns:
      A list of datasources.
    """

    query_params = {}
    if offset != None:
      query_params["offset"] = offset
    if limit != None:
      query_params["limit"] = str(limit)
    async with self._get_client() as client:
      return await self._get(client, self._endpoint, query_params, self._headers)

 
