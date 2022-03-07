
from sqlalchemy import desc

from mlops_client.model.missing_field import MissingFieldError


class GCPAuthentication:
  """
  Builds a GCPAuthentication object.

  Object building functions:
    - with_path: Path to the service account key file.
    - with_project_id: GCP project id.
    - build: Returns a complete instance of the object.

  Returns:
    GCPAuthentication object.

  Raises:
    MissingFieldError: If any of the required fields are missing.
  """

  @property
  def path(self):
    return self._path

  @property
  def project_id(self):
    return self._project_id

  def with_path(self, path: str):
    self._path = path
    return self
  
  def with_project_id(self, project_id: str):
    self._project_id = project_id
    return self
  
  def build(self) -> 'GCPAuthentication':
    required_fields = ["path", "project_id"]
    for r in required_fields:
      if not hasattr(self, f"_{r}"):
        raise MissingFieldError(r)
    return self