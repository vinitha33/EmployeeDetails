'''Loghangler file to file the logs in a .log file'''
import os
import logging


def logfile():
    """

    :return:
    logger returns the parameters to log data into a log file
    """

    logger = logging.getLogger()
    file_path = os.path.dirname(os.path.dirname(__file__)) + "\\logs\\logfile.log"

    file_handler = logging.FileHandler(file_path)
    formatter = logging.Formatter("%(asctime)s - %(name)s -"
                                  " %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
    logging.basicConfig(filename=file_path, filemode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
