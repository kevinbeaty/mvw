""" Converter using Pygments.
Registers Pygments for all lexer file types. Should
be registered first to allow overriding other converters
for specific extensions (markdown, etc). """

import os
import codecs

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_for_filename


class PygmentsConverter:
    def convert(self, config, source, **context):
        """ Converts the source file and saves to the destination """
        with codecs.open(source, encoding='utf-8') as src:
            code = src.read()

        theme = 'default'
        lexer = get_lexer_for_filename(source)
        formatter = HtmlFormatter(linenos=False, cssclass='syntax')
        content = highlight(code, lexer, formatter)

        return config.render_template(theme, content, **context)

    def register(self, config):
        """ Registers convert for all supported lexer file types """
        for (_, _, file_types, _) in get_all_lexers():
            for file_type in file_types:
                _, ext = os.path.splitext(file_type)
                config.converter(ext, self.convert)
