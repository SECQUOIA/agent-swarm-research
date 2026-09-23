SHELL := /bin/bash
PYTHON ?= python
.PHONY: all check package clean
all: main.pdf main.bbl
main.bbl: main.tex macros.tex bibliography.bib $(wildcard sections/*.tex)
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	bibtex main
main.pdf: main.bbl main.tex macros.tex bibliography.bib $(wildcard sections/*.tex)
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
check:
	$(PYTHON) scripts/verify_classical.py
	$(PYTHON) scripts/verify_cyclic.py
	$(PYTHON) checks/check_lower_identities.py
	$(PYTHON) checks/check_temporal_identities.py
	$(PYTHON) checks/check_structured_identities.py
package: main.pdf main.bbl
	$(PYTHON) scripts/package_submission.py
clean:
	rm -f main.aux main.blg main.log main.out main.toc
