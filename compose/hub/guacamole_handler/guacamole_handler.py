"""
Fetch a token from Guacamole

https://github.com/jupyterhub/jupyterhub/blob/5.0.0/examples/service-whoami/whoami-oauth.py
"""
import json
import os
from urllib.parse import urlparse

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.web import authenticated
from tornado.web import HTTPError
from tornado.web import RequestHandler

from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.services.auth import HubOAuthenticated
from jupyterhub.utils import url_path_join

from base64 import standard_b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hmac
import hashlib
import json
from time import time
from tornado.escape import url_escape
from http.client import responses

from tornado.log import app_log
log = app_log

GUACAMOLE_HOST = os.environ["GUACAMOLE_HOST"]
GUACAMOLE_PUBLIC_HOST = os.environ["GUACAMOLE_PUBLIC_HOST"]
JSON_SECRET_KEY = os.environ["JSON_SECRET_KEY"]


def sign(key, message):
    # openssl dgst -sha256 -mac HMAC -macopt hexkey:"$KEY" -binary <data>
    signature = hmac.new(bytes.fromhex(key), message, hashlib.sha256).digest()
    return signature


def encrypt(key, message):
    # openssl enc -aes-128-cbc -K "$KEY" -iv "$NULL_IV" -nosalt -a <stdin>
    null_iv = 32 * "0"

    # pkcs7 padding
    pad = 16 - (len(message) % 16)
    padding = bytes([pad] * pad)

    cipher = Cipher(algorithms.AES128(bytes.fromhex(key)), modes.CBC(bytes.fromhex(null_iv)))
    encryptor = cipher.encryptor()
    ct = encryptor.update(message + padding) + encryptor.finalize()
    return ct


async def guacamole_url(username):
    expiry_ms = int(time() * 1000) + 60000
    data = {
        "username": username,
        "expires": expiry_ms,
        "connections": {
            f"jupyter-{username}": {
                "protocol": "vnc",
                "parameters": {
                    "hostname": f"jupyter-{username}",
                    "port":"5901",
                }
            },
        }
    }
    message = json.dumps(data).encode()

    signature = sign(JSON_SECRET_KEY, message)
    ciphertext = encrypt(JSON_SECRET_KEY, signature + message)

    http_client = AsyncHTTPClient()
    body = "data=" + url_escape(standard_b64encode(ciphertext))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "content-length": str(len(body)),
    }
    log.error(f"Fetching http://{GUACAMOLE_HOST}/guacamole/api/tokens {message}")
    request = HTTPRequest(
        f"http://{GUACAMOLE_HOST}/guacamole/api/tokens",
        "POST",
        headers=headers,
        body=body,
    )
    response = await http_client.fetch(request)
    if response.error:
        d = response.error
        log.error(f"ERROR [guacamole]: {d}")
        raise HTTPError(500, "Failed to get Guacamole token")
    else:
        d = json.loads(response.body)
    return d


class GuacamoleHandler(HubOAuthenticated, RequestHandler):
    @authenticated
    async def get(self):
        user_model = self.get_current_user()
        log.debug(f"user_model: {user_model}")

        # Note if server field is missing (not just empty) this means the oauth
        # scopes are missing
        if not user_model["server"]:
            # This may be out of date, make an API call to refresh server info
            log.error(f"user_model: {user_model}")

            token = self.hub_auth.get_token(self)
            http_client = AsyncHTTPClient()
            response = await http_client.fetch(
                f"{self.hub_auth.api_url}/user",
                headers={"Authorization": f"token {token}"},
            )
            if response.error:
                raise HTTPError(500, reason="Failed to get user info")

            user = json.loads(response.body)
            if not user["server"]:
                log.error(f"user: {user_model}")
                raise HTTPError(409, reason="User's server is not running")

        d = await guacamole_url(user_model["name"])
        # log.debug(d)
        url = f"http://{GUACAMOLE_PUBLIC_HOST}/guacamole/#/client/?token={d['authToken']}"

        # self.set_header("content-type", "application/json")
        # self.write(json.dumps(d, indent=2, sort_keys=True))
        # self.redirect(url)
        self.render("index.html", guacamole_url=url)

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info")
        reason = responses.get(status_code, "Unknown HTTP Error")
        message = ""
        if exc_info:
            exception = exc_info[1]
            r = getattr(exception, "reason", "")
            if r:
                reason = r
            message = getattr(exception, "message", "")

        self.set_status(status_code, reason)
        self.render("error.html", status_code=status_code, reason=reason, message=message)


def main():
    app = Application(
        [
            (os.environ['JUPYTERHUB_SERVICE_PREFIX'], GuacamoleHandler),
            (
                url_path_join(
                    os.environ['JUPYTERHUB_SERVICE_PREFIX'], 'oauth_callback'
                ),
                HubOAuthCallbackHandler,
            ),
            (r'.*', GuacamoleHandler),
        ],
        cookie_secret=os.urandom(32),
    )

    http_server = HTTPServer(app)
    url = urlparse(os.environ['JUPYTERHUB_SERVICE_URL'])

    http_server.listen(url.port, url.hostname)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
