
import json
import aiohttp
import pytest
from aiohttp import web, test_utils
from unittest.mock import MagicMock, ANY

from sqlalchemy import INTEGER
from mlops_client.feature_store.feature import Feature
from mlops_client.feature_store.feature_key import FeatureKey
from mlops_client.feature_store.feature_value_type import FeatureValueType

from mlops_client.feature_store.featuretable_client import FeatureTable

@pytest.fixture
def server():
  app = web.Application()
  
  async def featuretable_handler(request):
    return web.Response(body=b'{"ok":"ok"}', headers={'Content-Type': 'application/json'})

  app.router.add_post("/featuretable", featuretable_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

@pytest.fixture
def server_with_error_auth():
  app = web.Application()
  async def featuretable_handler(request):
    return web.Response(body=b'{"error":"Invalid API-KEY"}', headers={'Content-Type': 'application/json'}, status=401)
  app.router.add_post("/featuretable", featuretable_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

async def test_create_featuretable(server, mocker):
  async with server:
    client = aiohttp.ClientSession()
    d = FeatureTable(host="http://localhost:8099", headers={}, client=client)
    mocker.spy(client, 'post')
    
    k = FeatureKey().with_key_name('testname'). \
      with_key_value_type(FeatureValueType.STRING). \
      build()
    keys = [k]

    f = Feature().with_feature_name('testfeat'). \
        with_feature_value_type(FeatureValueType.INTEGER). \
        build()
    features = [f]

    await d.create_mapping("did123", "tab123", "feature_tablen", keys=keys, features=features)

    assert client.post.call_count == 1

    feature_keys = [{'type': 'KEY', 'name': k.key_name, 'valueType': k.key_value_type} for k in keys]
    feature_columns = [{'type': 'FEATURE', 'name': f.feature_name, 'valueType': f.feature_value_type} for f in features]

    feature_keys.extend(feature_columns)
    #spied_data = client.post.call_args.kwargs['data']
    expected_body = {
      'dataSourceId': 'did123',
      'dataSourceEntityId': 'tab123',
      'featureTableName': 'feature_tablen',
      'columns': feature_keys
    }
    client.post.assert_called_with('http://localhost:8099/featuretable', data=json.dumps(expected_body), headers={'Content-Type': 'application/json'})