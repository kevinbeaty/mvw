import os
import shutil
import codecs
from markdown import Markdown
from markdown.extensions.meta import MetaPreprocessor


class Generator:
    """
    Generates the html for the wiki
    """

    def __init__(self, config):
        self.config = config

    def generate(self):
        """
        Generates the entire site.
        Cleans the outputdir, includes the theme
        and generates the source into the outputdir
        """
        config = self.config
        self.generate_from(config.sourcedir)
        self.generate_from(config.get_theme_public(), autoindex=False)

    def generate_from(self, sourcedir, autoindex=True):
        """
        Generates and includes the source into the outputdir
        """
        if not os.path.exists(sourcedir):
            return

        outputdir = self.config.outputdir
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

                if ext in ['.md', '.markdown']:
                    dest = os.path.join(destpath, "%s%s" % (base, '.html'))
                    sources.append(dict(src=src, dest=dest))
                else:
                    dest = os.path.join(destpath, f)
                    shutil.copy(src, dest)

            index = os.path.join(destpath, 'index.html')
            cindexes = [os.path.join(destpath, d, 'index.html') for d in dirs]

            pages = self.pages(p['dest'] for p in sources)
            children = self.pages(cindexes)

            for p in sources:
                self.convert(p['src'], p['dest'], pages, children)

            # If index not generated as part of pages, generate
            # an index with empty content
            if autoindex and not os.path.exists(index):
                self.convert(None, index, pages, children)

    def resource_path(self, relpath):
        """
        Retrieve a path to a static resource.

        Checks for resources and directories in theme public
        first and then falls back to path into source directory.
        """

        # Get base name and extension
        dbase, dext = os.path.splitext(os.path.basename(relpath))
        reldir = os.path.dirname(relpath)

        # Return files requested from theme public
        theme_public = self.config.get_theme_public()
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
        """
        Regenerate requested pages given a relative path.

        If requesting an html page, and a source file
        exists, regenerates from source and returns
        content. Otherwise returns None
        """

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
        reldir = os.path.dirname(relpath)
        srcdir = os.path.join(self.config.sourcedir, reldir)
        if dext != '.html' or not os.path.exists(srcdir):
            # Can only generate html from source in directories that exist
            return None

        destination = os.path.join(self.config.outputdir, relpath)
        destdir = os.path.dirname(destination)

        source_exts = ['.md', '.markdown']
        sources = []
        dests = []
        childdirs = []
        for src in os.listdir(srcdir):
            # Ignore hidden files and directories
            if src.startswith('.'):
                continue

            base, ext = os.path.splitext(os.path.basename(src))
            srcpath = os.path.join(srcdir, src)

            if ext in source_exts:
                sources.append(srcpath)
                dests.append(os.path.join(destdir, "%s%s" % (base, '.html')))
            elif os.path.isdir(srcpath):
                childdirs.append(os.path.join(destdir, src, 'index.html'))

        pages = self.pages(dests)
        children = self.pages(childdirs)

        for source_ext in source_exts:
            source = os.path.join(srcdir, '%s%s' % (dbase, source_ext))
            if source in sources:
                return self.convert(source, destination, pages, children)

        if dbase == 'index':
            # If requesting index, and index source does not exist,
            # generate with empty content
            return self.convert(None, destination, pages, children)

        return None

    def convert(self, source, destination, pages, children):
        """
        Converts the source file and saves to the destination
        """

        breadcrumb = self.breadcrumb(destination)
        pages = [p for p in pages if p not in breadcrumb]
        context = dict(title=self.title(destination),
                       breadcrumb=breadcrumb,
                       pages=pages,
                       children=children)

        content = ""
        theme = 'default'
        meta = {}
        Meta = {}

        if source and os.path.exists(source):
            with codecs.open(source, encoding='utf-8') as src:
                lines = src.readlines()

            # Parse metadata first so we can get theme extensions
            md = Markdown()
            lines = MetaPreprocessor(md).run(lines)

            Meta = md.Meta
            meta = {k: ' '.join(v) for k, v in Meta.items()}

            # Load theme from meta data if set
            theme = meta.get('theme', 'default')
            exts = self.config.get_markdown_extensions(theme=theme)
            md = Markdown(extensions=exts)
            md.Meta = meta  # restore already parsed meta data

            content = md.convert(''.join(lines))

        context['content'] = content
        context['Meta'] = Meta
        context['meta'] = meta

        template = self.config.get_content_template(source, theme=theme)
        rendered = template.render(**context)

        # Write to destination if destination directory exists
        if os.path.isdir(os.path.dirname(destination)):
            with codecs.open(destination, mode='w', encoding='utf-8') as dst:
                dst.write(rendered)

        return rendered

    def breadcrumb(self, destination):
        """
        Generates a breadcrumb for the specified destination file
        """

        outputdir = self.config.outputdir
        prefix = len(outputdir) + len(os.path.sep)
        destdir = os.path.dirname(destination[prefix:])
        dest = destination[:prefix]

        pages = []
        pages.append(TemplatePage(self, os.path.join(outputdir, 'index.html')))
        for p in destdir.split(os.path.sep):
            if len(p) > 0:
                dest = os.path.join(dest, p)
                pages.append(TemplatePage(self, dest))

        return pages

    def title(self, path):
        """
        Generates a title for the given path.
        """

        base = os.path.basename(path)

        if(base == 'index.html'):
            dirname = os.path.dirname(path)
            if dirname in [self.config.outputdir, self.config.sourcedir]:
                return self.config.get_breadcrumb_home()
            else:
                name = os.path.basename(os.path.dirname(path))
        else:
            name, ext = os.path.splitext(base)

        return name.replace("_", " ").title()

    def pages(self, dests):
        pages = [TemplatePage(self, d) for d in dests]
        pages.sort(key=lambda p: p.title)
        return pages


class TemplatePage:
    """
    Encapsulates data for a page to include in the template
    """

    def __init__(self, generator, destination):
        self.title = generator.title(destination)
        prefix = len(generator.config.outputdir)
        self.url = destination[prefix:].replace(os.path.sep, "/")

    def __eq__(self, other):
        return self.url == other.url

    def __ne__(self, other):
        return self.url != other.url
