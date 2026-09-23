# Source audit: block PSD precision with unconditional output error

Date: 2026-09-05. Focused independent source audit of
[the block-body extension](block-psd-unconditional-error-precision.md) and
[the rational block log-determinant oracle](rational-block-logdet-convex-body-oracle.md).
Separate reviewers assess the proofs.

## Assessment

No matching theorem was found in the checked literature. The supported
claim is the same individual-block-rank approximation guarantee against all
convex lifted formulations, now for a single unconditional convex output
error body. The bound is
`p_out<=p_conv+O(sum_b r_b log(r_b+1))`, with no output-dimension term in
the additive integer overhead. Noncommuting PSD Hessians within blocks
remain allowed.

Relative to the repository's block PSD theorem and positive-separable
unconditional-body theorem, this is a natural synthesis and a useful
generalization. It should be presented as an extension of that structural
theory, not as a separate discovery of convex matrix allocation. The direct
Euclidean oracle also simplifies the supporting construction, but its
convex-optimization mechanism is classical.

## Established sources and what they support

Vandenberghe, Boyd and Wu's
[Determinant maximization with linear matrix inequality constraints](https://web.stanford.edu/~boyd/papers/pdf/maxdet.pdf)
(1996 author preprint; 1998 journal publication) establishes the MAXDET
framework and interior-point methods. Linear trace budgets and block
semidefinite caps fit that framework directly. An arbitrary
separation-oracle body need not have an explicit finite LMI description:
the candidate's general-body solver therefore also invokes general
separation-based convex optimization. Calling this oracle an application
of an established log-determinant objective is accurate; calling every
oracle body an explicitly represented MAXDET instance would require an
additional representation assumption.

Groetschel, Lovasz and Schrijver's
[The ellipsoid method and its consequences in combinatorial optimization](https://ir.cwi.nl/pub/10046/10046D.pdf)
(1981), Definition (5) on printed page 172, gives rational weakly feasible,
approximately optimal outputs. Definition (6) specifies weak separation;
equation (7) requires known inner and outer balls about a common center.
Theorem (3.1), printed page 177, supplies polynomial separation--optimization
equivalence, with binary accuracy dependence. These conditions were checked
in the original text. GLS alone does not promise an exactly feasible
output; the candidate supplies its own rational central-ball repair.

Massoulie's primary report,
[Structural properties of proportional fairness: stability and insensitivity](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2005-102.pdf),
Section 1, equations (1)--(2), already optimizes log utility over general
convex downward-closed capacity regions. Section 2 also treats logarithmic
coordinates. This is a close scalar allocation precedent for arbitrary
monotone budgets, although it does not address matrix blocks or minimum
integer dimension.

The [block PSD audit](block-psd-quadratic-precision-novelty.md) records the
checked Fischer determinant inequality, Hessian-adjacency block
decomposition in MINLP, and anisotropic interpolation precedents. The
[positive unconditional-body audit](positive-separable-unconditional-error-novelty.md)
records the coordinatewise domination and general allocation antecedents.
Those findings carry over without a new priority claim for the ingredients.

## Oracle interface and scope distinctions

The supporting lemma supplies a bounded log-determinant hypograph in
independent symmetric-matrix coordinates. Its explicit spectral lower
caps and rational interior ball address the full-dimensionality and
conditioning requirements of the GLS import. Rational PSD separation,
exact inverses and determinants, and scalar logarithm intervals provide
the claimed weak separation interface. These are concrete implementation
details to verify, not a new optimization principle. A real-arithmetic
interior-point convergence theorem alone would not certify all these
rational bit guarantees.

The lemma allows an arbitrary rational linear map `L` and a closed convex
body containing a known ball; it does not require positivity or symmetry.
The graph application is narrower. It uses PSD trace outputs and
unconditionality to infer both `E(P) in K` from expected Jensen errors and
`E(P_tilde) in K` after Loewner-decreasing rational grid repair. Keeping
these scopes separate prevents attributing a stronger graph theorem to
the general oracle lemma.

## Comparison with formulation-wide literature

Lubin, Zadik and Vielma,
[Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
already supplies the midpoint/parity obstruction for unrestricted integer
variables, including a lower bound from pairwise midpoint incompatibility.
The [earlier source audit](bilinear-graph-binary-complexity-novelty.md)
documents the checked Definition 4.2 and Lemma 4.1. This is the foundational
lower-bound mechanism here, not a new consequence of unconditionality.

The extension's specific contribution is quantitative: the expected
nonnegative Jensen vector dominates a feasible block trace allocation in
the same body `K`. Combined with block covariance volume, this constrains
every convex lift. The matching compact grid controls the whole error
vector by that allocation and preserves the same block-rank overhead.
The final MILP does not need an exact polyhedral description of curved `K`.

The literature comparisons checked in the linked audits address
prescribed approximations, mesh resolution, convex representability, or
optimization algorithms. No checked source gives this finite comparison
to the minimum integer dimension over all convex lifts under a general
unconditional error budget.

## Limits and search record

The block coordinates must be disjoint original inputs, with the product
domain retained through separate common-kernel quotients. Copy-variable
decompositions introduce coupling and do not automatically qualify.
Unconditionality is stronger than central symmetry; arbitrary correlated
ellipsoids are not covered. Output dimension and oracle encoding affect
runtime and continuous size even though they do not appear in the additive
integer count. Constructing the MILP does not make it polynomial-time
solvable.

Fresh searches combined log-determinant allocation with monotone convex
bodies, block quadratic unconditional approximation, and mixed-integer
convex approximation with norm errors. They found no exact match beyond
the established source families above. This is a bounded no-match
assessment, not proof of global priority. The strongest presentation is
a general error-budget corollary within the block-rank precision theorem.
