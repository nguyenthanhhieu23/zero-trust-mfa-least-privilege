import os
from functools import wraps

import jwt
import requests
from flask import Flask, jsonify, request

ISSUER = os.environ.get("KEYCLOAK_ISSUER", "http://localhost:8080/realms/zero-trust")
AUDIENCE = os.environ.get("REQUIRED_AUDIENCE", "zero-trust-demo")
JWKS_URL = os.environ.get(
    "KEYCLOAK_JWKS_URL",
    f"{ISSUER}/protocol/openid-connect/certs",
)

app = Flask(__name__)


def bearer_token():
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


def require_role(*allowed_roles):
    def decorator(handler):
        @wraps(handler)
        def wrapped(*args, **kwargs):
            token = bearer_token()
            if not token:
                return jsonify(error="bearer_token_required"), 401
            try:
                header = jwt.get_unverified_header(token)
                keys = requests.get(JWKS_URL, timeout=5).json()["keys"]
                key_data = next(key for key in keys if key["kid"] == header["kid"])
                key = jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
                claims = jwt.decode(
                    token,
                    key=key,
                    algorithms=["RS256"],
                    audience=AUDIENCE,
                    issuer=ISSUER,
                )
            except (jwt.PyJWTError, requests.RequestException, StopIteration, KeyError):
                return jsonify(error="invalid_token"), 401

            roles = set(claims.get("realm_access", {}).get("roles", []))
            if not roles.intersection(allowed_roles):
                return jsonify(error="insufficient_privilege"), 403
            return handler(claims, *args, **kwargs)

        return wrapped

    return decorator


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/public")
def public_resource():
    return jsonify(resource="public", access="guest,user,admin")


@app.get("/api/user")
@require_role("user", "admin")
def user_resource(claims):
    return jsonify(resource="user-data", subject=claims["sub"])


@app.get("/api/admin")
@require_role("admin")
def admin_resource(claims):
    return jsonify(resource="admin-data", subject=claims["sub"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)