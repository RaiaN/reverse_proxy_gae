from google.appengine.api.urlfetch import fetch

import webapp2
import urllib

FORMAT_PLIST_AMT = 'plist_amt'

required = set(
    ['accept', 'accept-encoding', 'accept-language', 'connection',
     'user-agent', 'cache-control', 'x-serialize-format',
     'x-gs-cookie', 'x-gs-user-agent', 'x-gs-accept']
)


# def return_basic_headers():
#     h = (
#         {
#             'User-Agent': '0.1-dev/WindowsEditor/0.2/itunes',
#             'Accept': 'protocol/GSAPI.1, format/json',
#             'X-Serialize-Format': 'json'
#         }
#     )
#     h['X-GS-Cookie'] = (
#         'device_identifer=%s;account_type=guest;\
#          account_id=guest;\
#          account_secure=799a1ea440671c73d1124dd0b288df62' % 'Kong6F2D775D10266339A4A0C148F587774D'
#     )
#     return h


class ProxyHandler(webapp2.RequestHandler):
    def post(self, *args, **kwargs):
        path = self.request.path
        if path.startswith("/"):
            path = self.request.path[1:]

        print(path)
        print("REQUEST HEADERS")
        print(self.request.headers)

        payload = self.request.body
        if isinstance(self.request.body, dict):
            payload = urllib.urlencode(self.request.body)
        print(payload)

        request_headers = dict(
            (k.lower(), v) for k, v in self.request.headers.items()
        )
        true_headers = dict(
            ((key, request_headers[key])
             for key in request_headers if key in required)
        )
        true_headers["User-Agent"] = true_headers["x-gs-user-agent"]
        true_headers["Accept"] = true_headers["x-gs-accept"]

        target_url = 'http://dev.tinyarmypanoramic.appspot.com/%s' % path
        response = fetch(
            target_url,
            payload=payload,
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
