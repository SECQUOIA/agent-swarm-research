# Stage 7 author record

Status: author work complete; five independent Stage 7 reviews are pending.
The separate whole-manuscript review stage remains required. No author,
affiliation, submission, or external peer-review status has been invented.

## Final exposition

The abstract and new `sections/00-introduction.tex` organize the paper around
graph structure and retained state information. The contribution list and
structural scope table distinguish the exact residual-coordinate count of the
observation-sensitive construction from optimal extension complexity. They
foreground bounded-rank separation and the larger recovery parameter factor,
the sharp five-product K4, the unit-coefficient threshold through three
observed labels on flat chains, five profile tests at two labels, 16 circuits
at three, the sparse Fibonacci family, and unrestricted two-label universality.
Local checks, bound grouping, coefficient scaling, and the ambient-space scope
of minimum individual-coordinate completion remain explicit.

`sections/09-conclusion.tex` relates the positive results to the coefficient
obstructions and the corrected computational findings. Its claims concern
the stated graph families. Small treewidth alone and small label count alone
do not imply a coefficient bound for the unrestricted class, but no inference
of separation hardness or large extension complexity is made.

The native TikZ diagram `figures/flat-chain.tex` depicts G4, its arc pairs,
bypass, and shared state profile. It is placed after the graph definition;
the standard `flafter` package prevents a float from appearing before that
definition. Author metadata remains empty. The introductory table also gives
direct theorem locators for readers selecting a formulation or oracle.

## Mathematical addition and verification

`cor:integral-flows` records the classical fact that integral balances and
capacities permit restricting x to integer flows before convexification
without changing H. Its proof first establishes vertex integrality directly:
a nonempty nonintegral-arc subgraph contains an undirected cycle or a loop,
whose signed circulation gives a two-sided feasible perturbation. Boundedness
then permits integral-vertex decomposition. Refining every positive-weight
simplex-vertex flow gives the required integral graph-point mixture.

This does not preserve the at-most-m+1 bound for integral decomposition points;
the proof and explanatory paragraph explicitly retain that bound only for
continuous graph points. An m=0 fractional parallel-arc flow gives a concrete
counterexample to the stronger interpretation. Fractional coordinate sections
are not claimed to be integral.

`verification/stage07/integral-hull.py` independently enumerates bounded-flow
vertices by bound choices and rational column elimination. It checks 18 small
multigraphs, 78 exact integral vertices, 54 exact refined state decompositions,
empty and zero-dimensional systems, and the decomposition-size counterexample.
It imports no production oracle and calls no LP. These finite checks are
implementation evidence for the example construction, not a computational
proof of the general corollary.

## Literature and source consistency

The closest bilinear, gluing, RRLT, Cayley/transportation, fan, universality,
and multiflow comparisons remain intact. The precise published KD electronic
companion locator and its representation of equality balances by opposite
inequalities are retained. The transportation illustration now acknowledges
KD Section 4.2 as inspiration for the stated two-supplier/common-simplex model.

The new Fiorini comparison was checked against the openly accessible
[author manuscript](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf)
and [publisher metadata](https://www.sciencedirect.com/science/article/pii/S1572528606000168).
It attributes transfer from general 0/1-polytope facets to acyclic-subgraph
facets and distinguishes the present sparse bilinear coordinate sections.
The publisher search result verifies Discrete Optimization 3(2), 136–153
(2006), DOI 10.1016/j.disopt.2005.10.007; a direct publisher open returned an
internal fetch error, while the author PDF was readable. Neither large
coefficients nor broad facet transfer is claimed as a new phenomenon.

The integral-flow corollary cites Hoffman–Kruskal's classical integrality
work. The openly accessible [primary reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf)
identifies the original 1956 chapter, pages 223–246 in *Linear Inequalities
and Related Systems*. The bibliography uses the original publication rather
than a later electronic reissue date. The manuscript also supplies the direct
network proof, so the corollary does not depend on an unstated citation lemma.

`process/coverage.md` now supplies every previously missing manuscript locator.
The README is a complete entry point for the PDF, sources, build, code,
experiments, exact and numerical evidence, and review records. Historical
readiness and continuation notes receive short supersession pointers; their
original proofs, numbers, and assessments remain unchanged below those
pointers. The README identifies the earlier fixed-state and timing records
as historical rather than current conclusions.

## Corrected computational evidence

No production code, benchmark generator, accepted raw data, or generated table
was changed in Stage 7. The new introduction uses only accepted fixed-weight
metrics: the all-labels-observed control has 7,215 state-flow variables in
full/global disaggregation, 495 total variables in initial compression, and
367 after observed elimination. Median full/global times are about 30 ms,
versus about 10 ms for initial compression; elimination gives the smallest
model but takes longer. The globally merged LP is often fastest in the other
comparisons. No universal runtime or industrial claim is made.

The computation section retains scientifically relevant provenance: optimization
and membership measurements were collected separately, every optimization
method uses the same inputs and a fresh five-run comparison, and older sources
and records remain reproducible. Internal review chronology is left in the
process records. Numerical LP answers remain distinct from exact witnesses and
cuts. The H-intersected-with-budget interpretation is unchanged.

## Changes to accepted sections and final checks

The only mathematical addition to accepted sections is `cor:integral-flows`.
Section 01 also gains the Fiorini paragraph; section 06 gains the diagram and
its reference; section 07's title now emphasizes observed labels; section 08
gains the application attribution and cleaner measurement provenance. All
other accepted proofs are unchanged. The complete textual diff against the
Stage 6 accepted snapshot is retained in `verification/stage07/source.diff`.

Validation checks the complete source input tree, duplicate/missing labels,
citation keys, README links, all source-coverage locators, corrected benchmark
sizes and timings, the accepted table/data hashes, and unchanged production
dependencies. The table generator independently rechecks its raw summaries.
The final forced LaTeX build is clean. The front matter, scope table, integral
corollary, graph diagram, conclusion, and bibliography were rendered and
visually inspected. Source and evidence hashes, commands, exact check counts,
and build details are in `verification/stage07-validation.json`.

No unresolved substantive issue is known to the author. Stage 7 review must
finish before the full-manuscript five-reviewer cycle can begin.
