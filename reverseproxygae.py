from google.appengine.api.urlfetch import fetch

# import cgi
# import datetime
import webapp2


required = set(
    ['User-Agent', 'Accept', 'Accept-Encoding',
     'Cache-Control', 'Pragma', 'Expires',
     'X-Serialize-Format', 'X-Gs-Cookie']
)


class ProxyHandler(webapp2.RequestHandler):
    def post(self, *args, **kwargs):
        request_headers = dict(self.request.headers.items())
        true_headers = (
            ((key, request_headers[key])
             for key in request_headers if key in required)
        )
        print(self.request.path)
        print(self.request.body)
        print(self.request.headers)
        target_url = 'http://tinyarmypanoramic.appspot.com/%s' % self.request.path
        response = fetch(
             target_url, payload=self.request.body, method="POST",
             headers=dict(true_headers)
        )
        self.response.content_type = response.headers["Content-Type"]
        self.response.status = response.status_code
        self.response.headers = response.headers
        self.response.headers['Cache-Control'] = (
            'no-cache, must-revalidate'
        )
        self.response.headers['Pragma'] = 'no-cache'
        self.response.headers['Expires'] = 'Thu, 01 Dec 1994 16:00:00'
        self.response.out.write(response.content)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/<:.*>', handler=ProxyHandler)
])
