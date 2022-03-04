
from enum import Enum


class FeatureSourceType(str, Enum):

  FEATURE_TABLE="FEATURE_TABLE"
  REQUEST_BODY="REQUEST_BODY"
  REQUEST_BODY_KEY="REQUEST_BODY_KEY"