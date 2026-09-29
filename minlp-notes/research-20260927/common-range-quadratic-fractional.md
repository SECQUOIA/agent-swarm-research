# A PSD quadratic numerator outside the common-range parameter

Date: 2026-09-28. Status: complete proof, with fresh independent
[value](common-range-quadratic-fractional-value-review.md),
[field](common-range-quadratic-fractional-field-review.md), and
[optimizer](common-range-quadratic-fractional-algorithm-review.md)
reviews. The author independently checked the combined value and output
arguments. The proof uses the reviewed
[one-PSD-cut threshold theorem](common-range-optimization.md) and the
[quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md).
Novelty is not established.

A single convex quadratic numerator can have arbitrary rank without
enlarging the structural parameter that controls the native constraints.
For an affine positive denominator, its rational thresholds still add
only one convex quadratic inequality. The finite-value bound comes from
minimizing the numerator in the linear fibers, leaving quartic formulas
in a bounded number of retained coordinates.

## 1. Problem and value theorem

Let \(F\subseteq\mathbb R^k\times\mathbb R^n\) be defined by
rational native SOC constraints, quadratic inequalities with full
positive-semidefinite Hessians, or their intersection, together with
rational affine rows. All cone right-hand-side signs are retained.
The integer coordinates are \(z\in\mathbb Z^k\), and no variable
boxes are supplied. Minimize

\[
 \frac{P(z,x)}{d(z,x)},\qquad
 P(w)=\tfrac12w^TQ_0w+a_0^Tw+c_0,\quad Q_0\succeq0,       \tag{1}
\]

where \(w=(z,x)\), all data are rational, and \(d\) is affine
and strictly positive on the entire real set \(F\). Neither \(P\)
nor its gradient is required to be positive. Section 5 treats a domain
explicitly restricted by \(d>0\) instead of this promise.

For the native quadratic rows and squared SOC residuals, let \(H_i\)
be their full Hessians and put

\[
 K_*=\{v\in\mathbb R^n:H_i(0,v)=0\text{ for every }i\},
 \qquad \rho=\operatorname{codim}K_* .                    \tag{2}
\]

The objective Hessian \(Q_0\) is excluded from this definition.
The total explicit binary input length \(N\ge2\) includes \(Q_0\).
For an all-PSD native constraint model, \(\rho\) equals the common
range dimension of the continuous constraint Hessians. Indefinite squared
SOC Hessians require the cross-aware definition (2).

**Optimization theorem.** There are a computable function \(f\) and absolute
constant \(C\) such that feasibility, unboundedness below, and a finite
exact infimum can be distinguished in \(f(k,\rho)N^C\) bit operations.
A finite infimum \(\theta\) has degree at most \(f(k,\rho)\)
and primitive minimal-polynomial coefficient bit length at most
\(f(k,\rho)N^C\). The algorithm returns that polynomial and a
rational isolator. If the infimum is attained, some attaining integer
vector has bit length at most \(f(k,\rho)N^C\).
The algorithm also decides whether the finite infimum is attained.
If it is, the algorithm returns an optimal integer vector and one exact
continuous optimizer in a common real algebraic field, with total output
length and running time \(f(k,\rho)N^C\).

The numerator rank is unrestricted. This statement does not follow by
adding \(Q_0\) to the native Hessian family and applying an existing
common-range theorem; that would change its parameter. Sections 2--5
establish the value and integer-size bounds; Section 6 composes them
with the separate canonical-witness proof.

## 2. A constant-matrix fiber problem

Retain the denominator direction by setting

\[
 K'=K_*\cap\ker d_x^T,\qquad
 x=T_1u+T_0v,\qquad \operatorname{range}T_0=K',\qquad
 r=\dim u\le\rho+1.                                      \tag{3}
\]

Rational linear algebra gives this invertible coordinate change and its
inverse with polynomial bit length. In these coordinates all native
rows become

\[
                    Cv\le b(z,u),                        \tag{4}
\]

with constant rational \(C\) and quadratic rational \(b\).
The full-kernel condition excludes every quadratic product involving
\(v\), including products with \(z\). The denominator becomes
\(d_0(z,u)\), independent of \(v\).

Writing \(a=(z,u)\) only as a parameter tuple, the numerator has the form

\[
 P(a,v)=\tfrac12v^TQv+\ell(a)^Tv+c(a),                    \tag{5}
\]

where \(Q\succeq0\) is constant rational, \(\ell\) is affine,
and \(c\) is quadratic. Its whole Hessian in \((a,v)\) is PSD.

There is a useful preliminary dichotomy. Let \(a_v\) denote the
constant linear coefficient of \(v\). If the rational system

\[
               Ch\le0,\qquad Qh=0,\qquad a_v^Th<0         \tag{6}
\]

has a solution, every nonempty fiber has numerator infimum \(-\infty\).
Indeed PSD of the full numerator Hessian implies that a direction in
\(\ker Q\), padded by zero in the retained coordinates, is annihilated
by all numerator cross blocks. Along any feasible ray \(v+\lambda h\),

\[
 P(a,v+\lambda h)=P(a,v)+\lambda a_v^Th.
\]

The denominator is constant and positive along that fiber, so its ratio
also tends to \(-\infty\). After mixed-integer feasibility is checked,
this case can be classified immediately. System (6) is tested by the
rational LP with \(a_v^Th\le-1\), using homogeneity.

If (6) has no solution, every nonempty fiber QP has a finite attained
minimum, even at irrational parameter values. This is the
[unboxed-fiber lemma](common-range-optimization.md#unboxed-fibers):
split off \(\ker Q\); its remaining optimization is an LP with a
parameter-independent feasible dual, while the positive-definite
complement gives a coercive lower bound. The projected feasible
complement is closed by constant-matrix Farkas elimination. Hence the
complement and then the kernel LP attain their minima. This reasoning
does not import a rational-input theorem at an irrational right-hand side.

Absence of (6) does not prove the whole fractional problem bounded below.
Unboundedness can still occur as \((z,u)\) varies; Section 4 classifies it.
Conversely, numerator recession alone would not classify a ratio before
retaining its denominator direction. On \(v\ge0\), the numerator
\(-v\) is unbounded below, but \(-v/(v+1)\) has infimum \(-1\).
The use of (6) is valid because the denominator is constant along its
eliminated fiber.

## 3. Quartic charts for the exact ratio epigraph

Assume now that (6) has no solution. The
[reviewed QP chart lemma](common-range-optimization.md#2-a-parametric-convex-qp-projection)
gives finitely many rational polynomial maps \(v_I(z,u)\) of degree
at most two, indexed by linearly independent row subsets of \(C\),
including the empty subset. More explicitly,

\[
 \binom{v_I(a)}{\lambda_I(a)}
 =
 \begin{bmatrix}Q&C_I^T\\ C_I&0\end{bmatrix}^{+}
                       \binom{-\ell(a)}{b_I(a)}.          \tag{7}
\]

The Moore--Penrose inverse of each constant rational matrix is rational
with polynomial coefficient bit length. Define

\[
 D_I=\{a:Cv_I(a)\le b(a)\},\qquad G_I(a)=P(a,v_I(a)).
                                                                  \tag{8}
\]

The atoms defining \(D_I\) have degree at most two; \(G_I\)
has degree at most four. Every chart point is genuinely feasible.
Conversely, each nonempty fiber's minimum-norm numerator minimizer
belongs to at least one chart: use a basis of all row normals active
at that minimizer in the normal-cone and minimum-norm argument.
Singular KKT matrices and zero multipliers are allowed. The charts do
not need multiplier-sign or stationarity-consistency guards, because
feasibility and the actual objective value of their printed point are
tested directly.

The ratio epigraph projected onto \((z,t)\) is therefore exactly

\[
 E=\left\{(z,t):
     \exists u\ \bigvee_I
       \bigl[(z,u)\in D_I\ \wedge\
                    G_I(z,u)\le t\,d_0(z,u)\bigr]\right\}. \tag{9}
\]

For the forward inclusion, a threshold-feasible fiber has a numerator
minimizer with no larger numerator and the same positive denominator.
For the reverse inclusion, \(v_I\) supplies a feasible original
point satisfying the ratio threshold. There is no division by a
possibly vanishing parameter polynomial. Positivity of the denominator
is inherited from feasibility in the original \(F\).

Each atom in (9) has degree at most four and coefficient bit length
at most \(N^{C_0}\), for an absolute \(C_0\). The chart count
may be exponential, but its logarithm is polynomial in \(N\).
No common denominator is cleared across the complete chart family.
The family is used only to prove bounds and is never enumerated by
the final algorithm.

Eliminating only the \(r\) coordinates \(u\) gives a quantifier-free
description of \(E\) with individual atom bounds

\[
                d_E\le f_1(k,r),\qquad
                H_E\le f_2(k,r)N^{C_1},                  \tag{10}
\]

independent of the number of resulting atoms. A fixed weak slice
\(E_t\) is convex: before projection it is
\(F\cap\{P-td\le0\}\), an intersection of convex sets since
\(P-td\) has the same PSD Hessian as \(P\). This remains true
for negative \(t\) and negative numerator values. Strict slices
are nested unions of these convex weak slices and hence convex.

Apply the coefficient-sensitive quasiconvex mixed-value theorem to (10).
Its bound is linear in the incoming coefficient bit length, so

\[
 \deg\theta\le f_3(k,r),\qquad
 \operatorname{bit}(\operatorname{minpoly}\theta)
                                      \le f_4(k,r)N^{C_2} \tag{11}
\]

for every finite mixed-integer infimum, with absolute \(C_2\).
Convexity of the weak optimal slice also supplies the conditional small
attaining integer vector. This proves all encoding claims.

## 4. FPT exact classification and value recovery

For a rational threshold \(t\), the required exact question is

\[
               (z,x)\in F,\qquad z\in\mathbb Z^k,\qquad
                         P(z,x)-t\,d(z,x)\le0.             \tag{12}
\]

The last row is a single rational convex quadratic inequality. Its
Hessian is always \(Q_0\), regardless of \(t\). Apply the
one-PSD-cut threshold theorem with this row as the distinguished
objective threshold. The native range parameter remains \(\rho\).
All numerator, denominator, and rational-threshold coefficients are
included in that oracle's input length. Mixed PSD/SOC native rows can
also be converted to SOC rows by the rational LDL construction in
[the affine-fractional note](common-range-fractional-frontier.md#4-exact-value-recovery);
that reduction preserves \(\rho\) exactly and leaves the PSD
numerator padded with zero auxiliary directions.

First test native mixed-integer feasibility. If feasible and (6) holds,
return \(-\infty\). Otherwise (11) supplies an effective magnitude
bound \(M\) for every possible finite infimum. A feasible rational
threshold at \(-M-1\) is now equivalent to infimum \(-\infty\).
If that threshold is infeasible, the infimum is finite and lies in
\([-M,M]\). Bisection with (12) and algebraic recognition recover it.
At equality with an unattained infimum a weak threshold can be infeasible;
this does not affect the shrinking interval or recognition argument.

The threshold bit lengths, number of calls, and recognition precision
are \(f(k,\rho)N^C\). The threshold oracle has an absolute
polynomial input exponent, so composition preserves this FPT form.
The implicit chart description is not supplied to a general
quantifier-elimination algorithm during recovery.

## 5. An explicitly positive denominator domain

The same value theorem holds on \(F\cap\{d>0\}\) when positivity
does not hold on all of \(F\). Add one continuous \(s\) and the
rational cone

\[
                        \|(2,d-s)\|\le d+s.                \tag{13}
\]

As checked in the [positive-domain review](common-range-positive-domain-review.md),
this closed lift projects exactly onto \(F\cap\{d>0\}\), preserves
the objective values and attainment, and gives native cross-aware range
at most \(\rho+2\). The numerator is independent of \(s\),
so its augmented Hessian remains PSD and is still excluded from the
native parameter. Its denominator is positive throughout the closed
lift. Applying Sections 1--4 there proves the claim with the same
parameter family.

## 6. Attainment and exact continuous output

The conditional small integer vector does not itself decide attainment.
The separately reviewed
[quadratic-fractional witness proof](common-range-quadratic-fractional-witness.md)
supplies the remaining bounds and algorithm. Fix a global rational split
(3). After fixing an integer assignment with an attained optimal value
\(\theta\), the continuous optimal set is closed and convex. Its
projection onto \(u\) is

\[
 U_\theta=\bigcup_I
     \{u:(z,u)\in D_I,\ G_I(z,u)\le\theta d_0(z,u)\}.       \tag{14}
\]

This finite union of closed sets proves closedness of that projection,
which cannot be inferred from convexity alone. Select the unique
minimum-norm \(u_*\in U_\theta\), then the minimum-norm optimal
\(v_*\) in its fiber. Since the denominator is constant in the
fiber, \(v_*\) is its minimum-norm numerator minimizer and equals
one chart value \(v_{I_*}(z,u_*)\).

The point \(u_*\) is the unique norm minimizer on that one chart
set in (14). Describe this property using \(\theta\)'s minimal
polynomial and isolator and quantify over at most \(O(r)\) retained
coordinates. Coefficient-sensitive quantifier elimination bounds each
coordinate's degree and height. Multiplying degrees over only \(r\)
coordinates gives a common-field degree \(f(r,\deg\theta)\);
the bit height is \(f(r,\deg\theta)(N+H)^C\), where \(H\)
bounds \(\theta\)'s representation and \(C\) is absolute.
The chart map adds no field extension for \(v_*\). These bounds
give a uniform rational box containing that specified point for every
attaining integer assignment in the conditional integer box.

Intersect both boxes with the original model. The resulting
mixed-integer set is compact, so its ratio minimum is attained whenever
it is nonempty. Its exact value equals \(\theta\) if and only if
the original infimum is attained. The forward implication uses the
small attaining integer vector and its canonical point; the reverse
uses compactness. Integer interval bisection preserving boxed value
\(\theta\) then selects an actual optimal integer vector.

For its continuous fiber, compact rational cuts have value \(\theta\)
exactly when they meet the optimal set. Norm and coordinate cuts in
\(u\) therefore approximate the same canonical \(u_*\) at every
precision, without increasing the native range beyond \(\rho+1\).
To recover \(v_*\), write the fixed-fiber numerator as
\(P(x)=\tfrac12x^TQx+a^Tx+c\). Its raw gradient \(g=Qx+a\)
is constant over that continuous optimal set. Indeed, the midpoint
identity for \(P-\theta d\) and PSD imply \(Q(x-y)=0\)
for any two optimal \(x,y\). Rational affine cuts on coordinates of
\(Qx+a\) approximate this one gradient using the same compact
value oracle.

Choose a rational right inverse on \(\operatorname{range}Q\) and
set \(Qx_0=g-a\). Within the native fiber over \(u_*\), optimality
is equivalent to

\[
 Qx=g-a,\qquad
 a^Tx=\theta d_0(z,u_*)-c-\tfrac12x_0^TQx_0.              \tag{15}
\]

Both row matrices are rational; the algebraic quantities occur only
on the right. Rational outward rounding, minimum-norm QPs, and a
rational-matrix Hoffman bound approximate \(v_*\). The gradient and
all fiber coordinates lie in the same field as \((\theta,u_*)\).
Common-field recognition returns exact output, which is checked against
the original native constraints, cone signs, denominator sign, and
objective equality. The linked witness proof gives the full precision
and runtime accounting, all with an absolute input exponent.

One distinction from the affine-numerator proof matters. The minimum-norm
point in an arbitrary quadratic sublevel need not lie in the coefficient
field, even when the retained dimension is zero. For example,
\((v-2)^2\le2\) has minimum-norm point \(2-\sqrt2\), although
the numerator minimizer is the rational point \(2\). Thus a numerator-
minimizer chart cannot be used to encode every arbitrary nonempty
threshold fiber. At the actual global optimal ratio, any feasible
optimal point must minimize its numerator within its fixed denominator
fiber; that is the additional fact available for the intended output
proof. The algorithm uses only actual globally optimal fibers when
forming its uniform canonical box; it does not apply the stronger false
claim to arbitrary sublevels.

## 7. Significance, prior, and verification limits

The possible solver capability is exact classification, algebraic
values, and exact optimizers for unbounded mixed-integer fractional models whose native
nonlinearity occupies a small common range, even with a full-rank
quadratic cost. The proof supplies a worst-case parameterized algorithm;
it supplies no practical runtime estimate or implemented speedup.
The functions of the structural parameters can be large.

This is a composition of reviewed QP charts, the one-PSD-cut oracle,
and the quantitative quasiconvex mixed-value theorem. It does not claim
novelty for fractional threshold reformulation or quadratic programming.
The [focused prior audit](common-range-quadratic-fractional-prior.md)
identified a strong classical base case.
[Chandrasekaran--Tamir (1984), *Optimization problems with algebraic
solutions: Quadratic fractional programs and ratio games*](https://www.math.tau.ac.il/~atamir/opt_84.pdf)
already compute exact algebraic infima and decide attainment for continuous
quadratic fractional programs on possibly unbounded rational polyhedra.
Their stated model has a nonnegative convex quadratic numerator and a
positive concave quadratic denominator; affine denominators are included.
Printed page 334 removes their initial attainment assumption, and page
338 explains minimal-polynomial output. These continuous base-case
capabilities are not new here.

Del Pia's existing one-PSD-row algorithm supplies the polyhedral
rational-threshold oracle with fixed integer dimension. The proposed
addition is its composition with controlled mixed-integer fractional
value heights, native nonlinear constraints parameterized by \(\rho\),
and a bounded canonical common-field optimizer. The audit found no
equivalent full mixed-integer theorem in the sources inspected; this
does not establish novelty. The elementary example
\(\min_{x\ge1}(x^2+2)/x=2\sqrt2\) illustrates why rational
polyhedral data do not justify assuming rational fractional values.

The independent value reviewer also used a fresh focused review of the
recession and singular-chart arguments. Its targeted
`check_quadratic_fractional_value.py` passed exact symbolic
checks of denominator recession, the cross-aware kernel, singular and
inconsistent charts, quartic substitution, and an irrational optimum
with a rank-nine excluded numerator. The separate field and algorithm
reviews reconstruct the canonical-point and recovery arguments.

An author-run inline `python -` command independently checked
a quartic chart with a joint PSD numerator and an integer cross term,
the irrational polyhedral example, the denominator-recession boundary,
and the nonoptimal-sublevel field counterexample. All assertions passed.
The author read the 1984 source's model, nonattainment, and
minimal-polynomial passages in locally extracted text after the browser's
PDF screenshots timed out. These finite symbolic and source checks do
not establish the universal complexity theorem or publication priority.
The final targeted document command checked this note and the two affine
fractional notes: three documents, 32 local links, whitespace, control
characters, and paired math delimiters all passed. No project-wide
verification, CI inspection, or Lean verification is asserted.
