#!/usr/bin/env python

from mvw.generator import Generator
from optparse import OptionParser
import os
import sys


def run():
    """
    Entry Point for MVW
    """

    usage = """
            %prog init : Initializes MVW at the current directory
            %prog generate : Generates the site
            """
    desc = """Minimal Viable Wiki
            http://mvw.simplectic.com"""
    version = "0.0.1"

    opts = OptionParser(usage=usage, description=desc, version=version)
    (options, args) = opts.parse_args()

    if len(args) == 0:
        opts.print_usage()
        sys.exit(-1)

    command = args[0]

    start = os.getcwd()
    if command == "init":
        init(start)
    elif command == "generate":
        generate(start)
    else:
        opts.print_usage()
        sys.exit(-2)


def init(start):
    """
    mvw init
    Initializes the repository at the specified directory
    """

    root = get_root(start)
    if root is None:
        os.mkdir(os.path.join(start, '.mvw'))
    else:
        print("Cannot init within existing wiki: %s" % root)
        sys.exit(-3)


def generate(start):
    """
    Generates the site for the current wiki.
    Searches up the directory tree for a .mvw directory
    and generates the site into .mvw/site
    """

    root = get_root(start)
    if root is None:
        print("Run mvw init on the root directory of wiki")
        sys.exit(-4)

    destination = os.path.join(root, 'site')
    source = os.path.split(root)[0]

    # Load default theme
    moddir = os.path.dirname(__file__)
    projdir = os.path.normpath(os.path.join(moddir, '..'))
    theme = os.path.join(projdir, 'theme')

    Generator(source, destination, theme).run()


def get_root(path):
    """
    Finds the wiki root.
    Looks for a .mvw directory up the tree
    Returns the path to the root or None if not found
    """

    root = os.path.join(path, '.mvw')
    if os.path.isdir(root):
        return root

    parent = os.path.split(path)[0]
    if parent == '' or parent == path:
        return None
    else:
        return get_root(parent)

if __name__ == '__main__':
    run()
