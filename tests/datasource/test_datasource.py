from typing import cast
from unittest.mock import MagicMock, ANY
import aiohttp
import pytest
from aiohttp import web
from aiohttp.web_request import Request
from mlops_client.datasource.datasource_client import Datasource, DatasourceType
from mlops_client.datasource.datasource_type import InvalidTypeError
from mlops_client.datasource.redshift_authentication import RedshiftAuthentication
from mlops_client.model.failed_api_call import FailedAPICallError
from mlops_client.model.headers import Headers
from aiohttp import test_utils
import logging

from mlops_client.datasource.gcp_authentication import GCPAuthentication
from ..utils.matchers import AssertableFormData

@pytest.fixture
def server():
  app = web.Application()
  
  async def ds_handler(request):
    return web.Response(body=b'{"ok":"ok"}', headers={'Content-Type': 'application/json'})
  
  async def ds_delete_handler(request):
    return web.Response(body=b'{"ok":"ok"}', headers={'Content-Type': 'application/json'})
  
  async def ds_get_handler(request):
    return web.Response(body=b'[{"ok":"ok"}]', headers={'Content-Type': 'application/json'})

  app.router.add_post("/datasource", ds_handler)
  app.router.add_delete("/datasource/{id}", ds_delete_handler)
  app.router.add_get("/datasource", ds_get_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

@pytest.fixture
def server_with_error_auth():
  app = web.Application()
  async def ds_handler(request):
    return web.Response(body=b'{"error":"Invalid API-KEY"}', headers={'Content-Type': 'application/json'}, status=401)
  app.router.add_post("/datasource", ds_handler)
  server = test_utils.TestServer(app, port=8099)
  return server

async def test_create_datasource_bq(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      mocker.spy(client, 'post')
      auth = GCPAuthentication(). \
        with_path("tests/datasource/credentials-test.json"). \
        with_project_id("testproject")

      await d.create(DatasourceType.BIGQUERY, auth, "test")
      assert client.post.call_count == 1
      spied_data = client.post.call_args.kwargs['data']
      assert spied_data._fields[0][2] == 'test'
      assert spied_data._fields[1][2] == 'testproject'
      client.post.assert_called_with('http://localhost:8099/datasource', data=ANY, headers={})

async def test_create_datasource_rs(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      mocker.spy(client, 'post')
      auth = RedshiftAuthentication(). \
        with_api_key('test'). \
        with_api_secret_key('testsecret'). \
        with_aws_region('test-region'). \
        with_cluster_id('test-cluster'). \
        with_database('testdb')
      
      await d.create(DatasourceType.REDSHIFT, auth, "desc")
      fields = {'awsAccessKeyId': 'test', 'awsSecretAccessKey': 'testsecret', 
        'awsRegion': 'test-region', 'redshiftClusterIdentifier': 'test-cluster',
        'redshiftDatabase': 'testdb', 'description': 'desc'}
      expected_form = AssertableFormData(fields=fields)
      spied_data = client.post.call_args.kwargs['data']
      spied_data = cast(AssertableFormData, spied_data)
      assert client.post.call_count == 1
      client.post.assert_called_with('http://localhost:8099/datasource', data=ANY, headers={})
      assert spied_data == expected_form

async def test_create_datasource_csv(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      mocker.spy(client, 'post')
      auth = None

      await d.create(DatasourceType.CSV, auth, 'csv-desc', 
        'tests/datasource/test.csv')
      fields = {'file': 'file-content', 'description': 'csv-desc'}
      expected_form = AssertableFormData(fields=fields)
      spied_data = client.post.call_args.kwargs['data']
      spied_data = cast(AssertableFormData, spied_data)
      assert client.post.call_count == 1
      # hack because we're not asserting file content yet
      field_form = list(spied_data._fields[1])
      field_form[2] = 'file-content'
      spied_data._fields[1] = tuple(field_form)
      assert spied_data == expected_form
      client.post.assert_called_with('http://localhost:8099/datasource', data=ANY, headers={})

@pytest.mark.asyncio
async def test_invalid_type():
  with pytest.raises(InvalidTypeError):
    d = Datasource(host="any", headers={})
    await d.create("UNKNOWN", None, 'test')

@pytest.mark.asyncio
async def test_invalid_api_auth(server_with_error_auth):
  async with server_with_error_auth:
      async with aiohttp.ClientSession() as client:
        d = Datasource(host="http://localhost:8099", headers={}, client=client)
        with pytest.raises(FailedAPICallError) as err_info:
          await d.create(DatasourceType.CSV, None, 'csv-desc', 
            'tests/datasource/test.csv')
        assert str(err_info.value.message) == """
          Got bad status code [401] from the remote API. The API responded with [{'error': 'Invalid API-KEY'}]
        """.strip()

async def test_remove_datasource(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      mocker.spy(client, 'delete')
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      await d.remove("id123")
      assert client.delete.call_count == 1
      client.delete.assert_called_with('http://localhost:8099/datasource/id123', headers={})

async def test_list_datasources(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      mocker.spy(client, 'get')
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      await d.list()
      assert client.get.call_count == 1
      client.get.assert_called_with('http://localhost:8099/datasource', headers={})

async def test_list_datasources_with_params(server, mocker):
  async with server:
    async with aiohttp.ClientSession() as client:
      mocker.spy(client, 'get')
      d = Datasource(host="http://localhost:8099", headers={}, client=client)
      await d.list(offset="1234", limit=30)
      assert client.get.call_count == 1
      client.get.assert_called_with('http://localhost:8099/datasource?offset=1234&limit=30', headers={})
