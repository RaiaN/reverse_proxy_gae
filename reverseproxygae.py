from google.appengine.api.urlfetch import fetch
from google.appengine.api import urlfetch

import gzip
import json
import urllib
import webapp2

from StringIO import StringIO


class ProxyHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        print("IT WORKS!")
        print(self.request.headers)
        print(self.request.GET)
        return self.response.out.write("OK")

    def post(self, *args, **kwargs):
        urlfetch.set_default_fetch_deadline(60)

        path = self.request.path
        if path.startswith("/"):
            path = self.request.path[1:]
        print(path)

        request_headers = dict(
            (k.lower(), v) for k, v in self.request.headers.items()
        )
        print("Request headers")
        print(request_headers)

        true_headers = dict(((key, request_headers[key]) for key in request_headers))
        print("True headers")
        print(true_headers)

        target_url = 'http://blitztinyarmypanoramic.appspot.com/%s' % path
        print(target_url)

        response = fetch(
            target_url,
            payload=self.request.body,
            method="POST",
            headers=true_headers,
            deadline=60
        )

        self.response.content_type = 'application/json'
        self.response.status = response.status_code

        for k, v in response.headers.items():
            self.response.headers.add(k, v)

        self.response.out.write(response.content)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=ProxyHandler)
])
