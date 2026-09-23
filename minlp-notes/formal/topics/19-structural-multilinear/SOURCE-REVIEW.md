# Topic 19: independent source and scope review

Reviewed on 2026-09-20 against the live result notes and manuscript sources.
This is a source inventory and semantic review, not a declaration coverage map
or a claim that the obligations below have been checked by Lean. The frozen
inventory and actual implementation status belong in `CLAIMS.md` and
`COVERAGE.md`.

The queue promises **feedback-variable, frequency-two and
incidence-treewidth-two bounds and stated sharpness/box extensions**. That
includes the convex-cardinality results used for the stated physical-box
extensions. It does not mean only the final scalar arithmetic implications.
The required graph, distribution, envelope and extremal-witness bridges
must also be proved.

## Primary sources and manuscript correspondence

| Live source | Relevant content | Live manuscript correspondence |
|---|---|---|
| `results/positive-multilinear-feedback-gap.md` | Universal local-law domination; repair; conditional forest gluing; factor `2^f`; original nonnegative boxes; sharp feedback-one flower | `paper-relaxation-limits/sections/05-feedback-frequency.tex`: `lem:feedback-repair`, `thm:feedback`, `prop:feedback-sharp` |
| `results/positive-multilinear-frequency-two-gap.md` | Degree slabs; half-integral cycles; baseline-preserving rounding; odd-girth bound; bipartite exactness; odd-cycle sharpness; zero-lower boxes | Same section: `lem:degree-slab`, `thm:frequency-two`, `eq:coverage-baseline` |
| `results/convex-cardinality-frequency-two-gap.md` | Discrete-convex cardinality envelopes; common upper attainment; sharp odd-girth bound; common-aspect physical products; fixed-ratio sharpness | Same section: `lem:cardinality-envelopes`, `thm:cardinality-frequency`, `cor:cardinality-box` |
| `results/positive-multilinear-treewidth-two-exact.md` | All-cycle factor coloring; two TU row classes; factor-two bound; cardinality and common-aspect extension; fixed-ratio sharpness | `paper-relaxation-limits/sections/06-treewidth-two.tex`: `thm:one-sided-coloring`, `thm:width-two-gap` |
| `notes/multilinear-frequency-two-positive-box-obstruction.md` | Exact unequal-aspect bipartite counterexample, ratio `7/6` | Scope boundary for frequency-two box claims |
| `notes/multilinear-frequency-two-positive-box-investigation.md` | Unequal-aspect bipartite family tending to `3/2`; forest exactness; bipartite factor-two upper bound | Additional boundary and adjacent investigation; not a general positive-box frequency-two theorem |

The integrated manuscript's README has a section describing existing Lean
coverage. It must link the precise topic-19 status when that status changes.
The standalone `paper-multilinear-gap/main.tex` is about the earlier degree
growth and explicit family results; inspection found no feedback,
frequency-two or treewidth claims there. Its export need not be presented as
a topic-19 proof bundle. Files under `process/snapshots/`, review `build/`
directories and historical verification directories are evidence snapshots,
not live manuscript sources to rewrite.

## Complete core obligation candidates

These identifiers are review identifiers; a final claim inventory may group
them differently, but should retain every mathematical obligation.

| ID | Obligation |
|---|---|
| S01 | Define finite original factor scopes, their variable-factor incidence graph, feedback-variable deletion, frequency at most two, the loopless dual multigraph, odd girth/bipartiteness and incidence treewidth. Relate these definitions to the polynomial/factor being evaluated. |
| S02 | Define scalar graph-hull and original-factor termwise gaps using actual multiaffine functions and prescribed means; relate the finite-law extrema to continuous graph envelopes. Establish nonnegativity and `H <= T`; ratios require `H > 0`. |
| S03 | Preserve constant/affine terms, nonnegative weights, empty families, unused variables, boundary means, ties, fixed coordinates and degenerate boxes. Explain duplicate original factors/identical supports if the data representation combines them. |
| F01 | Construct the feedback orientation/threshold law with all singleton means and simultaneous entrywise `2^(-f)` domination on every `(F,i)` marginal and on `F` itself. Include `F` empty and the case with no outside variable. |
| F02 | Repair each local law on `F union e` while preserving the prescribed common `(F,i)` marginals and dominating the old law divided by `2^f`. Treat zero residual masses and factors contained in `F`. |
| F03 | From incidence-forest structure, construct one joint law realizing the compatible conditional factor laws. Deal with disconnected components, isolated variables and zero-probability separator states. Mixing over feedback states preserves every marginal and gives the simultaneous nonnegative-local-payoff guarantee. |
| F04 | Use actual monomial deficiencies and maximizing local laws to obtain the unit-cube bound `T <= 2^f H`. Prove forest equality for `f=0`. |
| F05 | Extend F04 to original monomials on every finite nonnegative box. Construct a scope-local affine majorant with the common upper-envelope expectation; use expansion only inside that original factor. Fixed coordinates must not invalidate the structural hypothesis. |
| F06 | For every `n >= 2`, establish the actual flower polynomial, evaluation means, unit coefficients, `T=2-1/n` and `H=1`, including a law attaining the latter and an upper bound for every law. Prove one-variable feedback membership and treewidth exactly two; prove the ratio tends to two and hence supremum sharpness. |
| F07 | Establish the stated generic-nonnegative-payoff sharpness of the loss `2^f` using cell indicators, if the universal payoff result is included as a theorem. Distinguish it explicitly from unproved positive-monomial sharpness for general `f`. Private mean-one variables give distinct genuine scopes if needed. |
| Q01 | Construct the dual graph, including a distinct dummy vertex for each private variable and parallel edges for shared-variable pairs; prove the frequency-to-dual correspondence. |
| Q02 | Derive the exact coverage-gap representation with baseline `b_v=max p_i` and local target `c_v=min(1,sum p_i)`. Do not drop the baseline in an approximation argument. |
| Q03 | Define the degree-slab polytope, prove compactness and membership of the mean vector, and prove its extreme points have vertex-disjoint odd fractional cycles with value `1/2`, including tight-row rank, incidence counting and the even-cycle perturbation. Derive the finite extreme-point decomposition. |
| Q04 | Construct maximum-matching/complement rounding on every fractional odd cycle. Prove individual edge marginals and vertex coverage probability `1-1/(2L)`; account for other selected integral edges. |
| Q05 | Prove `E c_v(Z)=c_v(p)` and `E b_v(Z)>=b_v(p)` and use them to obtain the pointwise odd-girth factor `g/(g-1)` and universal factor `3/2`. Prove bipartite equality through an integral decomposition. |
| Q06 | Prove actual odd-cycle witness gaps `T=g/2`, `H=(g-1)/2`, the sharp ratio and the triangle specialization. Prove zero-lower-box transfer without introducing new factor incidences. |
| C01 | Define the multiaffine interpolant of a discrete-convex cardinality table. Prove its lower envelope is the consecutive-integer affine interpolation at the cardinality mean, with an attaining prescribed-mean law. Tables may be negative or decreasing; only their successive differences must be nondecreasing. |
| C02 | Prove the common-threshold law attains the upper envelope of every such factor. A proof via supermodularity/uncrossing must justify existence and termination or an extremal secondary objective. |
| C03 | For degree-slab vertices, prove the local curvature gap formula and rounding loss `T_v(z)/L`, lower-envelope averaging equality and upper-envelope concavity inequality. Deduce sharp odd-girth and bipartite results for cardinality factors. |
| C04 | Transfer C03 to original physical monomials with a common positive aspect ratio on each scope (equivalently each connected component after removing fixed coordinates). Prove the exponential-table representation and its discrete convexity; do not replace original factors by their expansions. Handle the trivial ratio-one case. |
| C05 | Prove fixed-positive-ratio odd-cycle sharpness by affine invariance and common positive scaling of bilinear gaps. |
| W01 | Prove the one-sided coloring lemma for every finite bipartite graph of treewidth at most two: every cycle whose factor vertices have one color has an even number of factor vertices. If using two-terminal series-parallel induction, prove the invariant under all series/parallel terminal types and supply the bridge from actual treewidth to blocks/networks and the articulation-color gluing. |
| W02 | Deduce two totally unimodular row classes from W01 using a proved integrality criterion and the cycle decomposition of even-degree support graphs. Balancedness alone suffices only for the monomial unit-right-hand-side argument, not arbitrary cardinality slabs. |
| W03 | Prove integral cardinality-slab decompositions for each TU class and simultaneous lower-envelope attainment. Mix both class laws, retain all singleton means and bound other factors by their own upper envelopes. Deduce `T <= 2H` for cardinality factors and the unit/zero-lower/common-aspect monomial cases. |
| W04 | Complete sharpness by F06 on the unit cube and, for every fixed `rho>1`, by the physical flower with coefficient `1/(1-epsilon)`, `epsilon=1/rho`. Prove the exact `T_n`, hull-gap expectation representation, truncation bounds, positive denominator eventually, `H_n -> 1-epsilon` and ratio limit two. Relate scaling to the original `[1,rho]` box. |

F01-F05, Q01-Q06 and W01-W04 are not discharged by proving arithmetic
consequences under hypotheses that assert the missing law, decomposition or
coloring already exists. Such conditional theorems can be useful intermediate
results, but their hypotheses must be discharged before claiming the source
theorems.

## Boundaries that the documentation must retain

- Feedback sharpness for positive monomials is proved for `f=1`, not for all
  `f`. The generic-payoff cell-indicator example contains zero literals.
- Bipartite exactness concerns the scalar sum of positive factors. It does
  not assert equality of the full lifted multilinear polytope with its
  standard relaxation.
- The general positive-box frequency-two bound is unresolved in these
  sources. Unequal aspect ratios can destroy bipartite exactness; the exact
  `7/6` example is `xy+xyz` on `[1,2] x [1,2] x [1,3]` at
  `(5/4,5/4,5/2)`. The documented strengthening tends to `3/2`, and does not
  refute a universal `3/2` bound.
- The cardinality factor is its multiaffine vertex interpolant, generally
  not the continuous function `phi(sum x_i)`.
- Nonnegative values of arbitrary local factors are weaker than positive
  monomial coefficients or convex-cardinality structure. The manuscript's
  `ex:parity-three` gives `T=3`, `H=1` at incidence treewidth and frequency
  two for factors with mixed monomial coefficients.
- A series-parallel representation, a good coloring, a TU partition and
  treewidth at most two are different hypotheses. An implementation must
  not rename a certificate hypothesis as a graph-theoretic theorem without
  proving its existence from the stated structural condition.
- Generic affine expansion preserves a polynomial but can change the
  factor relaxation, feedback number, frequency and incidence treewidth.
  Existing broad degree/box transfer theorems do not supply the missing
  structural-preservation argument.
- Sharpness as a supremum is not attainment of ratio two by a finite flower.
  The unit flower ratio is strictly below two for every finite `n`.

## Adjacent claims and algorithms

The queued scope names gap bounds, sharpness and box extensions rather than
all claims of the integrated manuscript. The following are adjacent claims
and must be explicitly distinguished if not included in `CLAIMS.md`:

- `results/positive-multilinear-frequency-two-optimization.md` and the
  algorithm section of `results/convex-cardinality-frequency-two-gap.md`;
  manuscript `prop:edge-cover-oracle`, `prop:cardinality-matching`, and
  `cor:scalar-envelope-algorithm`. These assert actual polynomial-time
  optimization/separation with rational encoding bounds. Proving only
  correctness of a candidate matching or a finite distribution LP does not
  verify their algorithms or complexity. They are not prerequisites for
  the nonalgorithmic gap proof.
- Manuscript `prop:independent-payoffs`, the general width-three discussion,
  and finite search counts: these are separate payoff/graph boundaries and
  experiments, not claims of sharp positive-monomial width-three bounds.
- `paper-relaxation-limits/sections/appendix-structural-auxiliary.tex`:
  `lem:canonical-pairs`, `lem:twin-compression`, `prop:signed-forest`.
  These auxiliary reductions should not be implied verified by a blanket
  statement that all structural appendices are formalized. Forest gluing
  needed in F03 remains a core obligation independently of whether this
  stronger signed/arbitrary-box proposition is included.

This distinction does not authorize dropping core cardinality or fixed-ratio
sharpness statements: they are explicitly part of the stated box extensions.
An unverified adjacent theorem can remain in the paper with a precise Lean
scope statement, provided no mathematical error was found in it.

## Existing proof reuse

The following declarations already exist in the canonical Lean tree.
Their presence was inspected; this review did not rerun their builds.

| Existing module under `formal/Formal/` | Useful existing interface | Limits |
|---|---|---|
| `CubicGap/Laws.lean`, `CubicGap/Hull.lean` | `Law`, expectation, finite mixtures/products/maps, binary vertices, convex-hull law representation | No forest gluing or local marginal compatibility follows merely from finite laws. |
| `MultilinearGap/GeneralGaps.lean` | `weightedTermwiseGap`, `thresholdLaw_hasMeans`, `thresholdLaw_monomial_upper`, `positive_polynomial_maximum_general`, `coupling_gap_bound_general`, `hullGap_le_weightedTermwiseGap` | Coupling hypotheses still need actual structural witnesses. |
| `MultilinearGap/MonomialEnvelope.lean` | `monomial_lower_attaining_law` with all ambient singleton means | Individual attainment is not simultaneous compatible attainment. |
| `MultilinearGap/EnvelopeFunctions.lean`, `BoxTransfer.lean` | Continuous cube/box envelope semantics and affine parameterization, including fixed coordinates | Structural scope preservation requires a separate argument. |
| `MultilinearGap/PhysicalEnvelope.lean` | `countOn`, `physMonomial_vertex`, `chord_le_of_convex`, `convex_count_expect_lower`, `exists_adjacentLaw`, common-threshold physical product attainment, physical lower envelope | The single-factor exponential result does not by itself prove general discrete-convex common upper attainment. |
| `MultilinearGap/SlabIntegrality.lean` | `convexHull_slabVertices_eq`, `exists_slabLaw`, `exists_adjacentLaw_of_slab` | One cardinality slab only; not graph degree slabs, half-integral matching structure or general TU integrality. |
| `MultilinearGap/BalancedOrientation.lean`, `FairOrientationFolding.lean`, `IntegratedLaws.lean` | Orientation laws, means and finite/integrated law infrastructure | The required feedback-specific entrywise joint-cell domination is additional. |
| `MultilinearGap/OriginalBoxTransfer.lean` | Original-box parameterization and envelope comparison | Its expansion-based general bound cannot silently transfer a graph restriction. |

## Review outcome

No contradiction in the three primary written gap proofs was identified by
this source review. The main verification risks are omitted structural
existence theorems, changed meanings of factor/envelope gaps, and overstated
positive-box scope. This review made no mathematical-proof completion claim,
ran no builds or numerical experiments, and inspected no CI status or logs.
