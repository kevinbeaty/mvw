import os.path
try:
    # Try python 3 packages
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
    from urllib.parse import unquote
except ImportError:
    # Try python 2 packages
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from urllib import unquote


class RequestHandler(SimpleHTTPRequestHandler):
    """
    A SimpleHTTPRequestHandler that serves from the root
    of the generated site and regenerates requested source files
    """
    def do_GET(self):
        """Serve a GET request."""
        content = self._regenerate(self.path)
        if content:
            self._send_regenerated_head(content)
            self.wfile.write(content)
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        """Serve a HEAD request."""
        content = self._regenerate(self.path)
        if content:
            self._send_regenerated_head(content)
        else:
            SimpleHTTPRequestHandler.do_HEAD(self)

    def translate_path(self, path):
        path = self._relpath(path)
        generator = self.server.generator
        return generator.resource_path(path)

    def _regenerate(self, path):
        path = self._relpath(path)
        generator = self.server.generator
        content = generator.regenerate(path)
        if content:
            return content.encode('utf-8')

        return None

    def _relpath(self, path):
        """
        Translates the path to a file name.
        Based on translate_path implementation in
        SimpleHTTPRequestHandler but generates
        relative path, not path from current dir.
        """

        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = os.path.normpath(unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = ''
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word not in (os.curdir, os.pardir):
                path = os.path.join(path, word)

        return path

    def _send_regenerated_head(self, content):
        """ Sends head for regenerated content """
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.send_header("Content-Length", len(content))
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()


class Server(HTTPServer):
    """
    An HTTPServer for MVW
    """
    def __init__(self, generator, address, port):
        self.generator = generator
        print("Starting server on %s:%s" % (address, port))
        HTTPServer.__init__(self, (address, port), RequestHandler)
