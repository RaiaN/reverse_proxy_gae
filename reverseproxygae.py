from google.appengine.api.urlfetch import fetch

# import cgi
# import datetime
import webapp2
from StringIO import StringIO
import gzip

required = set(
    ['user-agent', 'accept', 'accept-encoding', 'accept-language',
     'cache-control', 'pragma', 'expires', 'host', 'content-encoding'
     'x-serialize-format', 'x-gs-cookie', 'x-unity-version', 'x-gs-accept']
)


class ProxyHandler(webapp2.RequestHandler):
    def post(self, *args, **kwargs):
        # print(self.request.path)
        # print(self.request.body)
        # print(self.request.headers)
        request_headers = dict(
            (k.lower(), v) for k, v in self.request.headers.items()
        )
        true_headers = (
            ((key, request_headers[key])
             for key in request_headers if key.lower() in required)
        )
        target_url = 'http://dev.tinyarmypanoramic.appspot.com/%s' % self.request.path
        response = fetch(
             target_url, payload=self.request.body, method="POST",
             headers=dict(true_headers), deadline=65
        )
        self.response.content_type = response.headers["Content-Type"]
        self.response.status = response.status_code
        self.response.headers = response.headers
        self.response.headers['Cache-Control'] = (
            'no-cache, must-revalidate'
        )
        self.response.headers['Pragma'] = 'no-cache'
        self.response.headers['Expires'] = 'Thu, 01 Dec 1994 16:00:00'
        print("TEST")
        print(response.content)

        if self.response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(self.response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            content = gzip_f.read()
        else:
            content = response.body
        self.response.out.write(content)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=ProxyHandler)
])
