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

[Universality](sections/05-universality.tex) transfers the classical slim
transportation representation into a sparse coordinate section. The
[series--parallel construction](sections/06-series-parallel.tex) proves
exponential facet-coefficient ratios with a sparse observation set, including
a simple graph of maximum degree three. The
[fixed-state chain section](sections/07-fixed-state-chains.tex) gives exact
profile elimination and recovery, a five-test oracle with two explicit
states, and a sharp unit-coefficient guarantee through three explicit states.
These last refinements were developed during the manuscript work.

```sh
python verification/stage05-padding.py
python verification/stage05-profile.py
```

The padding check uses exact standard-library arithmetic. The profile check
uses SymPy for exact circuit and inverse-basis calculations and NumPy/SciPy
for separately labeled numerical state-flow LP comparisons. It checks exact
recovered flows, all affine branches for one and two explicit states,
coefficient extrema and the exceptional bypass repairs for three states,
zero weights, and lower-dimensional profiles. It imports no existing
repository oracle implementation. Neither script implements or purports to
reprove the cited transportation universality construction computationally.

[The computation section](sections/08-computation.tex) documents the implemented
scope, exact-versus-numerical certificates, strengthened LP baselines, repeated
synthetic experiments, and a two-supplier transportation interpretation. Its
tables are generated directly from the retained five-run JSON:

```sh
PYTHONPATH=../code python -m network_simplex_benchmarks.paper_stage06 \
  --output verification/stage06-benchmarks.json
python verification/stage06-tables.py
```

Run these from the manuscript directory. The default study includes both
boundary and interior flat-chain weights, globally unused labels, an ablation
where every global label is observed, and one coupled aggregate budget.
The stronger LP baselines overturn the earlier boundary-face long-chain
speedup. Global merging explains much of the earlier many-label gain, while
the all-labels-observed control demonstrates additional local compression.
All timing ranges and audit distinctions remain in the raw data.

The current full/global optimization baselines substitute fixed simplex weights
before assembly, using only positive state flows and native scaled bounds.
The three optimization cases were remeasured after this correction; membership
and cold-library measurements remain unchanged. The original measurements and
sources are retained in `verification/stage06-corrections/round1-archive/`.
The table generator checks distinct complete case keys, optimization order,
expected method coverage, and all stored timing summaries. The correction
record includes the command for the optimization-only rerun.

The current exact flat oracle stores a compact default for unused labels,
uses no library at two observed labels, and returns unit flow/product cuts
through three observed labels. Its research predecessor is retained in
`verification/reference/stage06/`. See
[benchmark instructions](../code/network_simplex_benchmarks/README.md) and
[the updated exact-oracle API](../code/network_simplex/FLAT_CHAIN.md).

```sh
PYTHONPATH=../code python -m unittest network_simplex.test_separator \
  network_simplex.test_flat_chain \
  network_simplex_benchmarks.test_strong_baselines -v
```
