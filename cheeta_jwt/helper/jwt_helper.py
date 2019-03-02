import jwt
from .log_helper import Log

log = Log(__name__)
logger = log.logger()


class JWTHelper(object):
    """for more information visit 'API.MD' in ..docs/"""

    @classmethod
    def encode(cls, payload: dict, secret: str, algorithm: str):
        algorithm = algorithm.upper()
        encoded = jwt.encode(payload, secret, algorithm)
        logger.info('encoded successful : {}'.format(encoded))
        encoded = bytes.decode(encoded)  # convert from bytes to str
        return encoded

    @classmethod
    def decode(cls, token: str, secret: str, algorithm: str):
        algorithm = algorithm.upper()
        decoded = jwt.decode(token, secret, algorithms=algorithm)
        logger.info('decoded successful : {}'.format(decoded))
        return decoded

    @classmethod
    def get_header(cls, jwt_obj):
        header = jwt.get_unverified_header(jwt_obj)
        logger.info('get header successful : {}'.format(header))
        return header
