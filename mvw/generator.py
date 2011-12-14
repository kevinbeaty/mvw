import os
import shutil
import codecs
from markdown import Markdown
from mako.lookup import TemplateLookup

class Generator:
    def __init__(self, sourcedir, outputdir, themedir):
        self.sourcedir = os.path.normpath(sourcedir)
        self.outputdir = os.path.normpath(outputdir)
        self.themedir = os.path.normpath(themedir)

    def run(self):
        self.clean()
        self.include_theme()
        self.include_source()

    def clean(self):
        if os.path.exists(self.outputdir):
            shutil.rmtree(self.outputdir)

    def include_theme(self):
        public = os.path.join(self.themedir, 'public')
        if os.path.exists(public):
            shutil.copytree(public, self.outputdir)

        template = os.path.join(self.themedir, 'template')
        if os.path.exists(template):
            self.templatelookup = TemplateLookup(directories=[template])

    def include_source(self):

        prefix = len(self.sourcedir)+len(os.path.sep)

        for root, dirs, files in os.walk(self.sourcedir):
            # Prune hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if not f.startswith('.')]

            destpath = os.path.join(self.outputdir, root[prefix:])
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
                    if ext in ['.html']:
                        pages.append(dest)

            index = os.path.join(destpath, 'index.html')
            dirs = [os.path.join(destpath, d, 'index.html') for d in dirs]
            self.include_index(index, pages, dirs)
            

    def include_index(self, destination, pages, children):
        pages = [TemplatePage(self.outputdir, p) for p in pages]
        children = [TemplatePage(self.outputdir, c) for c in children]
        
        template = self.templatelookup.get_template('index.html')
        rendered = template.render(pages=pages, 
                                   children=children,
                                   title='MVW', 
                                   breadcrumb=self.breadcrumb(destination))
        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)


    def parse(self, source, destination): 
        md = Markdown(extensions=['codehilite(css_class=syntax,guess_lang=False)'])

        with codecs.open(source, encoding='utf-8') as src:
            parsed = md.convert(src.read())

        template = self.templatelookup.get_template('default.html')
        rendered = template.render(content=parsed,
                                   title='MVW', 
                                   breadcrumb=self.breadcrumb(destination))

        with codecs.open(destination, mode='w', encoding='utf-8') as dst:
            dst.write(rendered)

    def breadcrumb(self, destination):
        prefix = len(self.outputdir)+len(os.path.sep)
        destdir = os.path.dirname(destination[prefix:])

        crumb = '<a href="/">Home</a>'
        href = "/"
        for p in destdir.split(os.path.sep):
            if len(p) > 0:
                href += '%s/' % p
                crumb += ' &gt; <a href="%s">%s</a>' % (href, p.replace("_", " ").title())

        return crumb
    
class TemplatePage:
    def __init__(self, siteroot, pagepath):
        prefix = len(siteroot)
        self.url = pagepath[prefix:].replace(os.path.sep, "/") 

        (path, base) = os.path.split(pagepath)
        (name, ext) = os.path.splitext(base) 
        if name == 'index':
            name = os.path.basename(path)
        self.title = name.replace("_", " ").title()

