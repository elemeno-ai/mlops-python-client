
class MissingPathError(ValueError):

  def __init__(self, path: str):
    self._path = path

  def __str__(self):
    return f"Failed to perform operation. The path {self._path} doesn't exists and is required."