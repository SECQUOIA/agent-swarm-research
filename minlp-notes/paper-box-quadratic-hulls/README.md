# Quadratic hulls on boxes

This anonymous manuscript combines the three-variable inequality developments
and the finite semidefinite representability boundary. It is written as one
standalone journal paper, with complete proofs and an archived computational
companion.

- [Paper PDF](main.pdf)
- [LaTeX source](main.tex)
- [Submission source archive](submission-source.zip)
- [Computational companion](companion/README.md)
- [Companion archive](companion.zip)
- [Literature and novelty audit](evidence/literature-audit.md)
- [Verification record](verification/README.md)

The paper gives an exact rational counterexample to the named disjoint-support
and switched SOC relaxations; a valid inequality family with an order-five SDP
formulation; exposed rays in the strict parameter region and extreme
boundary rays; structural
results for the three-variable cone, including an analytic classification of
extreme rays with positive square coefficients and no vertex zero; the sharp
dimension threshold for finite SDP lifts; extensions to simple vertices and
positive graph minors; and finite
sparse lifts for small positive components. The proofs distinguish the new
results from the established tetrahedral hull construction and the external
real closed field preservation theorem.

The full completeness of the proposed three-variable inequality system and
the finite representability of the all-positive four-vertex path and star
remain explicit open questions. No established result in the manuscript
depends on their resolution. Computational claims concern archived root
relaxations, and distinguish floating-point estimates from exact certificates.

## Build and inspect

From this directory:

```sh
make
make check-records
python3 verification/check_package.py
```

The build requires a standard TeX installation with `latexmk`, `pdflatex`, and
BibTeX. The archive also includes `main.bbl` so the bibliography can be typeset
without fetching external files. The record inspection uses the Python
standard library and does not launch optimization experiments.

The paper's computational companion contains source code, generated inputs,
compact results, and checksummed provenance. It identifies excluded large
checkpoints and externally supplied benchmark inputs. It does not include
third-party literature PDFs.

## Review and provenance

The source material is in
[`research-20260925`](../research-20260925/README.md),
[`three-var-completeness`](../research-20261001/three-var-completeness/note.md),
and [`three-var-computation`](../research-20261001/three-var-computation/note.md).
The manuscript reconstructs its proofs and does not require these notes to
be understood. The evidence directory records proof development, source
contracts, and independent mathematical and editorial reviews. These are
internal research reviews, not journal peer review.

Existing optimization experiments were not rerun for this manuscript.
New targeted checks concern exact proof arithmetic, transcription, source
provenance, and the document build. The verification record lists the commands
actually run; no project-wide verification or CI inspection was performed.
