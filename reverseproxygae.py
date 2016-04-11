from google.appengine.api.urlfetch import fetch

import gzip
import json
import urllib
import webapp2

from StringIO import StringIO

FORMAT_PLIST_AMT = 'plist_amt'
GZIP_ENCODING = "gzip"

required = set(
    ['accept', 'accept-encoding', 'accept-language', 'connection',
     'user-agent', 'cache-control', 'x-serialize-format',
     'x-gs-cookie', 'x-gs-user-agent', 'x-gs-accept']
)


class ProxyHandler(webapp2.RequestHandler):
    def post(self, *args, **kwargs):
        path = self.request.path
        if path.startswith("/"):
            path = self.request.path[1:]

        print(path)
        print("REQUEST HEADERS")
        print(self.request.headers)
        print(self.request.POST)

        request_headers = dict(
            (k.lower(), v) for k, v in self.request.headers.items()
        )

        json_str = self.request.body
        if request_headers["content-encoding"] == GZIP_ENCODING:
            json_str = gzip.GzipFile(
                fileobj=StringIO(json_str)
            ).read()
        payload = json.loads(json_str.decode('utf-8'))

        true_headers = dict(
            ((key, request_headers[key])
             for key in request_headers if key in required)
        )
        true_headers["User-Agent"] = true_headers["x-gs-user-agent"]
        true_headers["Accept"] = true_headers["x-gs-accept"]

        target_url = 'http://dev.tinyarmypanoramic.appspot.com/%s' % path
        response = fetch(
            target_url,
            payload=urllib.urlencode(payload),
            method="POST",
            headers=true_headers
        )
        self.response.content_type = response.headers["Content-Type"]
        self.response.status = response.status_code

        for k, v in response.headers.items():
            self.response.headers.add(k, v)

        print("RESPONSE HEADERS")
        print(response.headers)

        self.response.out.write(response.content)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=ProxyHandler)
])
