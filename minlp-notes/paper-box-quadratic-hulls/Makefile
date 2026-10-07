.PHONY: all check-records clean

all: main.pdf

main.pdf: main.tex macros.tex references.bib $(wildcard sections/*.tex appendices/*.tex figures/*.pdf)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=verification main.tex
	cp verification/main.pdf main.pdf
	cp verification/main.bbl main.bbl

check-records:
	python3 companion/inspect_records.py

clean:
	latexmk -C -outdir=verification main.tex
