# Publication assessment: subset moments for quadratic indicator stars

Date: 2026-09-25. Scope: the completed September 25 indicator-star work.
This assessment prepares the existing results for possible publication;
it does not claim a compact formulation, a new tree optimization algorithm,
or resolution of the open extensions.
The fresh mathematical review passed without a substantive correction.
No unresolved proof gap is known in the claims listed below. Publication
priority remains a qualified source comparison, not a certified fact.

## Recommended contribution and status

The strongest result in this package is a quantitative failure of a
precisely specified local formulation. For each positive integer `k`, a
rational positive-definite quadratic on a star with `2k` leaves has a
point below its original indicator epigraph hull, although its moments
pass exact compatibility tests on every subset of at most `k` leaves.
The additive and relative gaps are bounded below by absolute constants
times `k^-2`. Spectral bounds, the norm of the prescribed continuous
means, and the true epigraph height are bounded independently of `k`.
The rational instance and displayed witness have polynomial encoding.

This is a credible focused theoretical contribution when presented with
the general moment-to-quadratic transfer theorem. Its value is the
simultaneous realization of a known incompatibility phenomenon in the
original variables of a strongly convex sparse optimization model, with
quantitative and arithmetic control. It is not a major algorithmic advance
on its own. A possible publication should make the transfer and its
restricted formulation consequence central, rather than treating quantum
incompatibility or a planar inverse-square rate as discoveries.

The supporting face result should remain a structural observation in the
same package or an appendix. The small explicit gaps are useful examples,
not separate headline contributions. No computational speedup, empirical
solver comparison, or unconditional extended-formulation lower bound has
been established.

## Exact claims available for use

Let

\[
 E_Q=\{(x,z,t):z\in\{0,1\}^{n+1},\quad
 x_i(1-z_i)=0,\quad t\ge x^TQx\},
 \qquad
 Q=\begin{pmatrix}a&b^T\\ b&\operatorname{Diag}(d)\end{pmatrix},
\]

with `d_i>0` and `a>sum_i b_i^2/d_i`. Continuous variables are free real
variables; there are no additional indicator or continuous constraints.
For the moment results fix the center indicator to one, its mean to `m`,
and the leaf masses to `z_i in (0,1)`. Write

\[
 M=\begin{pmatrix}1&m\\m&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

Order `k` requires, separately for every `J` with `|J|<=k`, matrices
`G_S^J` indexed by `S subset J` such that

\[
 G_S^J\succeq0,\qquad \sum_{S\subseteq J}G_S^J=M,
 \qquad \sum_{S\ni i}G_S^J=M_i\quad(i\in J).
\]

All subsets share `M` and the singleton matrices `M_i`. They do not
share higher-order pattern marginals on their intersections. This
definition must accompany any use of the term "subset moment relaxation."
It is not automatically the named `OptPairs` relaxation, a sparse SOS
hierarchy, or a hierarchy with consistent overlap measures.

At prescribed leaf means `y`, minimize

\[
 av+\sum_i\left[
 \frac{d_i}{z_i}\left(y_i+\frac{b_i}{d_i}s_i\right)^2
 -\frac{b_i^2}{d_i}r_i\right]
\]

over these moments. Denote this value by `R_k` and the true closed-hull
height at the same original means and indicators by `H_k`.

| Claim | Precise result and role | Main proof |
|---|---|---|
| Full compatibility | With all leaves in one parent, minimizing the displayed expression gives both the ordinary and closed convex-hull height. A minimum is attained by a finite scalar law with at most two atoms per nonzero pattern. A PSD parent describes a closed moment cone, but zero-mass second moments cannot occur at an optimum because the Schur complement is positive. This is supporting characterization, with no compact-size claim. | [Moment note, full compatibility](tree-indicator-moment-gluing.md#full-compatibility-gives-the-exact-hull-height) |
| General transfer | Every tuple satisfying the specified local tests but failing full compatibility can, after complementing selected leaf indicators, be separated in the original epigraph by a positive-definite star and suitable prescribed leaf means. The proof controls the unbounded moment set and closure. It is existential and gives no uniform conditioning, gap, or coefficient-size guarantee. | [General transfer](tree-indicator-moment-gluing.md#transferring-any-local-moment-incompatibility-to-a-star-epigraph) |
| Uniform all-proper-subset obstruction | For every `N>=2`, all proper subfamilies can be finitely realizable while the full family yields a strict original-epigraph gap. Rational data of polynomial encoding and `I/39 < Q < 12I` are possible. This strengthens the first regular-family construction, whose conditioning deteriorates with size. | [Uniform construction](star-uniform-condition-subset-gaps.md) |
| Quantitative rational obstruction | For every `k>=1`, `N=2k` and total nonzero-data encoding `O(k^2 log(k+1))` suffice for `I/39 < Q < 12I`, `0<=R_k<=F_k^*<H_k<122`, `F_k^*>=1/13`, `H_k-R_k>=1/(466560 k^2)`, and `(H_k-R_k)/H_k>=1/(56920320 k^2)`. In addition `11/416<=z_i<1/2` and `||y||_2^2<=486/13`. `F_k^*` is an explicit feasible relaxation value, not asserted to be its optimum. | [Accuracy theorem](star-subset-accuracy-lower.md#rational-data-give-the-same-inverse-square-order) |
| Small bounded faces | Every nonempty bounded face of the unconstrained star hull has an LP extended formulation with at most `(2n+2)(2n+1)` scalar inequalities, apart from equalities. This includes nonexposed bounded faces. The formulation depends on the face and supplies no simultaneous compact formulation of the full hull. | [Face note](../notes/research-20260925-star-epigraph-faces.md) |

The quantitative theorem implies that a dimension-independent relative
error guarantee `epsilon` by this particular scheme requires
`k=Omega(epsilon^-1/2)`. It proves a necessary order, not a convergence
upper bound, a runtime lower bound, or a lower bound for all conic
formulations. The degree of the center grows with `k`.

The rational construction generates the instance, the selected moment
tuple, and an affine inequality in the original variables by exact
polynomial-time rational arithmetic. No rationality or bit-size bound is
claimed for the atom locations of the local realizing laws. Their finite
existence follows from strict compatibility and positive-definite parent
blocks. Thus the counterexample also applies if local feasibility demands
actual scalar laws rather than only closure of moment feasibility.

## Prior-work boundary

The source comparison is completed in the separate
[publication priority review](publication-star-priority-review.md).
Its purpose is to identify the exact added statement, not to certify
originality by failure to find a duplicate. Prior compatibility hierarchies,
witness conversion, and planar approximation results must be cited in a
potential manuscript. The retained source versions and hashes are tracked
by the publication reproduction package.

Three close precedents materially restrict the novelty wording:

- Sun, Wang, Li-Jost, and Fei's
  [2020 hierarchy paper](https://doi.org/10.3390/e22020161), Section 2,
  already calls compatibility of every `k`-member subfamily
  `(n,k)`-compatibility. Normalizing `M` makes this the same abstract
  subset condition used here.
- Zhang, Zhang, and Chitambar's
  [planar simulation result](https://arxiv.org/abs/2302.09060v3),
  Proposition 4 and Corollary 2, derives an inverse-square-root lower
  bound on the number of outcomes of a global parent measurement.
  It establishes close prior geometry and exponent, with a different
  resource parameter from the size of separately tested subsets.
- Porto, Designolle, Pokutta, and Quintino's
  [global LP approximation](https://arxiv.org/abs/2506.03045v3),
  Theorem 1 and Section 3.3, approximates depolarizing robustness in fixed
  dimension with polynomial dependence on measurement count and inverse
  accuracy. It is a positive approximation result outside the architecture
  bounded here. Its robustness estimate is not automatically a bound on
  the variable-center star objective.

The full review also compares prior arbitrary-order Specker families,
generic witness-to-discrimination transfers, and an earlier four-node-star
gap for a different optimization relaxation. No claim that these phenomena
are new, or that this is the first star relaxation gap, is justified.
The assessment independently inspected the retained Sun definitions,
Zhang planar result, Porto approximation analysis, and the optimization
sources below; the detailed review records the broader primary-source audit.

The optimization comparison uses the full local texts of
[Bhathena, Fattahi, Gómez, and Küçükyavuz](https://doi.org/10.1007/s10107-025-02222-3),
especially Lemma 2, Proposition 1, and Theorem 2, and
[Choi, Fattahi, Han, Gómez, and Lozano](https://arxiv.org/abs/2608.22815),
Section 7.2, Theorem 2 and Corollary 1. The former gives a parametric
algorithm for free-variable positive-definite indicator quadratics over
arbitrary trees. The latter gives an exact SOCP lift of size
`O(n^(ell+1))` for a rooted tree with `ell` leaves and explicitly discusses
its exponential size on stars. The present result is consistent with
both: it concerns a particular relaxation and does not prove that star
optimization is difficult or that a compact star lift is impossible.

The face observation uses elementary scalar piecewise-quadratic counting
within that existing parametric framework. Its additional assertion is
the explicit affine-cube decomposition and the extension to every bounded
face. It rules out transferring a large correlation-polytope LP lower
bound through such a face and projection. It does not rule out affine
sections, unbounded faces, or other lower-bound methods.

## Proof and verification evidence

The current package has written independent reviews of the
[two-leaf example](tree-indicator-moment-gap-review.md),
[pairwise example](tree-indicator-pair-gap-review.md),
[general transfer](tree-indicator-projection-transfer-review.md),
[short-arc construction](star-short-arc-uniform-review.md),
[rational arithmetic and encoding](star-rational-uniform-review.md),
[quantitative theorem](star-subset-accuracy-review.md), and
[face result](../notes/review-20260925-star-epigraph-faces.md).
The publication pass adds a
[fresh adversarial mathematical review](publication-star-proof-review.md)
and the separate priority review. No Lean proof is claimed for this
package.

The publication assessment reran these targeted commands successfully:

```text
python research-20260925/check_star_subset_accuracy.py
python research-20260925/check_star_subset_accuracy_review.py
python research-20260925/check_publication_star_parents.py
python code/check_star_epigraph_faces.py
```

The first checked five rational orders and 852 exact subpolygons, as
well as the gap, mean, and cost bounds. It imports the polygon helper
from `verify_star_rational_uniform.py`; this is not an independent
implementation of that geometry. The second checked eight generic
three-leaf support identities and the candidate-cut identity symbolically,
then 4,706 real-family subsets in floating point. The third independently
constructed 215 local laws through order four, represented by 1,964
positive definite rational pattern matrices, and checked every total and
marginal exactly. It imports none of the author's polygon helpers. The
fourth checked 77 face cases and 3,232 supports with exact rational arithmetic.
These finite checks substantiate the algebra and implementation. The
all-order geometry, closure, coercivity, and encoding results rest on the
written proofs and their reviews. Floating-point checks are not exact
inequality certificates. No project-wide verification or CI inspection
was performed.

An inline Python check of the eight updated star documents also confirmed
that all 66 local file-link targets exist and that the files contain no
unexpected control characters or trailing whitespace. This checks document
integrity only; it does not test Markdown anchors or mathematics.

The general proof uses separation only after proving closedness of the
full compatibility set by bounded parent blocks. Its perturbation has a
nonnegative lower bound on the entire unbounded feasible moment set.
For the quantitative construction, a globally valid affine inequality
directly separates the original coordinates, so projection closure is
not assumed. These are essential proof steps; replacing them by a bare
auxiliary incompatibility observation would not prove the theorem.

## What remains outside this completed work

The exact formulation question for an arbitrary positive-definite star,
stronger overlap-consistent hierarchies, matching approximation upper
bounds, and bounded-degree analogues remain open in this package. They
are possible future projects, not missing lemmas in the accepted claims.
No attempt to resolve them is required for the focused contribution above.

Additional continuous bounds, nonnegative variables, coupled indicators,
or positive-semidefinite matrices require new analysis. The relative gap
concerns the pure quadratic epigraph height at prescribed means, not an
arbitrary affine objective added to an optimization problem. Uniform
conditioning already supplies coarse constant-factor perspective bounds;
the theorem does not show that fixed modest orders perform poorly on
typical instances.

Before choosing a publication venue, an author should weigh this focused
formulation limitation against the stronger positive algorithms already
available for trees. The current work supports an accurately scoped
research submission. It does not support claiming that the largest open
star-hull question has been solved, that a named solver formulation has
been invalidated without a formulation comparison, or that publication
priority is beyond doubt.
