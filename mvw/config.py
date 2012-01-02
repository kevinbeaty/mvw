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
        """
        Initializes with mvw root (.mvw directory)
        """

        root = os.path.normpath(root)

        # Load config
        default = os.path.join(root, 'config.yaml')

        # Use default config if not exists
        if not os.path.isfile(default):
            default = os.path.join(defaults, 'config.yaml')

        with codecs.open(default, encoding='utf-8') as src:
            self.config = yaml.load(src)

        # Load sourcedir with default same directory that contains .mvw
        self.sourcedir = self.config.get('sourcedir', os.path.split(root)[0])

        # Load outputdir with default .mvw/site
        self.outputdir = self.config.get('outputdir', os.path.join(root, 'site'))

        # Load themedir with default .mvw/theme
        self.themedir = self.config.get('themedir', os.path.join(root, 'theme'))

        # Load default theme if themedir does not exist
        if not os.path.isdir(self.themedir):
            self.themedir = os.path.join(defaults, 'theme')

        # Setup template environment
        template = os.path.join(self.themedir, 'template')

        # Use default if template does not exist in theme
        if not os.path.isdir(template):
            template = os.path.join(defaults, 'theme', 'template')

        self.environment = Environment(loader=FileSystemLoader(template))

        # Add extensions to path if exists
        extensions = os.path.join(self.themedir, 'extensions')
        if os.path.isdir(extensions):
            sys.path.append(extensions)

    def get_breadcrumb_home(self):
        """
        The text for the breadcrumb at the site root
        """

        return self.config.get('breadcrumb_home', 'Home')

    def get_index_template(self):
        """
        The template to use for the index
        """

        template = self.config.get('index_template', 'index.html')
        return self.environment.get_template(template)

    def get_theme_public(self):
        """
        The directory containing all public theme assets (css, images, etc)
        """

        return os.path.join(self.themedir, 'public')

    def get_content_template(self, source, theme):
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
