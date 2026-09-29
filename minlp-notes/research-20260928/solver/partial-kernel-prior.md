# Prior-work and significance audit for partial kernel rounding

Date: 2026-09-28. Independent source comparison for the proposed partial
smoothing extension. This note does not certify priority or replace the
independent proof review.

The candidate theorem is documented in
[partial-kernel-rounding.md](partial-kernel-rounding.md). The strongest
defensible distinction is a **quantitative convergence and
rounding theorem for a restricted sparse moment hierarchy**: degree grows
only in shared box variables, while private convex quadratic variables stay
at degree two. Matrix moments, partial lifting, pseudomoment Jensen
inequalities, parameter elimination, and matrix-size-independent kernel
rates all have substantial precedents. In particular, the extension should
be presented as a useful structural consequence of the sparse kernel
argument, not as the invention of any of those ingredients.

## Candidate being compared

For bags whose shared coordinate sets `S_b` satisfy running intersection,
consider

\[
 \min_{z\in[-1,1]^n,\ y_b\in P_b}
 \sum_b\{c_b(z_{S_b})+a_b(z_{S_b})^Ty_b
                     +y_b^TQ_b(z_{S_b})y_b\}.
\]

Each `P_b` is a fixed nonempty compact polytope contained in
`[-1,1]^{p_b}`; different bags have disjoint private variables. The
coefficients are polynomial and `Q_b(z)` is PSD throughout the shared
cube. There need be no convexity in `z`.

The candidate uses functionals on
`R[z]_{<=2r} tensor R[y]_{<=2}`, shared box preordering positivity on
squares affine in `y`, affine private constraint localizers, and redundant
private second-moment bounds. A common kernel smooths only `z`. Its scalar
mass densities glue; its matrix densities give feasible conditional
private means and a quadratic Jensen inequality. The asserted error is
`O(r^-2)`, with largest PSD block
`(p_b+1) binom(r+|S_b|,|S_b|)` and `2^{|S_b|}` shared preordering products.

Thus the exponent in the number of shared monomials is controlled by
`s=max_b |S_b|`. This is **not** a dimension-free theorem: the coefficient
budget, number of scalar moments, PSD matrix size, private inequality count,
and numerical costs can all grow with private dimension.

## Direct theoretical precedents

### Pseudomoment Jensen and convexity

[Lasserre (2009), *Convexity in semialgebraic geometry and polynomial
optimization*](https://doi.org/10.1137/080728214),
[open manuscript](https://optimization-online.org/wp-content/uploads/2008/07/2025.pdf),
Theorem 2.6, proves `L(f)>=f(L(x))` for an SOS-convex polynomial and a
normalized PSD truncated moment functional. A representing measure is
unnecessary. Theorem 3.3 treats exact low-order relaxations for
SOS-convex programs. The quadratic Jensen step in the candidate is a basic
special case, also seen immediately from a PSD block's Schur complement.
What remains additional is obtaining a normalized feasible conditional
functional at every smoothed shared point and controlling the smoothing
error uniformly over finite pseudomoments.

[Nie, Qu, Tang, and Zhang (2026), *Sparse polynomial optimization with
matrix constraints*](https://doi.org/10.1007/s10898-025-01539-9),
Theorem 5.2, proves exactness at every admissible order when all local
objectives are SOS-convex and all local matrix constraints are SOS-concave.
An optimal first-moment vector is a global minimizer; Slater gives the
corresponding SOS certificate. Their convexity assumptions concern all
variables of each bag. They do not cover arbitrary nonconvex dependence on
shared variables while keeping private degree fixed. Their numerical
discussion explicitly identifies special partly nonconvex structures as
an interesting further direction. The paper's full publisher text and the
theorem proof were inspected.

### Partial lifting and fixed degree in one variable block

[Kahl and Henrion (2005), *Globally optimal estimates for geometric
reconstruction problems*](https://homepages.laas.fr/henrion/Papers/vision.pdf),
Section 2.2, already proposes lifting only variables that enter PMIs
nonlinearly. It reports a substantial reduction in relaxation size, while
explicitly withholding an asymptotic convergence guarantee for those
partial relaxations. Rank-one moment matrices provide a numerical
optimality test. This is a direct historical precedent for the motivation
and terminology of partial relaxation, although its model and hierarchy
differ from the candidate.

[Guo and Wang (2025 volume; 2024 online), *A moment-sum-of-squares
hierarchy for robust polynomial matrix inequality optimization with
sum-of-squares convexity*](https://arxiv.org/html/2304.12628v3),
Section 4.2, equations (21)--(22), is especially relevant. Its hierarchy
keeps the degree in the SOS-convex decision variables at a bound determined
by the data, while increasing the matrix-moment order in uncertainty
variables. Proposition 27 supplies matrix pseudomoment Jensen; Theorem 29
is the convergence theorem. The paper
also develops matrix-measure extraction and asymptotic convergence. The
model has a robust universal PMI constraint, with different quantifiers
from minimizing jointly over shared coordinates and private QPs. No
quadratic rate or sparse conditional-density gluing result was located in
the inspected full text. Fixed degree in a convex variable block is
therefore a precedent, not a new general principle of the candidate.

### Matrix kernels and an important sparse obstruction

[Fang and Fawzi (2021 volume; 2020 online), *The sum-of-squares hierarchy
on the sphere and applications in quantum information theory*](https://doi.org/10.1007/s10107-020-01537-7),
Theorem 2, is the strongest matrix-kernel comparison found. For a
homogeneous symmetric polynomial matrix `F` of degree `2d` in `n`
variables, normalized by `0<=F<=I` on the sphere, it gives a matrix SOS
certificate for `F+C_d(n/r)^2 I` at sufficiently large order. Its constants
do not depend on matrix size. The authors explicitly interpret this as a
result for scalar polynomials of bidegree `(2d,2)` on products of spheres.
Consequently, quadratic kernel convergence with one variable block kept
quadratic already exists. The candidate adds fixed private polyhedral
feasibility, conditional convex means, and overlapping shared bags; it
does not introduce the matrix kernel principle.

[Slot and Laurent (2023 volume; 2022 online), *Sum-of-squares hierarchies
for binary polynomial optimization*](https://doi.org/10.1007/s10107-021-01745-9),
[open paper](https://ir.cwi.nl/pub/31368/31368.pdf), also extends positive
kernel analysis to matrix-valued polynomials. Section 5, equations
(53)--(55), formulates matrix lower and upper hierarchies and applies a
scalar polynomial kernel entrywise. The domain is a binary or finite
alphabet cube, with a different quantitative regime. This further limits
any claim that applying a common scalar kernel to PSD matrix moments is
itself an original contribution.

[Miller, Wang, and Guo, *Sparse polynomial matrix
optimization*](https://arxiv.org/html/2411.15479v3), Section 5, Example 5.1,
gives a counterexample to generic convergence of correlatively sparse
matrix hierarchies even with running intersection and local
Archimedean conditions. The paper also explains the standard matrix SOS
block size `p binom(n+r,r)`. The candidate must not be described as a
general matrix-valued measure-gluing theorem. It glues **scalar** shared
mass marginals; private matrix indices belong to one bag and are removed
by conditional means. That distinction is substantive and avoids applying
the false generic matrix analogue. The full counterexample and nearby
theorems were inspected; this audit does not reprove the counterexample.

### Bounded-size PSD hierarchies are already known

[Lasserre, Toh, and Yang, *A bounded degree SOS hierarchy for polynomial
optimization*](https://arxiv.org/pdf/1501.06126), Theorem 2, establishes
asymptotic convergence on suitable compact sets with the PSD block size
fixed in advance. It also proves first-step exactness for SOS-convex
problems under Slater. The growing part is a family of products of
constraint polynomials with nonnegative scalar multipliers. This is not a
shared-degree-only moment hierarchy, but it means that PSD block size by
itself is an inadequate novelty or complexity comparison.

[Weisser, Lasserre, and Toh, *Sparse-BSOS: a bounded degree SOS hierarchy
for large scale polynomial optimization with sparsity*](https://arxiv.org/pdf/1607.01151),
extends that approach to sparse data with running intersection. The paper
proves convergence and exactness for an SOS-convex subclass. Comparisons
must count the scalar multipliers, coefficient equations, constraint
products, and accuracy dependence as well as the largest PSD matrix.
Neither inspected BSOS paper provides the particular partial kernel rate
being proposed here.

### General matrix-constraint rates

[Tran and Toh (2026), *Convergence rates of sum-of-squares hierarchies
for polynomial semidefinite programs*](https://doi.org/10.1137/24M1670184),
[latest open preprint inspected](https://arxiv.org/html/2406.12013v3),
treats a scalar polynomial objective on a domain defined by a polynomial
matrix inequality. The analysis combines polynomial penalties,
approximation kernels, and geometric error bounds. It supplies a current
quantitative comparison for matrix constraints, but does not retain an
arbitrarily large block of private quadratic variables at degree two or
glue overlapping scalar marginals. The distinction is in both model and
hierarchy, so it would be misleading to claim a blanket improvement over
its more general feasible sets.

## Elimination is a real alternative

Independence of the private feasible sets gives the exact reduction

\[
 v_b(z)=\min_{y\in P_b}f_b(z,y),\qquad
 f^*=\min_{z\in[-1,1]^n}\sum_bv_b(z_{S_b}).
\]

This identity is elementary. Convexity makes evaluation of each `v_b` a
convex QP. It does not make `v_b` polynomial or convex in the shared
coordinates. For example, with `P=[-1,1]` and `f(z,y)=zy`, the value
function is `-|z|`. Thus applying a smooth-polynomial theorem directly to
the eliminated objective would need an additional approximation argument.

[Lasserre (2010), *A joint+marginal approach to parametric polynomial
optimization*](https://doi.org/10.1137/090759240),
[open manuscript](https://arxiv.org/pdf/0905.2497), constructs joint
moment relaxations with a prescribed parameter marginal. Theorems 3.3 and
3.5 establish convergence of moments and polynomial lower approximations
to value functions in an integral sense. Section 3 explicitly lifts joint
decision/parameter monomials. This is strong prior for the parameter-measure
viewpoint, but its conclusions do not directly give the candidate's
uniform optimization error or its restricted private degree.

[Bemporad, Morari, Dua, and Pistikopoulos (2002), *The explicit linear
quadratic regulator for constrained systems*](https://doi.org/10.1016/S0005-1098(01)00174-1),
[open paper](https://people.smp.uq.edu.au/YoniNazarathy/Control4406/resources/BemporadMorariDuaPistikopoulos2002.pdf),
Theorem 4, supplies an important explicit elimination comparison. In its
strictly convex multiparametric QP formulation, the optimizer is continuous
and piecewise affine and the value is continuous and piecewise quadratic.
Its fixed Hessian and affine parameter dependence are narrower than the
candidate's polynomial coefficient matrices, which can be singular.
Neither piecewise affine solutions nor globally polynomial value functions
should be assumed for the candidate.

## A grid baseline with the same accuracy exponent

The following is our comparison argument, not a theorem attributed to the
preceding sources. It uses the explicit kernel already proved in
[the sparse kernel note](sparse-kernel-rounding.md).

Let `d` bound the coordinate degrees of all shared coefficient
polynomials. For integer `m>=2`, use the `N` Gauss--Chebyshev nodes

\[
 G_N=\{\cos((2j-1)\pi/(2N)):1\le j\le N\},
 \qquad 2N-1\ge 2(m-1)+d.
\]

For every bag and grid assignment `z_{S_b}`, evaluate its convex QP to
obtain `v_b(z_{S_b})`. Junction-tree dynamic programming gives

\[
 U_N=\min_{z\in G_N^n}\sum_bv_b(z_{S_b})
\]

from tables with a total of `sum_b N^{|S_b|}` entries, up to ordinary tree
and indexing overhead. In an exact local-optimization model,

\[
 f^*\le U_N\le f^*+\frac{3A}{2m^2+1},                 \tag{1}
\]

where `A` is the candidate's coefficient budget: sum absolute shared
Chebyshev coefficients of `c`, `a`, and all entries of `Q`, weighted by
the sums of squared shared indices. Symmetric off-diagonal terms must be
counted consistently with the objective expansion.

To prove (1), choose a global optimizer `(z^*,y^*)`. On the shared grid,
put the product probability weights

\[
 \Pr(Z=z)=\prod_i K_m(z_i^*,z_i)/N.
\]

Quadrature is exact for each kernel section and each kernel section times
a shared coefficient polynomial, by the displayed degree condition. The
weights are nonnegative and sum to one. The kernel multiplier estimate
therefore gives

\[
 \mathbb E\sum_b f_b(Z_{S_b},y_b^*)
 \le f^*+3A/(2m^2+1).
\]

Private feasibility is unchanged because `P_b` is independent of `z`.
For every grid point, `v_b(z)<=f_b(z,y_b^*)`. The minimum of a finite set
is at most its probability average. These observations prove (1).
In particular, `U_N-3A/(2m^2+1)` is also a valid global lower bound.
An independent agent checked this degree count, normalization, feasibility,
expectation comparison, and tree-DP argument and found no gap. That review
is evidence, not a formal proof certificate.

There is also a direct smoothness explanation for the quadratic grid rate.
Hold `y^*` fixed and choose the nearest Chebyshev node in every coordinate.
At an interior optimal coordinate the corresponding derivative of
`f(z,y^*)` vanishes. At a boundary coordinate the node is `O(N^-2)` from
the endpoint. All other coordinate displacements are `O(N^-1)`, so a
bounded-Hessian Taylor remainder is `O(N^-2)` as well. This alternative
argument uses no kernel and no private convexity. Private convexity makes
the local table minimizations tractable. It does not by itself create the
quadratic grid rate.

This baseline already has an accuracy exponent governed by shared bag
width and local convex QP evaluations. It does not prove a bit-complexity
bound: the nodes are generally algebraic, and exact QP solutions,
approximate QP tolerances, and arithmetic certification require care.
With certified local value intervals, the usual interval propagation would
be needed. No numerical speed comparison has been performed.

The grid baseline does not show that the SDP is useless. SDP dual
certificates, intermediate bounds, and integration into branch-and-bound
may be valuable. Those are plausible benefits requiring implementation or
additional theory; they are not consequences of the block-size formula.

## Assessment and limits of the audit

The partial extension has a coherent mathematical role: it shows that
arbitrarily many bag-private convex quadratic variables need not enter the
degree-growth exponent in this sparse moment certificate. The proof is
likely a fairly short matrix/conditional-mean extension once the base
sparse scalar theorem is accepted. Its strongest presentation is therefore
as a meaningful structural corollary and possible modeling expansion of
that theorem. The [completed fresh proof review](partial-kernel-fresh-review.md)
found no substantive gap; publication priority remains unestablished. The sources examined do
not justify calling it a separate breakthrough or claiming an algorithmic
dimension reduction unavailable through elimination and grids.

Three limitations belong next to any application claim. Private variables
must be continuous and bag-private; arbitrary integer means are infeasible.
Private feasible sets must be fixed under smoothing; state-dependent
equalities and inequalities are not covered. Pointwise PSD of `Q_b(z)` is
an assumption, not a free preprocessing guarantee. A credible application
should identify how these restrictions arise naturally and why the SDP
certificate is preferable to the grid/QP baseline there.

The dense and sparse scalar kernel comparisons are recorded in
[kernel-prior.md](kernel-prior.md), especially Korda--Magron--Ríos-Zertuche
for sparse box rates and Laurent--Slot for dense box preordering rates.
This note read that local audit and the scalar theorem before conducting
additional searches. The local literature directory was also searched for
convexity, quadratic, parametric, and matrix-moment terminology; those hits
did not establish an equivalent theorem.

Web searches included `polynomial optimization partially convex`,
`convex variables moment relaxation`, `partial relaxation polynomial
matrix`, `matrix valued measure convex polynomial optimization`,
`matrix Jackson convergence polynomial optimization`, `polynomial
semidefinite programs convergence rates`, and `multiparametric quadratic
programming`. The primary papers linked above were inspected in their
stated sections. A second agent independently searched partial convexity
and located or corroborated the partial-lifting, robust-PMI, matrix-kernel,
and BSOS comparisons. This is evidence about the sources examined, not
evidence that all equivalent results have been found. Citation descendants
of those papers and application-specific formulations remain sensible
targets for a broader publication audit.

Targeted local commands actually run: `rg --files` in the solver and
repository directories; `cat AGENTS.md`; `sed` on the scalar kernel theorem
and its prior audit; `rg` over local literature metadata/full text; and
`git diff --check -- research-20260928/solver/partial-kernel-prior.md`
(exit 0; this checks tracked diff whitespace, not mathematical content). No
project-wide checks or CI status/log inspection were run. This source audit
contains no Lean verification or computational proof check. The displayed
grid baseline received the independent mathematical review described
above; the main partial-kernel proof has a separate review workflow.
