from eve.auth import BasicAuth
from flask import request, abort, make_response, jsonify, g
from authparser import AuthParser


AUTH_PARSER = AuthParser()


class NegotiableAuth(BasicAuth):
    """
    An Eve auth abstract base class that provides for multiple authorization schemes
    where the requester selects which to use.
    """
    def __init__(self):
        pass

    def set_auth_claims(self, claims):
        setattr(g, 'negotiable_auth_claims', claims)

    def get_auth_claims(self):
        return g.get('negotiable_auth_claims', {})

    def set_auth_issue(self, issue):
        setattr(g, 'es_auth_issue', issue)

    def get_auth_issue(self):
        return g.get('es_auth_issue', {})



    def check_auth(self, username, password, allowed_roles, resource, method):
        pass

    def authorized(self, allowed_roles, resource, method):
        auth_header = request.headers.get('Authorization')
        try:
            claims = {}
            if auth_header:
                claims = AUTH_PARSER.get_user_record(auth_header,
                                                    allowed_roles=allowed_roles,
                                                    resource=resource,
                                                    method=method,
                                                    request=request)
            if not claims:
                return False

            if '_issues' in claims:
                self.set_auth_issue(claims['_issues'])
                return False

            self.set_auth_claims(claims)
            authorized = self.process_claims(claims, allowed_roles, resource, method)
        except Exception as ex:
            # TODO: log exception?
            self.set_auth_issue({'user': f'{ex}. Error occurred while trying to process this user.'})
            authorized = False

        return authorized

    def authenticate(self):
        """
        Indicate to the client that it needs to authorize via a 401, and details as to how.
        """
        challenge_header = AUTH_PARSER.get_challenge_header(request=request, single_line=True)

        response_body = {
            '_status': 'ERR',
            '_error': {
                'code': 401,
                'message': 'Please provide proper credentials'
            },
        }
        issue = self.get_auth_issue()
        if issue:
            response_body['_issues'] = [issue]

        resp = make_response(jsonify(response_body), 401)
        resp.headers = {
            **resp.headers,
            **challenge_header
        }
        abort(resp)

    def process_claims(self, claims, allowed_roles, resource, method):
        raise NotImplementedError
