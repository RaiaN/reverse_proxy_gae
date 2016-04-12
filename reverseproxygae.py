from google.appengine.api.urlfetch import fetch
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

import gzip
import json
import urllib
import webapp2

from StringIO import StringIO

GZIP_ENCODING = "gzip"

required = set(
    ['accept', 'accept-encoding', 'accept-language', 'connection',
     'user-agent', 'cache-control', 'x-serialize-format',
     'x-gs-cookie', 'x-gs-user-agent', 'x-gs-accept']
)


class ProxyHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        print("IT WORKS!")
        print(self.request.headers)
        print(self.request.GET)
        return self.response.out.write("OK")

    def post(self, *args, **kwargs):
        path = self.request.path
        if path.startswith("/"):
            path = self.request.path[1:]

        # print(path)
        # print("REQUEST HEADERS")
        # print(self.request.headers)
        # print(self.request.POST)

        request_headers = dict(
            (k.lower(), v) for k, v in self.request.headers.items()
        )

        json_str = self.request.body
        if "content-encoding" in request_headers and\
                request_headers["content-encoding"] == GZIP_ENCODING:
            json_str = gzip.GzipFile(
                fileobj=StringIO(json_str)
            ).read()
        payload = json.loads(json_str.decode('utf-8'))

        if 'get_parent' in path:
            print(payload)

        true_headers = dict(
            ((key, request_headers[key])
             for key in request_headers if key in required)
        )
        true_headers["User-Agent"] = true_headers["x-gs-user-agent"]
        true_headers["Accept"] = true_headers["x-gs-accept"]

        conditions = ("configs/check_updates" in path,
                      "validate_action/Evolve" in path,
                      "validate_action/Fuse" in path,
                      "validate_action/SellMonsters" in path)
        if any(conditions):
            target_url = 'http://tinyarmypanoramic.appspot.com/%s' % path
        else:
            target_url = 'http://dev.tinyarmypanoramic.appspot.com/%s' % path

        response = fetch(
            target_url,
            payload=urllib.urlencode(payload),
            method="POST",
            headers=true_headers,
            deadline=60
        )

        response_content_type = response.headers["Content-Type"].replace(
            "; charset=utf-8", ""
        )

        self.response.content_type = response_content_type
        self.response.status = response.status_code

        for k, v in response.headers.items():
            self.response.headers.add(k, v)

        if "profile/load" in path:
            if "gs-content-type" not in set(
                key.lower() for key in self.response.headers.keys()
            ):
                self.response.headers.add("gs-content-type", "json")

        # print("RESPONSE HEADERS")
        # print(response.headers)
        # print(self.response.headers)

        self.response.out.write(response.content)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=ProxyHandler)
])
