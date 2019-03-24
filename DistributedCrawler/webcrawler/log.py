import logging
import sys

class Log(object):
    def __init__(self):
        self.formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.add_stream_handler()
        self.add_file_handler()


    def add_stream_handler(self):
        """
        将运行信息输出到控制台
        :return: None
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(self.formatter)
        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)

    def add_file_handler(self):
        """
        将运行信息输出到日志中
        :return: None
        """
        file_handler = logging.FileHandler("spider.log")
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(logging.ERROR)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message, exc_info=True)

    def critical(self, message):
        self.logger.critical(message)