import os
import shutil
from markdown import Markdown

class Generator:
    def __init__(self, sourcedir, outputdir, themedir):
        self.sourcedir = os.path.normpath(sourcedir)
        self.outputdir = os.path.normpath(outputdir)
        self.themedir = os.path.normpath(themedir)

    def run(self):
        self.include_theme()
        self.include_source()

    def include_theme(self):
        print("Include theme %s in %s" % (self.themedir, self.outputdir))

    def include_source(self):

        prefix = len(self.sourcedir)+len(os.path.sep)

        for root, dirs, files in os.walk(self.sourcedir):
            destpath = os.path.join(self.outputdir, root[prefix:])
            if not os.path.exists(destpath):
                os.makedirs(destpath)

            print()
            print('-'*25)
            print('Pages')

            for f in files:
                src = os.path.join(root, f)
                base, ext = os.path.splitext(f)
                if ext in ['.md', '.markdown']:
                    dest = os.path.join(destpath, "%s%s" % (base, '.html'))
                    self.parse(src, dest)
                else:
                    dest = os.path.join(destpath, f)
                    shutil.copy(src, dest)

            print('-'*25)
            print('Dirs')
            for d in dirs:
                print(os.path.join(destpath, d))

    def parse(self, source, destination): 
        md = Markdown()
        md.convertFile(source, destination)

