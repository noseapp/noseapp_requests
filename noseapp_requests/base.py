# -*- coding: utf-8 -*-
from functools import partial

import requests

from noseapp.datastructures import ModifyDict

from .urlbuilder import BaseUrlBuilder


class RequestsExError(BaseException):
    pass


class Session(object):
    def __init__(self,
                 base_url=None,
                 url_builder=None,
                 always_return_json=False,
                 raise_on_http_error=False,
                 **session_kwargs):

        if not url_builder:
            if base_url:
                url_builder = BaseUrlBuilder(base_url)
            else:
                ## Simple pass-through for kwargs parameters
                url_builder = lambda method, **kw: dict(method=method, **kw)

        self._url_builder = url_builder
        self.always_return_json = always_return_json
        self.raise_on_http_error = raise_on_http_error

        self._session = requests.Session()
        for attr, value in session_kwargs.items():
            setattr(self._session, attr, value)

    def _request(self, **kwargs):
        resp = self._session.request(**kwargs)

        if self.raise_on_http_error:
            resp.raise_for_status()

        if self.always_return_json:
            return resp.json(object_hook=ModifyDict)
        else:
            return resp

    def _dispatch(self, method, *args, **kwargs):
        request_params = self._url_builder(method, *args, **kwargs)

        return self._request(**request_params)

    def __getattr__(self, name):
        return partial(self._dispatch, name)


class Endpoint(object):
    def __init__(self, config):
        self._auth_cls = config.get('auth_cls')

        self._session_config = config.get('session_params', {})
        self._session_config.update(
            base_url=config.get('base_url'),
            url_builder=config.get('url_builder')
        )

    def get_session(self, **kwargs):
        if self._auth_cls is not None:
            try:
                kwargs['auth'] = self._auth_cls(*kwargs['auth'])
            except KeyError:
                raise RequestsExError(
                    'Auth class was set up, but no auth args were provided'
                )

        session_kwargs = self._session_config.copy()
        session_kwargs.update(kwargs)

        return Session(**session_kwargs)


class RequestsEx(object):
    name = 'requests'

    def __init__(self, *configs):
        self._endpoints = {}

        for config in configs:
            if config.get('base_url') is not None:
                if 'key' not in config:
                    config['key'] = config['base_url']

            self._endpoints[config['key']] = Endpoint(config)

    def get_endpoint_session(self, endpoint_key, *args, **kwargs):
        return self._endpoints[endpoint_key].get_session(*args, **kwargs)
