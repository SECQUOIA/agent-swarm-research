# Literature audit: an edge formulation for one-output pooling hulls

Date: 2026-09-25. Status: adversarial literature and significance assessment.
This is not a novelty certificate. A separate agent independently checked the
fractional-convexification literature described below.

The finite SOC hull has a complete, independently reviewed proof in
[the formulation note](pooling-hull-review.md), but its central edge reduction
is classical. In particular,
an established theorem on optimizing a linear function plus a linear-fractional
function already implies the simultaneous graph reduction by scalarization.
The conic description then follows from the standard reciprocal-arc hull and
disjunctive homogenization. The pooling application may still be useful; this
combination alone is not persuasive evidence of a substantial original
theoretical contribution.

## The claim being assessed

Let `P` be a compact polytope in flow variables `p=(x,w,v)`, with
`x=sum_i w_i`, `w>=0`. At positive flow retain proportions `q=w/x`. At zero flow
use the prescribed polyhedral face with `q` in a fixed polytope `Q`.
Any restrictions `q in Q` that are meant to hold at positive flow must also be
enforced there, for example through their homogenized inequalities in `P`.

The candidate construction fixes `x`, represents a point of the slice
`P intersect {x=constant}` by slice vertices, and observes that every such
vertex is a vertex of `P` or lies on an edge. On an edge with nonconstant `x`,
all flow coordinates are affine in `x`, and all proportion coordinates have
the form `a+b/x`. Thus the full edge graph is an affine image of
`{(x,1/x): l<=x<=u}`. With `l>0`, its hull has the standard description

```
l <= x <= u,
x r >= 1,
r <= (l+u-x)/(lu).
```

The product inequality is a rotated SOC inequality. Constant-flow edges give
line segments. When an edge reaches zero flow, `w(0)=0` makes its positive-flow
proportion vector constant, so its closure is also a segment. Its limiting
proportion must belong to the permitted zero-flow face. Degenerate polytopes
with no edges require their vertices to be included explicitly.

This is an **exact finite formulation whose size depends on the number of
edges**, not a polynomial-size formulation in an arbitrary inequality
description of `P`.

## Strongest direct prior: the edge reduction is established

Cambini and Martein, *Generalized Convexity and Optimization: Theory and
Applications* (2009), Section 8.3, Theorem 8.3.1(i), printed page 175, treat

```
min { a'x + (c'x+c0)/(d'x+d0) : Ax=b, x>=0 },
```

with positive denominator. If a minimum is attained, one is attained on an
edge. Their proof fixes the denominator at an optimal value and chooses a
vertex of the resulting LP slice. No pseudoconvexity assumption is needed for
this theorem. The section cites earlier work including Martein (1985),
*Maximum of the sum of a linear function and a linear fractional function*,
Rivista Matematica per le Scienze Economiche e Sociali 8, 13–20.
[Open book](https://www.convexoptimization.com/TOOLS/GeneralizedConvexity.pdf).

**Our consequence of that theorem:** every linear objective on the retained
graph `(p,(Ap+b)/t(p))` is a linear function of `p` plus one linear-fractional
function. Equality of its support values on the full polytope and on the
edge graph gives equality of their compact convex hulls. Standard slack and
affine-coordinate transformations cover arbitrary compact polytopes. Thus
retaining several proportions simultaneously does not avoid this prior result.

The 1985 paper itself was not obtained in this audit; the 2009 theorem and
proof were read in full. Kim and Mehrotra's *Solution Approaches to Linear
Fractional Programming and Its Stochastic Generalizations Using Second Order
Cone Approximations* (2021), Section 2.1.1, independently records the edge
property and parametric LP methods for two ratios. Its references identify
Cambini, Martein and Schaible (1989), *On Maximizing a Sum of Ratios*, and
Konno, Yajima and Matsui (1991), *Parametric Simplex Algorithms for Solving a
Special Class of Nonconvex Minimization Problems*.
[Open manuscript](https://par.nsf.gov/servlets/purl/10311743),
[1989 primary abstract](https://www.tandfonline.com/doi/abs/10.1080/02522667.1989.10698952).
The 1989 and 1991 full proofs were not inspected.

There is also direct general convexification prior. Tawarmalani (2010),
*Inclusion Certificates and Simultaneous Convexification of Functions*,
Theorem 2.1, pages 3–4, permits deletion of points with common inclusion
certificates while retaining original variables and several functions.
Specialize it to `F=H=(Ap+b)/t(p)`. In any face of dimension at least two,
a nonzero direction annihilating the denominator exists. The vector graph
is affine on a short feasible segment in that direction. This supplies the
common certificate; a finite face-reduction argument reaches the
one-dimensional skeleton. This specialization is our inference, not an
explicit example in that paper.
[Primary manuscript](https://optimization-online.org/wp-content/uploads/2010/09/2722.pdf),
[local full text](../literature/papers/tawarmalani2010-inclusion-certificates-and-simultaneous-convexification/fulltext.md).

## Other close results and their exact limits

| Source examined | Established result | Relation to this claim |
|---|---|---|
| Santana and Dey (2020), Theorem 1 | The hull of one quadratic equation intersected with any bounded polytope is SOC representable; the formulation may be exponential. | Covers each reciprocal arc and the case of one independent product equation. Several equations `x q_i=w_i` are not literally one quadratic equation. The edge reduction supplies the missing simplification, but is classical as above. |
| Dey, Kocuk and Santana (2020), Theorems 1–2 | Certain common-factor linear side constraints give polyhedral rank-one hulls; two arbitrary linear side constraints give SOC hulls. | Arbitrarily many quality and bypass rows do not directly fit the two-row theorem. The common-factor coefficient condition must be checked, not assumed from the presence of a shared scalar. |
| Jalilian and Kocuk (2026), Section 2.1, Theorem 1 | Nonnegative rank-one matrices with bounds on row sums, column sums, and total sum have an exact, generally exponential SOC hull. | Different side constraints. Arbitrary quality rows with bypass variables are not included by merely intersecting this hull with those rows. Their extreme-point/disjunctive proof is a close methodological precedent. |
| Luedtke, D'Ambrosio, Linderoth and Schweiger (2020) | Exact hull descriptions in three parameter cases for an aggregated one-pool, one-output, one-attribute set; explicit inequalities in the original variables. | A general extended edge formulation covers a richer local set but does not reproduce the compactness, direct separation, or explicit inequalities that make this work useful. Section 6 suggests retaining disaggregated input variables as a future direction. |
| He, Liu and Tawarmalani (2025), arXiv v2 Theorems 1–2 | Projective transfer between polynomial and fractional convex hulls. Corollary 4 gives an SDP graph hull for quadratic-over-affine functions on planar quadrilaterals; Section 5.1 develops univariate rational hulls. | No arbitrary-polytope simultaneous edge-SOC theorem was found. Their pages 4–5 distinguish retaining the original variables from taking only a fractional image; Charnes–Cooper alone does not give the retained graph hull. |
| Davarnia, Richard and Tawarmalani (2017) | Simultaneous bilinear graphs over a Cartesian product of a polytope and a simplex admit polyhedral descriptions. | The independent Cartesian product is essential. Coupling the denominator to the retained flow polytope is not obtained by intersecting an already convexified product hull. |

Primary sources for the table:

- [Santana–Dey](https://arxiv.org/abs/1812.10160); read also the
  [local full text](../literature/papers/santana2020-the-convex-hull-of-a/fulltext.md).
- [Dey–Kocuk–Santana](https://optimization-online.org/wp-content/uploads/2019/02/7056.pdf).
- [Jalilian–Kocuk](https://arxiv.org/abs/2306.10810); read Section 2.1 in the
  [local full text](../literature/papers/jalilian2026-improved-rank-one-based-relaxations/fulltext.md).
- [Luedtke et al.](https://arxiv.org/abs/1803.02955),
  [local full text](../literature/papers/luedtke2020-strong-convex-nonlinear-relaxations-of/fulltext.md).
- [He–Liu–Tawarmalani](https://arxiv.org/pdf/2310.08424),
  [local full text](../literature/papers/he2024-convexification-techniques-for-fractional-programs/fulltext.md).
- [Davarnia dissertation, Chapter 2](https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf).
  The locally stored file under the 2017 article's name is this dissertation;
  its theorem and page numbers must not be attributed to the journal PDF.

Fakhri and Ghatee (2016), *Minimizing the sum of a linear and a linear
fractional function applying conic quadratic representation: continuous and
discrete problems*, gives SOCP reformulations under pseudoconvexity and
canonical-form conditions. It does not establish an arbitrary retained graph
hull. The correct DOI is `10.1080/02331934.2015.1113532`; a different DOI found
in a later reference list was erroneous.
[Author-uploaded primary text](https://www.researchgate.net/publication/284880015_Minimizing_the_sum_of_a_linear_and_a_linear_fractional_function_applying_conic_quadratic_representation_continuous_and_discrete_problems).

An unresolved nearby lead is Oh, Wiecek and Yang (2026), *Convexification of a
Class of Bilinearly Constrained Sets Sharing a Common Variable*. Their public
conference abstract announces extreme-point and facet characterizations for
box-constrained sets with common-variable bilinear inequalities. An abstract
does not establish whether arbitrary correlated flow constraints are covered.
[INFORMS Optimization Society 2026 program](https://ios2026.isye.gatech.edu/sites/default/files/2026-03/program-book.pdf).

## Size, repository overlap, and significance

Exponential enumeration is possible even with no quality rows. Take
`n<=x<=n+1`, `0<=w_i<=1` for `i=1,...,n`, and
`w_(n+1)=x-sum_(i=1)^n w_i`. Nonnegativity of the last coordinate follows.
In coordinates `(x,w_1,...,w_n)` this is an `(n+1)`-dimensional box with
`2n+2` facets. It has `2^n` edges along which `x` varies. All but the edge
with `w_1=...=w_n=0` yield nonconstant proportion curves. Thus fixed quality
count alone does not make this particular edge formulation compact.
This is a limitation of enumeration, **not** a lower bound on every SOC
extension of the hull.

The existing
[common-factor optimization theorem](../results/common-factor-fixed-linking-optimization.md)
already gives exact polynomial optimization for a fixed number of linking
rows in a broader scalar-dependent LP model. Its rational basis curves can
have higher degree. The present flow-polytope restriction is special enough
to yield reciprocal arcs, but arbitrary edge enumeration does not improve
that oracle's complexity.

The existing
[many-leaf reciprocal-anchor hull](../results/common-factor-reciprocal-anchor-full-hull.md)
provides polynomial separation without enumerating all leaf patterns, under
box restrictions without arbitrary linking constraints. Edge enumeration can
handle additional admissible flow correlations, but loses that compact
algorithmic property. It should not be presented as subsuming all of the
earlier result's computational content.

The [September 22 pooling assessment](../research-20260922/pooling-multiattribute/assessment.md)
already proposed a finite union of hyperbolic pieces and identified correlated
attributes as the useful application. Its uncorrected tables must not be
reused: the correction at the top refutes the claimed improvement for sppb0
and revises the sppc0 comparison. No benchmark was rerun for this audit.

A credible next contribution would need more than existence of a finite SOC
hull: for example a structural size bound for a meaningful flow class,
scalable exact separation exploiting its capacity/quality structure,
provably stronger compact inequalities, or a carefully certified practical
improvement. A broad claim that multi-attribute pooling convexification is
previously unknown is unsupported. A narrower statement that this exact
disaggregated edge formulation was not located in the examined pooling
papers is supportable, but is not proof of novelty.

## Search and verification record

The audit read the local `common-factor` results, the September 22 assessment,
the local primary papers linked above, and external primary texts. Web queries
covered graph and simultaneous convexification of linear-fractional functions,
common denominators, polytope edges, linear-plus-linear-fractional optimization,
rank-one pooling hulls, and multi-attribute pooling. This terminology change
was decisive: searching only pooling hulls missed the classical edge theorem.

Targeted commands used `rg` and `sed` on the named literature and result files.
External PDFs for the 2009 book, 1994 fractional-programming survey, and
Kim–Mehrotra manuscript were downloaded to `/tmp` with Python `urllib.request`
and extracted with `pdftotext -layout`. The survey PDF was not text-searchable;
its search-engine excerpt was used only as a lead. The other two extracted
successfully, and Theorem 8.3.1 and the cited reference lists were inspected.
No project-wide verification or CI inspection was performed. No computational
test or Lean proof was needed for this literature-only change. The algebraic
box example above was checked directly; it is not a computational extension
complexity lower bound.
