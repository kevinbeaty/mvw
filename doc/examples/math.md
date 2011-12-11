LaTeX can be included inline between single dollar signs: $e = mc^2$ or
in blocks between double dollar signs:


$$
    \sum_{n=1}^\infty \frac{1}{n}
$$

$$
    \left(1+x\right)^n = 1 + nx + \frac{n\left(n-1\right)}{2!}x^2 + \ldots
$$

To enable MathJax rendering, you need to use `layout: math` at the beginning
of your file.  This is the source for the above example:

    LaTeX can be included inline between single dollar signs: $e = mc^2$ or
    in blocks between double dollar signs:


    $$
        \sum_{n=1}^\infty \frac{1}{n}
    $$

    $$
        \left(1+x\right)^n = 1 + nx + \frac{n\left(n-1\right)}{2!}x^2 + \ldots
    $$
