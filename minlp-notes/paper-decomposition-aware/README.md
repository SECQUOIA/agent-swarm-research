# Decomposition-aware global optimization: certified coordinate grids, conditional recourse, and structural limits

`main.tex` is the manuscript and `main.pdf` the compiled version. The author
field is intentionally blank. The manuscript rewrites and extends the
technical report in `research-20261002-decomposition/document/`; that folder,
its solver and its notes are unchanged.

Build from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## What is where

| Path | Content |
|---|---|
| `sections/` | manuscript sections (main text, then appendices A-H in section order) |
| `figures/` | the two figures used in Section 11 |
| `references.bib` | bibliography |
| `experiments/` | computational study of Section 11 and Appendix H: runners, instances, raw results, certificates, independent replay; `experiments/README.md` maps each experiment to its section and gives one command per experiment group |
| `PROCESS.md` | development and review process, stage by stage |
| `process/w1/` | verification of every result of the report, self-contained proofs, literature audits, exact-arithmetic checks |
| `process/w2/`, `process/w4/`, `process/w6/` | the three independent review rounds and the adjudication of every finding (`ADJUDICATION.md`) |
| `process/w3/`, `process/w5/`, `process/w7/` | the revision rounds: conventions, cut plan, per-group reports with verification, scratch checks, and backups of the sections before each round |

## Main results

For a sum of factors on a mixed-integer box with a tree decomposition of bag
size `p`, subtracting `L_i w^2/8` at each grid node turns exact dynamic
programming over a product grid into a valid lower bound. Min-marginals
filter the grids, and the stage grids form a certificate, checked by
recomputation, whose validity needs no convexity, uniqueness or growth.

* Under quadratic growth in a curvature-weighted norm, graded grids keep
  `O(sqrt(kappa_bar) log(n+2))` nodes per coordinate at every accuracy. For
  mixed-integer box quadratic programs this certifies accuracy `2^-q` in
  `f(p, kappa_bar) (I+q+1)^5` bit operations without knowing the growth
  constant; under point growth an exact minimizer takes
  `f_1(p, kappa) poly(I)` bit operations.
* Lower bounds: neither `p` nor `kappa` can be dropped and the dependence on
  `kappa` cannot be polylogarithmic unless P = NP; under rETH the exponent of
  `kappa` cannot be `o(p)`; for value oracles the exponent `p/2` is optimal.
* Extensions: exact partial minimization (conditional recourse) by value
  functions, convex recourse and minimum-cut residuals; totally unimodular
  coupling constraints; several minimizers (uniform cells, optimal-set
  descriptions); and structural limits (exact messages, moments, constraint
  faces, boundary certificates).
* An exact-arithmetic implementation with independent certificate replay is
  tested on synthetic families, the expanding-box chain, SCIP comparisons and
  recourse instances. All continuous families are synthetic; the paper does
  not claim that application models have small width and moderate `kappa`.

Novelty statements in the manuscript are limited to what the literature
audits in `process/w1/lit-*.md` and the review rounds support; they are not a
priority claim beyond that search. Internal reviews are not journal peer
review.

## Before submission

* Fill in the author data, and add the journal's statements and declarations
  block (funding, competing interests, data availability).
* The supplementary archive must include `experiments/` and the solver files
  it imports from `research-20261002-decomposition/` (`solver/` and
  `completion/`); they are listed with SHA-256 hashes in
  `experiments/results/dependencies_sha256.json`, pinned to commit
  `b59ed1b836e4`. The public corpus contains the reviewed committed source and sanitized evidence; upstream local material is outside this transfer.
