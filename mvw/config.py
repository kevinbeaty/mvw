from jinja2 import Environment, FileSystemLoader

import os
import sys


class Config:
    """ Holds configurable properties of MVW.
    Read by convention and from config.yml """

    def __init__(self):
        # directories relative to mvw root
        self.sourcedir = '..'
        self.outputdir = 'site'
        self.themedir = 'theme'
        self.site_root = '/'
        self.themes = {}
        self.breadcrumb_home = None
        self.port=8000

    def theme(self, theme, content_template=None, markdown_extensions=None):
        self.themes = self.themes or {}
        self.themes[theme] = {
                'content_template': content_template,
                'markdown_extensions': markdown_extensions }
        return self

    def jinja2_environment(self, loader):
        return Environment(loader=loader)

    def load(self, root, defaults):

        root = self.expandpath(root)
        defaults = self.expandpath(defaults)

        # Load sourcedir with default same directory that contains .mvw
        self.sourcedir = self.expandpath(self.sourcedir, root)

        # Load outputdir with default .mvw/site
        self.outputdir = self.expandpath(self.outputdir, root)

        # Load themedir with default .mvw/theme
        self.themedir = self.expandpath(self.themedir, root)
        self.configthemedir = self.themedir

        # Load default theme if themedir does not exist
        if not os.path.isdir(self.themedir):
            self.themedir = os.path.join(defaults, 'theme')

        # Add extensions to path
        extensions = os.path.join(self.themedir, 'extensions')
        if os.path.isdir(extensions):
            sys.path.append(extensions)

        # Setup template environment
        # Use default if template does not exist in theme
        template = os.path.join(self.themedir, 'template')
        if not os.path.isdir(template):
            template = os.path.join(defaults, 'theme', 'template')
        self.environment = self.jinja2_environment(FileSystemLoader(template))

        # Load theme public, using default if does not exist
        themepublic = os.path.join(self.themedir, 'public')
        if not os.path.isdir(themepublic):
            themepublic = os.path.join(defaults, 'theme', 'public')
        self.theme_public = themepublic

        # Set breadcrumb home based on sourcedir if not yet set
        if not self.breadcrumb_home:
            self.breadcrumb_home = self.title(self.sourcedir)

        return self

    def get_content_template(self, theme):
        """ The template to use for parsed content """

        template = self._theme(theme, 'content_template', '%s.html' % theme)

        return self.environment.get_template(template)

    def get_markdown_extensions(self, theme):
        """ List of Python Markdown extensions """

        exts = self._theme(theme, 'markdown_extensions', [
            'codehilite(css_class=syntax,guess_lang=False)'])
        return filter(None, exts)  # Removes empty lines

    def _theme(self, theme, key, default):
        themes = self.themes or {}
        cfg = themes.get(theme, None) or {}
        return cfg.get(key, None) or default

    def title(self, path):
        """ Generates a title for the given path.  """

        base = os.path.basename(path)

        if(base == 'index.html'):
            dirname = os.path.dirname(path)
            if dirname in [self.outputdir, self.sourcedir]:
                return self.breadcrumb_home
            else:
                name = os.path.basename(os.path.dirname(path))
        else:
            name, ext = os.path.splitext(base)

        return name.replace("_", " ").title()

    @staticmethod
    def expandpath(path, root=None):
        """ Fully expands path appending
        root if provided and path is relative """

        path = os.path.normpath(
                os.path.normcase(
                    os.path.expandvars(
                        os.path.expanduser(path))))
        if root and not os.path.isabs(path):
            path = os.path.join(root, path)
        return os.path.abspath(path)
