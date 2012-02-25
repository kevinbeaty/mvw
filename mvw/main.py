#!/usr/bin/env python

from mvw.config import Config
from mvw.generator import Generator
from mvw.server import Server
from optparse import OptionParser
import imp
import os
import shutil
import sys


def run():
    """ Entry Point for MVW """

    usage = """
            %prog [serve] : Serve the wiki locally
            %prog init : Initializes MVW at the current directory
            %prog generate : Generates the static site
            %prog theme : Copies the default theme into configured
                theme directory (default .mvw/theme) for customization
            %prog config : Copies the sample mvwconfig.py into mvw root
                for customization.
            """
    desc = """Minimal Viable Wiki
            http://simplectic.com/mvw"""
    version = "0.0.1"

    opts = OptionParser(usage=usage, description=desc, version=version)
    (options, args) = opts.parse_args()

    if len(args) == 0:
        command = "serve"
    elif len(args) == 1:
        command = args[0]
    else:
        opts.print_usage()
        sys.exit(-1)

    start = os.getcwd()
    if command == "init":
        result = init(start)
    elif command == "generate":
        result = generate(start)
    elif command == "serve":
        result = serve(start)
    elif command == "theme":
        result = theme(start)
    elif command == "config":
        result = config(start)
    else:
        opts.print_usage()
        sys.exit(-2)

    if not result:
        sys.exit(-3)


def init(start):
    """ mvw init
    Initializes the repository at the specified directory
    """

    root = get_root(start)
    if root is None:
        root = os.path.join(start, '.mvw')
        os.mkdir(root)
    else:
        print("Cannot init within existing wiki: %s" % root)
        return None
    return root


def config(start):
    """ mvw config
    Copies the sample mvwconfig.py into mvw root
    """

    root = get_root(start)
    if root is None:
        root = init(start)

    defaults = get_defaults()
    config = os.path.join(defaults, 'mvwconfig.py')
    mvwconfig = os.path.join(root, 'mvwconfig.py')
    if not os.path.exists(mvwconfig):
        shutil.copy(config, root)
    else:
        print("Will not overwrite existing mvwconfig.py %s" % mvwconfig)
        return False

    return True


def generate(start):
    """ mvw generate
    Generates the site for the current wiki.
    Searches up the directory tree for a .mvw directory
    and generates the site into .mvw/site
    """
    Generator(create_config(start)).generate()
    return True


def serve(start):
    config = create_config(start)
    generator = Generator(config)
    server = Server(generator, '127.0.0.1', config.port)
    server.serve_forever()
    return True


def create_config(start):
    root = get_root(start)

    # If no mvw root, use working directory
    config = None
    if root is None:
        root = os.path.join(start, '.mvw')
    else:
        mvwconfigpath = Config.expandpath('mvwconfig.py', root)
        if os.path.isfile(mvwconfigpath):
            mvwconfig = imp.load_source('mvwconfig', mvwconfigpath)
            config = mvwconfig.config

    if config is None:
        config = Config()

    return config.load(root, get_defaults())


def theme(start):
    """ mvw theme
    Copies the default theme into the configured directory.
    """

    root = get_root(start)
    if root is None:
        root = init(start)

    config = create_config(start)
    themedir = config.themedir
    configthemedir = config.configthemedir

    if themedir != configthemedir and \
        not os.path.exists(configthemedir):
        shutil.copytree(themedir, configthemedir)
    else:
        print("Will not overwrite existing themedir %s" % configthemedir)
        return False

    return True


def get_root(path):
    """ Finds the wiki root.
    Looks for a .mvw directory up the tree
    Returns the path to the root or None if not found """

    root = os.path.join(path, '.mvw')
    if os.path.isdir(root):
        return root

    parent = os.path.split(path)[0]
    if parent == '' or parent == path:
        return None
    else:
        return get_root(parent)


def get_defaults():
    moddir = os.path.dirname(__file__)
    return os.path.join(moddir, 'defaults')

if __name__ == '__main__':
    run()
