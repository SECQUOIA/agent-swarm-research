# Instance-dependent certification complexity in branch-and-bound

This manuscript studies the size of an optimality certificate for a fixed
relaxation and permitted operations. It covers continuous near-optimal
geometry, root-box face integrals and analytic rates, decomposition
certificates, propagation and branching, convex-class integer certificates,
and Gaussian sparse-regression and binary least-squares models.

The manuscript keeps covers, rectangular partitions, and branching trees
distinct. It also distinguishes certificate size from processed nodes,
relaxation evaluations, tightening rounds, and propagation rounds.

## Manuscript and archives

- [Paper PDF](main.pdf), 125 pages with complete proof appendices; authors are blank.
- [Manuscript source](main.tex).
- [Portable submission sources](delivery/bb-complexity-sources.zip).
- [Build instructions](BUILD.txt).
- [Archived computational evidence](reproducibility/README.md).
- [Portable evidence ZIP](delivery/bb-complexity-evidence.zip).
- [Claim and proof coverage](evidence/COVERAGE-FINAL.md).
- [Review resolutions](evidence/REVIEW-RESOLUTION.md).
- [Literature review and source comparisons](evidence/LITERATURE.md).
- [Targeted verification record](evidence/FINAL-VERIFICATION.md).

## Build

From this directory, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

A standard TeX Live installation supplies the packages listed in
[macros.tex](macros.tex). The manuscript sources require no original research
notes, network access, solver software, or computational experiment reruns.

## Evidence and scope

The computational companion preserves 209 original files byte for byte. Its
verification script checks hashes, record counts, and archived fit metadata.
The manuscript figure was drawn from retained observations. No solver run or
computational experiment was repeated during preparation.

Mathematical checks include independent source audits, new proof development,
and reviews of the actual manuscript statements and proofs. The internal
evidence directory records corrections and literature comparisons; it is
excluded from the submission source package. Literature discovery and
additions used the supplied literature workflow with Luna at maximum
reasoning. Opus supplied the architecture, initial framing, experiment map,
and an independent boundary review. Claude usage limits required the
authorized Sol fallback for the remaining writing and manuscript reviews.

Only checks targeted to this paper and its packages are run locally. No
project-wide checks or CI inspection are part of this work.
