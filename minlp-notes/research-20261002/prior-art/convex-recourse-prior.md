# Prior art for exact QP with low-dimensional nonconvexity and convex recourse

Date: 2026-10-02. This is a focused comparison of (i) a supplied coordinate
set whose deletion leaves a positive-semidefinite Hessian block and (ii) a
small negative-inertia factorization of a rational quadratic. The closest
literature already uses low-dimensional nonconvex coordinates, convex-QP
recourse, and spatial partitioning. The distinction under review is a
quadratic-growth-conditioned exact Turing bound, not the partitioning or
convexification template itself. This is a bounded source audit, not a
publication-priority claim.

## The parameter names describe different structure

The standard term in the closest QP papers is **negative inertia** or
**nonconvexity rank**: $k_-(A)$, the number of negative eigenvalues of the
objective Hessian. Del Pia's 2026 paper uses this parameter directly. A
coordinate **PSD-deletion set** $C$ instead requires the principal block
$A_{RR}\succeq0$ after deleting $C$, with $R=[n]\setminus C$. If

$$

A=P-T^TDT,\qquad P\succeq0,\quad D\succ0,

$$

then the row dimension of $T$ is a spectral nonconvexity dimension. A PSD
deletion set of size $r$ implies $k_-(A)\le r$ by interlacing, but small
negative inertia need not provide any small coordinate deletion set: its
negative eigenspace can be dense. For example, the rational matrix
$A=I-\frac{11}{10n}\mathbf{1}\mathbf{1}^T$ has one negative eigenvalue,
while a retained principal block on $m$ coordinates is PSD only if
$m\le 10n/11$. Thus a PSD-deletion set may need to grow linearly with $n$
even when $k_-(A)=1$. Conversely, a PSD-deletion set gives an especially simple
exact recourse oracle by fixing those coordinates and solving the remaining
convex rational QP.

“Distance to convexity” is not a safe substitute for either parameter without
a definition; in this literature it can refer to the magnitude of negative
curvature, the number of negative eigenvalues, or a structural deletion
number.

## Closest global-QP algorithms

**Del Pia (2026), “Rational Jacobi Rotations and the Complexity of
Approximating Mixed Integer Quadratic Programming.”** This is the strongest
direct Turing-model prior found for negative inertia. Theorem 1 covers
rational MIQP over a rational linear polyhedron with objective bounded below.
Its approximation metric is
$f(x)-f_{\inf}\le\varepsilon(f_{\sup}-f_{\inf})$. If
$f_{\sup}=+\infty$, the paper explicitly treats the guarantee as vacuous;
the bounded-polytope case has finite range. For fixed integer dimension $p$
and fixed $k_-(A)$, it returns such an approximation in time polynomial in
the input size, $\mathrm{size}(\varepsilon)$, and $1/\varepsilon$. The
continuous-QP case is $p=0$. The theorem does not promise exact optimization
or assume quadratic growth. The paper explicitly says the $1/\varepsilon$
dependence cannot in general be removed: exact QP with one negative
eigenvalue is NP-hard. [[pia2026-rational-jacobi-rotations-and-the]] p.1-2

The same paper addresses the irrational-eigenbasis obstacle. Its rational
Jacobi method returns an orthogonal rational change of basis for which the
transformed Hessian is diagonal up to a prescribed perturbation, with the
diagonal part retaining the exact inertia; further results handle factored
ellipsoids and precondition rational polytopes. These are useful
preprocessing tools for the present spectral route, but the Hessian is
represented as $D+E$ with $E\ne0$ in general. This is not an exact
decomposition into a convex quadratic plus a rank-$k_-$ concave quadratic,
so convex recourse for the original objective does not follow directly.
[[pia2026-rational-jacobi-rotations-and-the]] p.18-22

**Luo, Bai, Lim, and Peng (2019), “New Global Algorithms for Quadratic
Programming with A Few Negative Eigenvalues Based on Alternative Direction
Method and Convex Relaxation.”** This is the closest spatial branch-and-bound
template. For a bounded QCQP with linear and convex quadratic constraints,
they factor the objective as $x^TQ^+x-\|Cx\|^2$, where $C$ has one row
per negative eigenvalue, introduce $t=Cx$, and branch in the $r$-dimensional
$t$-range. Their convex relaxations preserve the original feasible set and
replace the concave quadratic by affine chord bounds. ADMBB's stated relaxed
subproblem count is

$$

O\!\left(N\prod_{i=1}^{r}
\left\lceil\frac{\sqrt r\,(t_i^u-t_i^l)}{2\sqrt\varepsilon}\right\rceil\right),

$$

where $N$ is the cost of a convex-QP relaxation. Their $\varepsilon$ is
an **absolute additive** objective error: Proposition 3.1 gives
$f(\hat x)\le f^*+\varepsilon$. Thus the method has the same projected
negative-curvature and convex-recourse architecture, with a count scaling as
$\varepsilon^{-r/2}$ for fixed ranges. It gives no quadratic-growth packing
bound, exact rational recovery theorem, or Turing bit-complexity analysis for
the convex-QP oracle. The feasible-set scope is broader than boxes, while a
box QP is a special case of the linear-constraint model. [Luo et al., full
author-hosted paper](https://peng.ie.uh.edu/wp-content/uploads/2018/01/QP2NE_Ver3-4.pdf),
pp.1-3, 10-11.

**Vavasis (1992), “Approximation Algorithms for Indefinite Quadratic
Programming.”** This is an earlier conceptual predecessor to the same
projection-and-recourse construction. It projects onto the negative spectral
coordinates, partially minimizes the convex component over the remaining
variables, and partitions the projected region with affine interpolation of
the concave quadratic. Its approximation metric is relative to the objective
range, and its subproblem count has a factor of the form
$\lceil n(n+1)/\sqrt\varepsilon\rceil^{k_-}$, times convex-QP cost. This
already establishes approximation tractability at fixed negative inertia;
the new analysis should not claim the spectral projection, partial
minimization, chord interpolation, or low-inertia approximation as new.
[[vavasis1992-approximation-algorithms-for-indefinite-quadratic]] p.1-7

**Zhang and Xia (2024), “On the Relaxation Complexity of Nonconvex Quadratic
Global Optimization.”** Their Dikin-ellipsoid bound is independent of ambient
dimension when both objective nonconvexity rank $q$ and the number $m$ of
convex quadratic constraints are fixed. It counts convex relaxation
subproblems for objective-range-relative approximation, not bit operations or
exact output. A box is represented by $m=n$ convex quadratic inequalities
$x_i^2\le 1$, so the advertised dimension-free case does not give a
dimension-free count for ordinary boxes. For linear constraints only, their
own Remark 3.4 notes the Dikin count again depends on dimension.
[Zhang–Xia, official full text](https://cot.mathres.org/issues/COT202419.pdf),
pp.1, 4-5.

## What exact recourse and growth add

For a supplied PSD-deletion set $C$, fixing $h=x_C$ leaves an exact
rational convex QP in $z=x_R$. The feasible residual box does not depend on
$h$. Comparing the residual optimizer at one core point against the same
residual point at a nearby core point gives a one-sided quadratic upper model
for the value function $v(h)=\min_z F(h,z)$, with curvature controlled by
the core Hessian block $A_{CC}$. This argument does not require a unique
residual optimizer. A projected quadratic-growth bound on $v$ then confines
any cell whose certified lower bound can still beat the incumbent to a
radius proportional to its mesh width. Packing in the $r$-dimensional core
can therefore bound the number of retained cells per refinement scale,
instead of enumerating every core cell.

The residual oracle is classical: Kozlov, Tarasov, and Khachiyan prove exact
polynomial-bit solvability of rational convex quadratic programming
([official MathNet record and author abstract](https://www.mathnet.ru/eng/zvmmf5189),
English translation, 1980). Thus fixing the core gives a standard exact
oracle call; the parameterized contribution would be the number of core
cells explored, not polynomial solvability of each residual QP.

Exact mixed-integer convex quadratic recourse is also available when the
number $p$ of integer coordinates is a parameter. Del Pia's Theorem 3 gives
an algorithm that “accurately solves” rational convex MIQP over a rational
polyhedron in FPT time in $p$, with any number of continuous coordinates.
The paper defines accurate solution to include feasibility and boundedness
decisions and, in the feasible bounded case, the exact optimum and an
attaining optimizer. Its Theorems 1 and 2 reduce lower-dimensional mixed
feasible sets while preserving mixed-integer points, and the proof uses
exact convex-QP subproblems and rational mixed-integer feasibility. Thus the
bounded-polytope setting needed here is covered, with absolute input-size
exponent and polynomial-bit rational output. [[pia2025-convex-quadratic-sets-and-the]]
pp.1-3, 7-13, 18-23

This corrects the continuous-only boundary for the negative-curvature
subdivision method: its corner oracle can be a convex MIQP oracle when the
integer dimension $p$ is included as a parameter. Under the same rational
growth and optimizer-recovery hypotheses, the retained-cell bound then
composes with Del Pia's oracle to give an FPT bound in the integer dimension,
nonconvex rank, and curvature-to-growth ratio. The oracle does not remove
dependence on $p$; it does not justify a polynomial bound when $p$ is
unrestricted. The original Del Pia result is exact, while the earlier
Del Pia 2023 and 2026 low-rank results are approximation algorithms; these
are complementary rather than substitutes for the recourse oracle.

For spectral nonconvexity, an exact rational representation
$A=P-T^TDT$ allows the same idea to partition $t=Tx$ and solve a convex
QP over the original polytope plus each slab. The chord error is
$\sum_i d_i w_i^2/8$; projected growth can bound the retained slabs. A
rational near-negative basis can be obtained using Del Pia's inertia-preserving
Jacobi result, then checked with exact rational PSD arithmetic. The separate
normalization argument must still account for zero eigenvalues, for example
with the exact rational projector onto $\mathrm{range}(A)$.

The possible new theorem is consequently an **exact, growth-conditioned
complexity refinement** of established low-inertia global approximation:
under a unique optimum and global (or projected-recourse) quadratic growth,
the active-cell count may depend on the number of nonconvex directions and a
curvature-to-growth ratio, while the input-bit and requested-accuracy
exponents stay polynomial; rational height bounds then recover an exact
optimizer and value. No checked source above states that combined guarantee.
However, the cell construction and pruning are close enough to Vavasis/Luo
that an absence search cannot establish novelty. The defensible claim should
be the proved QG-conditioned active-cell and exact-recovery bound, with the
standard spatial B&B template and Del Pia's rational Jacobi rotations cited
as direct predecessors.

The supplied-coordinate theorem and the spectral theorem are related but
incomparable. Coordinate deletion gives immediate exact convex recourse and
can be parameterized by the core dimension $r$. Negative inertia is more
general and can reduce the partition dimension to $k_-(A)$, but requires a
rational low-rank concavity representation and careful treatment of the
positive and zero eigenspaces. Neither parameter is controlled by treewidth
alone.

## Solver and source status

These papers describe globally valid convex relaxations, finite
epsilon-approximation procedures, and solver implementations such as ADMBB,
GSA, and iquad. They support exact lower bounds for each node and certified
approximate global solutions. They do not state the proposed exact
bit-complexity FPT theorem. Commercial spatial B&B capabilities likewise
should be described as global optimization to a requested tolerance, not as
an exact Turing-model guarantee.

The missing papers Luo et al. (2019), Zhang–Xia (2024), Fampa–Lee–Melo (2017),
and Cen–Xia (2021) were routed to `/root/literature_ingest` with identifiers,
lawful links, and relevance notes for serialized ingestion. Luo and
Zhang–Xia have open full texts; Fampa–Lee–Melo has a lawful author-hosted
preprint; I found only the publisher abstract for Cen–Xia. Del Pia (2026) and
Vavasis (1992) are already readable in the local KB. Dey et al. (2023) on
approximate Jordan form was also routed as a possible numerical-linear-algebra
reference, but Del Pia's existing Jacobi result is the closer and stronger
source for this problem. Kozlov–Tarasov–Khachiyan (1980) has since been
ingested and read by the sole ingestion agent; its exact rational-output
claim is verified in the local package [kozlov1980-the-polynomial-solvability-of-convex](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md),
pp.2, 3, 5.
