# Prior-art audit: pruned grids for sparse polynomial boxes

Date: 2026-10-02. This is a focused comparison for
[`polynomial-pruned-grid-extension.md`](../new-direction/polynomial-pruned-grid-extension.md).
I checked the cited primary texts available in the local literature packages;
I did not modify the literature knowledge base.

## Claim under review

The candidate extends the reviewed min-marginal-pruned geometric-grid method
from quadratic objectives to explicit rational polynomial factors of fixed
degree on a mixed product box. A verified upper bound on each continuous
coordinate's second derivative supplies the correction used for certified
additive approximation. Under a unique optimizer and global pointwise
quadratic growth, the proposed bit bound is
`f_d(p, κ) poly(I + q)`, with an absolute polynomial exponent, where `p` is
the supplied decomposition bag size and `κ = max(1, L/g)`. The growth
constant is not an input to the algorithm. For an all-integer box, the common
denominator of the original objective values lets an approximation gap below
one value-lattice step certify an exact optimizer found by the algorithm.

The proof reuses the pruned-grid theorem's semiconcave rounding inequality,
coordinate min-marginals, filtering, trial caps, and contraction argument.
Those are not polynomial-specific contributions. The polynomial extension
checks that curvature and rational table arithmetic can be verified at fixed
degree; the exact integer step is objective-value separation. The substantive
algorithmic boundary to test is therefore sparse tree-decomposition dynamic
programming with a logarithmic precision cost under quantitative growth,
including its exact all-integer consequence.

## Closest primary sources

**Bienstock and Muñoz, “LP Formulations for Polynomial Optimization
Problems,” SIAM Journal on Optimization 28(2), 2018, DOI
[10.1137/15M1054079](https://doi.org/10.1137/15M1054079), arXiv:1501.00288.**
Their Theorem 4 gives bounded-treewidth LP approximations for mixed-integer
polynomially constrained problems; for width `ω`, degree `π`, and tolerance
`ε`, the formulation has size on the order of
`(2π/ε)^(ω+1) n log(π/ε)` and certifies scaled feasibility and objective
tolerances. Their network reduction supplies related results for AC-OPF and
fixed-charge flow. This is the closest broad sparse-polynomial approximation
prior. It covers general polynomial constraints, while the candidate has only
a product box and a polynomial factor-sum objective. The stated tolerance
cost is polynomial in `1/ε` with a width-dependent exponent; it does not state
a `poly(log(1/ε))` bit bound under a quadratic-growth promise or the
denominator-based exact-integer discovery result. Conversely, the candidate
does not give their compact LP formulation or general constraint handling.
The exact binary reformulation in their Theorem 9 concerns finite Boolean
constraint satisfaction and is not an arbitrary-range integer-box result.
Primary text locators: Theorem 4 and its tolerance discussion, pp. 2–3;
Theorems 7 and 9, pp. 4–5 and 10–17. [[bienstock2018-lp-formulations-for-polynomial-optimization]]

**De Loera, Hemmecke, Köppe, and Weismantel, “FPTAS for optimizing
polynomials over the mixed-integer points of polytopes in fixed dimension,”
Mathematical Programming 115(2), 2008, DOI
[10.1007/s10107-007-0175-8](https://doi.org/10.1007/s10107-007-0175-8),
arXiv:0706.2354.** Theorem 1 gives an FPTAS for a nonnegative polynomial on a
bounded rational mixed-integer polytope when the *total dimension* is fixed;
Theorem 2 gives a weaker range-relative approximation for arbitrary-sign
polynomials. Runtime is polynomial in the input, degree, and `1/ε`. The
method discretizes continuous variables and uses fixed-dimensional lattice
optimization. This is a direct polynomial mixed-integer approximation
precedent, but fixed total dimension is stronger than bounded factor-graph
width when the number of variables grows. Its inverse-accuracy dependence
does not yield the candidate's logarithmic dependence on additive precision.
The arbitrary-sign guarantee is relative to the objective range, not an
exact optimum certificate from the original rational value spacing. Primary
text locators: input/encoding and Theorem 1, pp. 1–3; integer FPTAS, pp. 3–6;
mixed grid reduction, pp. 7–10; Theorem 2, pp. 13–15.
[[loera2008-fptas-for-optimizing-polynomials-over]]

**Lasserre, “Polynomials nonnegative on a grid and discrete optimization,”
Transactions of the American Mathematical Society 354(2), 2002.** This paper
gives an exact sum-of-squares/moment representation for polynomial
nonnegativity on a finite Cartesian grid, with a hierarchy order bounded in
terms of the grid cardinalities, and reduces discrete polynomial minimization
to a finite convex SDP. It is a direct exact-grid certificate predecessor.
Its matrix size depends on the dimension and grid cardinalities, so it does
not supply sparse treewidth DP with a cost logarithmic in interval range or
precision. The candidate uses a small adaptive grid and a global lower-bound
argument rather than a full-grid SOS representation. Primary text locators:
Theorem 3.2, pp. 8–10; representation theorem and discussion, pp. 14–19.
[[lasserre2002-polynomials-nonnegative-on-a-grid]]

## Discrete and hardness boundaries

**Del Pia and Di Gregorio, “On the Complexity of Binary Polynomial
Optimization Over Acyclic Hypergraphs,” Algorithmica 85, 2023, DOI
[10.1007/s00453-022-01086-9](https://doi.org/10.1007/s00453-022-01086-9).**
They give a strongly polynomial algorithm for β-acyclic binary polynomial
optimization, while α-acyclicity alone permits strong NP-hardness. This is a
useful exact discrete baseline and warns that local polynomial interactions
plus a broad acyclicity label do not automatically give tractability. It has
Boolean domains and hypergraph acyclicity, not large integer intervals,
quadratic-growth conditioning, or the candidate's precision-controlled
continuous relaxation. [[pia2023-on-the-complexity-of-binary]]

**Del Pia and Khajavirad, “Treewidth and the complexity of box-constrained
quadratic programs,” arXiv:2609.35595 (2026).** Their forest algorithm is an
exact quadratic-specific dynamic program; they prove strong NP-hardness for
quadratic box optimization at treewidth two and for quartic box optimization
on a path. These results make the candidate's fixed-degree and structural
assumptions consequential. The hardness statements do not establish hardness
under the candidate's global-growth/curvature ratio bound, and they do not
settle its conditioned approximation or integer-box theorem.
[[pia2026-treewidth-and-the-complexity-of]]

## Assessment and limits

The strongest close overlap is Bienstock–Muñoz for bounded-treewidth
polynomial optimization and De Loera et al. for mixed-integer polynomial
FPTASs. The local-grid and exact-value mechanisms each have clear
predecessors: adaptive min-marginal filtering is the reviewed pruned-grid
method, and a gap below the rational objective spacing is the standard way
to turn a certified additive approximation into exact discrete optimality.
The literature reviewed here does not state the combined guarantee of
fixed-degree sparse factor DP, arbitrary-width native integer ranges,
verified continuous-hull curvature, unknown global quadratic growth, and
`poly(log(1/ε))` bit cost (or exact all-integer discovery at the corresponding
conditioned bound). This is a bounded comparison, not a novelty proof; in
particular, it is not an exhaustive search for every treewidth-constrained
polynomial or MINLP algorithm.

For the exact integer statement, distinguish the algorithmic conclusion from
its promise: a unique optimum on a finite integer box has some positive
quadratic-growth constant, but that constant can be numerically tiny. The
polynomial-in-input consequence therefore requires `f_d(p,κ)` to be
polynomially bounded on the input family; uniqueness by itself does not make
the stated running time polynomial in input bits. Tied integer optima still
permit value-lattice stopping, but the draft does not give the same
growth-parameterized bound for that case.

No new source was identified that warrants addition to the knowledge base.
