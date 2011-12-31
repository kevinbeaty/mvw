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

        by_title = lambda p: p.title

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
            child_indexes = [os.path.join(destpath, d, 'index.html') for d in dirs]

            pages = [TemplatePage(self, p['dest']) for p in sources]
            children = [TemplatePage(self, c) for c in child_indexes]

            pages.sort(key=by_title)
            children.sort(key=by_title)

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

    def parse(self, source, destination, pages=None):
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

        meta = {k: ' '.join(v) for k, v in md.Meta.items()}
        context['Meta'] = md.Meta
        context['meta'] = meta

        # Load theme from meta data if set
        theme = meta.get('theme', 'default')
        exts = self.config.get_markdown_extensions(theme=theme)
        md = Markdown(extensions=exts)

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


class TemplatePage:
    """
    Encapsulates data for a page to include in the template
    """

    def __init__(self, generator, destination):
        self.title = generator.title(destination)
        prefix = len(generator.config.outputdir)
        self.url = destination[prefix:].replace(os.path.sep, "/")
