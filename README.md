# noseapp_requests
Requests/Requests-Oauthlib extension for NoseApp library

# Usage
```python
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
api = requests_ex.get_endpoint_session('httpbin', auth=('user', 'pass'))
api.get('basic-auth/user/pass')
api.get('get', key1='val1') # GET with query-string parameters
api.post('post', key1='val1') # POST form-encoded data
api.post('post', {'key1': 'val1'}) # POST JSON data
api.get('status/400') # raises HTTPError
```
