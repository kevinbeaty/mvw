import os
import shutil
import codecs


class Generator:
    """ Generates the html for the wiki """

    def __init__(self, config):
        self.config = config
        # Site root only valid in generate
        # everything else served from root
        self.site_root = '/'

    def generate(self):
        """ Generates the entire site.
        Cleans the outputdir, includes the theme
        and generates the source into the outputdir """

        config = self.config
        self.site_root = config.site_root
        self.generate_from(config.sourcedir)
        self.generate_from(config.theme_public, copyonly=True)

    def generate_from(self, sourcedir, copyonly=False):
        """ Generates and includes the source into the outputdir """

        if not os.path.exists(sourcedir):
            return

        config = self.config
        outputdir = config.outputdir
        prefix = len(sourcedir) + len(os.path.sep)

        for root, dirs, files in os.walk(sourcedir):
            # Prune hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if not f.startswith('.')]

            destpath = os.path.join(outputdir, root[prefix:])
            if not os.path.exists(destpath):
                os.makedirs(destpath)

            sources = []
            for f in files:
                src = os.path.join(root, f)
                base, ext = os.path.splitext(f)

                if not copyonly and config.is_page(src):
                    dest = os.path.join(destpath, "%s%s" % (base, '.html'))
                    sources.append((src, dest))
                else:
                    dest = os.path.join(destpath, f)
                    shutil.copy(src, dest)

            index = os.path.join(destpath, 'index.html')
            cindexes = [os.path.join(destpath, d, 'index.html') for d in dirs]

            pages = self.pages(p[1] for p in sources)
            children = self.pages(cindexes)

            # Remove previously generated index file to ensure it will
            # be regenerated whether it is a page or not
            if not copyonly and os.path.exists(index):
                os.remove(index)

            # Generate all pages from source
            for p in sources:
                src, dest = p
                self.convert(src, dest, pages, children, True)

            # If index not generated as part of pages, generate
            # an index with empty content
            if not copyonly and not os.path.exists(index):
                self.convert(None, index, pages, children, True)

    def resource_path(self, relpath):
        """ Retrieve a path to a static resource.

        Checks for resources and directories in theme public
        first and then falls back to path into source directory."""

        # Get base name and extension
        dbase, dext = os.path.splitext(os.path.basename(relpath))
        reldir = os.path.dirname(relpath)

        # Return files requested from theme public
        theme_public = self.config.theme_public
        src_public = os.path.join(theme_public, relpath)
        if os.path.exists(src_public):
            return src_public

        # If requesting index in theme public, return directory
        # Ignore requests for index at root since this will
        # be generated from source
        if reldir and not dext:
            themedir = os.path.dirname(src_public)
            if os.path.isdir(themedir):
                return themedir

        # Get resources from source
        return os.path.join(self.config.sourcedir, relpath)

    def regenerate(self, relpath):
        """ Regenerate requested pages given a relative path.

        If requesting an html page, and a source file
        exists, regenerates from source and returns
        content. Otherwise returns None """

        # Get base name and extension
        dbase, dext = os.path.splitext(os.path.basename(relpath))

        if dbase.startswith('.'):
            # Ignore hidden files
            return None

        if not dext:
            # Generate index.html for requested directory
            relpath = os.path.join(relpath, 'index.html')
            dbase = 'index'
            dext = '.html'

        # Try to regenerate from source
        config = self.config
        reldir = os.path.dirname(relpath)
        srcdir = os.path.join(config.sourcedir, reldir)
        if dext != '.html' or not os.path.exists(srcdir):
            # Can only generate html from source in directories that exist
            return None

        destination = os.path.join(config.outputdir, relpath)
        destdir = os.path.dirname(destination)

        source = None
        sources = []
        dests = []
        childdirs = []
        for src in os.listdir(srcdir):

            # Ignore hidden files and directories
            if src.startswith('.'):
                continue

            base, ext = os.path.splitext(os.path.basename(src))
            srcpath = os.path.join(srcdir, src)

            if config.is_page(srcpath):
                sources.append(srcpath)
                dests.append(os.path.join(destdir, "%s%s" % (base, '.html')))
                if base == dbase:
                    source = srcpath
            elif os.path.isdir(srcpath):
                childdirs.append(os.path.join(destdir, src, 'index.html'))

        pages = self.pages(dests)
        children = self.pages(childdirs)

        if source:
            # Convert the existing source file
            return self.convert(source, destination, pages, children)
        elif dbase == 'index':
            # If requesting index, and index source does not exist,
            # generate with empty content
            return self.convert(None, destination, pages, children)
        else:
            return None

    def convert(self, source, destination, pages, children, save=False):

        config = self.config
        site_root = self.site_root
        context = config.template_context(source, destination,
                site_root, pages, children)
        rendered = config.convert(source, **context)

        if save:
            with codecs.open(destination, mode='w', encoding='utf-8') as dst:
                dst.write(rendered)

        return rendered

    def pages(self, dests):
        config = self.config
        site_root = self.site_root
        return config.pages(site_root, dests)
