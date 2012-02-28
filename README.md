[![Build Status](https://secure.travis-ci.org/simplectic/mvw.png)](http://travis-ci.org/simplectic/mvw)

MVW is a minimal personal wiki engine.

Example and documentation at <http://simplectic.com/mvw>. The documentation source is included in the doc directory of this repository.

## Quick start
    
1. Install

    ```bash
    # Install from github 
    pip install -e git://github.com/simplectic/mvw.git#egg=MVW
    ```

2. Create

    ```bash
    # Use your favorite editor to create content
    $ vim notes.md
    # Directory trees will be preserved
    $ vim git/install.md   
    ```

3. View

    ```bash
    # Locally serve the wiki. Markdown files
    # are regenerated when page is refreshed
    $ mvw
    ```

## Licence
See LICENSE for details

