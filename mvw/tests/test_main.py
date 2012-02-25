""" Tests for mvw.main using nose """
import os
import os.path
import shutil
from mvw import main

def chdir(site):
    dirname = os.path.dirname(__file__)
    sitedir = os.path.join(dirname, 'sources', site)
    os.chdir(sitedir)
    return sitedir

def dotmvw(sitedir):
    return os.path.join(sitedir, '.mvw')

def mvwconfig(sitedir):
    return os.path.join(dotmvw(sitedir), 'mvwconfig.py')

def mvwtheme(sitedir):
    return os.path.join(dotmvw(sitedir), 'theme')

def test_init_empty():
    sitedir = chdir('empty')
    siteroot = dotmvw(sitedir)

    assert not os.path.exists(siteroot)
    assert not main.get_root(sitedir)

    assert main.init(sitedir)
    assert os.path.exists(siteroot)
    assert siteroot == main.get_root(sitedir)

    assert not main.init(sitedir)
    assert os.path.exists(siteroot)
    assert siteroot == main.get_root(sitedir)
    
    shutil.rmtree(siteroot)
    assert not os.path.exists(siteroot)
    assert not main.get_root(siteroot)

    assert main.init(sitedir)
    assert os.path.exists(siteroot)
    assert siteroot == main.get_root(siteroot)
    
    shutil.rmtree(siteroot)
    assert not os.path.exists(siteroot)
    assert not main.get_root(sitedir)

def test_init_basic():
    sitedir = chdir('basic')
    mvwroot = dotmvw(sitedir)

    assert not os.path.exists(mvwroot)
    assert not main.get_root(sitedir)

    childdir = os.path.join(sitedir, 'childdir')
    assert os.path.exists(childdir)
    assert not main.get_root(childdir)

    assert main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)

    assert not main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)

def test_config_empty():
    sitedir = chdir('empty')
    mvwroot = dotmvw(sitedir)
    configfile = mvwconfig(sitedir)

    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    assert not main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    assert not main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)

    assert main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)

def test_config_basic():
    sitedir = chdir('basic')
    mvwroot = dotmvw(sitedir)
    configfile = mvwconfig(sitedir)
    childdir = os.path.join(sitedir, 'childdir')

    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)
    
    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)

    assert main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)

    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)

def test_theme_empty():
    sitedir = chdir('empty')
    mvwroot = dotmvw(sitedir)
    configfile = mvwconfig(sitedir)
    themedir = mvwtheme(sitedir)
    themepublic = os.path.join(themedir, 'public')
    themepublicjs = os.path.join(themepublic, 'js')
    themepubliccss = os.path.join(themepublic, 'css')
    themepublicstyle = os.path.join(themepubliccss, 'style.css')
    themetemplate = os.path.join(themedir, 'template')
    themetemplatedefault = os.path.join(themetemplate, 'default.html')

    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert not os.path.exists(themedir)
    assert not os.path.exists(themepublic)
    assert not os.path.exists(themepublicjs)
    assert not os.path.exists(themepubliccss)
    assert not os.path.exists(themepublicstyle)
    assert not os.path.exists(themetemplate)
    assert not os.path.exists(themetemplatedefault)

    assert main.theme(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(themedir)
    assert os.path.exists(themepublicjs)
    assert os.path.exists(themepubliccss)
    assert os.path.exists(themepublicstyle)
    assert os.path.exists(themepublic)
    assert os.path.exists(themetemplate)
    assert os.path.exists(themetemplatedefault)

    assert not main.theme(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(themedir)
    assert os.path.exists(themepublicjs)
    assert os.path.exists(themepubliccss)
    assert os.path.exists(themepublicstyle)
    assert os.path.exists(themepublic)
    assert os.path.exists(themetemplate)
    assert os.path.exists(themetemplatedefault)

    assert not main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(themedir)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)

    assert os.path.exists(themedir)
    assert os.path.exists(themepublicjs)
    assert os.path.exists(themepubliccss)
    assert os.path.exists(themepublicstyle)
    assert os.path.exists(themepublic)
    assert os.path.exists(themetemplate)
    assert os.path.exists(themetemplatedefault)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert not os.path.exists(themedir)
    assert not os.path.exists(themepublic)
    assert not os.path.exists(themepublicjs)
    assert not os.path.exists(themepubliccss)
    assert not os.path.exists(themepublicstyle)
    assert not os.path.exists(themetemplate)
    assert not os.path.exists(themetemplatedefault)

    assert main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert not os.path.exists(themedir)
    assert not os.path.exists(themepublic)
    assert not os.path.exists(themepublicjs)
    assert not os.path.exists(themepubliccss)
    assert not os.path.exists(themepublicstyle)
    assert not os.path.exists(themetemplate)
    assert not os.path.exists(themetemplatedefault)

    assert main.config(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)
    assert not os.path.exists(themedir)
    assert not os.path.exists(themepublic)
    assert not os.path.exists(themepublicjs)
    assert not os.path.exists(themepubliccss)
    assert not os.path.exists(themepublicstyle)
    assert not os.path.exists(themetemplate)
    assert not os.path.exists(themetemplatedefault)

    assert main.theme(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(configfile)
    assert os.path.exists(themedir)
    assert os.path.exists(themepublic)
    assert os.path.exists(themepublicjs)
    assert os.path.exists(themepubliccss)
    assert os.path.exists(themepublicstyle)
    assert os.path.exists(themetemplate)
    assert os.path.exists(themetemplatedefault)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert not os.path.exists(themedir)

def test_theme_basic():
    sitedir = chdir('basic')
    mvwroot = dotmvw(sitedir)
    configfile = mvwconfig(sitedir)
    themedir = mvwtheme(sitedir)
    childdir = os.path.join(sitedir, 'childdir')

    assert not os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert not os.path.exists(themedir)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)
    assert not main.get_root(themedir)

    assert main.theme(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(configfile)
    assert os.path.exists(themedir)
    
    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)
    assert mvwroot == main.get_root(themedir)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(themedir)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)
    assert not main.get_root(themedir)

    assert main.init(sitedir)
    assert os.path.exists(mvwroot)
    assert not os.path.exists(themedir)

    assert main.theme(sitedir)
    assert os.path.exists(mvwroot)
    assert os.path.exists(themedir)

    assert mvwroot == main.get_root(sitedir)
    assert mvwroot == main.get_root(childdir)
    assert mvwroot == main.get_root(themedir)

    shutil.rmtree(mvwroot)
    assert not os.path.exists(mvwroot)
    assert not os.path.exists(themedir)
    assert os.path.exists(childdir)
    assert not main.get_root(sitedir)
    assert not main.get_root(childdir)
    assert not main.get_root(themedir)
