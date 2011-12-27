from mako.lookup import TemplateLookup

import os
import yaml


class Config:
    def __init__(self, sourcedir, outputdir, themedir):
        self.outputdir = os.path.normpath(outputdir)
        self.sourcedir = os.path.normpath(sourcedir)
        self.themedir = os.path.normpath(themedir)

        default = os.path.join(sourcedir, '.mvw', 'config')
        if os.path.isfile(default):
            self.default = yaml.load(default)
        else:
            self.default = {}

        template = os.path.join(themedir, 'template')
        if os.path.exists(template):
            self.templatelookup = TemplateLookup(directories=[template])

    def get_content_template(self, source):
        template = self.default.get('content', 'default.html')
        return self.templatelookup.get_template(template)

    def get_index_template(self):
        template = self.default.get('index', 'index.html')
        return self.templatelookup.get_template(template)

    def get_theme_public(self):
        return os.path.join(self.themedir, 'public')
