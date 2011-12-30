from jinja2 import Environment, FileSystemLoader
from markdown import Markdown

import os
import sys
import codecs


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
        default = os.path.join(mvw_root, 'config.md')
        if os.path.isfile(default):
            md = Markdown(extensions=['meta'])
            with codecs.open(default, encoding='utf-8') as src:
                md.convert(src.read())
                self.default = md.Meta
        else:
            # No config is OK, we'll just use defaults
            self.default = {}

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

        return self.default.get('breadcrumb-home', ['Home'])[0]

    def get_content_template(self, source, **context):
        """
        The template to use for parsed content
        """
        theme = context.get('meta', {}).get('theme', None)
        if theme is None:
            template = self.default.get('content-template', ['default.html'])[0]
        else:
            template = '%s.html' % theme

        return self.environment.get_template(template)

    def get_index_template(self):
        """
        The template to use for the index
        """

        template = self.default.get('index-template', ['index.html'])[0]
        return self.environment.get_template(template)

    def get_theme_public(self):
        """
        The directory containing all public theme assets (css, images, etc)
        """

        return os.path.join(self.themedir, 'public')

    def get_markdown_extensions(self):
        """
        List of Python Markdown extesions
        """

        exts = self.default.get('markdown-extensions', [])
        return filter(None, exts)  # Removes empty lines
