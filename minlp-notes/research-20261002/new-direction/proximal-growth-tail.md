# A sharp growth tail under independent linear perturbations

Date: 2026-10-02. Status: the continuous-noise theorem, uniform-volume
argument, and finite rational-grid completion passed a
[fresh review of the completed note](../reviews/proximal-growth-tail-adversary.md).
This note makes no literature-priority claim.

The logarithmic loss in the
[summed-response bound](summed-response-growth.md) is unnecessary for the
actual global quadratic-growth modulus. A proximal map bounds the bad
event directly, without summing maximal coordinate-response slopes.

## 1. Statement

Let \(X\subset\mathbb R^n\) be nonempty and compact, and let
\(f:X\to\mathbb R\) be continuous. Write

\[
 \ell_i=\min_{x\in X}x_i,\qquad r_i=\max_{x\in X}x_i,\qquad
 w_i=r_i-\ell_i.
\]

For a coefficient vector \(c\), set \(F_c(x)=f(x)+c^Tx\). Define
\(g_*(c)\) as the largest \(g\ge0\) for which some optimizer \(x^*\)
satisfies

\[
 F_c(x)-F_c(x^*)\ge g\|x-x^*\|^2\qquad(x\in X).
\tag{1}
\]

For a singleton \(X\), set \(g_*=\infty\). Otherwise \(g_*\) is the
infimum of the displayed ratios when the optimizer is unique, and is zero
when distinct optimizers exist.

**Theorem.** Suppose the coordinates of \(c\) are independent and have
densities bounded by \(\phi_i\). Then, for every \(\varepsilon>0\),

\[
 \boxed{\Pr\{g_*(c)<\varepsilon\}
       \le 2\varepsilon\sum_i\phi_iw_i.}
\tag{2}
\]

The right side can of course be capped at one. No differentiability,
convexity, or definability assumption on \(f\) or \(X\) is required.
The constant \(2\) is sharp.

If \(X\) is not a singleton, then with probability at least \(1-\rho\)
the optimizer is unique and

\[
 \boxed{g_*(c)\ge
       \frac{\rho}{2\sum_i\phi_iw_i}.}
\tag{3}
\]

For independent uniform noise on intervals of common half-width
\(\sigma\), this reads

\[
 \boxed{g_*(c)\ge
       \frac{\rho\sigma}{\sum_iw_i}.}
\tag{4}
\]

Arbitrary deterministic coefficient offsets are allowed. In particular,
on a box of coordinate width at most \(W\), the bound is
\(\rho\sigma/(nW)\), with no logarithmic factor.

## 2. A convex conjugate and its proximal map

Fix \(\varepsilon>0\), and use \(z=-c\) to simplify the signs. Put
\(\lambda=2\varepsilon\), and define the finite convex function

\[
 H(a)=\max_{x\in X}
       \{a^Tx-f(x)+\varepsilon\|x\|^2\}.
\tag{5}
\]

Compactness makes the maximum attained and \(H\) globally Lipschitz.
Every maximizing point is a subgradient of \(H\). Also

\[
 v_i\in[\ell_i,r_i]\qquad(v\in\partial H(a)).
\tag{6}
\]

For example, the coordinate difference quotients of \(H\) lie between
\(\ell_i\) and \(r_i\), which gives (6) directly from the subgradient
inequality.

Let

\[
 P(z)=\operatorname*{argmin}_{a\in\mathbb R^n}
       \left\{H(a)+\frac{\|a-z\|^2}{2\lambda}\right\},
 \qquad Q(z)=z-P(z).
\tag{7}
\]

The quadratic term makes the minimizer unique. Its optimality condition is

\[
 \frac{Q(z)}{\lambda}\in\partial H(P(z)).
\tag{8}
\]

We use three standard proximal-map facts, with their relevant justification.

1. \(P\) and \(Q\) are 1-Lipschitz. Monotonicity of \(\partial H\)
   applied to (8) gives
   \[
    \langle P(z)-P(z'),Q(z)-Q(z')\rangle\ge0.
   \]
   Combining this with \(z-z'=(P(z)-P(z'))+(Q(z)-Q(z'))\)
   proves the two Lipschitz bounds and monotonicity of both maps.
2. At almost every \(z\), \(DP(z)\) is symmetric and
   \[
    0\preceq DP(z)\preceq I.
   \tag{9}
   \]
   Indeed, \(P\) is the gradient of the convex conjugate of
   \(a\mapsto\|a\|^2/2+\lambda H(a)\). That function is strongly
   convex, so its conjugate has the 1-Lipschitz gradient \(P\).
   Almost-everywhere differentiability and Hessian symmetry give (9).
   Equivalently, both \(P\) and \(Q\) are gradients of convex functions.
3. By (6) and (8),
   \[
    Q_i(z)\in[\lambda\ell_i,\lambda r_i].
   \tag{10}
   \]
   For every fixed \(z_{-i}\), the function \(t\mapsto Q_i(t,z_{-i})\)
   is nondecreasing and Lipschitz. Its total variation on the real line
   is at most \(\lambda w_i\).

These facts concern a convex function of coefficients. They do not assume
that the original objective is convex in its decision variables.

## 3. Regular conjugate points certify global growth

Suppose \(H\) is differentiable at \(a=P(z)\). Every maximizer in
(5) is then the same point

\[
 x^*=\nabla H(a)=Q(z)/\lambda,\qquad z=a+2\varepsilon x^*.
\tag{11}
\]

The first equality follows because a maximizer is a subgradient and the
subgradient is unique. Optimality in (5) gives, for every \(x\in X\),

\[
 f(x)-f(x^*)-a^T(x-x^*)
 \ge\varepsilon(\|x\|^2-\|x^*\|^2).
\]

Substituting (11) yields

\[
 f(x)-z^Tx-\bigl(f(x^*)-z^Tx^*\bigr)
 \ge\varepsilon\|x-x^*\|^2.
\tag{12}
\]

Thus differentiability of \(H\) at \(P(z)\) implies growth at least
\(\varepsilon\) for \(F_{-z}\), including uniqueness of its optimizer.

Let \(N\) be a Borel null set containing the nondifferentiability points
of \(H\); such a set exists because \(H\) is Lipschitz. Define

\[
 E=P^{-1}(N).
\tag{13}
\]

This is measurable, and every coefficient \(z\) with
\(g_*(-z)<\varepsilon\) belongs to \(E\).

The actual bad-growth event is also measurable without using (13). The
set of coefficients admitting (1) with \(g=\varepsilon\) is closed:
along a convergent coefficient sequence, choose a convergent subsequence
of its optimizers in compact \(X\), and pass every inequality to the
limit. Its complement is precisely \(\{g_*<\varepsilon\}\).

## 4. The area formula bounds the bad event by a divergence

Apply the Lipschitz area formula to \(P\) on
\(E\cap[-m,m]^n\). Its image is contained in the null set \(N\), so

\[
 \int_{E\cap[-m,m]^n}|\det DP(z)|\,dz=0.
\tag{14}
\]

The possible multiplicity of this image does not affect the conclusion:
the image lies in a Lebesgue null set. Taking the union over positive
integers \(m\) proves

\[
 \det DP(z)=0\quad\hbox{for almost every }z\in E.
\tag{15}
\]

All eigenvalues of \(DP\) lie in \([0,1]\) by (9). On \(E\), at
least one is zero almost everywhere. Consequently

\[
 \boxed{\mathbf1_E(z)
       \le\operatorname{tr}(I-DP(z))
       =\sum_i\partial_iQ_i(z)
       \quad\hbox{almost everywhere}.}
\tag{16}
\]

Outside \(E\) the same inequality holds because its left side is zero
and every summand on the right is nonnegative. This is the step that
avoids summing maximal response slopes: only the trace of a bounded
proximal displacement is integrated.

## 5. Integration against the perturbation densities

Reflection \(z=-c\) preserves independence and the density bounds.
Condition on \(z_{-i}\). The coordinate section of \(Q_i\) is
absolutely continuous and nondecreasing, and (10) gives

\[
 \int_{\mathbb R}\partial_iQ_i(t,z_{-i})\,dt
 \le\lambda w_i.
\tag{17}
\]

Its derivative is nonnegative, so integrating against a density bounded
by \(\phi_i\), then averaging over \(z_{-i}\), gives

\[
 \mathbb E[\partial_iQ_i(z)]\le\lambda\phi_iw_i.
\tag{18}
\]

Fubini's theorem identifies these coordinate derivatives with the
almost-everywhere Jacobian entries used in (16). The product density is
absolutely continuous, so all preceding Lebesgue null sets have zero
probability. Combining (13), (16), and (18) proves

\[
 \Pr\{g_*(c)<\varepsilon\}
 \le\Pr(E)
 \le\sum_i\mathbb E[\partial_iQ_i(z)]
 \le2\varepsilon\sum_i\phi_iw_i.
\]

Independence is used only to retain the density bound after conditioning.
The same proof applies if all one-coordinate conditional densities have
the stated uniform bounds.

## 6. Uniform noise: an expanding-map explanation

For uniform noise one can also see the bound directly through volume.
Translate \(X\) so that its coordinate ranges are
\([-w_i/2,w_i/2]\). At every differentiability point \(a\) of \(H\),
define

\[
 T(a)=a+2\varepsilon\nabla H(a).
\tag{19}
\]

Monotonicity of \(\nabla H\) shows
\(\|T(a)-T(b)\|\ge\|a-b\|\), and \(P(T(a))=a\).
Equation (12) says that \(T(a)\) has growth at least
\(\varepsilon\). Moreover,

\[
 |T_i(a)-a_i|\le\varepsilon w_i.
\tag{20}
\]

Consider a coefficient box of side lengths \(L_i\). Its inner box,
obtained by removing a margin \(\varepsilon w_i\) at both ends of
coordinate \(i\), is mapped into the original coefficient box and into
the good-growth set, except for a null set of \(a\)'s.

For completeness, no measurability claim about a discontinuous forward
image is needed. Intersect the closed good-growth set with the original
coefficient box. Its image under the 1-Lipschitz map \(P\) contains the
inner box except for a null set. Lipschitz volume contraction therefore
shows that the good set has at least the volume of that inner box.
If \(2\varepsilon w_i<L_i\) for every coordinate, the bad probability
is at most

\[
 1-\prod_i\left(1-\frac{2\varepsilon w_i}{L_i}\right)
 \le2\varepsilon\sum_i\frac{w_i}{L_i}.
\tag{21}
\]

If a margin removes an entire coordinate interval, the final bound is
already at least one. This agrees with (2) for uniform densities
\(\phi_i=1/L_i\). The proximal-divergence proof also covers arbitrary
bounded independent densities.

## 7. Sharpness and relation to the earlier certificate

Take \(X=[-w/2,w/2]\), \(f=0\), and
\(c\sim\operatorname{Unif}[-\sigma,\sigma]\), whose density is
\(\phi=1/(2\sigma)\). For \(c\ne0\), direct comparison with the opposite
endpoint gives

\[
 g_*(c)=|c|/w.
\]

Therefore, for \(0<\varepsilon\le\sigma/w\),

\[
 \Pr\{g_*<\varepsilon\}
 =\frac{w\varepsilon}{\sigma}
 =2\varepsilon\phi w.
\tag{22}
\]

Thus constant \(2\) cannot be improved for the stated class. For a
product of these examples, with \(f=0\) and independent
\(c_i\sim\operatorname{Unif}[-\sigma_i,\sigma_i]\), the exact tail is
\(1-\prod_i(1-2\varepsilon\phi_iw_i)\) whenever every factor is
nonnegative, where \(\phi_i=1/(2\sigma_i)\).
Its small-\(\varepsilon\) expansion also attains the sum
of widths in (2) to first order.

The earlier sum of coordinate maximal slopes remains a valid certificate,
but can be weaker than the actual modulus by a factor of order
\(\log n\). The linear example in
[the summed-response note](summed-response-growth.md) already proves
that loss for that certificate. The present argument bounds the actual
bad-growth event, so that obstruction does not apply.

## 8. Finite rational perturbations for quadratic programs

The sharp continuous tail also has a finite-bit realization. Consider a
rational quadratic objective \(q_c\) on one of the compact feasible sets
covered by the earlier note: a continuous box, a mixed box, or a bounded
continuous rational polytope. Let \(F\) bound the number of faces, counting
the continuous faces separately at each integer assignment in a mixed
box. We may use

\[
 F=3^{n_c}\prod_{j\ {\rm integer}}N_j
 \quad\hbox{for a mixed box},\qquad
 F=2^m
 \quad\hbox{for a polytope with \(m\) supplied inequalities}.
\tag{23}
\]

A continuous box is the case \(n_c=n\) with an empty product. These
counts include vertices, and redundant polytope inequalities do not
invalidate the upper bound.

**Slice-complexity lemma.** Fix every coefficient except one linear
objective coefficient \(t\), and fix \(\varepsilon>0\). The set of values \(t\)
at which \(g_*<\varepsilon\) has at most

\[
 C=8(F+1)^2
\tag{24}
\]

interval components, allowing isolated points in this safe bound.
The bound is uniform in the fixed coefficients.

To prove it, recall the elementary quadratic candidate fact. A quadratic
on a compact polytope has an optimizer on a face whose tangent Hessian
is positive definite, with a vertex allowed as a zero-dimensional face.
Starting with an optimizer in the relative interior of its smallest
face, a singular positive-semidefinite tangent Hessian supplies a null
direction. Stationarity makes the objective constant along that direction.
Moving to a face boundary reduces the face dimension and preserves the
objective. Repeating proves the claim. In a mixed box first fix the
integer assignment. Thus at most \(F\) stationary face candidates
suffice for the global minimum of any fixed-Hessian quadratic in this
family.

For the original Hessian, every such candidate \(x_r(t)\) is affine in
\(t\), obtained from a nonsingular tangent stationarity system. Its
feasibility set is an interval, possibly empty or a singleton. For each
original candidate \(r\), form the quadratic in a new decision variable
\(y\):

\[
 \widetilde q_{r,t}(y)
   =q_t(y)-\varepsilon\|y-x_r(t)\|^2.
\tag{25}
\]

Its Hessian is the original Hessian minus \(2\varepsilon I\), restricted
to the continuous variables when integer assignments are fixed. Its
linear coefficient vector is affine in \(t\); it need not vary in just
one coordinate. Its stationary candidates \(y_{r,s}(t)\), at most
\(F\) for each \(r\), are therefore affine too. Each has an interval
feasibility set, and

\[
 d_{r,s}(t)=
 \widetilde q_{r,t}(y_{r,s}(t))-q_t(x_r(t))
\tag{26}
\]

is a polynomial of degree at most two.

Growth at least \(\varepsilon\) holds exactly when at least one
original candidate \(x_r(t)\) is feasible and

\[
 d_{r,s}(t)\ge0
 \quad\hbox{for every feasible modified candidate }y_{r,s}(t).
\tag{27}
\]

For sufficiency, the candidate fact makes (27) a bound on the modified
global minimum, hence it is exactly (1) with \(x^*=x_r(t)\).
It automatically proves that this candidate is an original global
optimizer. For necessity, positive growth gives a unique optimizer and
the original candidate fact supplies a stationary face candidate at it;
(1) then gives (27). Nonunique optima cannot pass this test: another
tied point \(y\ne x_r(t)\) makes (25) strictly smaller than
\(q_t(x_r(t))\).

The truth of this finite Boolean condition can change only at

- the at most \(2F\) original-candidate feasibility endpoints;
- the at most \(2F^2\) modified-candidate feasibility endpoints;
- the at most \(2F^2\) roots of nonzero polynomials (26).

Identically zero comparison polynomials create no breakpoints. With
\(K\le2F+4F^2\) total breakpoints, the real line has at most \(K+1\)
open cells and \(K\) individual breakpoints. Thus every Boolean union
of them has at most \(2K+1\le8(F+1)^2\) components, proving (24).
In fact the bad-growth set is open by the closedness argument in
Section 3; the stated bound does not need that improvement.

Now perturb each coordinate independently on the \(M\)-point rational
grid in \([-\sigma,\sigma]\), including both endpoints, with \(M\)
a power of two. The empirical distribution function of this grid differs
from that of the continuous uniform distribution by at most \(1/M\).
For any union of at most \(C\) intervals or points, the probability
discrepancy is therefore at most \(2C/M\).

Replace the continuous marginals by their grid versions one at a time.
At every replacement, conditioning on all other coefficients gives a
slice covered by (24). Its bound is uniform even when some other
coordinates are already discrete. Telescoping the \(n\) discrepancies
gives

\[
 \Pr_{\rm grid}\{g_*<\varepsilon\}
 \le
 \Pr_{\rm continuous}\{g_*<\varepsilon\}
       +\frac{2nC}{M}
 \le
 \frac{\varepsilon}{\sigma}\sum_iw_i+\frac{2nC}{M}.
\tag{28}
\]

Equation (28) holds for every \(\varepsilon>0\) on the same fixed
sampling grid. In particular its residual
\(\beta=2nC/M\) is independent of the growth threshold. Taking
one-sided limits also gives the same bound for
\(\Pr_{\rm grid}\{g_*\le\varepsilon\}\), and gives
\(\Pr_{\rm grid}\{g_*=0\}\le\beta\).

Assume \(X\) is not a singleton. Choose

\[
 \boxed{\varepsilon=\frac{\rho\sigma}{2\sum_iw_i},
 \qquad
 M\ge\frac{4nC}{\rho}
       =\frac{32n(F+1)^2}{\rho}.}
\tag{29}
\]

Then with probability at least \(1-\rho\) the rationally perturbed QP
has a unique optimizer and growth at least \(\varepsilon\).
This loses only a factor of two relative to (4), and has no logarithmic
loss in dimension or failure probability.

For rational input, take rational \(\rho,\sigma>0\), with
\(0<\rho<1\). The coordinate widths are rational; for bounded
polytopes they can be computed by rational linear programming. A sampled
coefficient has the form

\[
 -\sigma+\frac{2\sigma k}{M-1},
 \qquad k\in\{0,\ldots,M-1\}.
\]

The least sufficient power of two in (29) uses

\[
 \log_2M=O(\log F+\log(n/\rho))
\tag{30}
\]

random bits per coordinate. This is polynomial in the input size for
all families in (23), including integer intervals with binary-encoded
lengths. The sampler does not enumerate faces or grid points, determine
the optimizer, or test growth. Face candidates are counted only in the
analysis. The sampled coefficients have polynomial bit length.

## 9. Consequences for the conditioned algorithms

The reviewed algorithms and their bit-complexity arguments remain the
ones in the earlier notes. This theorem improves the growth parameter
inserted into those algorithms. Put \(S=\sum_iw_i\). For rational
uniform perturbations as in (29), with probability at least \(1-\rho\),

\[
 \max\{1,L/g_*\}\le\max\{1,2LS/(\rho\sigma)\}
\tag{31}
\]

for the [pruned-grid algorithm](pruned-coordinate-grid.md), and

\[
 \max\{1,\nu/g_*\}\le\max\{1,2\nu S/(\rho\sigma)\}
\tag{32}
\]

for the [continuous negative-inertia algorithm](negative-inertia-qp.md).
Linear perturbations preserve the interaction graph and Hessian.

Thus the high-probability polynomial-work consequences at fixed supplied
bag size or fixed negative inertia retain their earlier qualifications,
with these sharper numerical bounds. They concern the sampled objective
and require polynomial numerical bounds on the relevant scale ratios.
They do not establish FPT in the structural parameter alone.

## 10. Scope and verification

This theorem concerns the perturbed objective. It does not recover the
exact optimizer of the unperturbed problem, by itself establish expected
work for an uncapped solver, or supply an optimization oracle for
arbitrary continuous \(f\). Section 8 separately supplies finite-bit
input for the stated rational quadratic families.

The proof uses standard convex conjugacy, proximal maps, almost-everywhere
differentiability, the Lipschitz area formula, and one-dimensional
variation. The numerical tail and its use for optimization require a
separate literature comparison. No priority claim follows from the
independent derivations.

The root researcher and a separate child independently found the uniform
expanding-map proof. Another child independently derived the full
bounded-density proximal proof. Two child checks found no gap in the
determinant, trace, variation, or measurability steps before this note was
written. The
[completed-text review](../reviews/proximal-growth-tail-adversary.md)
also checked the finite rational-grid tail and solver substitutions,
finding no substantive gap. Its clarification of the product sharpness
example's centered uniform noise assumption is included above.
No executable optimization test, project-wide verification, or CI
inspection was used in this derivation.

A targeted inline Python document check passed trailing whitespace,
paired math delimiters, and local Markdown link targets. This formatting
check is separate from the analytic reviews.
