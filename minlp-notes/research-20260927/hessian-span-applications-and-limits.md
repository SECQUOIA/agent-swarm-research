# Applications and boundaries of the Hessian-span theorem

Date: 2026-09-27. Status: proved modeling consequences and limitations;
independent application and quartic reviews are linked below. This note does
not establish publication priority or a computational improvement.

The most concrete application identified here is vector-valued polynomial
fitting with Euclidean residual bounds and binary choices of which
observations to retain. With fixed polynomial degree, the number of
independent continuous Hessians stays bounded while the output dimension
and number of observations can grow. The current theorem gives a rational
MILP of polynomial size with exactly the same feasible observation choices
and no additional integer variables. This is an exact discrete modeling
consequence, rather than a new polynomial-time algorithm when the number of
binary choices grows.

The relevant ingredients are the
[value and precision theorem](hessian-span-reduction.md), the
[exact integer-projection theorem](mixed-integer-span-frontier.md), and the
[small feasible-point theorem](unbounded-hessian-span.md). Their assumptions
matter: the integer variables must be bounded, the quadratic rows used for
the formulation must be jointly convex, and the degree-two restriction
cannot simply be replaced by a bound on the number of convex polynomials.

## 1. A recognizable family with many quadratic rows

Let the rational scenario parameter be \(s\in\mathbb Q^p\). Suppose

\[
 A(s)=\sum_{|\alpha|\le d}s^\alpha A_\alpha,
\]

where the rational matrices \(A_\alpha\) have any common row and column
dimensions. Consider finitely many rows

\[
 q_i(x,z)=\|A(s_i)x+B_i z-b_i\|_2^2+
                   a_i^Tx+c_i^Tz+e_i\le0.                 \tag{1}
\]

The number of scenarios, continuous variables and residual coordinates can
grow. The matrices \(B_i\), vectors \(b_i,a_i,c_i\), and constants
\(e_i\) can vary independently across scenarios. Every row is jointly
convex in \((x,z)\). Its continuous Hessian is
\(2A(s_i)^TA(s_i)\), and

\[
 A(s)^TA(s)=\sum_{|\gamma|\le2d}s^\gamma H_\gamma,
 \qquad
 H_\gamma=\sum_{\alpha+\beta=\gamma}A_\alpha^TA_\beta.
\]

The matrices \(H_\gamma\) are symmetric after collecting the ordered
pairs. They need not be PSD. Nevertheless the evaluated matrices
\(A(s)^TA(s)\) are PSD, and

\[
 h\le {p+2d\choose 2d}.                                \tag{2}
\]

Thus fixed parameter dimension and fixed polynomial degree give fixed
Hessian span, independently of the other dimensions. The parameters
\(s_i\) are input data, not optimization variables. Treating them as
variables generally creates higher-degree, nonconvex rows and is outside
this statement.

Formula (2) is a sufficient recognition rule. The actual span is computable
by exact rational rank of the listed Hessian matrices and can be smaller.
An affine restriction \(x=x_0+Vu\) replaces the Hessians by
\(V^TQ_iV\) and cannot increase their span. Consequently affine dynamics,
conservation equations or other affine links do not destroy the bound.

For bounded integer \(z\), the current integer-projection theorem applies
to (1), together with arbitrary rational affine rows. Continuous bounds
can be supplied by the small-point theorem. For fixed \(p,d\), it gives a
polynomial-size rational MILP with the same feasible integer assignments
and no new integer variables. The safe complexity description after
inserting the radius is polynomial for fixed \(p,d\); this note does not
claim the original sharp exponent survives that insertion.

This is a modeling template, not evidence that every scenario model has
small span. If every scenario carries an unrelated matrix \(A_i\), the
span can grow with the number of scenarios. Likewise, separate constraints
on individual coordinates or independent time segments can introduce many
independent Hessians.

## 2. Vector-valued polynomial fitting and observation selection

Let

\[
 P_x(t)=\sum_{j=0}^d x_jt^j,\qquad x_j\in\mathbb R^r.
\]

Given rational samples \((t_i,y_i)\), with \(y_i\in\mathbb Q^r\),
and rational squared tolerances \(\tau_i\ge0\), call observation \(i\)
retained when

\[
 \|P_x(t_i)-y_i\|_2^2\le\tau_i.                        \tag{3}
\]

The coefficient vector has dimension \(r(d+1)\). The Hessian of row
\(i\), up to the harmless factor two, is the block matrix

\[
 Q_d(t_i)=\bigl[t_i^{a+b}I_r\bigr]_{a,b=0}^d
       =v_d(t_i)v_d(t_i)^T\otimes I_r,
 \qquad v_d(t)=(1,t,\ldots,t^d)^T.
\]

There are \(2d+1\) possible exponents \(a+b\), so

\[
 h\le2d+1.                                             \tag{4}
\]

If at least \(2d+1\) distinct sample locations are present, equality
holds. Indeed, the coefficient matrices for different exponents have
disjoint block antidiagonals and are nonzero, and a Vandermonde matrix at
\(2d+1\) distinct locations has full rank. The affine target terms do
not affect this calculation.

Introduce binary variables \(z_i\), where \(z_i=1\) permits discarding
observation \(i\). There may also be arbitrary rational affine constraints
on \((x,z)\), such as budgets, group rules, coefficient equalities and
bounded additional integer decisions. The intended condition is (3) for
each \(i\) with \(z_i=0\). No condition is imposed by a discarded
observation.

**Corollary.** For fixed \(d\), there is a polynomial-size rational MILP,
constructible in polynomial time, with exactly the same feasible bounded
integer assignments as this observation-selection model. No additional
integer variables are needed. Neither \(r\) nor the number of observations
is fixed. The original coefficient variables need not have input bounds.

**Proof.** Fix any assignment of the bounded integer variables. Delete the
discarded rows and substitute the assignment in all affine rows. The
remaining continuous problem is a rational convex QCQP with span at most
\(2d+1\) and input length bounded by one polynomial in the original input
length \(N\), uniformly over all assignments. The small-point theorem
therefore gives one computable integer \(R\), with polynomial bit length
for fixed \(d\), such that every feasible assignment has some feasible
coefficient vector in \([-R,R]^{r(d+1)}\). This assertion is uniform and
does not enumerate assignments. It preserves existence of a representative,
rather than every feasible coefficient vector.

Put

\[
 U_i=\sum_{\ell=1}^r
      \left(R\sum_{j=0}^d|t_i|^j+|y_{i\ell}|\right)^2,
 \qquad M_i=\max\{0,U_i-\tau_i\}.
\]

These are rational and have polynomial bit length for fixed \(d\). On
the coefficient box the residual squared is at most \(U_i\). Hence

\[
 \|P_x(t_i)-y_i\|_2^2\le\tau_i+M_i z_i                 \tag{5}
\]

has exactly the desired discard semantics on that box. Each row (5) is
jointly convex: its integer term is affine. It has the same continuous
Hessian as (3). Apply the boxed integer-projection theorem to (5), the box,
and the affine rows. This proves the corollary. The composition of the
radius and formulation bounds is polynomial for fixed \(d\). \(\square\)

A rational linear objective such as \(\sum_i w_i z_i\) is preserved
exactly because it depends only on the discrete assignment. The continuous
coefficient vector displayed by a feasible point of the resulting MILP
need not satisfy (3). The theorem ensures that some exactly feasible
coefficient vector exists for the selected observations. The subsequent
[algebraic witness theorem](algebraic-witness-recovery.md) recovers one
exactly after the integer assignment is fixed; this is a separate algorithm
from reading the MILP's continuous coordinates.

There is an important generic comparator for models in which **all**
original integer variables are binary. Once fixed-assignment feasibility
is decidable in deterministic polynomial bit-time, a polynomial-size
continuous-auxiliary linear formulation of the feasible binary assignments
also follows abstractly. Hardwire the model data into a Boolean circuit
for that decision algorithm. A polynomial-time computation has a
polynomial-size circuit: encode its tape and state at each of its
polynomially many time steps, and implement each local transition with
a constant-size Boolean circuit. Replace every gate by its elementary
linear hull. For example, an AND gate has

\[
 0\le g\le1,\qquad g\le a,\quad g\le b,
 \quad g\ge a+b-1,
\]

and a NOT gate has \(g=1-a\). All gate variables can be continuous.
Binary original inputs force each successive gate value to be binary and
correct. Requiring the output gate to equal one therefore gives exactly
the accepted binary assignments. The construction has polynomial size and
bounded integer coefficients. Removing redundant repeated-input gates
allows coefficients in \(\{-1,0,1\}\).
It need not describe their convex hull: fractional original inputs can
permit fractional gate values, so bounds on ideal extended formulations
do not contradict this construction.

Thus, in the purely binary case, the fitting formulation is not a stronger
complexity consequence than polynomial-time fixed-assignment feasibility.
The geometric approximation gives a direct formulation tied to the
quadratic model, whereas the circuit construction expresses the execution
of a decision algorithm. Neither route supplies an empirical performance
advantage. For general bounded integer variables, extracting binary digits
using only continuous auxiliary variables does not follow from this
argument; adding free binary digit variables would change the integer
variable count. The current theorem's general bounded-integer statement
therefore requires a separate justification.

Ordinary scalar fitting with rational absolute-error tolerances is already
linear: \(|P_x(t_i)-y_i|\le\epsilon_i\) is two affine inequalities.
The relevant class here uses vector outputs and a Euclidean residual with
one shared decision per observation. Keeping \(r\) unbounded also avoids
explaining the result solely by a fixed total continuous dimension. If
the input gives only a rational squared scalar tolerance, its square root
may be irrational; this does not justify claiming that all scalar versions
already have rational linear rows.

This application is close to established maximum-consensus models.
[Chin, Kee, Eriksson and Neumann (CVPR 2016)](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Chin_Guaranteed_Outlier_Removal_CVPR_2016_paper.pdf),
Section 3.1, equation (19), use binary outlier variables and vector norm
residual thresholds. They explicitly distinguish the Euclidean-norm
second-order-cone case from the \(1\)- and infinity-norm cases that have
ordinary linear formulations. The proposed contribution is a polynomial
rational formulation preserving the integer projection for the structured
Euclidean subclass above. It does not replace their geometric residual
models in general: varying denominators, rotations and unrelated data
matrices can violate the present assumptions.

[Gómez and Neto's conic regression formulations](https://arxiv.org/abs/2307.05975)
are also a practical comparator. Their objective and convexification
approach concern outlier-contaminated regression, rather than this precise
vector polynomial feasibility model. Their work underscores that stronger
conic relaxations already address such discrete fitting decisions. The
present worst-case MILP encoding gives no claim of a stronger relaxation
or faster solution than direct conic methods.

## 3. Why the affine-fitting family is not a fixed-generator example

For \(d=1\), the matrices in (4) are

\[
 Q_1(t)=\begin{pmatrix}I_r&tI_r\\tI_r&t^2I_r\end{pmatrix}.
\]

They have rank \(r\). Their span has dimension three when at least three
distinct locations occur, and their aggregate rank is \(2r\) as soon as
two distinct locations occur. Any common collection of nonzero
PSD matrices whose nonnegative combinations represent all \(m\) matrices
at distinct locations must have at least \(m\) members. This remains
true when the generators are allowed outside the three-dimensional span.

To see this, any positive PSD summand of \(Q_1(t)\) must have range
contained in

\[
 R_t=\{(u,tu):u\in\mathbb R^r\}.
\]

This follows by applying the summand decomposition to vectors in the
kernel: nonnegative quadratic forms summing to zero each vanish there.
For distinct \(s,t\), \(R_s\cap R_t=\{0\}\). A nonzero generator
therefore cannot be used for two sample locations. The
[package assessment](hessian-package-assessment.md) supplies the full
argument and an independent exact matrix check.

Thus fixed span is more general than a fixed number of shared
PSD quadratic generators. This does not rule out every other reformulation
of the fitting problem.

There is also an easy case to exclude from the motivation. Suppose both
the residual map and its target vary affinely in one scalar parameter,
and all scenarios have the same squared tolerance. For fixed decisions,
the residual squared is convex in that parameter. The constraints at the
smallest and largest parameter then imply all intermediate ones. Such a
family already reduces to two quadratic rows. Arbitrary observed targets
\(y_i\) or varying tolerances in (3) prevent this particular argument;
their presence is material to the proposed example.

## 4. Boundaries of the exact formulation claim

**Continuous slice convexity is insufficient.** Let \(z\) be integer in
\([-1,1]\), impose \(x=0\), and require

\[
 x^2+1-z^2\le0.
\]

Every continuous slice is convex, with one native continuous Hessian. The
feasible integer assignments are exactly \(z=-1,1\). No polyhedron with
only additional continuous variables can have exactly that integer
projection: its projection onto \(z\) is convex and contains the midpoint
zero. Thus joint convexity in the current MILP theorem has a mathematical
role even when continuous slice feasibility is easy.

**Unbounded integer domains cannot be handled by the same finite
polyhedral conclusion.** Consider

\[
 \{(a,b)\in\mathbb Z^2:b\ge a^2\}.                    \tag{6}
\]

The native quadratic is jointly convex and there are no continuous
variables, so its continuous Hessian-span parameter is zero. Suppose a
polyhedron \(P\subseteq\mathbb R^2\) had exactly the integer points
(6). Write its finite inequalities as
\(\alpha_j a+\beta_j b\le\gamma_j\). Since all integer
\((a,b)\) with \(b\ge a^2\) must satisfy each row,
\(\beta_j\le0\). If \(\beta_j=0\), allowing both signs and arbitrary
magnitudes of integer \(a\) forces \(\alpha_j=0\) and a redundant
row. If there are no remaining rows, \((0,-1)\in P\) is already a
contradiction. Otherwise every remaining row is an affine lower bound on
\(b\). For large positive integer \(a\), the ceiling of the maximum of these finitely
many affine functions grows at most linearly and is strictly below
\(a^2\). It is an integer point of \(P\) outside (6), a contradiction.
The same obstruction applies to a polyhedron with continuous auxiliary
variables, because a projection of a polyhedron is a polyhedron. This
explains why bounded integer assignments are essential to the stated
formulation theorem; it does not exclude other algorithms for particular
unbounded models.

**Quadratic degree is essential to the stated algebraic-degree bound.**
The separate [quartic boundary review](quartic-span-boundary-review.md)
constructs one globally convex quartic row whose boxed, linear-objective
optimum has algebraic degree \(3^n\). A bound on the number or span of
whole nonlinear polynomials therefore cannot replace the quadratic
Hessian-span hypothesis. Large algebraic degree alone does not imply a
superpolynomial exact decision algorithm, a tiny nonzero value gap, or
computational hardness. The degree phenomenon is classical; the explicit
example identifies the limit of the proposed generalization.

## 5. What this adds, and what would establish practical value

The application establishes a structural guarantee for exact observation
selection and for the more general matrix-polynomial family (1). It
allows arbitrary affine links, growing continuous dimension, many native
quadratic rows and singular or degenerate feasible fibers. Its integer
preservation does not require a strict feasible point. These are proved
consequences of the current theorem, conditional on that theorem's proof.

A useful implementation would need substantially better instance-specific
radius and residual-separation estimates than the universal bounds used
here. It would also need to recover suitable continuous coefficients and
compare the resulting MILP with existing conic formulations on the same
models. Rational encoding size is not a claim about useful LP strength,
numerical conditioning or branch-and-bound performance. With one binary
variable per observation, a polynomial-size formulation also does not
make maximum consensus a polynomial-time optimization problem.

The strongest next empirical or algorithmic question is whether a small
span detected after affine elimination can guide short, well-conditioned
approximations for structured vector fitting or scenario models. That
possible use is presently a research direction, not a demonstrated
solver improvement.

## 6. Verification and source record

The span calculations, uniform-radius construction, discard bounds and
two polyhedral obstructions are proved explicitly above. A fresh agent
independently examined the fitting corollary and its closest application
comparison; see [its review](polynomial-fit-application-review.md).
A second fresh agent examined the quartic algebraic-degree boundary.
A third independently checked the
[binary circuit formulation argument](binary-circuit-formulation-review.md),
including uniform construction and the distinction from an ideal
convex-hull formulation.

Primary sources examined for the application comparison were the CVPR
2016 paper above, the author record and abstract of Gómez--Neto, and
[Bartelt--Swetits's 2008 author record](https://digitalcommons.odu.edu/mathstat_fac_pubs/55/)
on finite-set vector-valued Chebyshev approximation. The last source
confirms that the underlying vector approximation setting is established;
its continuity theorem is not used in any proof here. A trajectory-planning
search also found [Freire--Xu](https://arxiv.org/abs/2111.00951), whose
B-spline SOCP already supplies continuous-time safety guarantees. That
paper was examined only at the abstract level. It is not evidence that
general trajectory models have fixed Hessian span, nor does the present
finite-sample result imply continuous-time safety.

These are targeted comparisons, not an exhaustive priority search. No
numerical performance experiment, Lean formalization, project-wide test or
CI check is claimed for this note.

Targeted local commands actually run were
`git diff --check -- research-20260927/hessian-span-applications-and-limits.md`
(no diagnostics) and an inline `python` check of this file's local links,
control characters, trailing whitespace and final newline (passed).
Because the file was newly created and untracked, the Python check,
rather than `git diff`, checked its content. Mathematical verification
consists of the proofs and independent reviews described above; these
document checks do not validate the theorems.
