#!/usr/bin/env python

from flask import Flask, request, Response
from StringIO import StringIO
import requests

app = Flask(__name__)

required = set(
    ['User-Agent', 'Accept', 'Accept-Encoding',
     'Cache-Control', 'Pragma', 'Expires',
     'X-Serialize-Format', 'X-Gs-Cookie']
)


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    request_headers = dict(request.headers.items())
    true_headers = (
        ((key, request_headers[key])
         for key in request_headers if key in required)
    )
    target_url = 'http://tinyarmypanoramic.appspot.com/%s' % path
    response = requests.post(
        target_url,
        headers=dict(true_headers),
        data=request.data
    )
    flask_response = Response(
        StringIO(response.content),
        content_type=response.headers["Content-Type"],
        status=response.status_code,
        headers=response.headers
    )
    return flask_response

if __name__ == '__main__':
    app.run()
