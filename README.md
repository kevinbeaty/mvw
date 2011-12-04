# MVW
Because the world needs another wiki engine.

Documentation and example [here](http:/mvw.simplectic.com).  Source [here](https://github.com/simplectic/mvw-doc)

MVW is a minimal personal wiki engine bringing together several projects:

  * [Jekyll][1] generation 
  * [BlueTrip][2] styles
  * [Pygments][3] syntax highlighting
  * [MathJax][4] for *optional* LaTeX support. 


## Step 1: Install dependencies
MVW relies on Jekyll for site generation and Pygments for syntax
highlighting. If `gem` and `pip` are installed, try this:

    $ gem install jekyll
    $ pip install pygments

For more detailed instructions or alternative installation, refer to 
the [installation][5] instructions for Jekyll.

## Step 2: Get MVW
    $ git clone https://github.com/simplectic/mvw.git

If you want to use github to store your wiki, fork and clone your
own copy.

## Step 3: Generate some content
    $ cd mvw/wiki
    $ cat > hello.md <<EOT 
    > ---
    > title: Hello
    > layout: default
    > ---
    > # Hello World!
    > EOT

Use `layout: default` in most cases. If you want LaTeX support,
use `layout: math` to load MathJax from the CDN and include LaTeX
inline between `$ $` or as a block between `$$ $$`. 

Use your favorite editor to create your files. Jekyll supports 
Markdown, Textile, and HTML files by default with the ability
to [support more][6].

Files can be organized in a directory tree rooted at `mvw/wiki`.
Index pages and breadcrumbs will be generated automatically.

## Step 4: Start Jekyll
    $ cd mvw/wiki
    $ jekyll --server

MVW is configured with `auto: true` so most changes should reload
automatically.

## Step 5: Click around
Point your browser at [http://localhost:4000](http://localhost:4000) to view your wiki.

## Step 6: Deployment
A static site is generated under `mvw/wiki/_site` so deployment is as simple as copying 
files to your server.  See the Jekyll [deployment][7] page for additional ideas.

## Licence
See LICENSE for details

[1]: https://github.com/mojombo/jekyll
[2]: http://bluetrip.org/
[3]: http://pygments.org
[4]: http://mathjax.org
[5]: https://github.com/mojombo/jekyll/wiki/install
[6]: https://github.com/mojombo/jekyll/wiki/Plugins
[7]: https://github.com/mojombo/jekyll/wiki/Deployment
