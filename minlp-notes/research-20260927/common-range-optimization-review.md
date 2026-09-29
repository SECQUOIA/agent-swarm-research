# Adversarial review of an objective excluded from the common range

Date: 2026-09-28. Scope: the proposed extension of
[common-range-fpt-frontier.md](common-range-fpt-frontier.md) to an arbitrary
rational PSD quadratic objective, without including its Hessian in the
constraint common range. This reviewer independently reconstructed the
projection argument before seeing an extension manuscript. The reviewer
then supplied the singular-KKT argument and the unbounded-fiber repair
below. Consequently this is an independent investigation of the proposal,
but not an independent review of those subsequently adopted repairs.

**Finding.** The proposed boxed residual-gap lemma is valid. A high-rank
PSD objective can be retained exactly while the native constraints are
approximated. Eliminating the remaining continuous directions gives a
finite union of basic closed sets defined by polynomials of degree at most
four. Singular KKT matrices cause no additional nonlinear variables.
The resulting bit bound is exponential only in the dimension of the
retained nonlinear coordinates, with an absolute exponent on input size.
An unboxed radius argument also needs the recession case in Section 4;
active-set minimizer charts alone omit feasible thresholds with an
unbounded fiber objective. No full unbounded mixed-integer optimization
theorem or novelty claim is certified by this review.

## 1. The projection problem

After splitting off the common kernel of the native constraint Hessians,
write their fiber, including affine rows and any supplied box, as

\[
 P(a)=\{v:Cv\le d(a)\}.
\]

Here \(a\) contains the retained nonlinear coordinates and, when needed,
a residual-epigraph variable. The matrix \(C\) is constant and rational;
each entry of \(d\) has degree at most two. An arbitrary quadratic
objective has the form

\[
 q(a,v)=\tfrac12v^TQv+b(a)^Tv+c(a),\qquad Q\succeq0,
\]

where \(b\) is affine and \(c\) is quadratic. It is enough for the
boxed argument that \(Q\succeq0\). Global positive semidefiniteness is
used later for the uniform recession case and by the final convex
quadratic mixed-integer oracle.

For a supplied rational threshold \(\theta\), consider

\[
 \{a:\exists v\in P(a),\ q(a,v)\le\theta\}.       \tag{1}
\]

If every nonempty fiber is compact, its objective has a minimizer.
Polyhedral KKT conditions hold at that minimizer without Slater,
independence of active rows, positive definiteness, or strict
complementarity.

## 2. Singular KKT systems still give quartic charts

For an active set \(I\), the stationarity and active equations are

\[
 \begin{bmatrix}Q&C_I^T\\ C_I&0\end{bmatrix}
 \binom v\lambda
 =\binom{-b(a)}{d_I(a)}.                            \tag{2}
\]

The matrix in (2) is constant. Rational row reduction gives polynomial
consistency equations, one particular solution \((v_0(a),\lambda_0(a))\)
of degree at most two on their zero set, and a constant rational basis
of the solution kernel. No parameter-dependent denominator is introduced.

Let \((\Delta v,\Delta\lambda)\) lie in that kernel. Then

\[
 Q\Delta v+C_I^T\Delta\lambda=0,
 \qquad C_I\Delta v=0.
\]

Multiplying the first equation by \(\Delta v^T\) gives
\(\Delta v^TQ\Delta v=0\), and positive semidefiniteness implies
\(Q\Delta v=0\). The stationarity equation for \(v_0\) now gives

\[
 q(a,v_0+\Delta v)-q(a,v_0)
 =(Qv_0+b(a))^T\Delta v+
        \tfrac12\Delta v^TQ\Delta v=0.             \tag{3}
\]

Thus the objective is constant across all solutions of (2), even when
the chosen particular solution is infeasible. Set

\[
                 \phi_I(a)=q(a,v_0(a)).
\]

This polynomial has degree at most four. The remaining requirements
\(Cv\le d(a)\) and \(\lambda\ge0\) are linear in the free kernel
coordinates, with constant rational coefficients and polynomial right
sides of degree at most two. Farkas elimination gives an exact basic
closed description in \(a\). Append \(\phi_I(a)\le\theta\).
Taking the union over \(I\) gives exactly (1).

Necessity follows from a fiber minimizer and its KKT multipliers.
Conversely, a parameter in a chart has a feasible solution to (2), by
the Farkas conditions; (3) proves its actual objective is \(\phi_I\).
In particular, no possibly infeasible particular solution is returned as
a feasible point.

All matrices have polynomial dimension. Rational minors and row reduction
give polynomial coefficient bit lengths. There are at most exponentially
many active sets, and each eliminated linear system has at most
exponentially many extreme-ray supports. Therefore each chart has

\[
 \deg\le4,\qquad \text{coefficient bits}\le(B+1)N^C,
 \qquad\log(\text{row count}+1)\le N^C,             \tag{4}
\]

for an absolute \(C\), where \(B\) bounds appended box and threshold
bits. Denominators are cleared separately within each row. The
exponential chart family is only used to prove bounds; an FPT algorithm
must not enumerate it.

The quartic degree is real: the native constraint \(v\ge u^2\) has
common range dimension one, while minimizing the PSD objective \(v^2\)
over its fiber gives the value \(u^4\). Also, singular stationarity alone
does not identify a feasible particular solution: for \(v_2\ge1\) and
objective \(v_1^2\), both \((0,0)\) and \((0,1)\) are stationary, but
only the latter is feasible. The free-coordinate feasibility conditions
cannot be omitted.

## 3. The boxed residual gap

Fix a finite rational box and retain the objective cut
\(q\le\theta\) exactly. If its intersection with the box is empty,
there is no candidate point and no residual minimum needs to be defined.
Otherwise let \(\alpha\) be the minimum of the maximum of zero and all
native residuals over this compact intersection.

Introduce a residual variable \(s\) with \(0\le s\le U\), where a
direct coefficient bound supplies finite rational \(U\). The projected
epigraph \(E\) in \((u,s)\) is compact and has minimum \(s=\alpha\).
Section 2 describes it as a finite union of basic closed sets \(E_I\)
with degree at most four. Each \(E_I\) is a closed subset of \(E\),
and hence compact.

If the original threshold system is infeasible, \(\alpha>0\). Each
nonempty set

\[
 H_I=\{(u,s,y):(u,s)\in E_I,\ sy=1,\ y\ge0\}
\]

is compact. Applying the containing-radius theorem, not the
meeting-radius theorem, to each such chart bounds every reciprocal
coordinate. In particular it bounds the chart containing an \(s=\alpha\)
point. For fixed degree four and dimension \(r+2\),
[Basu--Roy, Theorem 3](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf)
and (4) give

\[
        \log_2(1/\alpha)\le 2^{O(r)}(B+1)N^C.        \tag{5}
\]

No radius theorem for an arbitrary Boolean union is needed. Its use
chart by chart also avoids an incorrect assertion that a basic closed
description of the entire union has already been produced.

This proves the precision required for the proposed algorithm: build
rational outer approximations of the native convex quadratic or SOC
rows with residual error strictly below the uniform bound in (5), keep
the objective cut exact, and solve the resulting polyhedron plus one
PSD quadratic inequality. Any accepted integer assignment has an
original feasible point satisfying the same objective threshold. The
particular approximate continuous point need not be that point.

[Del Pia, Proposition 4, version 2](https://arxiv.org/html/2311.00099v2#S4.SS2)
supplies precisely the last feasibility oracle, FPT in the number of
integer variables. The reviewer inspected its statement and its
polyhedron-plus-one-PSD-quadratic model directly. The objective can have
arbitrary rank. This use of that result must be credited; the proposed
addition is the uniform native-residual precision bound, not a new
one-quadratic algorithm.

## 4. A necessary unboxed repair

Without a box, a feasible objective threshold need not have a fiber
minimizer. For example, \(v\ge0\), \(q(v)=-v\) admits every finite
threshold but has no KKT minimum. Active-set minimizer charts would miss
the whole projection.

For a globally PSD objective, this omission has a simple repair. Write
\(Q\) for its \(vv\) block and \(a_v\) for its constant linear part.
If \(Qd=0\), global positive semidefiniteness implies that the full
objective Hessian annihilates \((0,d)\). In particular all mixed
quadratic terms with retained parameters vanish on \(d\). The
existence of a descent direction is therefore the constant rational
linear feasibility question

\[
                 Cd\le0,\quad Qd=0,\quad a_v^Td\le-1.       \tag{6}
\]

If (6) is feasible, every nonempty fiber permits every threshold. Use
ordinary Farkas projection for the native fiber. Its small feasible
point, a small rational direction from (6), and a sufficiently large
positive multiple of that direction give a threshold-feasible point
with the required coefficient-sensitive radius bound.

If (6) is infeasible, every nonempty fiber has a finite attained
quadratic minimum, and Section 2 applies. Here is a proof valid even
for irrational parameter values. Split \(v=Ry+Tw\), with the columns
of \(T\) spanning \(\ker Q\); the quadratic form on \(y\) is
positive definite. The coefficient of \(w\) is the constant
\(a_T=T^Ta_v\). For a fixed \(y\), minimizing over \(w\) is an LP
with matrix \(C_T=CT\). Absence of (6) implies dual feasibility
\(\lambda\ge0\), \(C_T^T\lambda=-a_T\). Its value, on its
closed polyhedral feasible \(y\)-domain, is the maximum of finitely
many affine functions of \(y\). Adding the positive definite
\(y\)-quadratic is coercive, since one dual feasible vector already
provides an affine lower bound. The minimum in \(y\) is attained;
the finite \(w\)-LP optimum is attained as well. This is also a
special case of the classical quadratic-programming attainment and
recession results.

The dichotomy agrees with
[Del Pia, Proposition 5](https://arxiv.org/html/2311.00099v2#S4.SS3),
whose recession characterization was inspected. The direct argument
above explains why fixing a possibly irrational parameter does not
require invoking an algorithm stated only for rational input.

For the finite-minimum case, the meeting-radius theorem can now be
applied to any nonempty quartic chart. A bounded-norm solution of the
remaining constant-matrix linear fiber supplies bounded \(v\) and
multipliers. Equation (3) preserves the objective cut. Together these
give an unboxed threshold witness radius with the same
\(2^{O(r)}N^C\) bit form. Any unbounded-integer extension still has
to apply the integer-witness theorem to the full convex projection;
this review does not replace that separate argument.

## 5. Finite values and attainment: the quantifier-elimination audit

The author subsequently proposed continuous exact value recovery and
attainment classification. The reviewer inspected the coefficient claims
in these local primary-source texts:

- Basu--Pollack--Roy (1996), Section 1.3, Theorem 1.3.1, journal pages
  1004--1005, in
  [the local text](../papers/pooling/revision-20260909/checks/whole-review4/basu1996-on-the-combinatorial-and-algebraic.txt).
- Basu (2014), Theorem 2.27, in
  [the author's survey](../research-20260925/publication-sources/basu-2014-author-survey.txt).

The first explicitly makes output degree independent of the number of
input polynomials. The second additionally bounds the bit lengths of
intermediate and output integers by the input coefficient bit bound
times a function of degree and quantifier-block dimensions, independently
of the polynomial count. For a single existential block of \(r\)
variables, degree four, and one free value variable, both output degree
and coefficient bit length have bounds of the form

\[
                  D\le f(r),\qquad H\le f(r)N^C.              \tag{7}
\]

The number of predicates can be exponential; this affects the runtime
and number of QE outputs but not (7). The proof only invokes existence
of this description. It does not run quantifier elimination on the
exponential chart family.

Applying the result to the quartic epigraph description gives (7) for
any finite infimum \(\theta\), whether attained or not. Indeed the
threshold set is \([\theta,\infty)\) or \((\theta,\infty)\).
At its finite boundary at least one nonzero, nonconstant output
polynomial vanishes: otherwise all signs, and hence membership, would
be locally constant. Factoring an integer annihilator into the minimal
polynomial preserves an FPT coefficient bound by standard factor-height
bounds.

This justifies the proposed value algorithm. A uniform root bound
\(|\theta|\le M\) distinguishes a finite infimum from minus infinity
by a threshold query below \(-M\). Bisection with the rational
threshold oracle gives approximations even if equality with an
unattained infimum returns infeasible. Algebraic reconstruction from
the degree and coefficient bounds then recovers the exact value.

For attainment, let \(p_\theta\) be the recovered minimal polynomial,
and choose a closed rational isolating interval containing no other
root. In an active-set chart append

\[
       p_\theta(t)=0,\qquad a\le t\le b,
       \qquad\phi_I(u)\le t.
\]

If a global optimizer exists, some such chart is nonempty. The
meeting-radius theorem bounds a point in \((u,t)\); the constant-matrix
linear lifting argument bounds its corresponding original variables.
The resulting box has bit length \(f(r)N^C\), and contains an
optimizer whenever one exists. The radius call has degree \(f(r)\)
in dimension \(r+1\), so its parameter dependence need not remain
\(2^{O(r)}\); a generic computable \(f\) is the safe stated bound.

If that box is infeasible, the finite infimum is unattained. Otherwise
its boxed minimum \(\beta\) exists, and
\(\beta=\theta\) holds exactly when the original infimum is attained.
An alternative is to enlarge the conditional optimizer box by an
independent feasible-point radius, which ensures that the boxed minimum
is defined whenever the original problem is feasible. The same
finite-value reconstruction applies to the boxed problem.

The bounded-integer extension uses the same argument fiber by fiber.
There are finitely many integer assignments. A finite global infimum
therefore equals the infimum of one fiber, so (7) remains a uniform
single-fiber bound; no compositum or product over the number of
assignments is needed. A uniform conditional optimizer radius similarly
reduces global attainment to equality with the boxed optimum. Once the
continuous box has been supplied, its compactness permits interval
bisection of the original integer coordinates using boxed optimum
equality to recover an optimal assignment whenever one exists.

These arguments establish the proposed value and attainment extensions
at the proof level. They do not establish an FPT algorithm for exact
continuous optimizer output. Recovering a few retained coordinates and
then solving a convex quadratic program over their algebraic number
field would need a justified complexity bound for that last operation.
An assertion that a short algebraic optimizer exists is not by itself
such an algorithm. The unbounded-integer finite-value problem is also
outside this audit.

## 6. Verification and limits

The targeted command

```text
python research-20260927/check_common_range_objective_review.py
```

passed two exact examples and 166 rational KKT systems, including 159
kernel vectors. The calculations check the quartic example, the
infeasible-particular-solution example, and the identity (3) for singular
and nonsingular systems. They do not prove the radius theorem, bit
bounds, global algorithm, or novelty. No project-wide verification or
CI inspection was performed.

The key limitations remain explicit:

- The objective cut is retained exactly. Approximating it using the
  native common-range bound would silently reintroduce its high-rank
  Hessian.
- The projection proof establishes existence and bounds. Enumerating its
  exponentially many charts is not an FPT construction.
- Fixed parameter values, bounded integer variables, and unbounded
  integer variables require the distinctions in the feasibility note;
  a common kernel of continuous Hessian blocks alone does not remove
  arbitrary integer-continuous cross terms.
- Threshold decision does not by itself prove finite optimal-value
  bounds, attainment classification, or full exact optimizer recovery
  for an unbounded mixed-integer problem.
- No systematic new prior-art search for parametric quadratic
  programming was conducted in this proof review. The KKT and
  piecewise-polynomial mechanisms are classical; a novelty claim must
  concern a precise resulting complexity theorem and survive a separate
  literature comparison.
