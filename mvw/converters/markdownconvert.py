""" Converter using Python Markdown.
Theme is taken from Markdown meta data, or default if not set.
Extensions can be configured per theme using `markdown_extensions`
theme key.  Context contains all meta data lists as `Meta` and as
joined strings as `meta`. Markdown is parsed and then rendered
with template using theme from meta data or default."""

import os
import codecs
from markdown import Markdown
from markdown.extensions.meta import MetaPreprocessor


class MarkdownConverter:
    def __init__(self, config):
        self.config = config
        config.converter(self.handles, self.convert)

    def convert(self, source, **context):
        """ Converts the source file and saves to the destination """
        with codecs.open(source, encoding='utf-8') as src:
            lines = src.readlines()

        # Parse metadata first so we can get theme extensions
        md = Markdown()
        lines = MetaPreprocessor(md).run(lines)

        Meta = md.Meta
        meta = {k: ' '.join(v) for k, v in Meta.items()}

        # Load theme from meta data if set
        theme = meta.get('theme', 'default')

        exts = self.config.theme_get(theme, 'markdown_extensions', [
            'codehilite(css_class=syntax,guess_lang=False)'])
        exts = filter(None, exts)  # Removes empty lines

        md = Markdown(extensions=exts)
        md.Meta = meta  # restore already parsed meta data

        content = md.convert(''.join(lines))

        context['Meta'] = Meta
        context['meta'] = meta

        return self.config.render_template(theme, content, **context)

    def handles(self, source):
        _, ext = os.path.splitext(source)
        return ext in ['.md', '.markdown']
