import os
import shutil
import codecs
from markdown import Markdown


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

            pages = []
            for f in files:
                src = os.path.join(root, f)
                base, ext = os.path.splitext(f)

                if ext in ['.md', '.markdown']:
                    dest = os.path.join(destpath, "%s%s" % (base, '.html'))
                    self.parse(src, dest)
                    pages.append(dest)
                else:
                    dest = os.path.join(destpath, f)
                    shutil.copy(src, dest)

            index = os.path.join(destpath, 'index.html')
            dirs = [os.path.join(destpath, d, 'index.html') for d in dirs]
            self.include_index(index, pages, dirs)

    def include_index(self, destination, pages, children):
        """
        Includes the index page for the specified destination
        pages and children
        """
        outputdir = self.config.outputdir
        pages = [TemplatePage(outputdir, p) for p in pages]
        children = [TemplatePage(outputdir, c) for c in children]

        template = self.config.get_index_template()
        rendered = template.render(pages=pages,
                                   children=children,
                                   title='MVW',
                                   breadcrumb=self.breadcrumb(destination))
        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)

    def parse(self, source, destination):
        """
        Parses the source file and saves to the destination
        """

        code = 'codehilite(css_class=syntax,guess_lang=False)'
        md = Markdown(extensions=[code])

        with codecs.open(source, encoding='utf-8') as src:
            parsed = md.convert(src.read())

        template = self.config.get_content_template(source)
        rendered = template.render(content=parsed,
                                   title='MVW',
                                   breadcrumb=self.breadcrumb(destination))

        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)

    def breadcrumb(self, destination):
        """
        Generates a breadcrumb for the specified destination file
        """

        outputdir = self.config.outputdir
        prefix = len(outputdir) + len(os.path.sep)
        destdir = os.path.dirname(destination[prefix:])

        home = self.config.get_breadcrumb_home()
        crumb = '<a href="/">%s</a>' % home
        href = "/"
        for p in destdir.split(os.path.sep):
            if len(p) > 0:
                href += '%s/' % p
                text = p.replace("_", " ").title()
                crumb += ' &gt; <a href="%s">%s</a>' % (href, text)

        return crumb


class TemplatePage:
    """
    Encapsulates data for a page to include in the template
    """

    def __init__(self, siteroot, pagepath):
        prefix = len(siteroot)
        self.url = pagepath[prefix:].replace(os.path.sep, "/")

        (path, base) = os.path.split(pagepath)
        (name, ext) = os.path.splitext(base)
        if name == 'index':
            name = os.path.basename(path)
        self.title = name.replace("_", " ").title()
