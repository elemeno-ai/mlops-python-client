
from multiprocessing.sharedctypes import Value
import typing

class Headers:
  
  _default = ["X-API-KEY", "X-API-SECRET", "Content-Type"]
  _headers = {"Content-Type": "application/form-data"}

  def with_api_key(self, x_api_key: str):
    self._headers["X-API-KEY"] = x_api_key
    return self
  
  def with_api_secret(self, x_api_secret: str):
    self._headers["X-API-SECRET"] = x_api_secret
    return self

  def build(self) -> typing.Dict[str, str]:
    for expected in self._default:
      if self._headers.get(expected) == None:
        raise MissingExpectedHeaderError(expected)
    return self._headers

class MissingExpectedHeaderError(ValueError):
  def __init__(self, missing: str):
    return self.with_traceback(ValueError(f"Missing header {missing}. This header is mandatory"))
  
