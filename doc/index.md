# MVW

MVW is a minimal personal wiki engine.

## Quick start
    
1. Install

        :::bash
        # Install from github
        $ pip install -e \
        > git://github.com/simplectic/mvw.git#egg=MVW

2. Create

        :::bash
        # Use your favorite editor to create content
        $ vim notes.md
        # Directory trees will be preserved
        $ vim git/install.md   

3. View

        :::bash
        # Locally serve the wiki. Markdown files
        # are regenerated when page is refreshed
        $ mvw

## Longer start

1. Install MVW from [github][1]

        :::bash
        $ mkproject wiki 
        $ pip install -e \
        > git://github.com/simplectic/mvw.git#egg=MVW

    The [`mkproject`][3] command is part of [virtualenvwrapper][2]
    It will allow you to call `deactivate` when you are done and 
    remove `mvw` from your path.  Later you can call `workon wiki` 
    to switch to your `wiki` virtualenv and automatically `cd` into
    your wiki directory.


2. Add some content using [Markdown][4]

        :::bash
        $ cat > hello.md <<EOT
        > # Greetings
        > Hello World
        > EOT

    MVW uses the mostly reference implementation compliant 
    [Python-Markdown][5] with the [code hiliting][6] extension.
    Navigation links are generated automatically. Index files 
    are generated with empty content if index source files are
    not present.
    
3. Serve the wiki locally

        :::bash
        $ mvw 

    This serves the wiki locally at <http://localhost:8000> from the 
    current working directory. Changes to the markdown files will be
    regenerated automatically as they are requested.
    
    **Note**: `mvw` (or the alias `mvw serve`) should **only** be used to
    serve your wiki locally.  If you want to deploy your wiki, 
    [generate a static site][7].


[1]: http://github.com/simplectic/mvw
[2]: http://www.doughellmann.com/docs/virtualenvwrapper/
[3]: http://www.doughellmann.com/docs/virtualenvwrapper/command_ref.html#project-directory-management
[4]: http://daringfireball.net/projects/markdown/
[5]: http://www.freewisdom.org/projects/python-markdown
[6]: /examples/code.html
[7]: /site_generation.html
