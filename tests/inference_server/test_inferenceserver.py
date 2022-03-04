from typing import cast
import aiohttp
import pytest
from aiohttp import web, test_utils
from unittest.mock import MagicMock, ANY
from mlops_client.inference_server.feature_source import FeatureSource
from mlops_client.inference_server.feature_source_type import FeatureSourceType

from mlops_client.inference_server.inferenceserver_client import InferenceServer
from ..utils.matchers import AssertableFormData


@pytest.fixture
def server():
  app = web.Application()
  
  async def inferenceserver_handler(request):
    return web.Response(body=b'{"ok":"ok"}', headers={'Content-Type': 'application/json'})
  
  async def get_inferenceserver_handler(request):
    return web.Response(body=b'[{"ok":"ok"}]', headers={'Content-Type': 'application/json'})

  app.router.add_post("/inferenceserver", inferenceserver_handler)
  app.router.add_get("/inferenceserver", get_inferenceserver_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

@pytest.fixture
def server_with_error_auth():
  app = web.Application()
  async def inferenceserver_handler(request):
    return web.Response(body=b'{"error":"Invalid API-KEY"}', headers={'Content-Type': 'application/json'}, status=401)
  app.router.add_post("/inferenceserver", inferenceserver_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

async def test_create_inference_server(server, mocker):
  async with server:
    client = aiohttp.ClientSession()
    d = InferenceServer(host="http://localhost:8099", headers={}, client=client)
    mocker.spy(client, 'post')

    source_body_key = FeatureSource(). \
      with_source_type(FeatureSourceType.REQUEST_BODY_KEY). \
      with_body_json_path("$.id") \
      .build()
    
    source_feature_table = FeatureSource(). \
      with_source_type(FeatureSourceType.FEATURE_TABLE). \
      with_feature_table_id("id123"). \
      with_feature_name("featname"). \
      build()
    sources = [source_body_key, source_feature_table]

    await d.create_rest_inference_server('tests/inference_server/model.onnx', 1, sources)

    assert client.post.call_count == 1
    spied_data = client.post.call_args.kwargs['data']
    spied_data = cast(AssertableFormData, spied_data)

    file_field = list(spied_data._fields[7])
    file_field[2] = 'file-content'
    spied_data._fields[7] = tuple(file_field)

    fields = {'type': 'HTTP', 
      'instances': 1, 
      'sources[0].type': FeatureSourceType.REQUEST_BODY_KEY,
      'sources[0].requestBodyJSONPath': '$.id',
      'sources[1].type': FeatureSourceType.FEATURE_TABLE,
      'sources[1].featureTableID': 'id123',
      'sources[1].feature': 'featname',
      'modelFile': 'file-content'}
    expected_form = AssertableFormData(fields=fields)
    assert spied_data == expected_form
    client.post.assert_called_with('http://localhost:8099/inferenceserver', data=ANY, headers={})