from jinja2 import Environment, FileSystemLoader

import os
import sys
import codecs
import yaml


class Config:
    """
    Holds configurable properties of MVW.
    Read by convention and from config.yml
    """

    def __init__(self, root, defaults):
        if not root:
            root = os.path.join(os.getcwd(), '.mvw')

        root = self.expandpath(root)
        defaults = self.expandpath(defaults)

        # Load config
        default = os.path.join(root, 'config.yaml')

        # Use default config if not exists
        if not os.path.isfile(default):
            default = os.path.join(defaults, 'config.yaml')

        with codecs.open(default, encoding='utf-8') as src:
            self.config = yaml.load(src)

        # Load sourcedir with default same directory that contains .mvw
        self.sourcedir = self.expandpath(
                self.config.get('sourcedir', '..'), root)

        # Load outputdir with default .mvw/site
        self.outputdir = self.expandpath(
                self.config.get('outputdir', 'site'), root)

        # Load themedir with default .mvw/theme
        self.themedir = self.expandpath(self.config.get(
                'themedir', 'theme'), root)

        # Load default theme if themedir does not exist
        if not os.path.isdir(self.themedir):
            self.themedir = os.path.join(defaults, 'theme')

        # Setup template environment
        template = os.path.join(self.themedir, 'template')

        # Use default if template does not exist in theme
        if not os.path.isdir(template):
            template = os.path.join(defaults, 'theme', 'template')
        self.environment = Environment(loader=FileSystemLoader(template))

        # Add extensions to path
        extensions = os.path.join(self.themedir, 'extensions')
        if not os.path.isdir(extensions):
            template = os.path.join(defaults, 'theme', 'extensions')
        sys.path.append(extensions)

    @property
    def breadcrumb_home(self):
        """
        The text for the breadcrumb at the site root
        """

        return self.config.get('breadcrumb_home', 'Home')

    @property
    def theme_public(self):
        """
        The directory containing all public theme assets (css, images, etc)
        """

        return os.path.join(self.themedir, 'public')

    @property
    def site_root(self):
        """
        Returns the site root to be used when generating URLs.
        """
        return self.config.get('site_root', '/')

    def get_content_template(self, theme):
        """
        The template to use for parsed content
        """
        template = self._theme(theme, 'content_template', 'default.html')

        return self.environment.get_template(template)

    def get_markdown_extensions(self, theme):
        """
        List of Python Markdown extensions
        """
        exts = self._theme(theme, 'markdown_extensions', [])
        return filter(None, exts)  # Removes empty lines

    def _theme(self, theme, key, default):
        cfg = self.config.get('themes', {}).get(theme, {})
        return cfg.get(key, default)

    @staticmethod
    def expandpath(path, root=None):
        """ Fully expands path appending
        root if provided and path is relative
        """
        path = os.path.normpath(
                os.path.normcase(
                    os.path.expandvars(
                        os.path.expanduser(path))))
        if root and not os.path.isabs(path):
            path = os.path.join(root, path)
        return os.path.abspath(path)
