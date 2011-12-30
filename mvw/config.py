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

    def __init__(self, mvw_root):
        """
        Initializes with mvw root (.mvw directory)
        """

        mvw_root = os.path.normpath(mvw_root)

        self.sourcedir = os.path.split(mvw_root)[0]
        self.outputdir = os.path.join(mvw_root, 'site')
        self.themedir = os.path.join(mvw_root, 'theme')

        # Load config
        default = os.path.join(mvw_root, 'config.yaml')
        if os.path.isfile(default):
            with codecs.open(default, encoding='utf-8') as src:
                self.config = yaml.load(src)
        else:
            # No config is OK, we'll just use defaults
            self.config = {}

        # Setup template environment
        template = os.path.join(self.themedir, 'template')
        if os.path.exists(template):
            self.environment = Environment(loader=FileSystemLoader(template))
        else:
            raise Exception(
                """
                Cannot find theme templates in %s.
                This may have been caused by running mvw init with a
                previous version that did not support custom themes.

                To reset to default theme:
                $ cd %s
                $ rm -rf .mvw
                $ mvw init
                $ mvw generate

                """ % (template, self.sourcedir))

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
