
from enum import Enum


class FeatureSourceType(str, Enum):
  """
  FeatureSourceType is an enumeration of the possible sources of features for a feature set.

  FEATURE_TABLE: The feature set is based on a feature table.
  REQUEST_BODY: The feature set is based on a request body.
  REQUEST_BODY_KEY: The feature set is based on a request body key.
  """

  FEATURE_TABLE="FEATURE_TABLE"
  REQUEST_BODY="REQUEST_BODY"
  REQUEST_BODY_KEY="REQUEST_BODY_KEY"