# -*- coding: utf-8 -*-
class Config(dict):
    """
    Предполагается, что этот словарь
    будет хранить базовую конфигурацию
    """
    def configure(self, **params):
        self.update(params)

    def session_configure(self, **params):
        self.setdefault('session_params', {}).update(params)


def make_config():
    return Config()
