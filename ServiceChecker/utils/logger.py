import os
import logging.config


def init_logger():
    """
    初始化logger
    :return:
    """
    own_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
    conf_path = os.path.join(own_path, "config/logger.conf")
    defaults = {}
    defaults.setdefault('args', str((os.path.join(os.path.dirname(own_path), 'Logs/service_checker.log'), 'a+',
                                     50 * 1024 * 1024, 5)))
    logging.config.fileConfig(conf_path, defaults=defaults)
