from jinja2 import Environment, FileSystemLoader

import os
import sys
import codecs
from markdown import Markdown
from markdown.extensions.meta import MetaPreprocessor


class Config:
    """ Holds configurable properties of MVW.
    Read by convention and from config.yml """

    def __init__(self):
        # directories relative to mvw root
        self.sourcedir = '..'
        self.outputdir = 'site'
        self.themedir = 'theme'
        self.site_root = '/'
        self.themes = {}
        self.breadcrumb_home = None
        self.port = 8000

    def theme(self, theme, content_template=None, markdown_extensions=None):
        self.themes = self.themes or {}
        self.themes[theme] = {
                'content_template': content_template,
                'markdown_extensions': markdown_extensions}
        return self

    def title(self, path):
        """ Generates a title for the given path.  """

        base = os.path.basename(path)

        if(base == 'index.html'):
            dirname = os.path.dirname(path)
            if dirname in [self.outputdir, self.sourcedir]:
                return self.breadcrumb_home
            else:
                name = os.path.basename(os.path.dirname(path))
        else:
            name, ext = os.path.splitext(base)

        return name.replace("_", " ").title()

    def jinja2_environment(self, loader):
        return Environment(loader=loader)

    def load(self, root, defaults):

        root = self.expandpath(root)
        defaults = self.expandpath(defaults)

        # Load sourcedir with default same directory that contains .mvw
        self.sourcedir = self.expandpath(self.sourcedir, root)

        # Load outputdir with default .mvw/site
        self.outputdir = self.expandpath(self.outputdir, root)

        # Load themedir with default .mvw/theme
        self.themedir = self.expandpath(self.themedir, root)
        self.configthemedir = self.themedir

        # Load default theme if themedir does not exist
        if not os.path.isdir(self.themedir):
            self.themedir = os.path.join(defaults, 'theme')

        # Add extensions to path
        extensions = os.path.join(self.themedir, 'extensions')
        if os.path.isdir(extensions):
            sys.path.append(extensions)

        # Setup template environment
        # Use default if template does not exist in theme
        template = os.path.join(self.themedir, 'template')
        if not os.path.isdir(template):
            template = os.path.join(defaults, 'theme', 'template')
        self.environment = self.jinja2_environment(FileSystemLoader(template))

        # Load theme public, using default if does not exist
        themepublic = os.path.join(self.themedir, 'public')
        if not os.path.isdir(themepublic):
            themepublic = os.path.join(defaults, 'theme', 'public')
        self.theme_public = themepublic

        # Set breadcrumb home based on sourcedir if not yet set
        if not self.breadcrumb_home:
            self.breadcrumb_home = self.title(self.sourcedir)

        return self

    @staticmethod
    def expandpath(path, root=None):
        """ Fully expands path appending
        root if provided and path is relative """

        path = os.path.normpath(
                os.path.normcase(
                    os.path.expandvars(
                        os.path.expanduser(path))))
        if root and not os.path.isabs(path):
            path = os.path.join(root, path)
        return os.path.abspath(path)

    def convert(self, source, destination, site_root, pages, children):
        """ Converts the source file and saves to the destination """

        breadcrumb = self.breadcrumb(site_root, destination)
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
            exts = self.get_markdown_extensions(theme=theme)
            md = Markdown(extensions=exts)
            md.Meta = meta  # restore already parsed meta data

            content = md.convert(''.join(lines))

        context['content'] = content
        context['Meta'] = Meta
        context['meta'] = meta

        template = self.get_content_template(theme=theme)
        rendered = template.render(**context)

        return rendered

    def get_content_template(self, theme):
        """ The template to use for parsed content """

        template = self._theme(theme, 'content_template', '%s.html' % theme)

        return self.environment.get_template(template)

    def get_markdown_extensions(self, theme):
        """ List of Python Markdown extensions """

        exts = self._theme(theme, 'markdown_extensions', [
            'codehilite(css_class=syntax,guess_lang=False)'])
        return filter(None, exts)  # Removes empty lines

    def _theme(self, theme, key, default):
        themes = self.themes or {}
        cfg = themes.get(theme, None) or {}
        return cfg.get(key, None) or default


    def breadcrumb(self, site_root, destination):
        """ Generates a breadcrumb for the specified destination file """

        outputdir = self.outputdir
        prefix = len(outputdir) + len(os.path.sep)
        destdir = os.path.dirname(destination[prefix:])
        dest = destination[:prefix]

        pages = []
        pages.append(self.page(site_root,
            os.path.join(outputdir, 'index.html')))
        for p in destdir.split(os.path.sep):
            if len(p) > 0:
                dest = os.path.join(dest, p)
                pages.append(self.page(site_root,
                    os.path.join(dest, 'index.html')))

        return pages

    def page(self, site_root, destination):
        """ Creates a page passed to template context for destination.
        Page must contain a title attribute which is used for sorting."""
        return TemplatePage(self, site_root, destination)


class TemplatePage:
    """ Encapsulates data for a page to include in the template """

    def __init__(self, config, site_root, destination):
        self.title = config.title(destination)
        prefix = len(config.outputdir) + len(os.path.sep)
        self.url = '%s%s' % (site_root,
            destination[prefix:].replace(os.path.sep, "/"))

    def __eq__(self, other):
        return self.url == other.url

    def __ne__(self, other):
        return self.url != other.url
