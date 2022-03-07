from enum import Enum

class DatasourceType(Enum):
  """
  This is a class that defines the type of datasource that is being used.

  The DatasourceType class is an enumeration class that defines the type of datasource that is being used.

  Attributes
  ----------
  REDSHIFT : DatasourceType
      The REDSHIFT datasource type
  BIGQUERY : DatasourceType
      The BIGQUERY datasource type
  CSV : DatasourceType
      The CSV datasource type
    """
  REDSHIFT="REDSHIFT"
  BIGQUERY="BIG_QUERY"
  CSV="CSV"

class InvalidTypeError(ValueError):

  def __init__(self, dstype: str):
    self._dstype = dstype
  
  def __str__(self) -> str:
    return f"The DatasourceType {self._dstype} is not valid. Check the file mlops_client.datasource.datasource_type.py for a list of valid types"