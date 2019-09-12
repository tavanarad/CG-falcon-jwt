from json import dumps

import pytest

import falcon
from falcon import testing
from cheeta_jwt.middleware import JWTMiddleware

config = {"secret": "123",
          "algorithm": "hs256",
          "exempt_resources": [
              {'name': 'ValidateResource', 'methods': ['OPTIONS']}],
          "exempt_all_methods": ["OPTIONS"]}


class ValidatorResource(object):
    def on_get(self, req, resp, **kwargs):
        resp.body = dumps(kwargs)
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp, jwt_claims):
        resp.body = dumps(jwt_claims)
        resp.status = falcon.HTTP_OK


def add_arg(payload):
    payload['arg'] = 'test'


def remove_arg(payload: dict):
    payload.__delitem__('arg')


class TestValidator1:
    _validator = [
        remove_arg
    ]
    api = application = falcon.API(
        middleware=[JWTMiddleware(config, _validator)]
    )

    api.add_route('/ValidatorResource', ValidatorResource())

    @pytest.fixture('class')
    def client_validator(self):
        return testing.TestClient(self.api)

    def test_validate(self, client_validator):
        headers = {
            "AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
        }

        result = client_validator.simulate_get(path='/ValidatorResource',
                                               headers=headers)
        assert result.status == falcon.HTTP_UNAUTHORIZED


class TestValidator2:
    _validator = [
        add_arg
    ]
    api = application = falcon.API(
        middleware=[JWTMiddleware(config, _validator)]
    )

    api.add_route('/ValidatorResource', ValidatorResource())

    @pytest.fixture('class')
    def client_validator(self):
        return testing.TestClient(self.api)

    def test_validator(self, client_validator):
        headers = {
            "AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
        }

        result = client_validator.simulate_get(path='/ValidatorResource',
                                               headers=headers)

        assert result.status == falcon.HTTP_OK

        assert 'arg' not in result.json['jwt_claims']
        assert result.json['jwt_claims']['user'] == 123


class TestValidator3:
    _validator = [
        add_arg,
        remove_arg
    ]
    api = application = falcon.API(
        middleware=[JWTMiddleware(config, _validator)]
    )

    api.add_route('/ValidatorResource', ValidatorResource())

    @pytest.fixture('class')
    def client_validator(self):
        return testing.TestClient(self.api)

    def test_validator(self, client_validator):
        headers = {
            "AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
        }

        result = client_validator.simulate_get(path='/ValidatorResource',
                                               headers=headers)

        assert result.status == falcon.HTTP_UNAUTHORIZED
        #
        # assert 'arg' not in result.json['jwt_claims']
        # assert result.json['jwt_claims'] == {'user': 123}


class TestValidator4:
    api = application = falcon.API(
        middleware=[JWTMiddleware(config)]
    )

    api.add_route('/ValidatorResource', ValidatorResource())

    @pytest.fixture('class')
    def client_validator(self):
        return testing.TestClient(self.api)

    def test_validator(self, client_validator):
        headers = {
            "AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
        }

        result = client_validator.simulate_get(path='/ValidatorResource',
                                               headers=headers)

        assert result.status == falcon.HTTP_OK

        assert result.json['jwt_claims'] == {'user': 123}
