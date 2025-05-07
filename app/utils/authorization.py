from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from functools import wraps


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] not in roles:
                return jsonify(msg="Access forbidden: unauthorized role"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
