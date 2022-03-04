import aiohttp
from abc import ABC
from typing import Dict, Any, Optional

from mlops_client.model.failed_api_call import FailedAPICallError

class ServiceClient(ABC):

  def __init__(self, headers: Dict[str, str], host: str, endpoint: str):
    self._headers = headers
    self._host = host
    self._endpoint = endpoint

  async def _get(self, client: aiohttp.ClientSession, endpoint: str, query_params: Dict[str, str], headers: Dict[str, str]) -> Any:
    query_string = ""
    qp = [f"{k}={v}" for k, v in query_params.items()]
    if len(qp) > 0:
      params = "&".join(qp)
      query_string = f"?{params}"
    async with client.get(
      self._host + endpoint + query_string,
      headers = headers
    ) as resp:
      status = resp.status
      if not str(status).startswith("2"):
        raise FailedAPICallError(status, (await resp.json()))
      return (await resp.json())
  
  async def _delete(self, client: aiohttp.ClientSession, endpoint: str, headers: Dict[str, str]) -> Any:
    async with client.delete(
      self._host + endpoint,
      headers = headers
    ) as resp:
      status = resp.status
      if not str(status).startswith("2"):
        raise FailedAPICallError(status, (await resp.json()))
      return (await resp.json())

  async def _post(self, client: aiohttp.ClientSession, endpoint: str, form: Optional[aiohttp.FormData] = None, headers: Dict[str, str] = {}, json_payload: Optional[str] = None) -> Any:
    req_data = form if form is not None else json_payload
    async with client.post(
      self._host + endpoint,
      data=req_data,
      headers = headers
    ) as resp:
      status = resp.status
      if not str(status).startswith("2"):
        raise FailedAPICallError(status, (await resp.json()))
      return (await resp.json())