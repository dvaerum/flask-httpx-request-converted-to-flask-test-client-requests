import json
import flask
import unittest
from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI

app = OpenAPI(__name__)


class SumResponse(BaseModel):
    the_sum: int = Field(..., description="sum of 2 numbers")


class NumbersRequest(BaseModel):
    no_1: int = Field(..., description="1st number")
    no_2: int = Field(..., description="2nd number")


@app.post(rule="/multiply-2-numbers", responses={"200": SumResponse})
def multiply_2_numbers(body: NumbersRequest):
    resp = flask.Response(json.dumps({"the_sum": body.no_1 * body.no_2}))
    resp.headers.set('Content-Type', 'application/json')
    resp.status_code = 200
    return resp


class Testing(unittest.TestCase):
    def test_10_generate_rest_lib(self):
        from pathlib import Path
        from openapi_python_client import GeneratorData, Config, Project, MetaType

        config = Config()
        with app.test_client() as client:
            resp = client.get("/openapi/openapi.json")
            openapi = GeneratorData.from_dict(data=resp.json, config=config)

            path = Path(__file__).parent.parent.joinpath("test_rest_api")
            path.mkdir(exist_ok=True)
            project = Project(openapi=openapi, meta=MetaType.NONE, config=config)
            project.package_dir = path
            project.project_dir = path
            project.update()

    def test_20_generate_rest_lib(self):
        from test_rest_api.api.default.multiply_2_numbers_multiply_2_numbers_post import (
            sync_detailed as rest_api_multiply_2_numbers)
        from test_rest_api.models.numbers_request import (
            NumbersRequest as RestApiNumbersRequest)
        from flask_httpx_request_converted_to_flask_test_client_request import ConvertHttpx2FlaskTestClient

        app.test_client_class = ConvertHttpx2FlaskTestClient

        with app.test_client() as client:
            resp = rest_api_multiply_2_numbers(client=client,
                                               json_body=RestApiNumbersRequest(no_1=42, no_2=1337))
            assert 200 == resp.status_code
            result = resp.parsed
            assert 56154 == result.the_sum
