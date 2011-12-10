from generator import Generator
from optparse import OptionParser

if __name__ == '__main__':

    usage = """%prog [options] [SOURCEDIR]
            If SOURCEDIR not given, wiki is assumed"""
    desc = """Minimal Viable Wiki
            http://mvw.simplectic.com"""
    version = "0.0.1"

    opts = OptionParser(usage=usage, description=desc, version=version)
    opts.add_option('-d', '--destination', dest='destination', default='_site',
                    help='Source directory of the wiki files')
    (options, args) = opts.parse_args()

    if len(args) == 0:
        source = 'wiki'
    else:
        source = args[0]

    Generator().run(source, options.destination)
