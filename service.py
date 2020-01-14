import ntplib
import signal
from time import gmtime,strftime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 80
NTP_POOL = 'uk.pool.ntp.org'

class HTTPHandlerClass(BaseHTTPRequestHandler):
    sys_version=server_version=''

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _text(self, output):
        return output.encode("UTF-8")

    def do_GET(self):
        if (self.path == '/web'):
            self._set_headers(200)
            self.wfile.write(self._text(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
            return
        c = ntplib.NTPClient()
        # Provide the respective ntp server ip in below function
        try:
            response = c.request(NTP_POOL, version=3)
        except ntplib.NTPException:
            self._set_headers(500)
            self.wfile.write(self._text("Timeout connecting to remote ntp server"))
            return

        if abs(response.offset) < 1:
            self._set_headers(200)
            self.wfile.write(self._text("fine " + str(response.offset)))
        else:
            self._set_headers(500)
            self.wfile.write(self._text("not fine " + str(response.offset)))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers(500)
        # Doesn't do anything with posted data
        self._set_headers()



server_address = ('', PORT)
httpd = HTTPServer(server_address, HTTPHandlerClass)
httpd.serve_forever()
