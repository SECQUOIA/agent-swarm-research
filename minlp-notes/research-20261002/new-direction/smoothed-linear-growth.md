# Independent linear perturbations give quantitative global quadratic growth

Date: 2026-10-02. Status: the continuous-noise, rational-box, mixed-box,
and polytope arguments passed a
[fresh independent review](../reviews/smoothed-linear-growth-adversary.md).
This note makes no literature-priority claim. Its claims concern the
perturbed objective, and its algorithmic conclusion is a high-probability
work bound, not an expected running-time bound.

## 1. Result and scope

Independent linear perturbations control global quadratic growth without
enumerating or separating all pairs of competing optimal faces. The
continuous-noise argument applies to every continuous objective on a
compact bounded feasible set. For quadratic objectives on rational boxes
or bounded rational polytopes,
a bound on the number of pieces of a scalar optimizer response also permits
polynomial-bit rational perturbations.

Let \(X\subseteq[-R,R]^n\), where \(R>0\), and let

\[
 F_c(x)=f(x)+c^Tx.
\]

For a rational box quadratic, independently perturb each linear
coefficient by a uniform element of

\[
 \mathcal G=\left\{-\sigma+\frac{2\sigma k}{M-1}:
                      k=0,\ldots,M-1\right\},
\tag{1}
\]

where \(\sigma>0\) is rational. For a continuous box put

\[
 F=3^n,\qquad B=(F+1)^2,
\tag{2}
\]

and choose a power of two \(M\) satisfying

\[
 M\ge \frac{8nB^2}{\rho},\qquad 0<\rho<1,
\tag{3}
\]

with rational \(\rho\) when the perturbation is sampled by an algorithm.

With probability at least \(1-\rho\), the perturbed problem has a unique
global optimizer \(x^*\), and

\[
 \boxed{F_c(x)-F_c(x^*)\ge
       \frac{\rho\sigma}{48n^2R}\|x-x^*\|_2^2
       \quad(x\in X).}
\tag{4}
\]

Only \(O(n+\log(n/\rho))\) random bits per coordinate are needed to
sample (1). Independent diagonal perturbations may also be present:
condition on them before applying the result. No Hessian eigenvalue
bound, supplied optimizer, or interaction-width assumption is needed for
(4).

The [pruned-coordinate-grid theorem](pruned-coordinate-grid.md) then
gives a high-probability polynomial work bound for the perturbed rational
problem at fixed supplied bag size, when \(R,L,\sigma^{-1},\rho^{-1}\)
are polynomially bounded numerically. Here \(L\) bounds upper coordinate
curvature. This does not give FPT in bag size alone, an expected polynomial
running time, or an exact solution of the original unperturbed objective.

## 2. A scalar response to a linear tilt

Assume throughout this section that \(X\) is nonempty and compact and
\(f\) is continuous. Fix every coefficient except coefficient \(i\),
and write the remaining coefficient as \(t\). Define

\[
 u(t)=\max\{x_i:x\in\operatorname{argmin}_{x\in X}F_t(x)\}.
\tag{5}
\]

Compactness makes this definition valid, including at ties. If \(s>t\),
the two optimality inequalities for arbitrary minimizers at \(s\) and
\(t\) show that their \(i\)-th coordinates satisfy
\(x_i(s)\le x_i(t)\). Consequently \(u\) is nonincreasing, takes
values in \([-R,R]\), and has total variation at most \(2R\).

Define the anchored maximal secant slope

\[
 A(t)=\sup_{s\ne t}\frac{|u(s)-u(t)|}{|s-t|}.
\tag{6}
\]

The word anchored means that every secant has one endpoint at the realized
coefficient \(t\). It is not a bound on slopes between all pairs of
other coefficients.

**Maximal-slope lemma.** For every \(K>0\),

\[
 \bigl|\{t:A(t)>K\}\bigr|\le\frac{12R}{K}.
\tag{7}
\]

Here and below vertical bars denote Lebesgue measure when applied to a
subset of the real line.

To prove this, let \(\mu\) be the variation measure of the monotone
function, with total mass at most \(2R\). Values at a discontinuity lie
between its two one-sided limits. Thus, for \(a<b\),

\[
 |u(a)-u(b)|\le\mu([a,b]).
\]

For a bad point \(t\), select a violating secant with length
\(r=|s-t|>0\). The centered closed interval of radius \(r\) contains
that secant and has mass greater than \(Kr\). Enlarge it slightly to
an open centered interval \(J\) while preserving

\[
 \mu(J)>(K/2)|J|.
\]

The strict secant inequality makes this enlargement possible. For a
compact subset of the bad set, these open intervals have a finite
subcover. Select intervals greedily in nonincreasing order of length,
discarding every interval intersecting an already selected interval.
The selected intervals are disjoint, and their triple dilations cover
the finite subcover. Hence the compact subset has measure at most

\[
 3\sum_J|J|<\frac6K\sum_J\mu(J)
 \le\frac{12R}{K}.
\]

Inner regularity proves (7). Using open disjoint intervals avoids counting
an atom twice at a shared endpoint. The bad set is measurable: for a
monotone function the supremum in (6) can equivalently be computed using
limits along rational \(s\).

## 3. Good responses imply a global growth bound

At the realized vector \(c\), suppose the responses in all coordinates,
with the other coefficients fixed at their realized values, satisfy

\[
 A_i(c_i)\le K.
\tag{8}
\]

First, the optimizer is unique. If two minimizers had coordinate values
\(a<b=u_i(c_i)\), every minimizer at coefficient \(c_i+h\), for
\(h>0\), would have coordinate at most \(a\), by the optimality
comparison above. Therefore

\[
 A_i(c_i)\ge(b-a)/h
\]

for every \(h>0\), contradicting (8). The coordinate values of all
minimizers are thus equal in every coordinate.

Let \(x^*\) denote the unique minimizer and fix arbitrary \(x\in X\).
For a coordinate \(i\), set

\[
 d=x_i-x_i^*,\qquad h=-d/(2K).
\]

The case \(d=0\) is immediate. Otherwise, take a minimizer \(y\) of
\(F_{c+h e_i}\) attaining the response in (5). Equation (8) gives

\[
 |y_i-x_i^*|\le K|h|.
\]

Optimality for the two objectives yields

\[
 \begin{aligned}
 F_c(x)+hx_i&\ge F_c(y)+hy_i\\
            &\ge F_c(x^*)+hy_i.
 \end{aligned}
\]

It follows that

\[
 F_c(x)-F_c(x^*)\ge h(y_i-x_i)
 \ge |h||d|-K|h|^2=\frac{d^2}{4K}.
\tag{9}
\]

Choose a coordinate with
\(d^2\ge\|x-x^*\|_2^2/n\). Then

\[
 F_c(x)-F_c(x^*)\ge\frac{1}{4nK}\|x-x^*\|_2^2.
\tag{10}
\]

This is a global inequality. No local curvature bound or assumption about
the winning face appears in its proof.

## 4. Continuous independent noise

Suppose the linear perturbations are independent and each has a density
bounded above by \(\phi\). Condition on all coefficients except one.
Equation (7) gives

\[
 \Pr\{A_i(c_i)>K\mid c_{-i}\}\le12R\phi/K.
\]

A union bound and (10), with \(K=12nR\phi/\rho\), prove the following
statement for every continuous \(f\) on compact
\(X\subseteq[-R,R]^n\): with probability at least \(1-\rho\), there
is a unique optimizer and a valid growth constant

\[
 g=\frac{\rho}{48n^2R\phi}.
\tag{11}
\]

In particular, uniform perturbations on \([-\sigma,\sigma]\) have
\(\phi=1/(2\sigma)\), giving

\[
 g=\frac{\rho\sigma}{24n^2R}.
\tag{12}
\]

Conditional response functions are measurable. For example, if
\(m(c)=\min_{x\in X}F_c(x)\), then \(m\) is continuous and concave,
and (5) is its left partial derivative. That derivative is a limit of
measurable difference quotients. The rational-secant description of (6)
then gives the joint measurability needed in the conditional probability
argument.

Continuous perturbations generally produce irrational input. Equation
(12) alone therefore does not establish an exact finite-bit solver
consequence. The next two sections supply the rational completion for
box quadratics.

## 5. Box quadratics have finitely many response pieces

Fix a quadratic Hessian and all linear coefficients except \(t=c_i\).
There are at most \(F=3^n\) faces of a continuous box, including its
vertices. Coordinates on a face are fixed at their lower endpoint, fixed
at their upper endpoint, or free.

**Candidate lemma.** At every \(t\), the maximum in (5) is attained by
a feasible stationary candidate on a face whose free principal Hessian
is positive definite. The empty free set is allowed.

Choose a minimizer maximizing coordinate \(i\), and consider the
smallest box face containing that point. The point lies in the relative
interior of this face, so its free gradient vanishes and its free Hessian
is positive semidefinite. If that Hessian is singular, a nonzero kernel
direction preserves objective along its feasible line segment. Such a
direction must have zero \(i\)-th component: otherwise one of its two
locally feasible signs would increase coordinate \(i\) at an optimal
point. Move to an endpoint of the segment. This preserves optimality and
coordinate maximality while reducing the face dimension. Repeating the
argument proves the lemma.

For each positive-definite free face, solve its free stationarity system.
The candidate vector is affine in \(t\), its feasibility domain is an
interval, possibly empty or a singleton, and its objective value is a
quadratic polynomial in \(t\). The global minimum is the lower envelope
of these feasible candidate values, by the candidate lemma.

There are at most two finite feasibility endpoints per candidate and at
most two intersections for each pair of distinct, nonidentical quadratic
value polynomials. Thus the real line has at most

\[
 2F+F(F-1)+1=F^2+F+1\le B=(F+1)^2
\tag{13}
\]

open intervals on which candidate feasibility and value ordering remain
fixed. If two candidates have identical value polynomials, their
\(i\)-th-coordinate functions are identical as well: differentiating
the stationary candidate value with respect to \(t\) gives precisely
that coordinate. Therefore \(u_i(t)\) is affine on each interval in
(13). Its values at intervening breakpoints lie between the one-sided
limits by monotonicity.

**Bad-set component lemma.** If a bounded monotone response has at most
\(B\) affine open pieces, then

\[
 E=\{t:A(t)>K\}
\]

has at most \(4B^2\) interval components, counting isolated points as
components.

For completeness, fix an open affine piece containing \(t\). On any
other affine piece, the secant quotient in (6), viewed as a function of
\(s\), is fractional linear with a derivative of constant sign. Its
supremum is attained as a one-sided endpoint limit. On the piece
containing \(t\), the quotient equals the magnitude of the local slope.
The unbounded exterior pieces are constant, since the response is
bounded; their limits at infinity contribute zero. Values at individual
breakpoints add nothing beyond the two one-sided response limits.

Consequently, for \(t\) in its fixed piece, membership in \(E\) is
determined by the local slope and comparisons with at most
\(2(B-1)\) one-sided breakpoint values. Each comparison is a strict
linear inequality in \(t\): the order of the breakpoint and \(t\) is
fixed, and monotonicity fixes the sign of the response difference.
These inequalities divide the piece into at most \(2B-1\) open
subintervals. Their strict union cannot create an isolated interior
point. Adding all original breakpoints, whether or not they belong to
\(E\), leaves fewer than \(4B^2\) components. This deliberately loose
bound suffices for sampling.

## 6. Rational perturbations and sampling bits

Use the grid (1), with spacing \(\eta=2\sigma/(M-1)\). A subset of the
real line of length \(\ell\) and at most \(C\) interval components
contains at most \(\ell/\eta+C\) points of any translated grid of
spacing \(\eta\). This includes singleton components.

Condition on all perturbations except coordinate \(i\). Equations (7)
and the component lemma imply

\[
 \begin{aligned}
 \Pr\{A_i(c_i)>K\mid c_{-i}\}
 &\le\frac{12R}{KM\eta}+\frac{4B^2}{M}\\
 &\le\frac{6R}{K\sigma}+\frac{4B^2}{M}.
 \end{aligned}
\tag{14}
\]

Set

\[
 K=\frac{12nR}{\rho\sigma}.
\tag{15}
\]

The first term in (14) is \(\rho/(2n)\); condition (3) bounds the
second term by the same quantity. A union bound and (10) prove (4).

Choose the smallest power of two satisfying (3). A uniform index
\(k\in\{0,\ldots,M-1\}\) then uses exactly \(\log_2M\) unbiased
random bits. Since

\[
 \log_2M=O(n+\log(n/\rho)),
\]

and \(\sigma\) is rational, each sampled coefficient has polynomial
bit length in the base input length and the binary descriptions of
\(\sigma\) and \(\rho\). The exponentially large grid is specified
implicitly; it is never enumerated. Adding unary linear or diagonal
terms does not enlarge the interaction graph.

## 7. Mixed boxes

The same rational argument extends to product boxes with continuous and
integer coordinates. Let \(n_c\) be the number of continuous coordinates,
and let \(N_j\) be the number of allowed values of integer coordinate
\(j\), after rounding endpoints inward and rejecting empty domains.
Replace (2) by

\[
 F=3^{n_c}\prod_{j\text{ integer}}N_j,\qquad B=(F+1)^2.
\tag{16}
\]

For each integer assignment, the candidate lemma and affine stationarity
argument apply to its continuous faces. Thus the full problem still has
at most \(F\) affine candidates, with interval feasibility domains and
quadratic scalar value functions. The proof of (13)--(15) is unchanged,
and the growth metric in (4) includes both coordinate types.

If the rational mixed box has input length \(I\), then

\[
 \log F=n_c\log3+\sum_j\log N_j
\]

is polynomial in \(I\). Consequently the random index and perturbed
coefficients still have polynomial bit length. This is a counting bound
for analysis; the solver need not enumerate all integer assignments or
all faces. Every linear coordinate, including each integer coordinate,
receives independent noise.

## 8. Consequence for the pruned-grid solver

Suppose a rational continuous or mixed box QP has a supplied tree
decomposition with maximum bag size \(p\). Let \(I'\) be the total
input length after sampling, and let \(L>0\) bound upper coordinate
curvature of the perturbed objective. On the event proved above,

\[
 \kappa=\max\{1,L/g\}
 \le\max\left\{1,\frac{48n^2RL}{\rho\sigma}\right\}
 =:\overline\kappa.
\tag{17}
\]

If all diagonal curvatures are nonpositive, endpoint dynamic programming
already solves the problem and this conditioning argument is unnecessary.
Linear perturbations leave \(L\) unchanged; if diagonal perturbations
are also used, a bound on their support supplies a corresponding bound
on \(L\).

The [existing theorem](pruned-coordinate-grid.md) returns an exact
rational optimizer and optimum. Its proof uses
\(O(\sqrt\kappa\log(n+2))\) coordinate states, a number of refinement
stages polynomial in the rational input length and requested accuracy
bits, and rational arithmetic of polynomial bit length in the input,
stage index, and state count. Exact reconstruction requires accuracy
bits polynomial in \(I'\), plus \(O(\log\kappa)\). The capped
conditioning trials have geometric state-count overhead. Therefore, for
each fixed \(p\), that proof gives a polynomial bound in
\(I'\) and \(\overline\kappa\) on work needed on the event (4).

In particular, if \(R,L,\sigma^{-1},\rho^{-1}\) are polynomially
bounded numerically in the base input size, the exact perturbed problem
is solved in polynomial work with probability at least \(1-\rho\),
for every fixed \(p\). Polynomial input bit length alone does not bound
these numerical magnitudes. On the unit box with polynomially bounded
Hessian coefficients, \(R=1\) and a polynomial numerical \(L\) suffice.

One can cap the solver at the resulting deterministic work bound and
return failure if that bound is exhausted. It then returns an exact
certified answer with probability at least \(1-\rho\); an accepted
answer remains valid outside the good-growth event because the solver's
certificate validity does not depend on its growth assumption.

The exponent of this polynomial can depend on fixed \(p\), through
the \(p\)-th power of the coordinate state count. Substituting the
polynomial-in-\(n\) bound (17) into a theorem parameterized by both
\(p\) and \(\kappa\) does not establish FPT in \(p\) alone.

Nor does the argument bound expected running time of an uncapped solver.
A bound with failure probability proportional to a growth threshold need
not control the expectation of work growing as a higher inverse power
of that threshold. The rational-grid residual term in (14) also requires
care in any expectation calculation. Finally, the exact answer is for
the sampled objective. No claim here recovers the exact optimizer of the
unperturbed objective.

## 9. Diagonal perturbations alone do not suffice

On \([-1,1]\), consider

\[
 F_d(x)=(-1+d)x^2+\varepsilon x,
 \qquad d\in[-1/2,1/2],\quad\varepsilon=2^{-m}>0.
\]

Every realization is strictly concave and has the unique global optimizer
\(x^*=-1\). Nevertheless,

\[
 F_d(1)-F_d(-1)=2\varepsilon,\qquad |1-(-1)|^2=4,
\]

so every valid global quadratic-growth constant obeys

\[
 g\le\varepsilon/2=2^{-m-1}.
\]

The base coefficients are bounded and their input length is \(O(m)\).
Arbitrary independent diagonal noise supported in the displayed interval
therefore leaves exponentially poor growth. The positive theorem requires
linear noise in every coordinate; diagonal noise can accompany it but
cannot replace it in general.

## 10. Coordinate ranges make the scaling explicit

The radius \(R\) need not charge an arbitrary translation of the feasible
set. Let

\[
 a_i=\min_{x\in X}x_i,\qquad b_i=\max_{x\in X}x_i,\qquad
 w_i=b_i-a_i,\qquad W=\max_i w_i.
\tag{18}
\]

Remove constant coordinates. If none remain, the feasible set is a
singleton and optimization is immediate. Otherwise \(W>0\). Translate
coordinate \(i\) by \((a_i+b_i)/2\). The translated set lies in
\([-W/2,W/2]^n\); linear perturbations change only by a random constant,
and objective gaps and Euclidean distances are unchanged. Thus the
rational-noise bound (4) becomes

\[
 \boxed{g_0=\frac{\rho\sigma}{24n^2W}.}
\tag{19}
\]

For continuous uniform noise the corresponding bound is
\(\rho\sigma/(12n^2W)\). The squared diameter of the bounding box is
\(\Delta^2=\sum_i w_i^2\), and the actual squared feasible-set diameter
is at most \(\Delta^2\), with \(W^2\le\Delta^2\le nW^2\).
These quantities record the numerical scaling; bounded binary encoding
does not make their numerical values polynomially bounded.

For integer domains the translation is only a proof device. The actual
solver keeps the original integer coordinates and their integrality
convention. The finite mixed-box count (16) is unchanged. Equation (19)
therefore replaces the factor \(48n^2R\) in (17) by \(24n^2W\)
without altering the integer model.

## 11. Bounded rational polytopes

Let \(X=\{x:Cx\le d\}\) be a nonempty bounded rational polytope,
with \(m\) supplied inequalities. It may have lower dimension. Its
coordinate ranges (18) can be computed by rational linear programming.
The continuous-noise proof already applies to this compact set. For a
quadratic objective, the rational-noise argument also applies after
replacing (2) by

\[
 F=2^m,\qquad B=(F+1)^2.
\tag{20}
\]

Here \(F\) bounds the number of nonempty faces: each face is determined
by its set of tight input inequalities. This count is only for analysis;
no faces are enumerated by the perturbation sampler or optimization
algorithm.

To prove the analogue of the candidate lemma, choose a global optimizer
maximizing coordinate \(i\), and take the smallest face containing it.
Its gradient vanishes on the face's tangent space and its Hessian
restricted to that space is positive semidefinite. If a tangent null
direction changed coordinate \(i\), one locally feasible sign would
increase it while preserving the quadratic objective, a contradiction.
Every such null direction therefore preserves coordinate \(i\). Move
along one until reaching the boundary of the face. Boundedness ensures
an endpoint exists. The objective and coordinate maximum are preserved,
and the face dimension decreases. Eventually the restricted Hessian is
positive definite, or the face is a vertex.

For each face with positive-definite tangent Hessian, choose an affine
parameterization \(x=x_0+Zy\) of its affine hull. The stationarity
system in \(y\) has a unique solution affine in the scalar tilt \(t\).
Membership in the face imposes linear inequalities in \(t\), so its
feasibility set is an interval. Its objective value is quadratic in \(t\),
and the derivative of that value is its \(i\)-th coordinate, because
the candidate is tangent-stationary. Vertices supply the zero-dimensional
candidates. This proves exactly the same response-piece and bad-component
bounds as Sections 5--6, with (20).

This null-direction argument is also the geometric step behind the
[minimal-face rational-height proof](negative-inertia-qp.md). Here it is
used to count scalar response pieces, not to find or enumerate the active
face. The counting argument is independent of constraint qualification,
strict complementarity, or a nonempty ambient interior.

Choose the rational noise grid (1) with \(M\) a power of two satisfying
(3), using (20). Then

\[
 \log_2 M=O(m+\log(n/\rho)),
\]

so sampling and the perturbed coefficient encoding remain polynomial in
the input length. With probability at least \(1-\rho\), the perturbed
polytope QP has a unique optimizer and the global growth bound (19).

Let \(k\) be the negative inertia and
\(\nu=\max\{0,-\lambda_{\min}(A)\}\) for its Hessian \(A\).
Linear perturbations change neither. Applying the
[negative-inertia theorem](negative-inertia-qp.md) gives the high-probability
parameter bound

\[
 \max\{1,\nu/g\}\le
 \max\left\{1,\frac{24n^2W\nu}{\rho\sigma}\right\}.
\tag{21}
\]

For fixed \(k\), the theorem's displayed packing counts and exact
convex-QP bit bounds are polynomial in the right side of (21) and in
the perturbed input length. Thus, if
\(W,\nu,\sigma^{-1},\rho^{-1}\) are numerically polynomially bounded,
the perturbed continuous QP is solved exactly in polynomial work with
probability at least \(1-\rho\). Large positive curvature contributes
to input length and preprocessing precision rather than to (21).

As in Section 8, this is a high-probability statement, not an expected-work
bound. It solves the sampled objective. The theorem remains a continuous
polytope-QP result; this section does not provide a polynomial-time
mixed-integer convex recourse oracle for general coupled constraints.

## 12. Verification and source comparison

The proof uses scalar monotonicity, an elementary interval covering
argument, and finite active-face algebra. It does not apply affine
finite-family isolation directly to continuous face values, and it does
not union-bound small eigenvalues over principal submatrices. Quadratic
face values and exponentially many faces enter only the discretization
component bound; their logarithmic count controls sampling bits.

This note was derived from targeted reads of the existing theorems and
their significance and hardness reviews. The
[fresh mathematical review](../reviews/smoothed-linear-growth-adversary.md)
found no substantive gap in the compact-set, rational-box, and mixed-box
proofs. The root researcher independently derived the response-slope
argument and then read the complete compact-set, rational-box, and
mixed-box proofs, finding no substantive gap. The independent reviewer
also checked the coordinate-range scaling, polytope candidate count, and
fixed-negative-inertia consequence without finding a gap. These are
analytic reviews, not computational checks.

The [separate literature audit](../prior-art/smoothed-linear-growth-prior.md)
documents qualitative generic quadratic-growth results and discrete
isolation results. It does not establish publication priority for the
quantitative bound here. No external search by the proof authors,
executable optimization test, project-wide verification, or CI inspection
was used to establish this derivation.

The targeted document command `python3 - <<'PY'` checked trailing
whitespace, paired inline/displayed math delimiters, and local Markdown
link targets in this note and the significance assessment. It passed.
This formatting check is separate from the analytic proof reviews.
