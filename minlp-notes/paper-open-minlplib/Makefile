# Build build/main.pdf and build/supplement.pdf with all cross-document
# references resolved. Each document reads the other's .aux file
# (xr-hyper), so latexmk (settings in latexmkrc) runs over both twice: the
# first pass writes both .aux files, the second reruns each document whose
# inputs changed. No document prints a page number of the other, so two
# passes suffice.
.PHONY: all clean

all:
	latexmk main.tex supplement.tex
	latexmk main.tex supplement.tex

clean:
	latexmk -C main.tex supplement.tex
