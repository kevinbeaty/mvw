theme: mathjax

Include `theme: mathjax` at the beginning of your file to enable MathJax
rendering. The default MathJax theme uses the [CDN][1]. 

LaTeX can be included inline between single dollar signs: $e = mc^2$ or
in blocks between double dollar signs:

$$
    \sum_{n=1}^\infty \frac{1}{n}
$$

$$
    (1+x)^n 
    = 1 + nx 
    + \frac{n(n-1)}{2!}x^2 
    + \frac{n(n-1)(n-2)}{3!}x^3 
    + \ldots
$$


[1]: http://www.mathjax.org/download/mathjax-cdn-terms-of-service/

This is the source for the above example:

---
    theme: mathjax

    Include `theme: mathjax` at the beginning of your file to enable MathJax
    rendering. The default MathJax theme uses the [CDN][1]. 

    LaTeX can be included inline between single dollar signs: $e = mc^2$ or
    in blocks between double dollar signs:

    $$
        \sum_{n=1}^\infty \frac{1}{n}
    $$

    $$
        (1+x)^n 
        = 1 + nx 
        + \frac{n(n-1)}{2!}x^2 
        + \frac{n(n-1)(n-2)}{3!}x^3 
        + \ldots
    $$


    [1]: http://www.mathjax.org/download/mathjax-cdn-terms-of-service/
