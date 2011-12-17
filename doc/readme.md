# MVW

MVW is a minimal personal wiki engine.

## Quick start
    
1. Install

        :::bash
        $ mkproject wiki       # Creates a virtualenvwrapper project
        $ pip install -e git://github.com/simplectic/mvw.git#egg=MVW
        $ mvw init             # Initializes the wiki 

2. Create

        :::bash
        $ vim notes.md         # Use your favorite editor to create content
        $ vim git/install.md   # Directory trees will be preserved

3. View

        :::bash
        $ mvw generate         # Generates the static site
        $ mvw serve            # Locally serve the wiki. Markdown files
                               # are regenerated when page is refreshed

## Longer start

1. Install MVW from [github][1]

        :::bash
        $ mkproject wiki 
        $ pip install -e git://github.com/simplectic/mvw.git#egg=MVW

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
    
3. Initialize mvw at the root of your wiki

        :::bash
        $ mvw init

    Creates an `.mvw` folder used for the generation of the site
    and to identify the site root for other commands.  Markdown files 
    can be created in any directory tree under the wiki root and this
    directory tree will be preserved when generating the site.

4. Generate the wiki

        :::bash
        $ mvw generate

    Call anywhere under the wiki root. MVW will search up the directory 
    tree for the `.mvw` folder created using `mvw init`.  A static site
    will be (re)generated in `.mvw/site` for the entire directory tree. 
    Markdown files will be parsed and surrounded with a template. Hidden 
    files and directories are ignored. Everything else is simply copied. 
    Directory trees are preserved.
    
    **Note**: `mvw serve` can automatically regenerate the markdown files 
    on demand, so this command is not always required.

5. Serve the wiki locally

        :::bash
        $ mvw serve

    This serves the generated site at <http://localhost:8000>. This command
    can also be run in any directory under the wiki root.  You should run
    `mvw generate` at least once to ensure the template files are copied
    and index files are generated. Changes to the markdown files will
    be regenerated automatically as they are requested.


[1]: http://github.com/simplectic/mvw
[2]: http://www.doughellmann.com/docs/virtualenvwrapper/
[3]: http://www.doughellmann.com/docs/virtualenvwrapper/command_ref.html#project-directory-management
[4]: http://daringfireball.net/projects/markdown/
[5]: http://www.freewisdom.org/projects/python-markdown
[6]: /examples/code.html
