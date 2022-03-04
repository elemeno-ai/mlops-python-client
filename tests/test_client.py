
from client import MLOpsClient
from model.headers import Headers
from model.missing_field import MissingFieldError
import pytest
from unittest.mock import MagicMock, ANY


def test_without_api_key(mocker):
  with pytest.raises(MissingFieldError) as exc_info:
    m = MLOpsClient().with_api_secret('sec').build()
  mferror = exc_info.value
  assert str(mferror) == "Incomplete request, missing field api_key. Make sure you call with_api_key before calling build()"

def test_without_api_secret(mocker):
  with pytest.raises(MissingFieldError) as exc_info:
    m = MLOpsClient().with_api_key('key').build()
  mferror = exc_info.value
  assert str(mferror) == "Incomplete request, missing field api_secret. Make sure you call with_api_secret before calling build()"

def test_with_staging_host(mocker):
  m = MLOpsClient().with_api_key('key').with_api_secret('sec').\
    use_staging().build()
  assert m.datasource != None
  assert m.host == 'http://localhost:8080'

def test_client_instances(mocker):
  expected_host = 'https://c3p0.elemeno.ai'
  m = MLOpsClient().with_api_key('key').with_api_secret('sec').build()
  assert m.datasource != None
  assert m.datasource._host == expected_host
  assert m.datasource._headers == Headers().with_api_key('key').with_api_secret('sec').build()
  assert m.featuretable != None
  assert m.featuretable._host == expected_host
  assert m.featuretable._headers['Content-Type'] == 'application/json'
  assert m.inferenceserver != None
  assert m.inferenceserver._host == expected_host
  assert m.inferenceserver._headers['Content-Type'] == 'application/form-data'
