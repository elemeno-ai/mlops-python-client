from enum import Enum

class FeatureValueType(str, Enum):
  """
  FeatureValueType is an enumeration of the possible types of values that a feature can have.

  STRING: A string value.
  FLOAT: A floating point value.
  INTEGER: An integer value.
  ARRAY: An array of values.
  """
  
  STRING="STRING"
  FLOAT="FLOAT"
  INTEGER="INTEGER"
  ARRAY="ARRAY"

class InvalidFeatureValueTypeError(ValueError):

  def __init__(self, value_type: str):
    self._value_type = value_type
  
  def __str__(self) -> str:
    return f"Invalid type {self._value_type} specified for FeatureValueType"