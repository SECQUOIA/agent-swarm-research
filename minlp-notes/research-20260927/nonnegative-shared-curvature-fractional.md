# Shared quadratic curvature with nonnegative scenario weights

Date: 2026-09-28. Status: complete proof. A separate
[structural and field audit](nonnegative-curvature-field-audit.md)
and a [fresh review of the exact QP subroutine](number-field-psd-qp-fresh-review.md)
found no unresolved gap; the integrating author read both reviews
and independently reconstructed the complete QP proof. No novelty
claim is made.

The [positive-weight theorem](common-range-shared-curvature-fractional.md)
extends to affine scenarios with zero curvature weight.
Its previous choice of the minimum-norm original optimizer does not
extend. A different fiber selector does: minimize the lifted quadratic
residual when it has a finite minimum, and otherwise follow one fixed
negative recession direction from a selected polyhedral point.

This note keeps the previously proved positive-weight theorem unchanged.
It records the additional arguments needed for nonnegative weights.

## Model and conclusion

Retain the rational closed native PSD/SOC feasible set \(F\) and the
cross-aware native kernel \(K_*\) from the
[single quadratic numerator theorem](common-range-quadratic-fractional.md).
Write \(w=(z,x)\), where \(z\in\mathbb Z^k\), and set
\(\rho=\operatorname{codim}K_*\). The domain and the integer variables
may be unbounded. Every native quadratic Hessian is full PSD; native
SOC constraints retain their affine sign conditions.

Let \(Q\succeq0\) be rational, put
\(B(w)=\tfrac12w^{\mathsf T}Qw\), and consider
\[
 \inf_{(z,x)\in F,\ z\in\mathbb Z^k}
 \Psi(w),\qquad
 \Psi(w)=\max_{1\le j\le m}
 \frac{\lambda_j B(w)+a_j^{\mathsf T}w+c_j}{d_j(w)}.
 \tag{1}
\]
Here \(m\ge1\), every \(\lambda_j\ge0\) is rational, and the
rational affine denominator \(d_j\) is strictly positive on all real
points of \(F\). Some or all weights may be zero. The matrix \(Q\)
has arbitrary rank and is excluded from \(\rho\).

Let \(\ell\) be the rank of the denominator gradients restricted to
\(K_*\), and choose a rational decomposition
\[
 K'=K_*\cap\bigcap_j\ker d_{j,x}^{\mathsf T},\qquad
 x=T_1u+T_0v,\qquad r=\dim u\le\rho+\ell .
 \tag{2}
\]
Every denominator depends only on \((z,u)\). Let \(N\) be the total
explicit input bit length.

**Theorem.** There is an exact optimization algorithm using
\(f(k,\rho,\ell)N^C\) bit operations, with an absolute exponent \(C\):
infeasibility, unboundedness below, exact finite algebraic value,
attainment, and one exact optimizer when attained. The value and the
selected optimizer have parameter-only algebraic degree and
\(f(k,\rho,\ell)N^C\) representation length. This conclusion does
not bound the field of every optimizer or of the minimum-norm original
optimizer. The new selector is defined below.

The structural assertions through the field and box argument below
have direct proofs. The algorithm additionally uses the separately
proved and reviewed number-field QP procedure specified in the
recovery section.

## A rational threshold still uses one PSD quadratic row

At a rational threshold \(t\), introduce one scalar \(\eta\) and write
\[
 \begin{split}
 w&\in F,\qquad z\in\mathbb Z^k,\\
 \lambda_j\eta+a_j^{\mathsf T}w+c_j&\le t\,d_j(w)
                                      \quad(1\le j\le m),\\
 B(w)-\eta&\le0 .
 \end{split}
 \tag{3}
\]
This is equivalent to \(\Psi(w)\le t\). In one direction set
\(\eta=B(w)\); in the other use \(\lambda_j\ge0\).
At fixed rational \(t\), all new rows except the last are affine,
and the last has full PSD Hessian \(\operatorname{diag}(Q,0)\).
The existing one-PSD-cut algorithm therefore remains applicable.
No positive-weight division or additional scenario-dependent nonlinear
coordinate is required.

After (2), the native rows are \(Cv\le b(z,u)\), with constant
rational \(C\) and degree-two \(b\). All affine rows in (3) have
the form
\[
 \widehat C y\le \widehat b(z,u,t),\qquad
 y=(v,\eta),
 \tag{4}
\]
where \(\widehat C\) is constant rational and \(\widehat b\) has
degree at most two. Define
\[
 \Phi(z,u,y)=B(z,T_1u+T_0v)-\eta .
 \tag{5}
\]
Its Hessian in \(y\) is constant rational and PSD.

Unlike the positive-weight case, a native feasible fiber need not
give a nonempty polyhedron (4): the zero-weight scenarios impose
threshold inequalities independently of \(\eta\). Every argument
below tests nonemptiness of (4) itself.

## The common negative-ray test has a different meaning

Write \(Q_{vv}\) for the eliminated block of the transformed
quadratic matrix. Consider the rational linear system
\[
 Ch\le0,\qquad Q_{vv}h=0,\qquad
 a_{j,v}^{\mathsf T}h+\lambda_j\le0\quad(1\le j\le m).
 \tag{6}
\]
It tests whether \(d=(h,1)\) is a negative recession direction
for the objective \(\Phi\) on every nonempty polyhedron (4).
The test is independent of \((z,u,t)\).

To prove this, a direction \((h,\sigma)\) with zero quadratic
curvature satisfies \(Q_{vv}h=0\). Full positive semidefiniteness
of \(Q\) implies that all cross blocks also kill \(h\), so
\[
 \Phi(z,u,y+s(h,\sigma))=\Phi(z,u,y)-s\sigma .
 \tag{7}
\]
A negative direction has \(\sigma>0\). Dividing by \(\sigma\)
gives (6), and its affine recession conditions are exactly those
of (4). The standard recession criterion for convex quadratic
programming over a polyhedron therefore gives two exhaustive cases:
if (6) is infeasible, every nonempty fiber of (4) has a finite
attained \(\Phi\)-minimum; if (6) is feasible, every such fiber has
\(\Phi\)-infimum \(-\infty\).

Feasibility of (6) does not imply that (1) is unbounded below.
Along its ray, a positive-weight scenario decreases, while a
zero-weight scenario may remain constant. For example,
\(\inf_v\max\{-v,0\}=0\), despite the common negative lifted
direction \((h,\sigma)=(1,1)\).

## Closed polynomial descriptions in both cases

First suppose (6) is infeasible. The
[constant-matrix QP chart lemma](common-range-optimizer-witness.md#2-constant-matrix-quadratic-programming-charts)
gives finitely many rational polynomial maps
\[
 y_I(z,u,t),\qquad \deg y_I\le2,
 \tag{8}
\]
such that the least-norm \(\Phi\)-minimizer in every nonempty
fiber equals one of them. Their coefficients have polynomial
bit length. Singular Hessians and singular KKT matrices are allowed.
Define
\[
 \begin{split}
 D_I&=\{(z,u,t):\widehat C y_I\le\widehat b(z,u,t)\},\\
 q_I(z,u,t)&=\Phi(z,u,y_I(z,u,t)).
 \end{split}
 \tag{9}
\]
The atoms in \(D_I\) have degree at most two, and \(q_I\) has
degree at most four. Existence of a feasible lift of (3) is exactly
\[
 (z,u,t)\in
 \bigcup_I \bigl(D_I\cap\{q_I\le0\}\bigr).
 \tag{10}
\]
Every retained chart point is a feasible lift. Conversely, a feasible
lift implies that the attained fiber minimum is at most zero.
No multiplier-sign or KKT-consistency guard is needed for the first
implication.

Now suppose (6) is feasible. Choose one rational solution \(h\) of
polynomial bit length and fix \(d=(h,1)\). On each nonempty
polyhedron (4), first select its unique minimum-norm point \(y_0\).
Applying the same chart lemma to the positive definite norm objective
gives degree-two rational maps \(y_I^0(z,u,t)\) covering this
selection. Put
\[
 D_I^0=\{\widehat C y_I^0\le\widehat b\},\qquad
 q_I^0=\Phi(z,u,y_I^0).
 \tag{11}
\]
Then the projection of (3) is precisely
\[
                    \bigcup_I D_I^0 .
 \tag{12}
\]
Indeed, every feasible point of (4) can be shifted along \(d\)
until (5) is nonpositive. For explicit charts of a feasible lift, use
\[
 Y_I(z,u,t)=
 \begin{cases}
 y_I^0(z,u,t),&q_I^0\le0,\\
 y_I^0(z,u,t)+q_I^0(z,u,t)d,&q_I^0\ge0 .
 \end{cases}
 \tag{13}
\]
Both domains are closed, both formulas agree at \(q_I^0=0\),
and both points satisfy (3). The output maps have degree at most
four and introduce no field extension. The formula
\(y_0+\max\{\Phi(y_0),0\}d\), using the unique selected \(y_0\),
defines one canonical lift. Arbitrary feasible charts are used only
for the existence and encoding bounds.

In particular, for every fixed \(z,t\), the projected feasible set
in \(u\) is closed: it is a finite union of the closed sets in
(10) or (12). It is convex because it is a projection of the
convex threshold set in (3). No general closed-projection theorem
is being assumed.

The all-zero-weight case is included. Then \(h=0\), with
\(\sigma=1\), always satisfies the lifted recession test, and the
same argument reduces threshold feasibility to the linear scenarios.

## Values, an attained selector, and a uniform box

Eliminating only \(u\) from (10) or (12) describes the projected
epigraph in \((z,t)\) with individual coefficient heights
\(f(k,r)N^C\) and degrees \(f(k,r)\). The logarithm of the number
of charts is polynomial in \(N\); the charts are not enumerated
by the algorithm. The coefficient-sensitive quantifier-elimination
bounds are the same ones used in the positive-weight theorem.

Each weak threshold set of (1) is convex because its inequalities
have Hessians \(\lambda_jQ\succeq0\), and each strict sublevel
is a nested union of weak threshold sets. Thus the
[quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md)
applies. It gives a parameter-only degree and height bound for a
finite mixed-integer infimum \(\theta\), and a conditional bound on
an attaining integer vector. Rational threshold calls then distinguish
unboundedness from finite value and recover the latter as before.
The negative-ray test alone is not used for this classification.

Fix an integer vector attaining the global value \(\theta\). Its
nonempty projected optimal set in \(u\) is closed and convex, so
it has a unique minimum-norm point \(u_*\). In the case without
a negative ray, select the least-norm \(\Phi\)-minimizer in
the fiber (4) over \((z,u_*,\theta)\). Its value is at most zero,
so its original \(v\)-coordinate gives an optimizer of (1).
The \(\Phi\)-minimum need not equal zero.

In the negative-ray case, use the canonical shifted polyhedral
selection from (13). It too gives an original optimizer. Neither
selection is claimed to minimize the norm of all original optimizers.

Choose a chart representing the selected point. In the first case,
\(u_*\) is the unique minimum-norm point on that chart's closed
quartic domain in (10). In the second case it is the unique
minimum-norm point on the corresponding closed quadratic domain
in (12). These domains are contained in the full projected optimal
set and contain \(u_*\). The same small-dimensional singleton
formula used in the
[single-numerator field review](common-range-quadratic-fractional-field-review.md#3-a-direct-bound-using-classical-quantifier-elimination)
therefore bounds one joint field
\[
 K=\mathbb Q(\theta,u_*)
 \tag{14}
\]
by degree \(f(k,r)\) and representation length \(f(k,r)N^C\).
The chart outputs (8) or (13) have coordinates in \(K\).
This is a joint field bound, without multiplying separate coordinate
degree bounds over the ambient dimension.

Uniform substitution of every integer vector in the conditional
attaining box gives a uniform rational box containing the specified
optimizer in every attaining fiber. The auxiliary \(\eta\) can be
discarded from that box for original-variable recovery. These bounds
use one chart at a time and do not enumerate the integer assignments
or the active sets.

## Exact recovery using rational QPs and one number field

The rational one-PSD-cut oracle and finite-value recovery already
give the same compact optimal-set oracle as in the positive-weight
theorem. Intersect with the uniform integer and continuous boxes.
The boxed value equals \(\theta\) exactly when the original
infimum is attained. Integer bisection preserving that equality
selects an attaining assignment.

After fixing it, rational affine cuts in \(u\) and a rational
bound on \(\|u\|^2\) preserve compactness. Equality of the resulting
value with \(\theta\) tests intersection with the original optimal
set. Norm and coordinate bisection approximate the same unique
point \(u_*\). The norm row only adds curvature in the retained
directions, so the structural parameters remain bounded by
\((k,r)\). Exact recognition recovers (14) from these rational
queries, as in the previous theorem.

There is no longer a common quadratic gradient on the original
optimal set. Instead substitute the exact \((z,u_*,\theta)\)
into the polyhedron (4). Its matrix and the Hessian of \(\Phi\)
are rational; its right-hand side and the linear objective
coefficients belong to the one explicitly represented real field
\(K\).

The [exact number-field QP theorem](number-field-psd-qp-review.md)
supplies the following subroutine:

> Given rational \(C\), rational \(H\succeq0\), and \(b,c\) in one real number
> field \(K\), find the minimum-norm optimizer of
> \(\tfrac12y^{\mathsf T}Hy+c^{\mathsf T}y\) over \(Cy\le b\),
> when the feasible set is nonempty and the infimum is finite,
> in polynomial time in the total dense common-field input length,
> including the field degree and the number of coordinates.

In the case without a negative ray, apply this to \(\Phi\).
In the ray case, apply it to the positive definite norm objective
to find \(y_0\), then use (13) with an exact sign test in \(K\).
The existential chart lemma proves that both QP selectors lie in
\(K\) with polynomial representation length. The algorithm does
not enumerate their active sets. It solves rational QPs with outward
rounding of the affine data and a small positive norm penalty.
Two computable Hoffman bounds control approximation of the same
least-norm QP optimizer at every requested precision. The first repairs
the rounded feasible point. The second uses the original QP's
polyhedral optimal set, with matrix consisting of its constraint
matrix, Hessian, and linear-objective row.

Although that last row is algebraic, field norms give polynomial-bit
bounds for every nonzero minor, and hence for a sufficient Hoffman
constant. Exact recognition of the tuple containing the known field
generator and the selected point then recovers all coordinates in
one field. Rational basis inversion returns them in the original
input power basis. These steps are detailed in the supporting proof
and independently checked in its fresh review.

The one-field QP input here has length \(f(k,r)N^C\), including its
field representation. Polynomial time in that full length preserves
the required FPT form. Exact substitution verifies the selected
optimizer against the native constraints and every original ratio
at the independently recovered value \(\theta\).

## Boundary examples and scope

For
\[
 \min_v\max\{(v-2)^2,2\}=2,
 \tag{15}
\]
the minimum-norm original optimizer is \(2-\sqrt2\).
This does not belong to the field of the rational value when the
retained dimension is zero. With \(B(v)=v^2\), the lifted
inequality is \(\eta-4v+4\le2\), while the zero-weight row is
simply \(2\le2\). Minimizing
\(\Phi(v,\eta)=v^2-\eta\) on this polyhedron gives
\((v,\eta)=(2,6)\), with minimum \(-2\). Its original
coordinate is rational and optimal. This verifies that the new
selection addresses the previous boundary example and that
\(\Phi=0\), \(\eta=B\), and a common original gradient cannot
be assumed.

An explicit negative-ray example with a necessary shift is
\[
 s=1,\qquad \min_{s,v}\max\{s^2-v,0\}=0 .
 \tag{16}
\]
At threshold zero, the lifted polyhedron has \(s=1\) and
\(\eta-v\le0\). Its minimum-norm \((s,v,\eta)\) point is
\((1,0,0)\), whose residual is one. The direction
\((0,1,1)\) shifts it to \((1,1,1)\), a feasible optimal lift.
The zero-weight scenario prevents the objective from tending
to \(-\infty\).

The threshold reformulation and parametric QP tools are established
methods. The prior comparisons in the
[positive-weight theorem](common-range-shared-curvature-fractional.md#7-positive-domains-boundaries-and-significance)
still apply: generalized fractional programming is classical, and
prior work allows much more general quadratic numerators for different
purposes. This extension concerns the exact parameterized conclusion
and the revised selector. No priority or practical speedup claim is
made.

Explicit positive domains are included by the same
[shared reciprocal lift](common-range-positive-domain-review.md)
used in the positive-weight theorem. Introduce one common scalar
\(s\) and the cones
\(\|(2,d_j-s)\|\le d_j+s\). Their projections enforce exactly
\(d_j>0\), preserve all objective values and attainment, and raise
the native codimension by at most \(\ell+1\). The added coordinate
has zero objective curvature. This argument does not require
\(\lambda_j>0\), so it applies unchanged to (1).

The extension lets affine scenarios, including objective floors,
coexist with the common quadratic scenario cost without increasing
the curvature parameter. Its practical value still requires an
implementation and an assessment of the exact-arithmetic overhead.
The proof establishes a complexity bound, not a solver speedup.

The structural reviewer checked the boundary examples and ray
identities by exact symbolic computation. The supporting QP author
checked its scalar precision inequalities symbolically; its fresh
reviewer independently reconstructed the proof without repeating
those tests. The root investigator separately read the integrated
structural argument, and the integrating author read the complete
QP proof and its fresh review. No numerical SDP or QP experiment,
Lean proof, project-wide verification, or CI inspection is asserted.

Targeted document verification run after integration: an inline Python
check passed for this note, the rational-nullvector caution, the fresh
moment review, and both number-field QP notes. It checked 19 local links
across those five files, paired math delimiters, final newlines, trailing
whitespace, and control characters. The scoped command below also
completed without output; the Python check supplies content coverage
for newly created files that Git does not yet track.

    git diff --check -- research-20260927/nonnegative-shared-curvature-fractional.md research-20260927/rational-nullvector-compression-caution.md research-20260927/strict-hessian-moment-arithmetic-fresh-review.md research-20260927/number-field-psd-qp-review.md research-20260927/number-field-psd-qp-fresh-review.md
