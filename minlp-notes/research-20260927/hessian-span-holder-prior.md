# Prior audit: Hölder bounds and the span of quadratic Hessians

Date: 2026-09-27. Independent literature audit for the proposed exponent
\(2^{-h}\), where \(h=\dim\operatorname{span}\{Q_i\}\) and every
\(Q_i\succeq0\) is a constraint Hessian. This is a dimension in the space
of symmetric matrices, not the dimension of their combined ranges.

## Assessment

Unconditional Hölder error bounds for convex quadratic inequalities are
classical. So is the mechanism of accumulating square-root losses through
facial reduction. The plausible additional claim here is the structural
bound of at most \(h\) nonlinear reduction stages, and hence an exponent
controlled by a readily defined feature of the original quadratic data.
The sources examined below do not state that refinement. This search does
not establish its novelty, and the original Wang–Pang paper still needs a
full-text comparison before making a publication-level priority claim.

The comparison should distinguish a bound on each bounded set from a
global bound on all of \(\mathbb R^n\). Wang–Pang's result is global;
the symmetric-cone result cited below is uniform on bounded sets. An
existential error-bound constant is also different from an explicit bound
on its rational encoding or a polynomial-time procedure for computing it.

## Wang–Pang and the precise degeneracy count

Tao Wang and Jong-Shi Pang, *Global error bounds for convex quadratic
inequality systems*, Optimization 31 (1994), 1–12,
[publisher abstract and DOI](https://doi.org/10.1080/02331939408844003).
The abstract states a global bound with residual terms \(r+r^{2^{-d}}\),
without a constraint qualification; \(d=0\) under Slater's condition, and
the general count is bounded by the number of constraints. Only the
publisher abstract was accessible here, not the original proof.

Rujun Jiang and Xudong Li, *Hölderian error bounds and Kurdyka–Łojasiewicz
inequality for the trust region subproblem*, author manuscript dated
13 May 2022, [Section 3.1, Definitions 3.1–3.4 and Lemma 3.5](https://rjjiang.github.io/papers/EBKLTRS_mor.pdf),
explicitly reproduce Wang–Pang's terminology and Theorem 3.1:

- A singular row is zero at every feasible point. A singular system has
  only singular rows.
- Such a system is critical if it has at most one nonlinear row, or if
  deleting any nonlinear row makes all remaining nonlinear rows
  nonsingular.
- An irregular row is nonlinear, singular, and belongs to no critical
  subsystem.
- The count is zero without nonlinear singular rows; otherwise it is
  one plus the number of irregular rows.

Their cited bound, writing \(J\) for the singular indices and \(K\) for
the others, is
\[
\operatorname{dist}(x,S)\le C\left(
\|[q_K(x)]_+\|+\|[q_J(x)]_+\|
+\|[q_J(x)]_+\|^{2^{-d}}\right).
\]
These definitions are not a Hessian-span parameter. The trust-region
paper is a primary research source, but its account of the 1994 theorem
is necessarily a reproduction, not a substitute for inspecting that
original proof.

### Why the raw count cannot simply be bounded by \(h\)

Here is an independently derived check on the displayed definitions.
Take \(k\) indexed copies of
\[
q_i(x,y)=x^2-y\le0\quad(i=1,\ldots,k),\qquad
q_{k+1}(x,y)=y^2\le0.
\]
The feasible set is \(\{(0,0)\}\), and \(h=2\). Each of the first
\(k\) rows is irregular: a subsystem omitting the last row admits a
point where all its rows are strict; a subsystem including the last row
and any first row is singular, but deleting a first row leaves the last
row singular. The singleton last row is critical. Thus the reproduced
definition gives \(d=k+1\).

This observation disproves the shortcut \(d\le h\) for that raw row
count. It does **not** prove separation from every consequence of
Wang–Pang: removing duplicate inequalities immediately improves this
particular system. It also does not conflict with a theorem asserting
that some better exponent exists after an additional reduction. A proper
comparison must examine the reduction argument, not identify parameters
by name.

### The one-dimensional span case is already a direct corollary

When \(h=1\), choose a nonzero PSD quadratic form \(q\). Every
nonzero PSD Hessian in its span is a positive multiple of its Hessian.
Positive row rescaling therefore puts all nonlinear inequalities in the
form \(q(x)+\ell_i(x)\le0\), with affine \(\ell_i\). Introduce one
variable \(t\) and use
\[
t\ge\ell_i(x)\quad\text{for every }i,\qquad q(x)+t\le0.
\]
Keep all original affine constraints. This equivalent extended system has
only one nonlinear row, so the reproduced Wang–Pang count is at most one.
For any test point \(x\), select \(t=\max_i\ell_i(x)\). All new
affine inequalities are then satisfied, and the nonlinear violation is
exactly the maximum of the rescaled original quadratic violations.
Projection cannot increase distance. Thus its global one-half exponent
already gives the corresponding bound in the original variables.

This is our derivation from the classical theorem, not a claim that the
1994 paper explicitly used Hessian-span terminology. Wu Li's older
piecewise-quadratic theory is another relevant base-case comparison:
*Error Bounds for Piecewise Convex Quadratic Programs and Applications*
(1995), [DOI](https://doi.org/10.1137/S0363012993243022).
The publisher abstract was inspected. Guoyin Li's accessible
[follow-up manuscript, introduction](https://web.maths.unsw.edu.au/~gyli/papers/Li_MP_July_20_Final.pdf)
records the global one-half bound for convex piecewise convex quadratic
functions. After the above rescaling, differences of quadratic rows are
affine, so their maximum has polyhedral dominance regions. A maximum of
arbitrary distinct quadratic forms need not have that property.

## Symmetric cones and partial polyhedrality

Bruno F. Lourenço, *Amenable cones: error bounds without constraint
qualifications*, Mathematical Programming 186 (2021), 1–48,
[open preprint](https://arxiv.org/pdf/1712.06221), Proposition 38 and
Remark 39. For a feasible intersection \((L+a)\cap K\) with a symmetric
cone, bounded points whose distances to the cone and affine space are
at most \(\varepsilon\le1\) have distance at most
\(C\varepsilon^{2^{-d_{\rm PPS}}}\) to the intersection. The integer
\(d_{\rm PPS}\) measures reduction until a partial-polyhedral Slater
condition holds. For a product of symmetric cones, the displayed bounds
include
\[
d_{\rm PPS}\le
\min\left\{\dim(L^\perp\cap\{a\}^\perp),
\sum_j(\operatorname{rank}K_j-1),d_S\right\}.
\]
The rank here is Jordan-algebra rank, not matrix-space dimension of
quadratic Hessians.

Bruno F. Lourenço, Masakazu Muramatsu, and Takashi Tsuchiya,
*Facial reduction and partial polyhedrality*, SIAM Journal on
Optimization 28 (2018), 2304–2326,
[open preprint, version 4](https://arxiv.org/pdf/1512.02549),
Definition 1, Example 1, and Theorem 10. Partial-polyhedral Slater permits
the polyhedral factors to remain on their boundaries. The reduction
bound is \(1+\sum_j\ell_{\rm poly}(K_j)\), where
\(\ell_{\rm poly}\) measures the length of a chain before reaching
polyhedral faces. For second-order cones each nonpolyhedral block
contributes one.

These sources establish the reduction framework underlying the proposed
argument. A separate SOC block for every quadratic row yields a bound
based on the number of rows. Replacing that count by \(h\) requires an
additional argument; a basis of PSD Hessians need not generate all the
input Hessians by nonnegative combinations. A signed linear basis alone
does not justify a lift with only \(h\) convex quadratic epigraphs.

Jos F. Sturm, *Error bounds for linear matrix inequalities*, SIAM Journal
on Optimization 10 (2000), 1228–1248,
[publisher abstract and DOI](https://doi.org/10.1137/S1052623498338606),
is the earlier central source for the \(2^{-d}\) singularity-degree
phenomenon in SDP. The publisher abstract was inspected; the complete
theorem comparison above uses the accessible Lourenço manuscript.

## A directly related QCQP facial-reduction paper

Hao Hu and Xinxin Li, *Facial reduction for the Shor SDP relaxation of
QCQPs*, Applied Set-Valued Analysis and Optimization 5 (2023), 181–191,
[published open paper](https://asvao.biemdas.com/issues/ASVAO2023-2-5.pdf),
Section 4 and Theorems 4.2 and 4.5. They relax the Shor moment matrix
condition further by requiring only its lower-right block to be PSD.
When the quadratic data matrices are PSD, exposing directions for this
further relaxation can be found through a linear system with nonnegative
multipliers. They compute that relaxation's singularity degree in
polynomial time. Their procedure need not fully regularize the original
Shor relaxation. No Hessian-span Hölder exponent is stated there.

This paper reinforces that PSD aggregation and nullspace restriction are
established operations. The proposed result should isolate exactly what
the accounting by \(h\) adds, rather than claim these operations as new.

## Coefficient-height bounds for the multiplicative constant

Saugata Basu and Ali Mohammad-Nezhad, *Improved effective Łojasiewicz
inequality and applications*, Forum of Mathematics, Sigma 12 (2024),
e115, [published open article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B),
Theorem 2.2, equation (2.3), gives a coefficient-sensitive constant bound.
For a compact semialgebraic domain and continuous semialgebraic
\(f,g\), with \(f^{-1}(0)\subseteq g^{-1}(0)\), suppose the domain
and both graphs have quantifier-free descriptions of degree at most
\(d\), with integer coefficients of bit size at most \(\tau\).
Then
\[
|g|^M\le c|f|,\qquad M=(8d)^{2(n+7)},\qquad
c\le\min\{2^{\tau d^{O(n^2)}},2^{\tau d^{O(n\log d)}}\}.
\]
Section 3.1 records Solernó's earlier coefficient bound using the sum of
description degrees; that original source was not inspected. The same
paper's Theorem 4.1 explicitly tracks coefficient bits in block
quantifier elimination, and its proof of Theorem 2.2 obtains a bound on
\(c\) by elimination and univariate root bounds.

The implication for the present research is limited but important.
Bounding an error-bound constant from rational coefficients is already
an established objective with general solutions. A result
\(\log C\le N^{O(h^2)}\), for total input length \(N\), must add
the particular dependence on the Hessian span, while retaining the
stronger exponent \(2^{-h}\). The displayed generic bound uses ambient
dimension and its own prescribed exponent. It does not supply its same
constant for an independently proved, stronger exponent.

Also, substituting \(g(x)=\operatorname{dist}(x,S)\) requires a
description of that function's graph. Quadratic defining constraints
alone do not make the distance graph a quantifier-free degree-two set.
Any elimination used to describe that graph must carry its degree and
coefficient growth into the comparison. A bound on an algebraic
constant's height, a bound on the value of a valid real constant, and an
algorithm outputting a rational upper bound are three distinct claims.

Huynh Van Ngai's 2011 preprint, *Global Error bounds for systems of
convex polynomials over polyhedral constraints*,
[open primary text](https://optimization-online.org/wp-content/uploads/2011/11/3237.pdf),
Theorem 10, provides a useful comparison for the role of the constant.
For a convex polynomial system over a polyhedron with nonempty compact
feasible set, it establishes a global bound
\(\operatorname{dist}(x,S)\le\tau(r(x)+r(x)^\gamma)\).
The proof constructs \(\tau\) from local constants, a finite cover,
and a positive residual on an annular region. It does not track the
binary encoding length of \(\tau\).

For a pure bound \(\operatorname{dist}(x,S)\le C r(x)^{2^{-h}}\)
on an entire bounded test domain, the domain's size must be included in
the input data. For example, the system \(x\le0,\ y^2\le1\) has
\(h=1\). At \((R,0)\), with \(R>0\), its distance and maximum
positive violation both equal \(R\), so \(C\ge\sqrt R\).
This example does not obstruct a global mixed bound
\(C(r+r^{1/2})\), or a bound restricted to \(r\le1\).

No inspected source in this targeted pass stated the proposed
\(N^{O(h^2)}\) bound. This is a search limitation, not a novelty
certificate or a verification of the candidate's quantitative proof.

## Search record and remaining obligations

The local literature file catalog had no Wang–Pang, Sturm, or Lourenço
full text under those names. Web queries combined the exact 1994 title,
its DOI, “degree of singularity,” “critical subsystem,” “irregular
inequalities,” “Hessian span,” “Hessian matrices,” “linearly independent,”
“rank,” “quadratic inequalities,” and “facial reduction.” The primary
sources above were examined. Search results also pointed to general
polynomial and Banach-space error bounds; none of those snippets was
treated as proof of a matching or absent theorem.

Before a strong novelty claim:

1. Obtain the original 1994 text and compare its induction, preprocessing,
   and any dimension refinements with the proposed Hessian-span descent.
2. Check whether a standard definition of quadratic-system reduction
   depth already has the bound \(h\), possibly as an unstated elementary
   corollary.
3. Keep the claims separate: the error-bound exponent; any effective
   constant; and any optimization or solver consequence.

An additional lead identified by a separate literature scout is
Luo–Sturm, *Error Analysis*, in the *Handbook of Semidefinite Programming*
(2000), especially Sections 7.6.1–7.6.2 on convex and generalized convex
quadratic systems. Its full text was not inspected here. It is distinct
from their chapter *Error Bounds for Quadratic Systems* in *High
Performance Optimization* (2000). These are unresolved comparison leads,
not sources used to assert a theorem in this audit.

### Targeted follow-up on unavailable original sources

One further pass checked author and university pages and publisher open
previews. The [Springer chapter page](https://link.springer.com/chapter/10.1007/978-1-4615-4381-7_7)
now identifies *Error Analysis* precisely as pages 163–189. Its
[two-page primary preview](https://page-one.springer.com/pdf/preview/10.1007/978-1-4615-4381-7_7)
was inspected. On page 164 it announces a \(2^{-d}\) error exponent
and bounds \(d\) for pure SOC systems by the number of SOC constraints.
It also describes the use of regularized residuals. The preview does not
include Section 7.6, so it does not settle the Hessian-span comparison.

The [Tilburg institutional record](https://research.tilburguniversity.edu/en/publications/error-bounds-for-mixed-semi-definite-and-second-order-cone-progra)
lists that Handbook contribution under the alternate title *Error bounds
for mixed semi-definite and second-order cone programming*. Its separate
[quadratic-systems chapter record](https://research.tilburguniversity.edu/en/publications/error-bounds-for-quadratic-systems)
also contains metadata only. Luo's [publication page](https://tomluo123.github.io/publications.html)
and [author CV](https://tomluo123.github.io/files/cv_2026.pdf) supplied no
full-text chapter link. Searches for Wang–Pang through USC and Johns
Hopkins domains returned bibliography or citation records, without an
accessible original paper. The Wang–Pang full-text gap remains.

The additional constant search combined “convex quadratic,” “error
bound,” “Hölder,” “coefficient,” “rational,” “bit complexity,” “bitsize,”
and “encoding length.” Basu–Mohammad-Nezhad's published Theorem 2.2 and
coefficient-sensitive elimination statement were inspected directly; no
claim of an exhaustive search is made.

This audit used source inspection and the symbolic examples above.
It did not verify the proposed general proof, run project-wide checks,
or inspect CI.
