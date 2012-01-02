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

    def run(self):
        """
        Generates the entire site.
        Cleans the outputdir, includes the theme
        and generates the source into the outputdir
        """

        self.clean()
        self.include_theme()
        self.include_source()

    def clean(self):
        """
        Cleans (rm -rf) the outputdir
        """
        outputdir = self.config.outputdir
        if os.path.exists(outputdir):
            shutil.rmtree(outputdir)

    def include_theme(self):
        """
        Includes the theme in the outputdir
        """
        outputdir = self.config.outputdir
        public = self.config.get_theme_public()
        if os.path.exists(public):
            shutil.copytree(public, outputdir)

    def include_source(self):
        """
        Generates and includes the source into the outputdir
        """
        sourcedir = self.config.sourcedir
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

            pages = [TemplatePage(self, p['dest']) for p in sources]
            children = [TemplatePage(self, c) for c in cindexes]

            _pagesort(pages)
            _pagesort(children)

            for p in sources:
                self.parse(p['src'], p['dest'], pages)

            self.include_index(index, pages, children)

    def include_index(self, destination, pages, children):
        """
        Includes the index page for the specified destination
        pages and children
        """
        template = self.config.get_index_template()
        rendered = template.render(pages=pages,
                                   children=children,
                                   title=self.title(destination),
                                   breadcrumb=self.breadcrumb(destination),
                                   Meta={}, meta={})
        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)

    def regenerate(self, relpath):
        """
        Regenerate requested pages and resources given
        a relative path.

        If resource is available in theme public, copy.

        If requesting an html page, and a source file
        exists, regenerate.
        """

        # Get base name and extension
        dbase, dext = os.path.splitext(os.path.basename(relpath))

        if dbase.startswith('.'):
            # Ignore hidden files
            return

        if not dext:
            # Generate index.html for requested directory
            relpath = os.path.join(relpath, 'index.html')
            dbase = 'index'
            dext = '.html'

        destination = os.path.join(self.config.outputdir, relpath)
        destdir = os.path.dirname(destination)
        reldir = os.path.dirname(relpath)
        srcdir = os.path.join(self.config.sourcedir, reldir)

        # Copy files requested from theme public
        theme_public = self.config.get_theme_public()
        src_public = os.path.join(theme_public, relpath)
        if os.path.exists(src_public):
            print('Copying %s to %s' % (src_public, destdir))
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            shutil.copy(src_public, destdir)
            return

        # If requesting index in theme public, copy tree
        # Ignore requests for index at root since this will
        # be generated from source
        if reldir and dbase == 'index':
            themedir = os.path.dirname(src_public)
            if os.path.isdir(themedir):
                print('Copying tree %s to %s' % (themedir, destdir))
                if os.path.exists(destdir):
                    shutil.rmtree(destdir)
                shutil.copytree(themedir, destdir)
                return

        # Try to regenerate from source
        if dext != '.html' or not os.path.exists(srcdir):
            # Can only generate html from source in directories that exist
            return

        source_exts = ['.md', '.markdown']
        sources = []
        dests = []
        childdirs = []
        for src in os.listdir(srcdir):
            # Ignore hidden files and directories
            if src.startswith('.'):
                continue

            base, ext = os.path.splitext(os.path.basename(src))

            if ext in source_exts:
                sources.append(os.path.join(srcdir, src))
                dests.append(os.path.join(destdir, "%s%s" % (base, '.html')))
            elif os.path.isdir(src):
                childdirs.append(os.path.join(destdir, src, 'index.html'))

        pages = [TemplatePage(self, d) for d in dests]
        _pagesort(pages)

        if dbase == 'index':
            print("Regenerating Index %s" % destination)
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            children = [TemplatePage(self, c) for c in childdirs]
            _pagesort(children)
            self.include_index(destination, pages, children)
            return

        for source_ext in source_exts:
            source = os.path.join(srcdir, '%s%s' % (dbase, source_ext))
            if source in sources:
                print("Regenerating %s %s" % (source, destination))
                if not os.path.exists(destdir):
                    os.makedirs(destdir)
                self.parse(source, destination, pages)

    def parse(self, source, destination, pages):
        """
        Parses the source file and saves to the destination
        """

        context = dict(title=self.title(destination),
                       breadcrumb=self.breadcrumb(destination),
                       pages=pages)

        with codecs.open(source, encoding='utf-8') as src:
            lines = src.readlines()

        # Parse metadata first so we can get theme extensions
        md = Markdown()
        lines = MetaPreprocessor(md).run(lines)

        Meta = md.Meta
        meta = {k: ' '.join(v) for k, v in Meta.items()}
        context['Meta'] = Meta
        context['meta'] = meta

        # Load theme from meta data if set
        theme = meta.get('theme', 'default')
        exts = self.config.get_markdown_extensions(theme=theme)
        md = Markdown(extensions=exts)
        md.Meta = meta  # restore already parsed meta data

        context['content'] = md.convert(''.join(lines))

        template = self.config.get_content_template(source, theme=theme)
        rendered = template.render(**context)

        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)

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

def _pagesort(pages):
    pages.sort(key=lambda p: p.title)

class TemplatePage:
    """
    Encapsulates data for a page to include in the template
    """

    def __init__(self, generator, destination):
        self.title = generator.title(destination)
        prefix = len(generator.config.outputdir)
        self.url = destination[prefix:].replace(os.path.sep, "/")

