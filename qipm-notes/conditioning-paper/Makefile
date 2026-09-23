PYTHON ?= python
.PHONY: all reproduce clean
all:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
reproduce:
	OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 $(PYTHON) repro/reproduce.py
clean:
	latexmk -C main.tex
