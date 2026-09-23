PYTHON ?= python3
PDFLATEX ?= pdflatex
BIBTEX ?= bibtex
TEXFLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all figures submission clean
all: main.pdf

# Checked-in figure PDFs keep the ordinary LaTeX build independent of Python.
main.pdf: main.tex macros.tex bibliography.bib $(wildcard sections/*.tex) figures/query-overview.pdf
	$(PDFLATEX) $(TEXFLAGS) main.tex
	$(BIBTEX) main
	$(PDFLATEX) $(TEXFLAGS) main.tex
	$(PDFLATEX) $(TEXFLAGS) main.tex

figures:
	$(PYTHON) scripts/query_overview.py
	$(PYTHON) scripts/joint_accuracy_diagnostics.py

submission: main.pdf
	$(PYTHON) scripts/package_source.py

# Keep main.bbl and required figures so distributed sources stay portable.
clean:
	rm -f main.aux main.blg main.log main.out main.pdf
