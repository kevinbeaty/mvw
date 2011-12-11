import os
import shutil
from markdown import Markdown

class Generator:
    def __init__(self, sourcedir, outputdir, themedir):
        self.sourcedir = os.path.normpath(sourcedir)
        self.outputdir = os.path.normpath(outputdir)
        self.themedir = os.path.normpath(themedir)

    def run(self):
        self.clean()
        self.include_theme()
        self.include_source()

    def clean(self):
        if os.path.exists(self.outputdir):
            shutil.rmtree(self.outputdir)

    def include_theme(self):
        public = os.path.join(self.themedir, 'public')
        if os.path.exists(public):
            shutil.copytree(public, self.outputdir)

    def include_source(self):

        prefix = len(self.sourcedir)+len(os.path.sep)

        for root, dirs, files in os.walk(self.sourcedir):
            destpath = os.path.join(self.outputdir, root[prefix:])
            if not os.path.exists(destpath):
                os.makedirs(destpath)

            for f in files:
                src = os.path.join(root, f)
                base, ext = os.path.splitext(f)
                if ext in ['.md', '.markdown']:
                    dest = os.path.join(destpath, "%s%s" % (base, '.html'))
                    self.parse(src, dest)
                else:
                    dest = os.path.join(destpath, f)
                    shutil.copy(src, dest)

            for d in dirs:
                print(os.path.join(destpath, d))

    def parse(self, source, destination): 
        md = Markdown()
        md.convertFile(source, destination)

