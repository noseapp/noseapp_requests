# -*- coding: utf-8 -*-
"""Here be dragons."""
import urlparse


class BaseUrlBuilder(object):
    SUPPORTED_METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, base_url):
        self.base_url = base_url

    def __call__(self, method, url, json_object=None, **params):
        if method not in self.SUPPORTED_METHODS:
            raise AttributeError(
                "Method {} not supported by {}!".format(method, self.__class__)
            )

        if self.base_url:
            url = urlparse.urljoin(self.base_url, url)

        ret_params = {
            'method': method,
            'url': url
        }

        if json_object is not None:
            ret_params['json'] = json_object

        elif method == 'get' and params:
            ret_params['params'] = params

        elif params:
            ret_params['data'] = params

        return ret_params
