
from inspect import Traceback


class MissingFieldError(ValueError):

  def __init__(self, field: str):
    self._field = field

  def __str__(self):
    return f"Incomplete request, missing field {self._field}. Make sure you call with_{self._field} before calling build()"
