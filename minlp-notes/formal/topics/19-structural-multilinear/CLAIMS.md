# Topic 19: structural multilinear gaps — claim inventory

Scope fixed on 2026-09-20 after independent source review. The obligations
below were frozen before implementation. They are now discharged by the
declarations in the [coverage map](COVERAGE.md); check results are recorded
separately in [VERIFICATION.md](VERIFICATION.md).

The sources and live manuscript labels are listed in
[SOURCE-REVIEW.md](SOURCE-REVIEW.md). The main paper is
`paper-relaxation-limits`, sections 5 and 6. This package covers the queued
feedback-variable, frequency-two and incidence-treewidth-two gap theorems,
including their stated sharpness and box extensions. Constants and affine
terms, zero coefficients, empty supports, boundary means, unused variables,
fixed coordinates and zero gaps must retain their correct semantics.

## Required mathematical statements

These identifiers are the frozen topic-19 obligations. All remain in scope
until proved; partial helper results do not discharge their missing premises.

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

## Scope boundaries

The full statements above require the actual structural hypotheses. A law,
coloring, decomposition, or totally unimodular partition supplied as a premise
is a useful intermediate result, but it does not prove that the stated graph
hypothesis supplies that object. No theorem may be marked complete by assuming
its central conclusion.

The following adjacent claims are outside the queued gap scope:

- Polynomial-time weighted-matching/edge-cover optimization, scalar-envelope
  separation and their rational bit-complexity claims. They are separate
  corollaries in the source notes and paper, not prerequisites for these
  existence and gap proofs. This package must not describe them as verified.
- The broader manuscript's width-three investigation, parity-factor
  counterexample, canonical-pair and twin-compression lemmas, and signed-factor
  forest extension. F03's forest gluing remains required.
- Novelty, priority, historical experiments, physical validation and external
  peer review.

The general unequal-positive-box frequency-two bound remains unresolved in
the sources. Its exact bipartite counterexample (ratio 7/6) must be retained in
the documentation. Positive-monomial feedback sharpness for arbitrary f is
not claimed: the generic-payoff example uses zero literals. All cardinality
factors mean their multiaffine vertex interpolants, not phi of the mean sum.
Sharpness of the constant two means a supremum, not finite-family attainment.
