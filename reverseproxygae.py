from google.appengine.api.urlfetch import fetch

# import cgi
# import datetime
import webapp2
from StringIO import StringIO
import gzip

required = set(
    ['accept', 'accept-encoding', 'accept-language', 'connection',
     'user-agent', 'cache-control', 'x-serialize-format',
     'x-gs-cookie']
)


def return_basic_headers():
    h = (
        {
            'User-Agent': '0.1-dev/WindowsEditor/0.2/itunes',
            'Accept': 'protocol/GSAPI.1, format/plist_amt',
            'X-Serialize-Format': 'plist_amt'
        }
    )
    h['X-GS-Cookie'] = (
        'device_identifer=%s;account_type=guest;\
         account_id=guest;\
         account_secure=799a1ea440671c73d1124dd0b288df62' % 'Kong6F2D775D10266339A4A0C148F587774D'
    )
    return h


class ProxyHandler(webapp2.RequestHandler):
    def post(self, *args, **kwargs):
        print("REQUEST HEADERS")
        print(self.request.headers)
        if "ping" in self.request.path:
            true_headers = return_basic_headers()
        else:
            request_headers = dict(
                (k.lower(), v) for k, v in self.request.headers.items()
            )
            true_headers = (
                ((key, request_headers[key])
                 for key in request_headers if key.lower() in required)
            )

        path = self.request.path
        if path.startswith("/"):
            path = self.request.path[1:]
        target_url = 'http://dev.tinyarmypanoramic.appspot.com/%s' % path
        response = fetch(
             target_url, payload=self.request.body, method="POST",
             headers=dict(true_headers)
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
