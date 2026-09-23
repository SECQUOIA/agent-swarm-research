PYTHON ?= python

.PHONY: all clean verify figures
all:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	latexmk -c main.tex
verify:
	$(PYTHON) scripts/verify_scalar_certificate.py
	$(PYTHON) scripts/verify_standard_geometry.py
	$(PYTHON) scripts/verify_barrier_dependence.py
	$(PYTHON) scripts/verify_primal_dual_formulations.py
figures:
	$(PYTHON) scripts/make_figures.py
