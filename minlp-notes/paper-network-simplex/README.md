# Sparse convex hulls for network flows coupled to a simplex

The [submission PDF](delivery/submission.pdf), [standalone LaTeX source](delivery/latex-source.zip),
and [computational supplement](delivery/computational-supplement.zip) are prepared
for the September 9 submission revision. Author and affiliation fields are
intentionally empty. No external submission has been made.

All three stages and the whole-manuscript review are complete under the required
five-reviewer process. All accepted findings are resolved. That submission manuscript
has 50 pages; its source archive builds independently and its computational
supplement includes reproducible checks and measurements. See the
[final report](revision-20260909/FINAL_REPORT.md),
[validation record](revision-20260909/final-validation.json), and
[process](PROCESS.md). Earlier September 7 completion records are historical
and do not establish acceptance of this revision.

The [current PDF](main.pdf) includes the later Lean verification account below
and was rebuilt from clean sources for the
[September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md).
The submission PDF and archives retain the September 9 revision.

Build the manuscript from this directory with TeX Live and BibTeX:

```sh
SOURCE_DATE_EPOCH=946684800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The [delivery guide](delivery/README.md) explains deterministic package rebuilding
and manifests. Each archive builds or runs independently of the repository.

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

## Computation and verification

Lean verification covers the general simplex disaggregation and flat-chain
profile equivalences in [topic 06](../formal/topics/06-network-simplex/COVERAGE.md)
and the mathematical claims of Section 7 in
[topic 15](../formal/topics/15-flat-chain-threshold/COVERAGE.md). The latter
includes determinant bounds, exact circuit counts, the unit-coefficient threshold,
rational separation and recovery, and observed-label reduction. The
[topic 06](../formal/topics/06-network-simplex/VERIFICATION.md) and
[topic 15](../formal/topics/15-flat-chain-threshold/VERIFICATION.md) verification
records distinguish the original checks from later additions. These proofs cover
the stated arithmetic and word-operation models and rational bit bounds; they do
not certify the compiled rational backend, the Python implementations, historical
timings, or novelty. They do not cover the rest of the manuscript.

The [supplement instructions](delivery/README-supplement.md) give dependencies,
precise commands, independent-check scope, and the distinction between exact
certificates and numerical LP outputs. The [interface guide](delivery/API.md)
records supported inputs and output conventions. The principal regression suite
can also be run from the repository root:

```sh
PYTHONPATH=code python -m unittest network_simplex.test_separator network_simplex.test_flat_chain network_simplex_benchmarks.test_strong_baselines -v
```

The supplement includes the canonical raw measurements and all five generated
table/value files. Its full benchmark command writes fresh timings to a separate
file; the table generator reproduces the reported tables from canonical data.
The strongest globally merged LP is often fastest. Local compression has a
separate size benefit when all labels occur globally but each block sees few.
All instances are synthetic and timings were collected on a shared host.

## Historical records

The September 7 [final summary](process/final-summary.md),
[whole-manuscript assessment](process/assessments/stage08-accepted.md),
[source coverage map](process/coverage.md), and
[validation manifest](verification/final-validation.json) describe their reviewed
versions. They remain unchanged as provenance. The active revision's author,
review, adjudication, and freeze records are under `revision-20260909/`.
Internal acceptance is distinct from journal peer review or proof of priority.
