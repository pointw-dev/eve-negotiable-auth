# eve-negotiable-auth
An auth module for Eve.  Allows for easy configuration and handling of multiple auth schemes - including schemes like Digest which require "negotiation".

`NegotiableAuth` is an abstract base class.  It uses the authparser library, which parses the `Authorization:` header and dispatches to handlers.  As a result, there is only one function to override:

`process_claims(claims, allowed_roles, resource, method)`
This is where you will use the passed to set up the Eve authorization context (e.g. calling `set_request_auth_value()`).
- **claims** - a dict of name-value pairs containing the claims provided by the scheme handlers, derived from parsing the `Authorization:` header
- **allowed_roles** - the user's allowed roles, passed through from BasicAuth
- **resource** - the resource being requested
- **method** - the HTTP verb of the request
- Return True/False whether the user is authenticated.

When NegotiableAuth calls AuthParser, it passes the following kwargs:
`get_user_record()` - passed through to the scheme's `user_record_fn`
- allowed_roles
- resource
- method
- request

`get_challenge_header()` - passed through to the scheme's `challenge_fn`
- request
