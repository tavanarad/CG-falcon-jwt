import falcon
from cheeta_jwt.middleware import JWTMiddleware

config = {"secret": "123",
          "algorithm": "hs256",
          "exempt_resources": [{"name": "AuthorizationResource", "methods": ["OPTIONS", "GET", "POST"]},
                               {"name": "UserResource", "methods": ["OPTIONS", "GET"]},
                               {"name": "LogResource", "methods": None}], "exempt_all_methods": ["OPTIONS"]}


class UserResource(object):
    def on_get(self, req, resp, **kwargs):
        resp.body = 'get'

    def on_post(self, req, resp, jwt_claims):
        resp.body = jwt_claims['user'].__str__()
        pass

    def on_put(self, req, resp, jwt_claims):
        resp.body = jwt_claims['user'].__str__()
        pass


api = application = falcon.API(
    middleware=[JWTMiddleware(config)]
)

api.add_route('/UserResource', UserResource())
