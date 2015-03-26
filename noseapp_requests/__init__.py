# -*- coding: utf-8 -*-
"""
========================
Setting up the extension
========================

::

    from noseapp.ext.requests import RequestsEx, make_config

    endpoint = make_config()
    endpoint.configure(
        base_url='http://httpbin.org/',
        key='httpbin'
    )
    endpoint.session_configure(
        always_return_json=True,
        raise_on_http_error=True
    )
    requests_ex = RequestsEx(endpoint)

===============
Making requests
===============

Get an API session:

>>> api = requests_ex.get_endpoint_session('httpbin', auth=('user', 'pass'))

Simple *GET* request (if ``always_return_json`` option is set,
response is automatically parsed as JSON into a
``noseapp.datastructures.ModifyDict`` which allows access to values via dot):

>>> api.get('basic-auth/user/pass')
{u'authenticated': True, u'user': u'user'}
>>> r = api.get('basic-auth/user/pass')
>>> r.authenticated
True
>>> r.user
u'user'

*GET* with query-string parameters:

>>> api.get('get', key1='val1')
{u'args': {u'key1': u'val1'},
 <...>
 u'url': u'http://httpbin.org/get?key1=val1'}

*POST* form-encoded data:

>>> api.post('post', key1='val1')
{u'form': {u'key1': u'val1'},
 <...>
 u'url': u'http://httpbin.org/post'}

*POST* JSON data:

>>> api.post('post', {'key1': 'val1'})
{u'data': u'{"key1": "val1"}',
 u'json': {u'key1': u'val1'},
 <...>
 u'url': u'http://httpbin.org/post'}

If ``raise_on_http_error`` option is set,
an exception is raised if response status code is 4xx or 5xx

>>> api.get('status/400')
HTTPError: 400 Client Error: BAD REQUEST

==============
Authentication
==============

You can provide custom authentication class for an endpoint via ``auth_cls``
config parameter:

>>> from requests_oauthlib import OAuth2
>>> endpoint.configure(auth_cls=OAuth2)

Then you can pass authentication parameter in runtime
when getting an API session:

>>> api = requests_ex.get_endpoint_session('oauth2', auth=(client_id, client, token))

"""
from .base import RequestsEx
from .config import make_config

__all__ = (RequestsEx, make_config)
