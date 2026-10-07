# Submission source packaging review, revision 1

The manuscript source has a local, self-contained dependency closure. The
planned source archive needs 30 files, listed below: 27 TeX files, one BibTeX
file, `main.bbl`, and `BUILD.txt`. All listed files exist, including the
subsequently created and inspected `BUILD.txt`. No final archive has been
inspected; forming and inspecting it remain packaging tasks. This review does not establish
mathematical correctness, literature coverage, or final submission readiness.

## Scope and result

Reviewed the entry point, macros, included-source filenames, file-loading
commands, bibliography output, repository-specific prose and paths, author
metadata declarations, and existing PDF document metadata. The manuscript was
left untouched. No build, mathematical verification script, experiment, CI
inspection, project-wide check, or external research was run.

`main.tex` includes `macros.tex`, 13 section files, and 12 appendix files. Its
only other source dependency is `references.bib`, using the standard
`plainnat` bibliography style. Included files introduce no further file loads.
There are no figures, image assets, custom classes, custom packages, custom
bibliography styles, shell commands, or external file reads to package.
Bibliographic URLs are printed references; compilation does not fetch them.

No absolute filesystem paths, references to the development `evidence/` or
`verification/` directories, or repository-specific prose were found in the
manuscript sources or bibliography output. The repository README describes
development records and the verification script, so it should remain outside
the source archive in favor of a short, submission-specific `BUILD.txt`.

## Exact archive contents

Paths are relative to the source archive root. Preserve the two directories.

```text
main.tex
macros.tex
sections/abstract.tex
sections/00-introduction.tex
sections/01-models.tex
sections/02-points.tex
sections/03-upper.tex
sections/04-reductions.tex
sections/05-constraints.tex
sections/06-algebraic.tex
sections/07-heights.tex
sections/08-fields.tex
sections/09-certificates.tex
sections/10-recourse.tex
sections/11-discussion.tex
appendices/A-upper.tex
appendices/B-reductions.tex
appendices/C-points.tex
appendices/D-constraints.tex
appendices/E-algebraic.tex
appendices/F-heights.tex
appendices/G-fields.tex
appendices/H-certificates.tex
appendices/I-recourse.tex
appendices/J-quadratic-contrast.tex
appendices/K-boundaries.tex
appendices/L-further-arithmetic.tex
references.bib
main.bbl
BUILD.txt
```

Exclude `evidence/`, `verification/`, `README.md`, `.gitignore`, and generated
`.aux`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, and `.toc` files. Deliver
the compiled `main.pdf` separately from the source archive.

The present `main.bbl` is a conventional `thebibliography` file with 120
entries. Including it lets a recipient compile the supplied bibliography
without running BibTeX and avoids dependence on a submission system choosing
to run BibTeX. Keep `references.bib` too, so the bibliography remains editable
and reproducible. The final packaging step should include the `.bbl` produced
by the final accepted manuscript build.

## Build requirements

Use a standard TeX distribution with pdfLaTeX, BibTeX, the `article` class,
`plainnat.bst`, and these packages declared in `main.tex`:

```text
fontenc inputenc lmodern geometry amsmath amssymb amsthm mathtools mathrsfs
booktabs array longtable tabularx enumitem microtype graphicx natbib url hyperref
```

The TeX distribution supplies their ordinary transitive dependencies and
fonts. No repository program, Python environment, network download, special
data file, or shell escape is needed to compile the paper.

The inspected `BUILD.txt` identifies `main.tex` as the entry point, directs
commands to run from the extracted archive root, lists the standard package
requirements, and provides these workflows:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or, without latexmk:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

For a recipient using the supplied `.bbl`, repeated pdfLaTeX runs can resolve
cross-references without the BibTeX step. These are documented build
instructions, not commands executed by this review.

## Anonymous submission check

`main.tex` declares empty `\author{}` and `\date{}`, and explicitly sets
`pdfauthor={}` in `\hypersetup`. No affiliation, acknowledgement, email,
ORCID, or development attribution was found in the manuscript source.
Bibliography author names describe cited works and are appropriate to retain.

`pdfinfo paper-exact-arithmetic/main.pdf` reported an empty Author field and
the intended title. Creator and Producer identify ordinary LaTeX/pdfTeX tools;
no personal author identity appears in those fields. This result applies to
the existing PDF read during this review (creation time 2026-10-05 17:12:08
EDT), not automatically to a later rebuild or archive. The source declarations
preserve anonymity on subsequent normal builds.

## Targeted checks actually run

- `rg --files paper-exact-arithmetic` and the focused listing of `sections/`
  and `appendices/`: located the source files and confirmed the included
  filenames.
- `sed -n '1,240p' paper-exact-arithmetic/main.tex` and the corresponding macro
  read: inspected the complete entry point and macro file.
- `sed -n '1,180p' paper-exact-arithmetic/README.md`: identified repository
  build and development instructions that should not accompany submission
  source.
- Focused `rg -n` searches over `main.tex`, `macros.tex`, `sections/`,
  `appendices/`, `references.bib`, and `main.bbl`: found only the expected
  source inputs and bibliography commands; no external asset or file load.
- Focused `rg -ni` searches over the same files for repository/development
  terminology and author identifiers: no manuscript attribution or
  repository-only prose found; the one GitHub URL is a cited paper URL.
- `ls -la paper-exact-arithmetic` and `rg --files` restricted to `BUILD.txt`,
  `.cls`, `.sty`, `.bst`, and `.bbl`: found the existing bibliography output
  and no local class/style assets; `BUILD.txt` was initially absent.
- `cat paper-exact-arithmetic/BUILD.txt`: inspected the subsequently created
  build instructions and confirmed their entry point, commands, package list,
  standard bibliography style, and explanation of the supplied `.bbl`.
- `sed -n '1,60p' paper-exact-arithmetic/main.bbl` and
  `tail -45 paper-exact-arithmetic/main.bbl`: inspected its standard format,
  120-entry declaration, and closing environment.
- `pdfinfo paper-exact-arithmetic/main.pdf`: confirmed empty Author metadata
  in the existing PDF.

No technical source dependency or anonymity blocker was identified. Before
calling the package complete, form the archive from the exact list and inspect
its contents. Final acceptance remains subject to the
separate manuscript and literature review gates.
