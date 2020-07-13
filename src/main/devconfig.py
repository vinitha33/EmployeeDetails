'''Config file for the connection part'''
import configparser
import os

config = configparser.ConfigParser()
file_path = os.path.dirname(os.path.dirname(__file__))+"\\config"
config.read(file_path + "\\dev.properties")


def connect(env):
    """

    :param
     env: Specified production environment
    :return:
    host, user, password, db to connect to the database
    """
    host = config.get(env, "host")
    user = config.get(env, "user")
    password = config.get(env, "password")
    db1 = config.get(env, "db")
    return host, user, password, db1
