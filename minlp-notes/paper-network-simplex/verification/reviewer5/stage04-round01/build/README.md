# Sparse convex hulls for network flows coupled to a simplex

The manuscript source is [main.tex](main.tex). Build it from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The generated paper is `main.pdf`. The source uses the standard `article`
class, BibTeX, and packages supplied by TeX Live. Author metadata is left empty
for the repository owner to supply; no authorship or affiliation is inferred.

[PROCESS.md](PROCESS.md) records the required staged author and five-reviewer
protocol. Stage-specific source coverage, reviews, corrections, and checks are
retained under `process/` and `verification/`. The process record identifies
which stages have been accepted; the current compiled file is not a claim that
the entire writing process has finished.

Notation is defined in [the foundations](sections/01-foundations.tex):
`D=(V,E)` is the directed multigraph, `A` uses incoming minus outgoing,
`P` is the bounded equality-flow polytope, `O` is the observation set, `H` is
the sparse original-coordinate hull, `lambda_0` is the global residual state,
and `*_B` is a block-local merger. `r_B` is ambient block cycle rank and `a_B`
counts observed labels even if their candidate weights vanish.

Later stages will add separate section files through `main.tex`, preserving
this notation and the labels of the foundation results. Existing research
notes and code remain in their original repository locations; they are not
replaced by this manuscript.

[The compression section](sections/02-compression.tex) gives both cycle and
observation-sensitive formulations, a forest-complement original-coordinate
hull, and exact recovery. Its new worked example and fixed-coordinate
preprocessing checks can be run with:

```sh
python verification/stage02-exact.py
```

This check uses SymPy and exact rational arithmetic. The existing independent
observation-rank audit is `../code/network_simplex_review/verify_observed_rank.py`.

[The structured-oracle section](sections/03-structured-oracles.tex) develops
the cycle/theta support tests, exact compact recovery, and parallel-path
transportation cuts. Its standalone exact checks use only Python's standard
library:

```sh
python verification/stage03-exact.py
```

The checks enumerate theta vertices and small bounded transportation matrices,
verify the cut minimization identity, and check the joint-state example.

[The bounded-rank section](sections/04-bounded-rank.tex) gives complete finite
separation libraries, rank-dependent coefficient bounds, exact finite-basis
recovery, and sharp K4 examples. The recovery check uses the existing support
library builder (NumPy/SciPy are imported by that module), but calls no LP:

```sh
python verification/stage04-recovery.py
```

Every recovered state is checked exactly, as are the original-flow witnesses
and negative support certificates for the five-product K4 section.
