LATEX = pdflatex -interaction=nonstopmode -halt-on-error

.PHONY: all clean
all: main.pdf

main.pdf: Makefile main.tex references.bib $(wildcard sections/*.tex) $(wildcard appendices/*.tex) supplement/critical_additive_particles.pdf
	$(LATEX) main.tex
	bibtex main
	$(LATEX) main.tex
	$(LATEX) main.tex
	$(LATEX) main.tex

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.toc main.fls main.fdb_latexmk
