# Prior work on smooth quadratic recourse and sparse certificates

Date: 2026-09-28. This is the completed literature audit for
[regular recourse multiplier rates](active-region-rates.md), an improvement
of [affine recourse rounding](affine-recourse-kernel-upper.md) under stated
regularity assumptions. It is not a proof review or a claim of publication
priority.

The QP sensitivity results that supply examples of regular multipliers
are established. The potentially distinct contribution is an explicit
`O(r^-2)` bound for the stated anisotropic sparse moment hierarchy, with
private degree fixed at two. Neither smooth QP value functions nor
polynomial lower approximation of recourse functions is new.

## Parametric QP regularity

Consider the convention

\[
 v(u)=c(u)+\min_y\{\tfrac12 y^THy+q(u)^Ty:Ay\le b+Bu\},
 \qquad H\succ0,
\]

where `H,A` are fixed, `q` is affine, and fixed private bounds can be
included among the rows of `A`. The distinction between regularity of the
primal optimizer, the multipliers, and the value is essential.

[Baotić, *Gradient of the Value Function in Parametric Convex Optimization
Problems*](https://arxiv.org/pdf/1607.00366), arXiv:1607.00366 (2016),
Corollary 3, treats a positive-definite QP with parameter-affine right-hand
side. Under LICQ at every feasible parameter, it gives a continuously
differentiable value on the interior of the feasible parameter set.
The proof uses continuous piecewise-affine primal and dual solutions on
polyhedral critical regions. Its formula is `grad V=-S^T lambda` in the
paper's coordinates. The relevant passage is Section IV, physical PDF
page 5. Thus continuity of multipliers and differentiability of the value
are explicitly prior results. On a compact convex parameter domain within
that interior, finitely many affine pieces also give Lipschitz
multipliers and a Lipschitz gradient; this last deduction is elementary,
not a new sensitivity theorem. The paper excludes boundary points from
its differentiability statement. A theorem on a closed master box must
state its own boundary convention or assume an open feasible neighborhood.

[Tøndel, Johansen, and Bemporad, *An algorithm for multi-parametric
quadratic programming and explicit MPC
solutions*](https://doi.org/10.1016/S0005-1098(02)00250-9), *Automatica*
39 (2003), 489–497, is an earlier active-set baseline. Its Theorem 1 gives
piecewise-affine primal solutions and multipliers, with continuity of the
primal solution and, under LICQ, of the multipliers. The repository has an
[open full-text package](../../literature/papers/tndel2003-an-algorithm-for-multi-parametric/paper.md).
Theorem 1 was checked on rendered physical PDF page 3. Its statement and
the surrounding discussion distinguish degeneracy
from an ordinary change of active set. Consequently, a rate
theorem need not assume one fixed active set or strict complementarity
everywhere merely to obtain Lipschitz policies. Conversely, enumerating
the active regions is an established exact alternative, whose region
count may be large; a hierarchy result should compare its representation
cost with that baseline.

[Klatte, *Lipschitz stability for a class of parametric optimization
problems with polyhedral feasible set
mapping*](https://link.springer.com/article/10.1007/s10287-025-00547-0),
online 25 November 2025, *Computational Management Science* 23, 4 (2026),
Remark 4.2(ii), states Lipschitz continuity of the unique optimizer of
positive-definite QPs with graph-convex polyhedral feasible-set mapping.
It follows from polyhedrality, uniqueness, and the uniform upper
Lipschitz property, without an LICQ assumption. Section 4 attributes the
underlying single-valued multifunction argument to Robinson. This is a
stronger baseline for primal regularity than an LICQ-only theorem.
It does not identify primal Lipschitz continuity with multiplier
continuity or differentiability of the value under arbitrary RHS changes.

[Pang and Sun, *First-Order Sensitivity of Linearly Constrained Strongly
Monotone Composite Variational
Inequalities*](https://defengwebsite.github.io/files/QP_dd_corrected.pdf),
author manuscript dated 23 December 2008, Theorem 8, establishes local
Lipschitz continuity for the relevant transformed solution as both the
linear objective term and the RHS change. With the identity transformation
and a positive-definite linear operator, it includes the unique primal
optimizer of the QP above. Its multiplier discussion also supplies a
bounded multiplier selection via a bound depending on the fixed constraint
matrix. A bounded selection is weaker than a continuous selection. The
paper is useful for separating these claims, not as an automatic source
of Lipschitz multipliers in degenerate problems.

[Lau and Womersley, *Multistage quadratic stochastic
programming*](https://doi.org/10.1016/S0377-0427(00)00545-8), *Journal of
Computational and Applied Mathematics* 129 (2001), 105–138, already uses
piecewise-quadratic recourse functions with Lipschitz gradients. The
publisher's accessible Section 2 passage includes linear independence of
active constraint gradients in the smooth recourse result. The conclusion
discusses removing LICQ when extending to convex Lipschitz objectives.
The abstract's abbreviated description should therefore not be read as
claiming that strict convexity alone makes arbitrary RHS-parametric
recourse differentiable. Full PDF retrieval from the publisher was
blocked in this audit; the abstract and indexed publisher passages were
examined, so theorem numbers and all technical qualifications remain to
be checked against the full paper before using it as a formal hypothesis
reference.

## A direct assumption check

The following elementary example is included as an audit check, with no
novelty claim:

\[
 \min_{|u|\le z\le1}(z^2+z)=u^2+|u|,
 \qquad -1\le u\le1.
\]

The private objective has a constant positive-definite Hessian. Recourse
is complete and its constraints have fixed coefficients and affine RHS.
The optimizer `z*(u)=|u|` is Lipschitz. Nevertheless, the value is not
differentiable at zero. In the interior near zero, with multipliers for
`u-z<=0` and `-u-z<=0`, the unique multiplier on the active nonzero side
tends to `(1,0)` from the right and `(0,1)` from the left. No continuous
multiplier selection exists. Thus a rate argument requiring smooth value
or multiplier policies cannot replace that assumption by strict convexity
and complete recourse.

For an affine objective perturbation `q(u)=q0+Du`, the formal envelope
expression is

\[
 \nabla v(u)=\nabla c(u)+D^Ty^*(u)-B^T\lambda^*(u).
\]

Stationarity separately fixes
`A^T lambda*(u)=-H y*(u)-q(u)`. The completed rate theorem assumes
regularity only of the projection `B^T lambda` (including zero rows for
the fixed box bounds). Its KKT inequality needs no regularity of the full
multiplier vector. Theorem 1 uses weighted absolute tensor Chebyshev
coefficients; Theorem 2 uses coordinatewise Hölder or Lipschitz
projections. The scalar case is a special case of Theorem 2. The proof
explicitly includes the closed-box boundary, uses only the bounded
projection in integrals, constructs a Borel optimal private policy
independently of multiplier selection, and verifies the truncated
preordering degree. These are claims of the companion proof, not new
QP sensitivity results or conclusions obtained from an unsuccessful
literature search.

## Closest polynomial and sparse relaxation results

[Lasserre, *A joint+marginal approach to parametric polynomial
optimization*](https://arxiv.org/pdf/0905.2497), *SIAM Journal on
Optimization* 20 (2010), 1995–2022, Theorem 3.5, constructs SOS-certified
polynomial lower approximations of parameter-dependent optimal values.
With compactness certificates and nonempty fibers, the approximations
converge in `L1` for a specified parameter measure; their running maximum
converges almost uniformly. Thus the polynomial recourse approximation
idea and its SDP realization are established. The inspected theorem is
asymptotic, uses increasing degrees in the joint variables, and does not
state the companion theorem's uniform inverse-square bound with private
degree two.

[Zhong, Cui, and Nie, *Towards Global Solutions for Nonconvex Two-Stage
Stochastic Programs: A Polynomial Lower Approximation
Approach*](https://arxiv.org/pdf/2310.04243), *SIAM Journal on Optimization*
34 (2024), 3477–3505, applies polynomial lower approximation directly to
nonconvex recourse. Theorem 4.1 proves `L1` convergence under an
Archimedean quadratic module and continuity of the recourse function.
Corollary 4.2 permits separate degrees for groups of variables, but its
stated limit requires the minimum of those degrees to grow. This is close
prior for two-stage solver use and variable-group degree choices. The
inspected theorem does not hold private degree fixed at two or give an
explicit inverse-square rate. Its nonnegative-polynomial and SOS cones
must be distinguished from an exact local-measure relaxation.

[Qu and Tang, *A Correlatively Sparse Lagrange Multiplier Expression
Relaxation for Polynomial
Optimization*](https://arxiv.org/pdf/2208.03979), *SIAM Journal on
Optimization* 34 (2024), 127–162, constructs sparse KKT reformulations and
applies sparse SOS relaxations. Their Assumption 1 is a polynomial-matrix
nonsingularity condition over complex points for each local constraint
tuple; it is not merely LICQ along the real optimal recourse graph.
Theorem 4.2 establishes convergence when a minimizer is a KKT point and
the original local modules are Archimedean. The reformulation changes
the polynomial optimization problem by incorporating KKT equations and
auxiliary variables. It is important prior for exploiting multipliers
without destroying sparsity, but does not directly prove a rate for the
unchanged affine-recourse hierarchy considered here.

[Schlosser, Tacchi-Bénard, and Lazarev, *Convergence rates for the moment-SoS
hierarchy*](https://arxiv.org/pdf/2402.00436), version 3 (7 May 2025), gives a general method using
quantitative polynomial approximation, effective positivity certificates,
and a geometric Slater condition. Section 3.2 and Theorem 3.8 already
connect smoothness to better polynomial approximation, while Section 3.3
handles strict feasibility of approximations. The smoothness-to-rate
principle is therefore established. A new claim must identify the
specific benefit of QP structure: an explicit certificate or rounding
argument that avoids growth of private degree and the losses of generic
positivity bounds. Smoothness alone does not prove that claim.

The sparse box hierarchy comparison is recorded more fully in
[sparse-putinar-prior.md](sparse-putinar-prior.md) and
[kernel-prior.md](kernel-prior.md). In particular, a general sparse
preordering inverse-square rate already appears in Magron's 2025 slides.
A recourse theorem must be distinguished by its shared-dependent feasible
fibers, fixed private degree, and stated regularity assumptions, rather
than by the exponent in isolation.

## Claim boundary and search record

No source located in this audit states the full proved combination:
private convex quadratic blocks with affine master-dependent feasible
sets, one of the precise projected-multiplier regularity conditions,
sparse shared moment consistency, private degree two, and an explicit
`O(r^-2)` error in the Lipschitz or weighted-coefficient cases.
This unsuccessful search does not establish novelty. The strongest
comparison is with known QP sensitivity, joint+marginal recourse
approximation, sparse KKT reformulations, and general smooth dual
approximation arguments, taken together.

The companion theorem bounds the unchanged rectangular hierarchy (3);
it adds no KKT equations or multiplier variables. Its constants are the
objective coefficient sum and explicitly stated regularity norms of the
projected multipliers. Estimating those norms from QP data can depend on
active-constraint conditioning. Neither a rate in relaxation order nor a
fixed private degree by itself proves a practical speedup. The proved
capability is controlled global lower bounds for polynomial master
problems coupled to regular convex QPs. The possible solver benefit is
avoiding growth of private degree; numerical conditioning, exact
certificate construction, and performance on applications are not
established by this theorem.

Searches included `parametric quadratic programming value function
continuously differentiable Lipschitz gradient`, `continuous multiplier
selection quadratic`, `polynomial multipliers parametric quadratic`,
`sum squares hierarchy recourse rate`, `joint marginal parametric
optimization`, and `correlatively sparse Lagrange multiplier expression`.
The sources above were inspected at their linked primary locations, with
the stated exception for the 2001 publisher PDF. Local inspection used
`rg` on the literature index and relevant research notes, and `sed` on
the Tøndel and Koeln source records and the Tøndel full text. A Python
rendering attempt failed because `fitz` was unavailable;
`pdftoppm -f 3 -singlefile -scale-to 1600 -png` successfully rendered the
Tøndel theorem page for visual inspection. A targeted Python scan found
no trailing whitespace in this file.

During closure, the author separately reopened the primary PDFs of
Baotić, Lasserre, Zhong--Cui--Nie, Qu--Tang, Schlosser--Tacchi-Bénard--Lazarev,
and Pang--Sun, and the Klatte article. The theorem passages rechecked were
Baotić Corollary 3, Lasserre Theorem 3.5, Zhong--Cui--Nie Theorem 4.1 and
Corollary 4.2, and Qu--Tang Theorem 4.2. The local Tøndel source record was
also reread. Additional exact-phrase searches combined `sparse quadratic
recourse convergence rate moment`, `multiplier Chebyshev recourse sparse`,
and `fixed degree private recourse sum of squares`; they produced no
closer equivalent. Search coverage remains incomplete, and no priority
claim follows. The uninspected full 2001 PDF is not used to justify a
theorem hypothesis. Targeted proof checks are recorded in
[active-region-verification.md](active-region-verification.md). This
source audit ran no Lean checks, project-wide verification, or CI
inspection.
