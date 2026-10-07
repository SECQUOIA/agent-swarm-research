Smoothed exact global optimization beyond convexity

This source package contains an anonymous manuscript, its complete proof
appendices, bibliography, and generated bibliography file.

Build from the directory containing main.tex:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Without latexmk, run:

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

A standard TeX distribution is required. All packages are listed in main.tex.
The document uses pdfLaTeX and BibTeX with the plainnat bibliography style.
No external data, image, code, or optimization experiment is required.

The title page intentionally has no author names or date. Journal-specific
formatting and author information may be added for the chosen submission.
