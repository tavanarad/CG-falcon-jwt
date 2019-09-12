import logging
import os
from datetime import date

default_path = os.getcwd() + '/log'
default_format = '%(asctime)s -> %(levelname)s -> %(name)s : %(funcName)s -> %(message)s'


class Log:
    """


    """

    def __init__(self, module_name,
                 _format=default_format,
                 path=default_path,
                 level=logging.ERROR,
                 stream=False,
                 stream_format=False
                 ):
        self._name = module_name
        self._format = _format
        self.level = level
        self._path = path
        self._stream = stream
        self._stream_format = stream_format

    def logger(self):

        logger = logging.getLogger(self._name)
        logger.setLevel(self.level)

        # path to save main.log
        if not os.path.exists(self._path):
            os.mkdir(self._path)

        if self._stream:  # print in console
            stream_handler = logging.StreamHandler()
            if self._stream_format:  # print with our format
                stream_handler.setFormatter(self._format)
            logger.addHandler(stream_handler)

        name_file = '/jwt-middleware-' + date.today().__str__() + '.log'

        file_handler = logging.FileHandler(self._path + name_file)  # path + name of file
        formatter = logging.Formatter(self._format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger
