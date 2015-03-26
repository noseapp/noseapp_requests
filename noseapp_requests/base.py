# -*- coding: utf-8 -*-
from functools import partial

import requests

from noseapp.datastructures import ModifyDict as JsonObjectHook

from .urlbuilder import BaseUrlBuilder


class RequestsExError(BaseException):
    pass


class Session(object):
    """
    Represents an API/requests session. Actual interface is dependent
    on the ``url_builder`` provided; by default it mimics
    :mod:`requests` interface.

    :param base_url: Base URL for endpoint; if provided, default URL builder \
    will prepend it to all URLs provided in method calls.
    :param url_builder: A custom URL builder callable. \
    See :mod:`noseapp_requests.urlbuilder` documentation for details.
    :param bool always_return_json: Parse all responses to JSON if set.
    :param bool raise_on_http_error: Raise HTTPError \
    if response status code >= 400.
    All other keyword arguments are set directly on :class:`requests.Session`.

    Default interface:

    .. py:method:: get(url, **params)
    .. py:method:: post(url, json_object=None, **params)
    .. py:method:: put(url, json_object=None, **params)
    .. py:method:: delete(url, **params)

    All keyword parameters for ``get`` go into query string,
    for other methods they are urlencoded into request body.
    """
    def __init__(self,
                 base_url=None,
                 url_builder=None,
                 always_return_json=False,
                 raise_on_http_error=False,
                 **session_kwargs):

        if not url_builder:
            url_builder = BaseUrlBuilder(base_url)

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
            return resp.json(object_hook=JsonObjectHook)
        else:
            return resp

    def _dispatch(self, method, *args, **kwargs):
        request_params = self._url_builder(method, *args, **kwargs)

        return self._request(**request_params)

    def __getattr__(self, name):
        return partial(self._dispatch, name)


class Endpoint(object):
    """
    Represents an API endpoint.

    :param Config config: endpoint config
    """
    def __init__(self, config):
        self._auth_cls = config.get('auth_cls')

        self._session_config = config.get('session_params', {})
        self._session_config.update(
            base_url=config.get('base_url'),
            url_builder=config.get('url_builder')
        )

    def get_session(self, **kwargs):
        """
        Get API session for the endpoint.

        If ``auth`` argument is provided and ``auth_cls`` parameter
        was present in config, ``auth`` will be passed as arguments
        to ``auth_cls`` instance. All other arguments will be passed
        to :class:`Session` as is.
        """
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
    """
    Extension initializer.

    Usage:

    >>> requests_ex = RequestsEx(ENDPOINT1_CONFIG, ENDPOINT2_CONFIG, ...)

    Each endpoint config represents an API endpoint (basically, a base URL)
    that you need access to in tests. So, for example, if you need to call
    your app's API at http://yourapp.test/api/v1/ and also get data from
    some external source at http://databank.test:6847/, you'll provide
    two configs to the extension:::

        app_config = make_config()
        app_config.configure(base_url='http://yourapp.test/api/v1/')
        databank_config = make_config()
        databank_config.configure(base_url='http://databank.test:6847/')
        requests_ex = RequestsEx(app_config, databank_config)

    Each config can be provided a ``key`` that will be used to refer to it.
    By default, ``base_url`` is used as key.
    """
    name = 'requests'

    def __init__(self, *configs):
        self._endpoints = {}

        for config in configs:
            if config.get('base_url') is not None:
                if 'key' not in config:
                    config['key'] = config['base_url']

            self._endpoints[config['key']] = Endpoint(config)

    def get_endpoint_session(self, endpoint_key, **kwargs):
        """
        Get API session for endpoint ``endpoint_key``. Any additional ``kwargs``
        will be passed to :meth:`Endpoint.get_session`.
        """
        return self._endpoints[endpoint_key].get_session(**kwargs)
