# Source audit: compact precision for any dense convex polynomial

Date: 2026-09-05. Status: bounded primary-source audit. The candidate and its
signed-curvature integration dependency still require their separate proof
reviews.

The [hybrid candidate](compiled-convex-polynomial-hybrid-precision.md) claims
a deterministic polynomial-time rational MILP construction for the entire
graph of any dense rational polynomial convex on `[0,1]`, at rational
absolute tolerance `epsilon`, with `p_out<=p_conv+11`. The minimum `p_conv`
allows arbitrary convex lifts, unrestricted continuous size, and unrestricted
integer coordinates. Unlike earlier local results, polynomial coefficients
may have either sign and curvature need not be monotone.

No matching construction and whole-formulation comparison was found in the
checked primary sources. There are close established algorithms for optimal
scalar segmentation, including greedy construction, dichotomic extension,
and splitting into pieces with controlled shape. Those ingredients require
explicit attribution. The proposed contribution is the compact rational
realization and constant integer overhead, with polynomial bit complexity
even when an explicit near-optimal segment list would be exponentially long.

## Exact rational sign tests are an established import

[Sagraloff and Mehlhorn, Computing Real Roots of Real Polynomials](https://arxiv.org/pdf/1308.4088),
Theorem 3, restated as Theorem 36, gives certified real-root isolation and
refinement. For square-free integer degree `n` and coefficient bit bound
`tau`, the stated refinement complexity is polynomial in `n,tau,kappa`,
where requested isolating width is `2^(-kappa)`; the integer-input bound is
`O-tilde(n(n^2+n tau+kappa))`. Rational denominator clearing and square-free
factorization permit its use here. Repeated roots do not require deciding
polynomial signs by floating-point evaluation at approximate critical points.

For completeness, the exact sign-decision reduction needed in the hybrid is
short. Given rational `q` and rational `[a,b]`, first handle `q=0`, constants,
and a degenerate interval directly. Isolate all distinct interior real roots
in disjoint rational intervals with nonroot endpoints. Rational roots at
`a,b` can be detected and factored out for isolation purposes. Evaluate the
original `q` at `a,b` and at both ends of every interior isolating interval;
if there are no interior roots, one interior rational sample also suffices.
These samples detect the sign on every component between consecutive roots,
including both sides of each root. The value at a root itself is zero.
Thus they decide nonnegativity or nonpositivity exactly. A conventional
Sturm or subresultant sign algorithm is an equivalent standard implementation.

Apply this to `q=chord_(a,b)-f-epsilon/2`. The chord coefficients are rational
with polynomial bit length because `a,b` are rational grid points of polynomial
encoding length and `f` is densely encoded. The same import checks `f''>=0`
and isolates roots of `f'''`. Its dependence on root separation is through
precision bits; an inverse-separation number of uniform grid cells is not
required. This is a source justification for exact scalar decisions, not
a new polynomial-nonnegativity algorithm.

## Closest segmentation predecessors

**LinA.**
[Codsi, Ngueveu, and Gendron, open 2021 report](https://www.cirrelt.ca/documentstravail/cirrelt-2021-39.pdf),
Section 3, Proposition 1, Corollary 1, and Algorithm 1, establish greedy
maximal-segment optimality for corridor fitting. Section 4.1, Algorithm 2,
uses dichotomy. Section 5.2, Algorithm 5 and Lemma 4, gives at most `k-1`
extra segments after splitting into `k` convexity pieces. That section
explicitly describes logarithmic complexity *per segment*; Algorithm 1
enumerates the whole list. These are direct method predecessors, but not
a compact random-access result polynomial in accuracy encoding. The
[final publication](https://link.springer.com/article/10.1007/s12532-024-00274-8)
is Mathematical Programming Computation 17, 265--306 (2025). The theorem
and algorithm numbering just cited refers to the checked open report.

**Continuous-function regression.**
[Warwicker and Rebennack](https://publikationen.bibliothek.kit.edu/1000168639/152338266)
extend discrete-data PWL algorithms to continuous functions and preserve
convexity in the convex case. Their Theorem 3 bounds runtime using accuracy,
domain length, a bound involving `sqrt(max|f''|)`, final discretization size,
and optimal breakpoint count. This is an explicit useful complexity result,
but it is not a polynomial-bit compact graph formulation measured against
the minimum number of unrestricted integer coordinates. Their final article
appeared in IISE Transactions 57(3), 231--245, with online publication in 2024.

**Optimal scalar interpolation.**
[Fathabad, Cheng, Pan, and Yang](https://ira.lib.polyu.edu.hk/bitstream/10397/99199/1/Fathabad_Asymptotically_Tight_Conic.pdf),
Section 3.2, prove minimum interpolation-point counts for their monotone
concave setting via sequential extension. The
[earlier scalar audit](compiled-curvature-quantile-precision-novelty.md)
also records minimax segmentation and discrete-data fitting predecessors.
The hybrid must not be called the first algorithm for minimum-error or
minimum-piece polynomial approximation. Its output need not even attain
the exact minimum piece count; the theorem is a constant integer-count
comparison and a uniform representation guarantee.

**A direct PSE predecessor.**
[Geissler and coauthors, Solving power-constrained gas transportation problems](https://optimization-online.org/wp-content/uploads/2014/11/4660.pdf),
Section 2.1, Algorithm 1 and Theorem 2.2, use minimax piecewise-linear
approximations and explicit MILP error bands in gas-network models. Their
optimality statement is conditional on termination; the text explicitly
notes the absence of a general convergence proof for that algorithm.
This supports the modeling relevance and supplies early application context,
but does not give the hybrid's polynomial-bit guarantee.

## What the hybrid adds, subject to proof review

The useful distinction is its treatment of the additive cost of splitting
at `O(D)` curvature changes. It first enumerates at most `9D` greedy grid
segments. If that finishes, the explicit list is already polynomial in
input size and has a controlled count. If it does not, a proved lower
bound `N_epsilon>D` absorbs the splitting cost into a constant-factor total
cell count. Certified local curvature routines then provide random access
to each local grid, and one global index selects from the sum of local cell
counts. The circuit compiler makes this compact without extra integer gate
variables. This is a synthesis of existing tools; the random-access and
bit-complexity conclusions are essential to distinguish it from explicit
segmentation algorithms.

The [compiler source audit](compiled-rational-knot-formulations-novelty.md)
credits established Boolean extended formulations and index-bit product
encoding. The [signed-curvature dependency](certified-monotone-polynomial-curvature-quantiles.md)
uses classical Taylor certificates, polynomial root separation, and adaptive
quadrature. Its proof, especially the polynomial number of analytic panels,
must be validated independently; root isolation alone does not certify
the complete integration or formulation theorem.

No sparse binary-degree complexity, nonconvex-polynomial graph theorem,
multivariate nonseparable result, ideal relaxation, or polynomial-time MINLP
solution claim follows. The finite scalar two-bit comparison and the
constructive eleven-bit comparison are different statements. The bounded
literature search supports a qualified novelty claim for the latter scope,
not a broad claim of priority for optimal scalar approximation.
