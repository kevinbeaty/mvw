from mako.lookup import TemplateLookup

import os
import yaml


class Config:
    def __init__(self, mvw_root):
        mvw_root = os.path.normpath(mvw_root)

        self.sourcedir = os.path.split(mvw_root)[0]
        self.outputdir = os.path.join(mvw_root, 'site')
        self.themedir = os.path.join(mvw_root, 'theme')

        default = os.path.join(mvw_root, 'config.yml')
        if os.path.isfile(default):
            with open(default) as data:
                self.default = yaml.load(data)
        else:
            self.default = {}

        template = os.path.join(self.themedir, 'template')
        if os.path.exists(template):
            self.templatelookup = TemplateLookup(directories=[template])

    def get_breadcrumb_home(self): 
        return self.default.get('breadcrumb_home', 'Home')

    def get_content_template(self, source):
        template = self.default.get('content_template', 'default.html')
        return self.templatelookup.get_template(template)

    def get_index_template(self):
        template = self.default.get('index_template', 'index.html')
        return self.templatelookup.get_template(template)

    def get_theme_public(self):
        return os.path.join(self.themedir, 'public')

    def get_markdown_extensions(self):
        defaults = ['codehilite(css_class=syntax,guess_lang=False)']
        return self.default.get('markdown_extensions', defaults)

