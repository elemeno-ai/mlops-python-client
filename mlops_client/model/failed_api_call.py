
from typing import Any


class FailedAPICallError(ValueError):

  def __init__(self, status_code: int, response_body: Any):
    self._response = response_body
    self._status_code = status_code
  
  def __str__(self) -> str:
    return f"""Got bad status code [{self._status_code}] from the remote API. The API responded with [{self._response}]"""
  
  @property
  def message(self) -> str:
    return self.__str__()