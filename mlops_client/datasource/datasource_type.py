from enum import Enum

class DatasourceType(Enum):
  REDSHIFT="REDSHIFT"
  BIGQUERY="BIG_QUERY"
  CSV="CSV"

class InvalidTypeError(ValueError):

  def __init__(self, dstype: str):
    self._dstype = dstype
  
  def __str__(self) -> str:
    return f"The DatasourceType {self._dstype} is not valid. Check the file mlops_client.datasource.datasource_type.py for a list of valid types"