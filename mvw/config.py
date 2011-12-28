from mako.lookup import TemplateLookup
from markdown import Markdown

import os
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

        default = os.path.join(mvw_root, 'config.md')
        if os.path.isfile(default):
            md = Markdown(extensions=['meta'])
            with codecs.open(default, encoding='utf-8') as src:
                md.convert(src.read())
                self.default = md.Meta
        else:
            # No config.yml is OK, we'll just use defaults
            self.default = {}

        template = os.path.join(self.themedir, 'template')
        if os.path.exists(template):
            self.templatelookup = TemplateLookup(directories=[template])
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

    def get_breadcrumb_home(self):
        """
        The text for the breadcrumb at the site root
        """

        return self.default.get('breadcrumb-home', ['Home'])[0]

    def get_content_template(self, source):
        """
        The template to use for parsed content
        """

        template = self.default.get('content-template', ['default.html'])[0]
        return self.templatelookup.get_template(template)

    def get_index_template(self):
        """
        The template to use for the index
        """

        template = self.default.get('index-template', ['index.html'])[0]
        return self.templatelookup.get_template(template)

    def get_theme_public(self):
        """
        The directory containing all public theme assets (css, images, etc)
        """

        return os.path.join(self.themedir, 'public')

    def get_markdown_extensions(self):
        """
        List of Python Markdown extesions
        """

        return self.default.get('markdown-extensions', [])
