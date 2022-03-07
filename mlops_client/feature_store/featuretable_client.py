import json
import aiohttp
from typing import Any, Dict, List, Optional
from mlops_client.feature_store.feature import Feature
from mlops_client.feature_store.feature_key import FeatureKey
from mlops_client.service_client import ServiceClient

class FeatureTable(ServiceClient):

  def __init__(self, headers: Dict[str, str], host: str, 
      client: Optional[aiohttp.ClientSession] = None):
    """FeatureTable is the client for interacting with the /featuretable endpoint on
    Elemeno MLOps API.

    Params:
      - headers: A dictionary with the headers to be used in the call. Consider using mlops_client.model.headers.Headers which already contain the default required headers
      - client: An optional parameter in case you think it's useful to specify your own aiohttp.ClientSession, if not specified this class creates one
    
    Returns:
      An instance of FeatureTable
    """

    self._endpoint = "/featuretable"
    self._headers = headers
    self._host = host
    self._client = client

  def _get_client(self):
    if self._client == None:
      return aiohttp.ClientSession()
    return self._client

  async def create_mapping(self, datasource_id: str, source_table_id: str, 
    feature_table_name: str, keys: List[FeatureKey], features: List[Feature]) -> Any:
    """
    Creates a feature table mapping for a given datasource and source table.

    Parameters:
      - datasource_id (str): The datasource id.
      - source_table_id (str): The source table id.
      - feature_table_name (str): The feature table name.
      - keys (List[FeatureKey]): A list of FeatureKey objects.
      - features (List[Feature]): A list of Feature objects.

    Returns:
      Any: The response from the API.
    """

    async with self._get_client() as client:
      headers = self._headers
      headers['Content-Type'] = 'application/json'
      body = {
        'dataSourceId': datasource_id,
        'dataSourceEntityId': source_table_id,
        'featureTableName': feature_table_name
      }

      feature_keys = [{'type': 'KEY', 'name': k.key_name, 'valueType': k.key_value_type} for k in keys]
      feature_columns = [{'type': 'FEATURE', 'name': f.feature_name, 'valueType': f.feature_value_type} for f in features]

      feature_keys.extend(feature_columns)
      body['columns'] = feature_keys
      return await self._post(client, endpoint=self._endpoint, \
        headers=headers, json_payload=json.dumps(body))
