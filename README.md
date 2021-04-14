# eve-negotiable-auth
An advanced yet easy to use auth module for APIs built on [Eve](https://docs.python-eve.org/en/stable/).  

The auth class that ships with Eve, `BasicAuth`, allows users of your API to authenticate with [Basic Authentication](https://tools.ietf.org/html/rfc7617).  The `NegotiableAuth` class in this package extends this to allow the user to choose from any authentication scheme your API supports.  This allows for easy configuration and handling of multiple auth schemes - including schemes like [Digest](https://tools.ietf.org/html/rfc7616) which require negotiation.

> NOTE: This package is near-production ready.  Before calling it 1.0 it needs better docs and perhaps a bit more tweaking.  It is already in use in a number of production systems - but use at your own risk!

## Getting Started

The steps are:

1. Create a handler functions for each scheme you support
2. Register those functions with AUTH_PARSER
3. Extend `NegotiableAuth` and override `process_claims()`

### Step 1 - Create handler functions

To handle a scheme you must define at least one function, usually two, which the [authparser](https://pypi.org/project/authparser/) library will call.  You can name them however you like - authparser calls them user_record_fn and challenge_fn

* `user_record_fn(token, **kwargs)` 
* `challenge_fn(**kwargs)` [optional - see  [authparser](https://pypi.org/project/authparser/) for details, mandatory for schemes like `Digest`]

This is best described with an example.  Let's say you want to handle `Bearer` token authorization.  When the time comes to validate the token, your user_record_fn will be called.  So let's create it.  I'll call it `handle_bearer`:

```python
def handle_bearer(token, **kwargs):
    # do stuff to validate the token
    # ...
    # if it checks out, populate the user record:
    record = {
        'user': 'someone@example.com',
        'role': 'employee'
    }
    # if there is a problem (if NegotiableAuth sees '_issues' then it will deny access):
    record = {
        '_issues': {
            'token': 'The token has expired.'
        }
    }
    
    return record
```

### Step 2 - Register the handler functions

The best place to do this is above the class definition you will create in step 3.  I will start by creating a file named **`my_auth.py`**

```python
from eve_negotiable_auth import NegotiableAuth, AUTH_PARSER
from --wherever you defined your handler-- import handle_bearer

AUTH_PARSER.add_handler('Bearer', handle_bearer)
```

Now when the time comes, `NegotiableAuth` will know if it receives a request whose `Authorization` header has a `Bearer` token, it will call your `handle_bearer()` function.

Step 3 - Extend `NegotiableAuth` and override `process_claims()`

The `NegotiableAuth` class is an abstract base class and cannot be used on its own.  You must make your own class that inherits from it.  There is only one function to override: `process_claims()`. 

Building on the **`my_auth.py`** we started in step 2:

```python
from eve_negotiable_auth import NegotiableAuth, AUTH_PARSER
from --wherever you defined your handler-- import handle_bearer

class MyAuth(NegotiableAuth):
    def __init__(self):
        super(MyAuth, self).__init__()
        
    def process_claims(self, claims, allowed_roles, resource, method):
        authorized = 'user' in claims
        role = claims.get('role')

        if resouce = 'salary' and role != 'employer':
            authorized = False
        
        if resource == 'position' and method != 'GET' and role != 'employer':
            authorized = False
        
	    return authorized
     
```

This is a too-simple example for illustration only.  The request will be authorized if `user` exists in claims, unless the request is for `salary` then only employers are allowed.  If it is a `GET` request for `position`, it is allowed for everyone - only employers can `POST`, `PUT`, `DELETE`, etc.

There are many things you can do in your own `process_claims()`.  Please read the [Eve docs](https://docs.python-eve.org/en/stable/authentication.html) for more details.

The things you need to know:

* `claims` is the record returned from your handler function.  
  * If the handler returns falsey, or dict with `_issues`, it will reject the request before your class's `process_claims()` is called
  * your `process_claims()` need only return `True` or `False`, depending whether the `claims` is allowed in or not.
  * As you see, you are in full control of what's in `claims` and how to determine whether to grant access based on what is in the `claims`.
* `allowed_roles`, `resource`, and `method` are passed in from Eve depending on the request and what is in your Eve settings.
* If you are using Eve's [User-Restricted Resource Access](https://docs.python-eve.org/en/stable/authentication.html#user-restricted-resource-access), process_claims() is where you will call `self.set_request_auth_value()`

### Wire it into your project

Once you have defined your auth class, add it to your Eve app.  When you instantiate the app, pass the class name as the `auth` param.

```python
app = Eve('app-name', auth=MyAuth)
```

## Beyond the Basics

When `NegotiableAuth` calls your handler function, it passes the following kwargs to `get_user_record()` 

- allowed_roles
- resource
- method
- request - the flask request object

When you define that function, have it return an dict with each member a claim (e.g. username, email, role).  If the function returns falsey, or a dict that has a member named `_issues`, then access will be denied.  To communicate issues back to the requestor, have `_issues` be a dict of name/value pairs, for example (this example has just one name/value):

```python
{
    '_issues': {
        'user': 'This user does not exist.'
    }
}
```

`get_challenge_header()` - passed through to the scheme's `challenge_fn`

- request

...more docs coming soon...