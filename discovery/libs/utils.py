import logging
import os
import sys
import traceback
import netifaces
from logging.handlers import TimedRotatingFileHandler

from config import PROJECT_ROOT


def retrieve_logger(logger_name, file_name="log"):
    try:
        logs_path = os.path.join(PROJECT_ROOT, "logs")
        if not os.path.isdir(logs_path):
            os.mkdir(logs_path)

        logs_folder_path = os.path.join(logs_path, logger_name)
        if not os.path.exists(logs_folder_path):
            os.mkdir(logs_folder_path)

        log_file_path = os.path.join(logs_folder_path, "{}.log".format(file_name))

        logger = logging.getLogger(file_name)

        stream_handler = logging.StreamHandler(sys.stdout)
        rotating_file_handler = TimedRotatingFileHandler(log_file_path)
        formatter = logging.Formatter(
            "[%(asctime)-15s] - [%(levelname)s - %(filename)s - %(threadName)s] %(message)s")

        for handler in [stream_handler, rotating_file_handler]:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(logging.DEBUG)
        return logger

    except Exception as err:
        print("Error occurred while retrieving the logger")
        print(err)
        print(get_traceback())


def get_traceback():
    return traceback.format_exc()


def get_ip_address():
    interface = '{2576603B-FBB1-4CF7-AD3B-899450084477}'
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']


class FakeLogger(object):
    def __init__(self):
        pass

    def debug(self, message, **kwargs):
        print("[Fake Logger][DEBUG] {}".format(message))

    def info(self, message, **kwargs):
        print("[Fake Logger][INFO] {}".format(message))

    def warning(self, message, **kwargs):
        print("[Fake Logger][WARNING] {}".format(message))

    def error(self, message, **kwargs):
        print("[Fake Logger][ERROR] {}".format(message))

    def critical(self, message, **kwargs):
        print("[Fake Logger][CRITICAL] {}".format(message))


if __name__ == '__main__':
    print(get_ip_address())
