import os
import shutil

class Generator:

    def run(self, sourcedir, outputdir):
        sourcedir = os.path.normpath(sourcedir)
        outputdir = os.path.normpath(outputdir)
        prefix = len(sourcedir)+len(os.path.sep)
        for root, dirs, files in os.walk(sourcedir):
            destpath = os.path.join(outputdir, root[prefix:])
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
        print("Parse Source: %s Destination: %s" % (source, destination))

