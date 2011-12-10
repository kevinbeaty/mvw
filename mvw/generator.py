import os

class Generator:
    def run(self, sourcedir, outputdir):
        sourcedir = os.path.normpath(sourcedir)
        outputdir = os.path.normpath(outputdir)
        prefix = len(sourcedir)+len(os.path.sep)
        for root, dirs, files in os.walk(sourcedir):
            relpath = os.path.join(outputdir, root[prefix:])

            print()
            print('-'*25)
            print('Pages')

            for f in files:
                print(os.path.join(relpath, f))

            print('-'*25)
            print('Dirs')
            for d in dirs:
                print(os.path.join(relpath, d))

