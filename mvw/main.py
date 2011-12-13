#!/usr/bin/env python

from mvw.generator import Generator
from optparse import OptionParser
import os

def run():
    usage = """%prog [options] [SOURCEDIR]
            If SOURCEDIR not given, doc is assumed"""
    desc = """Minimal Viable Wiki
            http://mvw.simplectic.com"""
    version = "0.0.1"

    opts = OptionParser(usage=usage, description=desc, version=version)
    opts.add_option('-d', '--destination', dest='destination', default='_site',
                    help='Source directory of the wiki files')
    opts.add_option('-t', '--theme', dest='theme', default=None,
                    help='Directory containing custom theme, uses default if ommitted')
    (options, args) = opts.parse_args()

    if len(args) == 0:
        source = 'doc'
    else:
        source = args[0]

    theme = options.theme
    if theme is None:
        moddir = os.path.dirname(__file__)
        projdir = os.path.normpath(os.path.join(moddir, '..'))
        theme = os.path.join(projdir, 'theme')

    Generator(source, options.destination, theme).run()

if __name__ == '__main__':
    run()
