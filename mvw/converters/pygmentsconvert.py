""" Converter using Pygments.
Registers Pygments for all lexer file types. Should
be registered first to allow overriding other converters
for specific extensions (markdown, etc). """

import codecs

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename


class PygmentsConverter:
    def __init__(self, config):
        self.config = config
        config.converter(self.handles, self.convert)

    def convert(self, source, **context):
        """ Converts the source file and saves to the destination """
        with codecs.open(source, encoding='utf-8') as src:
            code = src.read()

        theme = 'default'
        lexer = get_lexer_for_filename(source)
        formatter = HtmlFormatter(linenos=False, cssclass='syntax')
        content = highlight(code, lexer, formatter)

        return self.config.render_template(theme, content, **context)

    def handles(self, source):
        try:
            return get_lexer_for_filename(source) is not None
        except:
            return False
