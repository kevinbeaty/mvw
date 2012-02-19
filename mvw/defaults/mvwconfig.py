""" Customized MVW configuration.
MVW will automatically load mvwconfig.py from
mvw root (.mvw/mvwconfig.py) if it exists.
If no mvwconfig.py is found at mvw root, the
default configuration will be used."""
from mvw.config import Config
config = Config()

# Link text for site root when generating breadcrumb
# Uses title generated from sourcedir name if not set
#config.breadcrumb_home = 'Home'

# The site root to use to prepend to generated links
# when generating the site.  This only applies to
# `mvw generate`.  `mvw` (and `mvw serve`) will only
# serve at site root of localhost:8000
#config.site_root = '/'

# Directories are relative to mvw root (.mvw), but
# can be absolute.
#config.sourcedir = '..'
#config.outputdir = 'site'

# Default theme will be used if themedir does not exist
# Can use `mvw theme` to copy default theme to mvw root
# to allow customization from defaults
#self.themedir = 'theme'

# List of Jinja2 Extensions to use for all templates
# configured in themes below.
# Can be used to add custom  Jinja2 extensions,
# filters, tests, etc by adding the extension to
# ${themedir}/extensions which is added to the
# python path if it exists.
#config.jinja2_extensions = []

# Map of themes.  Can be selected using `theme: $themename`
# markdown metadata.  If no theme is selected, default is
# assumed. Mapping of themes is optional. If themes are not
# configured below, `theme: $themename` will select Jinja2
# template with ${themename}.html and use default mvw
# markdown extensions
#
# `content_template` refers to Jinja2 template in
# ${themedir}/template and defaults to ${themename}.html
#
# `markdown_extensions` can be listed per theme.
# Custom markdown extensions can be placed in
# ${themedir}/extensions which is added to the
# python path if it exists.
#
#config.theme('default',
#   content_template='default.html',
#   markdown_extensions=[
#        'codehilite(css_class=syntax,guess_lang=False)'])
