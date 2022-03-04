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
      headers: A dictionary with the headers to be used in the call. Consider using mlops_client.model.headers.Headers which already contain the default required headers
      client: An optional parameter in case you think it's useful to specify your own aiohttp.ClientSession, if not specified this class creates one
    
    Returns:
      An instance of InferenceServer
    """

    self._endpoint = "/inferenceserver"
    self._headers = headers
    self._host = host
    if client == None:
      client = aiohttp.ClientSession()
    self._client = client

  async def create_rest_inference_server(self, model_path: str, num_instances: int, 
    sources: List[FeatureSource]) -> Any:

    async with self._client as client:
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

  async def list_inference_servers(self, offset: Optional[str] = None, limit: Optional[int] = None) -> Any:
    query_params = {}
    async with self._client as client:
      if offset != None:
        query_params["offset"] = offset
      if limit != None:
        query_params["limit"] = str(limit)
      return await self._get(client, self._endpoint, query_params, self._headers)