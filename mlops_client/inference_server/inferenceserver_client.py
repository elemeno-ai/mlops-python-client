from typing import Any, Dict, List, Optional

import aiohttp
from mlops_client.inference_server.feature_source import FeatureSource
from mlops_client.inference_server.feature_source_type import FeatureSourceType
from mlops_client.service_client import ServiceClient


class InferenceServer(ServiceClient):

  def __init__(self, headers: Dict[str, str], host: str, 
      client: Optional[aiohttp.ClientSession] = None):
    """InferenceServer is the client for interacting with the /inferenceserver endpoint on
    Elemeno MLOps API.

    Params:
      - headers: A dictionary with the headers to be used in the call. Consider using mlops_client.model.headers.Headers which already contain the default required headers
      - client: An optional parameter in case you think it's useful to specify your own aiohttp.ClientSession, if not specified this class creates one
    
    Returns:
      - An instance of InferenceServer
    """

    self._endpoint = "/inferenceserver"
    self._headers = headers
    self._host = host
    self._client = client

  def _get_client(self):
    if self._client == None:
      return aiohttp.ClientSession()
    return self._client

  async def create_rest(self, model_path: str, num_instances: int, 
    sources: List[FeatureSource]) -> Any:
    """
    Creates a REST inference server for a given model.

    Args:
      - model_path: Path to the model file.
      - num_instances: Number of instances to create.
      - sources: A list of FeatureSource objects.

    Returns:
      - A list of InferenceServer objects.
    """

    async with self._get_client() as client:
      with aiohttp.MultipartWriter('application/octet-stream') as mpwriter:
        form = aiohttp.FormData()
        form.add_field("type", "HTTP")
        form.add_field("instances", num_instances)
        for i, s in enumerate(sources):
          form.add_field(f"sources[{i}].type", s.source_type)
          if s.source_type == FeatureSourceType.FEATURE_TABLE:
            form.add_field(f"sources[{i}].featureTableID", s.feature_table_id)
            form.add_field(f"sources[{i}].feature", s.feature_name)
          else:
            form.add_field(f"sources[{i}].requestBodyJSONPath", s.body_json_path)
        with open(model_path, 'rb+') as file:
          mpwriter.append(file)
          form.add_field("modelFile", mpwriter)
          return await self._post(client, self._endpoint, form=form, headers=self._headers)

  async def list(self, offset: Optional[str] = None, limit: Optional[int] = None) -> Any:
    """
    List all inference servers.

    Parameters:
      - offset: An optional string that represents the starting item, should be the value of 'next' field from the previous response.
      - limit: An optional integer to limit the number of returned items.

    Returns:
      - A list of InferenceServer objects.
    """
    query_params = {}
    async with self._get_client() as client:
      if offset != None:
        query_params["offset"] = offset
      if limit != None:
        query_params["limit"] = str(limit)
      return await self._get(client, self._endpoint, query_params, self._headers)