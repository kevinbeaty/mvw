from jinja2 import Environment, FileSystemLoader

import os
import sys


class Config:
    """ Holds configurable properties of MVW.
    Read by convention and from config.yml """

    def __init__(self, config, root, defaults):
        self.config = config or {}

        root = self.expandpath(root)
        defaults = self.expandpath(defaults)

        # Load sourcedir with default same directory that contains .mvw
        self.sourcedir = self.expandpath(
                self.config.get('sourcedir', '..'), root)

        # Load outputdir with default .mvw/site
        self.outputdir = self.expandpath(
                self.config.get('outputdir', 'site'), root)

        # Load themedir with default .mvw/theme
        self.themedir = self.expandpath(self.config.get(
                'themedir', 'theme'), root)
        self.configthemedir = self.themedir

        # Load default theme if themedir does not exist
        if not os.path.isdir(self.themedir):
            self.themedir = os.path.join(defaults, 'theme')

        # Set site root
        self.site_root = self.config.get('site_root', '/')

        # Add extensions to path
        extensions = os.path.join(self.themedir, 'extensions')
        if os.path.isdir(extensions):
            sys.path.append(extensions)

        jinja2_extensions = self.config.get('jinja2_extensions', [])
        jinja2_extensions = filter(None, jinja2_extensions)

        # Setup template environment
        # Use default if template does not exist in theme
        template = os.path.join(self.themedir, 'template')
        if not os.path.isdir(template):
            template = os.path.join(defaults, 'theme', 'template')
        self.environment = Environment(
                loader=FileSystemLoader(template),
                extensions=jinja2_extensions)

        # Load theme public, using default if does not exist
        themepublic = os.path.join(self.themedir, 'public')
        if not os.path.isdir(themepublic):
            themepublic = os.path.join(defaults, 'theme', 'public')
        self.theme_public = themepublic

        # Set breadcrumb home, default sourcedir name
        self.breadcrumb_home = self.config.get('breadcrumb_home',
                self.title(self.sourcedir))

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
        themes = self.config.get('themes', None)
        if not themes:
            return default

        cfg = themes.get(theme, {})
        if not cfg:
            return default

        return cfg.get(key, default)

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
