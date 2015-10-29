Devourer
========

[![Build Status](https://travis-ci.org/bonnierpolska/devourer.svg)](https://travis-ci.org/bonnierpolska/devourer)

Devourer is a generic API client for Python 2.7 and 3.3+.

It features an object-oriented, declarative approach to simplify the communication.
It depends on the brilliant requests package as the gateway to API server. A simple example:

```python
from devourer import GenericAPI, APIMethod, APIError


class TestApi(GenericAPI):
    posts = APIMethod('get', 'posts/')
    comments = APIMethod('get', 'posts/{id}/comments')
    post = APIMethod('get', 'posts/{id}/')
    add_post = APIMethod('post', 'posts/')

    def __init__(self):
        super(TestApi, self).__init__('http://jsonplaceholder.typicode.com/',
                                      None,  # this can be ('user', 'password')
                                             # or requests auth object
                                      load_json=True,
                                      throw_on_error=True
                                     )
                                     
api = TestApi()
posts = api.posts()
post = api.post(id=posts[0]['id'])
comments = api.comments(id=post['id'])
new_post_id = api.add_post(userId=1,
                           title='Breaking news',
                           body='I just got devoured.')
try:
    post = api.post(id=new_post_id)
except APIError:
    print('Oops, this API is not persistent!')
```

The init function gives details so you don't need to repeat them elsewhere, enables parsing json responses and
raising exceptions on error. You can also obtain raw string with `load_json=False` and silence errors getting
None instead when they happen with `throw_on_error=False`.

Installation
------------
You can just `pip install devourer`.

Documentation
-------------

Feel free to browse the code and especially the tests to see what's going on behind the scenes.
The current version of docs is available on http://devourer.readthedocs.org/en/latest/.

Questions and contact
---------------------

If you have any questions, feedback, want to say hi or talk about Python, just hit me up on
https://twitter.com/bujniewicz

Contributions
-------------

Please read CONTRIBUTORS file before submitting a pull request.

We use Travis CI. The targets are 10.00 for lint 10.00 and 100% for coverage, as well as building sphinx docs.

You can of also check the build manually, just make sure to `pip install -r requirements.txt` before:

```
pylint devourer --rcfile=.pylintrc
coverage run --source=devourer -m devourer.tests && coverage report -m
cd docs && make html
```