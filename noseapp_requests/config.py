# -*- coding: utf-8 -*-
class Config(dict):
    """
    Extension configuration.
    """
    def configure(self, **params):
        """
        Set endpoint configuration params.

        :param key: A key that will be used to refer to the endpoint.
        :param base_url: Base URL for endpoint.
        :param auth_cls: Authentication class to use with endpoint, \
        e.g. :class:`requests_oauthlib.OAuth2`.
        """
        self.update(params)

    def session_configure(self, **params):
        """
        Set common session params.

        :param bool always_return_json: Parse all responses to JSON if set.
        :param bool raise_on_http_error: Raise HTTPError \
        if response status code >= 400.
        :param: + Any params for :func:`requests.request` or :class:`requests.Session`
        """
        self.setdefault('session_params', {}).update(params)


def make_config():
    """Return :class:`Config` instance with default values."""
    return Config()
