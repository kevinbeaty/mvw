import os
import sys


class Config:
    """ Holds configurable properties of MVW.
    Custom configuration can by provided as a config
    property in `.mvw/mvwconfig.py`.  Use `mvw config`
    to copy configuration template to mvw root """

    def __init__(self):
        """ Initializes default values """

        # directories relative to mvw root
        self.sourcedir = '..'
        self.outputdir = 'site'
        self.themedir = 'theme'
        self.site_root = '/'
        self.themes = {}
        self.breadcrumb_home = None
        self.port = 8000

        self._converters = []

    def converter(self, predicate, converter):
        """ Registers a converter function for a given predicate.
        All source files will be checked against `predicate(source)`
        If the predicate returns a True value, the source will be
        converted as pages by calling converter with:
        `converter(source, **context)` where source is the path to source
        file to convert and context created from `template_context` """
        self._converters.append((predicate, converter))
        return self

    def theme(self, theme, **kwargs):
        """ Sets configuration for a specified theme.
        Stores all kwargs into configuration per theme.
        Configuration values can be obtained using theme_get"""
        self.themes = self.themes or {}
        self.themes[theme] = kwargs
        return self

    def theme_get(self, theme, key, default):
        """ Gets a configuration value for the given theme.
        Config values are added using self.theme and may be
        used for configuration of templates, converters, etc. """
        themes = self.themes or {}
        cfg = themes.get(theme, None) or {}
        return cfg.get(key, None) or default

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

    def pages(self, site_root, dests):
        """ Creates and sorts pages for the given destination """
        pages = [self.page(site_root, d) for d in dests]
        pages.sort(key=lambda p: p.title)
        return pages

    def template_environment(self, templatedir):
        """ Creates the template environment to load themes
        from the themedir. The environment is stored in
        self.environment and can be used in content_template.
        Sets up a Jinja2 environment by default."""

        from jinja2 import Environment, FileSystemLoader
        return Environment(loader=FileSystemLoader(templatedir))

    def content_template(self, theme):
        """ The template to use for parsed content.
        Default implementation attempts to load content_template
        using theme_get with default value ${theme}.html
        Loads template using environment.get_template (as Jinja2)."""

        template = self.theme_get(theme, 'content_template', '%s.html' % theme)

        return self.environment.get_template(template)

    def template_context(self, source, dest, site_root, pages, children):
        """ Creates a template context to be used to convert and render.
        Default implementation stores title, breadcrumb, pages and children.
        The pages are siblings within same directory, children are index
        pages of subdirectories.  Both pages and children params have already
        been created using `self.pages` """

        breadcrumb = self.breadcrumb(site_root, dest)
        pages = [p for p in pages if p not in breadcrumb]

        context = dict(title=self.title(dest),
                       breadcrumb=breadcrumb,
                       pages=pages,
                       children=children)
        return context

    def render_template(self, theme, content, **context):
        """ Renders the content for the given theme and context """

        template = self.content_template(theme)
        context['content'] = content
        rendered = template.render(context)
        return rendered

    def load(self, root, defaults):
        """ Loads and configures remaining config properties.
        Called after running custom mvwconfig.py if it exists """

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
        self.environment = self.template_environment(template)

        # Load theme public, using default if does not exist
        themepublic = os.path.join(self.themedir, 'public')
        if not os.path.isdir(themepublic):
            themepublic = os.path.join(defaults, 'theme', 'public')
        self.theme_public = themepublic

        # Set breadcrumb home based on sourcedir if not yet set
        if not self.breadcrumb_home:
            self.breadcrumb_home = self.title(self.sourcedir)

        return self

    @property
    def converters(self):
        """ A list of tuples with predicate to converter """
        if not self._converters:
            # No converters registered, assume pygments and markdown

            # Register markdown converter
            from mvw.converters.markdown import MarkdownConverter
            MarkdownConverter(self)

            # Register all supporter lexers from pygments
            # This must be done last to allow overridding
            # by short circuiting with specific converters above
            from mvw.converters.pygments import PygmentsConverter
            PygmentsConverter(self)

        return self._converters

    def is_page(self, source):
        """ Returns True if a converter exists for the given source file """
        if source and os.path.exists(source):
            for (predicate, _) in self.converters:
                if predicate(source):
                    return True
        return False

    def convert(self, source, **context):
        """ Converts the given source file. """

        converter = None
        if source and os.path.exists(source):
            for (predicate, converter) in self.converters:
                if (predicate(source)):
                    converter = converter
                    break

        if(converter):
            # Convert with first converter that source file
            return converter(source, **context)
        else:
            # Simply render empty content in default template
            return self.render_template('default', "", **context)

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
