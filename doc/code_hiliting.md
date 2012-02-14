[Pygments][1] is used for code highlighting with the [CodeHilite][2] extension.

If you want to hilite code without line numbers, use `:::{language}` as the first line of the indented code block.

    :::javascript
    hello = function(world){
        alert("Hello "+world);
    };

If the first line is `#!{language}`, the code is hilited with line numbers.  

    #!ruby
    def hello(world)
        puts "Hello #{world}"
    end

If the first line contains a shebang with a path, the first line is included:

    #!/usr/bin/env python
    def hello(world):
        print("Hello %s" % world)


Note that MVW uses the Pygments `syntax` class instead of `codehilite` as described by the extension and turns off language guessing to allow indented code blocks without hiliting. 

[1]: http://pygments.org
[2]: http://www.freewisdom.org/projects/python-markdown/CodeHilite

----

The markdown source for the above:

    [Pygments][1] is used for code highlighting with the [CodeHilite][2] extension.

    If you want to hilite code without line numbers, use `:::{language}` as the first line of the indented code block.

        :::javascript
        hello = function(world){
            alert("Hello "+world);
        };

    If the first line is `#!{language}`, the code is hilited with line numbers.  

        #!ruby
        def hello(world)
            puts "Hello #{world}"
        end

    If the first line contains a shebang with a path, the first line is included:

        #!/usr/bin/env python
        def hello(world):
            print("Hello %s" % world)


    Note that MVW uses the Pygments `syntax` class instead of `codehilite` as described by the extension and turns off language guessing to allow indented code blocks without hiliting. 

    [1]: http://pygments.org
    [2]: http://www.freewisdom.org/projects/python-markdown/CodeHilite

