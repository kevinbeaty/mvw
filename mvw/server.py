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
    def translate_path(self, path):
        """
        Translates the path to a file name.
        Based on translate_path implementation in
        SimpleHTTPRequestHandler but starts at
        outputdir instead of cwd.

        Also regenerates requested source files
        """
        generator = self.server.generator

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

        dest = os.path.join(generator.outputdir, path)

        # If requesting an html page, and a source file
        # exists, regenerate. This allows auto regeneration
        # of requested pages if edited while served
        base, ext = os.path.splitext(path)
        if ext == '.html':
            for source_ext in ['.md', '.markdown']:
                source = os.path.join(generator.sourcedir,
                        "%s%s" % (base, source_ext))
                if os.path.exists(source):
                    print("Regenerating %s %s" % (source, dest))
                    generator.parse(source, dest)

        return dest


class Server(HTTPServer):
    """
    An HTTPServer for MVW
    """
    def __init__(self, generator, address, port):
        self.generator = generator
        print("Starting server on %s:%s" % (address, port))
        HTTPServer.__init__(self, (address, port), RequestHandler)