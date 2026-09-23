# Sparse convex hulls for network flows coupled to a simplex

Read the [paper PDF](main.pdf) or [LaTeX source](main.tex). The manuscript covers
observation-sensitive formulations, exact structural separators and recovery,
sharp coefficient boundaries, implementations, and reproducible synthetic
comparisons. Author and affiliation metadata are left empty for the owner.

Build from this directory with TeX Live (including TikZ) and BibTeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The [source coverage map](process/coverage.md) connects repository results to
manuscript statements. [PROCESS.md](PROCESS.md) records acceptance and the
required five independent reviews of each stage and of the complete manuscript.
Internal acceptance is distinct from journal peer review or proof of priority.

## Main results and where to find them

| Topic | Manuscript source |
|---|---|
| Model, precise predecessors, known disaggregation, integral-flow hull equality, block gluing | [Foundations](sections/01-foundations.tex) |
| Exact residual-coordinate count from unobserved cycle ranks, forest complements, minimum individual-coordinate completion | [Compression](sections/02-compression.tex) |
| Cycle/theta unit cuts and recovery; parallel-path transportation separator | [Structured oracles](sections/03-structured-oracles.tex) |
| Bounded-rank separation and finite-basis recovery; sharp two-label, five-product K4 | [Bounded rank](sections/04-bounded-rank.tex) |
| Sparse coordinate-section universality and unrestricted coefficient ratios with two labels | [Universality](sections/05-universality.tex) |
| Sparse Fibonacci coefficient growth and simple maximum-degree-three realization | [Series–parallel obstructions](sections/06-series-parallel.tex) |
| Five tests for two observed labels; 16 circuits and unit coefficients for three; failure at four | [Flat chains](sections/07-fixed-state-chains.tex) |
| Implemented scope, exact/numerical evidence, strengthened comparisons, transportation interpretation | [Computation](sections/08-computation.tex) |

The residual-coordinate count concerns the supplied formulation, not minimum
extension complexity. Coefficient bounds apply to flow/product coordinates in
the stated rational row scaling. The compact at-most-m+1 decomposition uses
continuous graph points; the classical integral-flow hull equality does not
preserve that count for integral decomposition points.

## Code and verification

[Exact oracle instructions](../code/network_simplex/README.md), the
[flat-chain API](../code/network_simplex/FLAT_CHAIN.md), and
[compressed-formulation instructions](../code/network_simplex_compressed/README.md)
describe supported models and outputs. Exact cuts and decompositions are
rational certificates. Floating-point LP feasibility and the general API's
`numerically_feasible` status are not exact membership certificates. The
bounded-rank libraries are verification prototypes, not a production oracle
for every general graph.

Run the principal regression suite from this directory:

```sh
PYTHONPATH=../code python -m unittest network_simplex.test_separator \
  network_simplex.test_flat_chain \
  network_simplex_benchmarks.test_strong_baselines -v
```

The following standalone checks cover manuscript constructions and exact
recovery. Some require SymPy, NumPy, and SciPy; the individual files distinguish
exact arithmetic from numerical LP comparisons.

```sh
python verification/stage02-exact.py
python verification/stage03-exact.py
python verification/stage04-recovery.py
python verification/stage05-padding.py
python verification/stage05-profile.py
python verification/stage07/integral-hull.py
```

[Stage 7 validation](verification/stage07-validation.json) records source hashes,
checks, the source diff from the preceding accepted manuscript, and the build.
Earlier stage evidence, independent reviewer programs, and accepted correction
records remain under `verification/` and `process/`.

## Reproduce the comparisons

Run from this directory:

```sh
PYTHONPATH=../code python -m network_simplex_benchmarks.paper_stage06 \
  --output verification/stage06-benchmarks.json
python verification/stage06-tables.py
```

[Benchmark instructions](../code/network_simplex_benchmarks/README.md) give the
methods, dependencies, controls, and an optimization-only rerun command.
[Raw results](verification/stage06-benchmarks.json) retain objectives, side rows,
versions, warmups, five rotated measurements, timing summaries, and separate
audits. Optimization and membership measurements were collected separately;
current optimization records use native fixed-weight state-flow bounds.
Tables are generated from these records and check complete case keys, method
coverage, rotations, and every stored timing summary.

The strongest globally merged LP is often fastest. In the control where all
labels are globally observed but each block sees few, local compression reduces
7,215 state-flow variables to 495 total variables and observed elimination to
367. Initial compression is faster than elimination on that control. Stronger
LPs also overturn earlier boundary-face long-chain speedups. All experiments
are synthetic and run on a shared host; no universal runtime or industrial
performance claim follows.

## Historical records

The [old paper-readiness record](../notes/network-simplex-paper-readiness.md)
and [continuation record](../notes/network-simplex-reopened-status.md) are
superseded research closeouts. Their original 41-circuit descriptions, earlier
K4 examples, timings, and default-method assessments remain useful provenance,
but the manuscript contains the sharper observed-label results and stronger
baseline comparisons. The older fixed-state theorem is retained in
[the result note](../results/network-simplex-flat-chain-fixed-states.md).

[Pre-upgrade source copies](verification/reference/stage06/README.md) preserve
the unreduced flat oracle. [The first computational archive](verification/stage06-corrections/round1-archive/)
retains earlier sources and measurements. These are reproducible historical
references, not additional production APIs or current performance conclusions.
