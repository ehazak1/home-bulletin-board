import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0923jrnva7f7hq7623mvalNBTCR63RNADG7BGDASDANUBSDF'
