try:
    # Try python 3 packages
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
except ImportError:
    # Try python 2 packages
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class RequestHandler(SimpleHTTPRequestHandler):
    """
    A SimpleHTTPRequestHandler that serves from the root
    of the generated site.
    """
    def translate_path(self, path):
        print(self.path)
        return SimpleHTTPRequestHandler.translate_path(self, path)


class Server(HTTPServer):
    """
    An HTTPServer for MVW
    """
    def __init__(self, generator, address, port):
        self.generator = generator
        HTTPServer.__init__(self, (address, port), RequestHandler)
