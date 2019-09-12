from copy import deepcopy
from typing import List, Callable

import falcon
from cheeta_jwt.helper import JWTHelper as Jwt
from cheeta_jwt.helper.log_helper import Log
from cheeta_jwt.exception import ValidatorException

log = Log(__name__)
logger = log.logger()


class JWTMiddleware(object):
    """for more information visit 'API.MD' in ..docs/"""

    def __init__(self, options: dict, validators: List[Callable] = None):
        self.secret = options['secret']  # str
        self.algorithm = options['algorithm']  # str
        self.exempt_resource = options['exempt_resources']  # list of dicts
        self.exempt_all_methods = options['exempt_all_methods']  # list of string
        self.log_level = options.get('log_level')

        self.validators = validators

        if self.log_level:
            logger.setLevel(self.log_level)

        logger.info(options)

    def __check_exempt_resource(self, resource, method):
        for ex_res in self.exempt_resource:
            if resource == ex_res['name']:
                if ex_res['methods'] is None or method in ex_res['methods']:
                    return True
        return False

    def process_resource(self, req, resp, resource, params):
        client_method = req.method

        _is_pass = False

        if client_method in self.exempt_all_methods:
            logger.info('{} method is existing in exempt_all_methods list'.format(client_method))
            _is_pass = True

        elif self.__check_exempt_resource(resource.__class__.__name__,
                                          client_method):
            logger.info('{0} method exempt at {1}'.format(client_method, resource.__class__.__name__))
            _is_pass = True

        try:
            token = req.headers.get('AUTHORIZATION', '').partition('Bearer ')[2]
            payload = Jwt.decode(token, self.secret, self.algorithm)

            if self.validators:
                try:
                    list(map(lambda x: x(deepcopy(payload)), self.validators))
                    params['jwt_claims'] = {}

                    for claim in payload:
                        params['jwt_claims'][claim] = payload[claim]
                except Exception as e:
                    logger.exception(e)
                    raise ValidatorException(e)
            else:

                params['jwt_claims'] = {}

                for claim in payload:
                    params['jwt_claims'][claim] = payload[claim]
        except ValidatorException as e:
            raise falcon.HTTPUnauthorized('Invalid Token', description=e.__str__())
        except Exception as e:
            if _is_pass:
                return
            else:
                logger.exception(e)
                raise falcon.HTTPUnauthorized('Invalid Authorization', e.__dict__)
