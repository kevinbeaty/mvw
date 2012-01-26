"""
MathJax extension for Python-Markdown
=====================================

Renders LaTeX inline between '$' and blocks between '$$'.

Include in MVW by adding 'mathjax' to list of markdown
extensions and using the 'mathjax.html' extension.

Modified version of [python-markdown-mathjax][1], but
renders `math-tex` script tags instead of using MathJax
preprocessor.


[1]: http://github.com/mayoff/python-markdown-mathjax
"""
from markdown.inlinepatterns import Pattern
from markdown import Extension


class MathJaxPattern(Pattern):
    def __init__(self, markdown):
        self.markdown = markdown
        Pattern.__init__(self, r'(?<!\\)(\$\$?)(.+?)\2')

    def handleMatch(self, m):
        script_type = "math/tex"
        if m.group(2) == '$$':
            script_type += '; mode=display'

        tex = m.group(3)
        script = '$<script type="%s">%s</script>$' % (script_type, tex)
        stash = self.markdown.htmlStash
        return stash.store(script)


class MathJaxExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathjax', MathJaxPattern(md), '<escape')


def makeExtension(configs=None):
    return MathJaxExtension(configs)
