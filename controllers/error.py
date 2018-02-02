from flask import *
import flask

import werkzeug.exceptions as ex

def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    print(resp)

    return resp



