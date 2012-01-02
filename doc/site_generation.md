1. Initialize mvw at the root of your wiki

        :::bash
        $ mvw init

    Creates an `.mvw` folder used for the generation of the site
    and to identify the site root for other commands.  Markdown files 
    can be created in any directory tree under the wiki root and this
    directory tree will be preserved when generating the site.

2. Generate the wiki

        :::bash
        $ mvw generate

    Call anywhere under the wiki root. MVW will search up the directory 
    tree for the `.mvw` folder created using `mvw init`.  A static site
    will be (re)generated in `.mvw/site` for the entire directory tree. 
    Markdown files will be parsed and surrounded with a template. Hidden 
    files and directories are ignored. Everything else is simply copied. 
    Directory trees are preserved.

3. Deploy 

    Copy the files generated in `.mvw/site` to your web server.
