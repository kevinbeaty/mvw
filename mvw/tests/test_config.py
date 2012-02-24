""" Tests for mvw.config uses nose """
from mvw.config import Config

def test_defaults():
    config = Config()
    assert config.sourcedir == '..'
    assert config.outputdir == 'site'
    assert config.themedir == 'theme'
    assert config.site_root == '/'
    assert not config.themes
    assert not config.breadcrumb_home
    assert config.port == 8000
    assert not config.converters

