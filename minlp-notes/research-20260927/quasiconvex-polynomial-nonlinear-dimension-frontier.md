# Quasiconvex polynomial optimization with few nonlinear directions

Date: 2026-09-28. Status: complete proof with a
[fresh full adversarial review](quasiconvex-polynomial-nonlinear-dimension-review.md)
that found no remaining substantive gap, conditional on the separately
reviewed dependencies. The projection, oracle, and affine-direction
arguments also have separate independent reviews. Novelty is not established.

## 1. Result and its scope

Consider the rational polynomial model

\[
 \min g_0(z,u,v),\qquad g_i(z,u,v)\le0\ (1\le i\le m),
 \quad z\in\mathbb Z^k,\ u\in\mathbb R^r,\ v\in\mathbb R^n,
 \qquad g_i=C_i v+p_i(z,u).                         \tag{1}
\]

Every native polynomial, including the objective, is globally quasiconvex:
each of its real weak sublevels is convex. The constant row vectors
\(C_i\) and all coefficients are rational, and \(\deg p_i\le d\).
The monomials and rational coefficients are explicitly encoded in total
length \(N\ge2\). Global quasiconvexity is a promise on the input, not
something the algorithm recognizes. Put \(D=\max(2,d)\).

**Theorem.** There is a deterministic algorithm with bit cost
\(f(k,r,d)N^C\), where \(C\) is absolute, that reports infeasibility,
unboundedness below, or an attained finite optimum. In the finite case it
returns the exact algebraic value and a complete optimizer. Their common
number-field degree is at most \(g(r,d)\), and their coefficient and
output bit lengths are at most \(f(k,r,d)N^C\). Input bounds, a Slater
condition, and a rational continuous optimizer are unnecessary.
If \(r=0\), the value and continuous optimizer can be rational.

This extension replaces the global convexity assumptions of
[polynomial feasibility](polynomial-nonlinear-dimension-frontier.md) and
[full polynomial optimization](polynomial-nonlinear-dimension-optimization.md).
It preserves their constant-matrix linear extension. The proof below
identifies every place where convexity was used and supplies the needed
replacement. It does not assert that an arbitrary polynomial description
of a convex feasible set has this complexity.

Qualitative finite attainment is old: Bank--Mandel's 1987 Theorems 3(iii)
and 7(ii) imply it for rational globally quasiconvex polynomial rows and
objective, in arbitrary mixed dimension. The primary statement and its
application are recorded in the
[attainment prior audit](mixed-integer-attainment-prior.md). The proposed
addition is the exact parameterized arithmetic and algorithmic conclusion.

## 2. Which quasiconvex rows survive a linear projection

**Lemma 1.** If \(c\ne0\) and the set
\(\{(y,v):c^Tv+p(y)\le0\}\) is convex, then \(p\) is convex.

Choose \(a\) with \(c^Ta=1\) and restrict to \(v=ta\). The
resulting set \(\{(y,t):t\le-p(y)\}\) is the hypograph of
\(-p\). Its convexity says exactly that \(p\) is convex. This
argument requires neither polynomiality nor the other sublevels.

Consequently every row of (1) with \(C_i\ne0\) is actually convex.
Only rows independent of all eliminated variables may be merely quasiconvex.

Let \(C\) collect the eliminated-variable coefficients for a feasibility
system and define

\[
 \Lambda=\{\lambda\ge0:C^T\lambda=0,\ \mathbf1^T\lambda=1\}.
                                                               \tag{2}
\]

**Lemma 2.** A vertex of \(\Lambda\) is either a unit vector
\(e_i\) with \(C_i=0\), or has support only on rows with
\(C_i\ne0\).

If \(C_i=0\), then \(e_i\in\Lambda\). Whenever
\(0<\lambda_i<1\),

\[
 \lambda=\lambda_i e_i+(1-\lambda_i)
             \frac{\lambda-\lambda_i e_i}{1-\lambda_i}
\]

is a nontrivial convex decomposition in \(\Lambda\). If
\(\lambda_i=1\), the vector is \(e_i\).

Farkas' lemma now describes the weak projection by the finite family
\(\lambda^Tp(y)\le0\), for vertices of (2). Each projected
polynomial is either a native zero-\(C_i\) quasiconvex row or a
nonnegative combination of convex rows. Thus every member of the family
is globally quasiconvex. Its degree, individual coefficient bit bound,
and logarithmic row-count bound are exactly those in the convex note.
The projection is basic closed and convex.

For strict relaxed rows, the same assertion holds after subtracting a
common rational \(\epsilon\) from native right-hand sides and appending
strict rational boxes. An exact membership oracle can first test the
zero-\(C_i\) rows directly, and then solve the rational phase-I LP for
the remaining rows. Opposite \(v\)-box rows make that LP finite. If
\(n=0\), all rows were tested directly, so return membership without
forming an empty phase-I problem. A
basic optimal dual solution either certifies strict membership or supplies
one violated projected convex polynomial. Equivalently, a dual vertex for
the whole family yields the classification in Lemma 2. The returned row
comes from one fixed finite family; its coefficient bits depend on the
constant rational matrix and original row coefficients, not on the query
point. Clear its denominators by a positive multiplier.

Vertex selection, or the direct treatment of zero rows, matters. An
arbitrary optimal dual multiplier can mix a quasiconvex nonconvex row
with a convex row and return a nonquasiconvex polynomial. The
[projection review](quasiconvex-polynomial-projection-review.md) gives
the exact example \(F(y)=y^3/2+y^2/4\) and checks this failure at
a dual optimum. The oracle never relies on quasiconvexity of arbitrary
nonnegative sums.

## 3. A rational shallow-cut oracle for quasiconvex rows

This section replaces only the convex-gradient construction in the
[implicit integer oracle audit](polynomial-nonlinear-dimension-oracle-audit.md).
The global quasiconvex version of this construction is established prior
art in Hildebrand--Koppe, Sections 5.2--5.3. The details below use rational
LDL coordinates and explicit line samples to make the interface and bit
bounds transparent.

Let \(Y\subset\mathbb R^s\) be defined by a fixed finite family of
strict inequalities \(F_j(x)<0\). The \(F_j\) are globally
quasiconvex integer polynomials of degree at most \(D\), with individual
coefficient bits at most \(H\). The family may be implicit. At a rational
query, an oracle decides membership and, on failure, returns one such
polynomial with \(F_j(x)\ge0\). Suppose the current containing
ellipsoid is

\[
 E(A,c)=\{x:(x-c)^TA^{-1}(x-c)\le1\},\qquad A\succ0,
                                                               \tag{3}
\]

with rational data. All cuts below are valid for the closure of \(Y\).

### 3.1 A constant-line fact

If a globally quasiconvex polynomial \(F\) is constant on a complete
line \(a+\mathbb Rb\), it is invariant in direction \(b\) everywhere.
Indeed, for any \(x\), the closed convex sublevel at
\(\alpha=\max(F(x),F(a))\) contains \(x\) and the complete line.
Taking limits of convex combinations shows that it contains
\(x+\mathbb Rb\). Thus \(t\mapsto F(x+tb)\) is bounded above
on the whole real line. A nonconstant univariate quasiconvex polynomial
cannot be bounded above: an odd degree or a positive even leading
coefficient is unbounded above, and a negative even leading coefficient
violates quasiconvexity between sufficiently distant endpoints.
The restriction is therefore constant. This proves the assertion.

It follows that if \(F(c+tb_i)\) is constant for every vector in a
basis \(b_1,\ldots,b_s\), then \(F\) itself is constant. This is
the constant-line part of Hildebrand--Koppe Lemma 5.2 and Corollary 5.3,
proved here to specify the exact hypothesis needed by the oracle.

### 3.2 Test points and rounding

Compute rational \(A=L\operatorname{diag}(a_i)L^T\), where all
\(a_i>0\). Choose positive dyadic numbers \(t_i\) with
\(\sqrt{a_i}/2\le t_i\le\sqrt{a_i}\), by comparing rational
squares. Set \(b_i=t_iLe_i\). These vectors are orthogonal in the
\(A^{-1}\) inner product, with lengths in \([1/2,1]\).
Query the \(2s\) points

\[
                     y_i^\pm=c\pm\frac{b_i}{2(s+1)}.      \tag{4}
\]

If all are in \(Y\), their convex hull lies in \(Y\) and contains
\(E(A/\beta^2,c)\) for \(\beta=4s(s+1)\). To check the last
inclusion, transform by \(A^{-1/2}\): the cross-polytope's orthogonal
half-axes have lengths at least \(1/[4(s+1)]\), so it contains the
Euclidean ball of radius \(1/[4\sqrt{s}(s+1)]\), which is at least
\(1/\beta\). No square root is needed by the algorithm.

Otherwise keep one returned polynomial \(F\) and its violated point
\(y\) fixed during the rest of this call.

### 3.3 Find a nearby violation with nonzero gradient

If \(F(c)<0\), let \(q(t)=F(c+t(y-c))\). Since
\(q(0)<0\) and \(q(1)\ge0\), quasiconvexity implies
\(q(t)\ge0\) for every \(t>1\). Otherwise the strict sublevel
would contain both endpoints surrounding \(y\). The polynomial is
nonconstant. Among the \(D\) distinct rational numbers

\[
                         t_j=1+\frac{j}{D+1},\quad 1\le j\le D,
                                                               \tag{5}
\]

one satisfies \(q'(t_j)\ne0\). At
\(w=c+t_j(y-c)\), we have \(F(w)\ge0\),
\(\nabla F(w)\ne0\), and
\(\|w-c\|_{A^{-1}}<1/(s+1)\).

If \(F(c)\ge0\), inspect the univariate restrictions
\(q_i(t)=F(c+tb_i)\). If all are constant, Section 3.1 proves
that \(F\) is a nonnegative constant and \(Y\) is empty.
Otherwise choose one nonconstant restriction. Evaluate it at the
\(D\) positive and \(D\) negative rational numbers

\[
                  t_j^\pm=\pm\frac{j}{(D+1)(s+1)}.
                                                               \tag{6}
\]

At least one whole side of this finite sample has \(q_i\ge0\):
a negative value on each side would put \(c\) in the convex strict
sublevel. On that side, at least one sample has \(q_i'\ne0\),
since a nonzero polynomial of degree at most \(D-1\) has fewer than
\(D\) roots. Its point \(w\) has the same three properties as
above. All computations are exact rational evaluations or coefficient
tests. The constant case is also handled by direct coefficient inspection.

For any \(x\in Y\), differentiable quasiconvexity gives
\(\nabla F(w)^T(x-w)\le0\). This follows by differentiating
the restriction on the segment from \(w\) toward \(x\), whose values
are at most \(F(w)\). Thus \(g=\nabla F(w)\ne0\) gives

\[
             g^Tx\le g^Tc+\frac{\sqrt{g^TAg}}{s+1}.       \tag{7}
\]

This is the required shallow cut. The algorithm returns its rational
normal \(g\); it does not need to represent the square root in (7).

### 3.4 Bit bounds and integer recursion

Rational LDL, the dyadic square comparisons, the samples (4)--(6),
restriction coefficients, and gradient evaluations use bit lengths at most
\(f(s,D)(H+H_E+1)\), where \(H_E\) bounds the ellipsoid data.
The dependence on these varying lengths is linear: determinant bits,
fixed-degree substitutions, and coefficient sums have this property.
The time cost is a fixed polynomial in the input and query lengths,
multiplied by \(f(s,D)\) and the membership-oracle cost. It is
independent of the number of implicit rows.

The rest of the reviewed integer recursion needs only these properties:
strict integer-polynomial margins, a containing ball, the rational
shallow-cut oracle, and closure under integer affine restrictions.
Quasiconvexity is preserved under affine substitution. The uniform
strict-margin volume bound uses coefficient and derivative bounds, not
convexity of the polynomials. The rational ellipsoid rounding, quadratic
lattice subroutines, correct maps \(a^TU=e_s^T\), refreshed bounding
balls, and linear bit recurrence are those already proved in the
[oracle audit, Section 3.3](polynomial-nonlinear-dimension-oracle-audit.md#33-recursion-and-the-absolute-input-exponent).
They therefore yield the same deterministic implicit-family integer
feasibility theorem for globally quasiconvex rows.

In particular, the convex shortcut declaring emptiness when a violated
row has zero gradient is not used. For \(F(x)=x^3\), the point
\(0\) violates \(F<0\) and has zero derivative, although all
negative points are feasible. Construction (6) instead selects a positive
point and returns the correct cut.

## 4. Exact feasibility transfers

The radius, positive-gap, and grid arguments in the convex feasibility
note transfer with the following precise changes.

1. Lemmas 1--2 supply quasiconvex Farkas rows with the same individual
   degree and height bounds. Their intersection and projection onto the
   integer coordinates are convex. Khachiyan--Porkolab's integer witness
   bound therefore still supplies a short integer box.
2. Basu--Roy's meeting and containing radius bounds are semialgebraic
   statements; they do not require globally convex row polynomials.
   The compact residual epigraph used for the positive infeasibility gap
   may fail to be convex here, but the containing-radius argument still
   applies exactly as stated. The reciprocal graph remains compact when
   the positive gap is assumed.
3. Polynomial gradient bounds on a fixed box give the same mesh size and
   rounding guarantee. Relaxing the native right-hand sides preserves
   their quasiconvexity, and boxes are affine. Section 2 supplies the
   exact strict membership/violated-row oracle for that very relaxed set.
4. Section 3 replaces the convex integer oracle. The grid introduces only
   \(r\) extra integer variables and is never enumerated.

When \(k=0\), use this same construction with \(r\) grid integer
coordinates; no convex-only continuous gradient shortcut is imported.
When \(k+r=0\), the original problem is a rational linear program.

Consequently exact threshold feasibility has bit cost
\(f(k,r,d)N^C\), with the same absolute exponent convention. This
includes rational objective thresholds because \(g_0-t\) is
quasiconvex for every fixed rational \(t\). It does not require the
joint epigraph polynomial in \((z,u,v,t)\) to be quasiconvex.

## 5. Exact values and complete optimizers transfer

Let

\[
 E=\{(z,t):\exists u,v\ [g_i(z,u,v)\le0\ (i\ge1),\
                                      g_0(z,u,v)\le t]\}.       \tag{8}
\]

For each real \(t\), its weak slice \(E_t\) is a projection of
an intersection of convex sublevels and is convex. Its strict slice
\(\bigcup_{s<t}E_s\) is a nested union of convex sets and is
convex as well. The joint set \(E\) need not be convex.

Farkas elimination of \(v\) uses the constant matrix obtained by
appending \(C_0\). It yields degree-\(D\) polynomials in
\((z,u,t)\), with individual coefficient bits \(N^{O(1)}\).
They need not be jointly quasiconvex in these variables; no such property
is needed for quantifier elimination. Eliminating \(u\) gives the
same parameter-only degree and coefficient-sensitive height bounds as
in the convex optimization note. Apply the reviewed
[quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md),
using the strict slices for the finite value bound and the weak optimal
slice for the attained-integer bound. These give value degree
\(f(k,r,d)\), value height \(f(k,r,d)N^C\), and some optimal
integer vector of that bit size whenever the value is finite.

The field-degree bound can be sharpened to depend only on \((r,d)\).
Fix any attained optimal integer assignment and substitute it into the
Farkas epigraph description before eliminating \(u\). The remaining
formula has only \((u,t)\) as variables, so its finite endpoint has
degree \(g(r,d)\), independently of the size or dimension of that
integer assignment. The preceding mixed-value theorem still supplies
the uniform height bound. The later singleton formula for the canonical
\(u^*\) uses only this value and \(O(r)\) real variables, so its
coordinate and joint-field degrees also depend only on \((r,d)\).
If \(r=0\), the fixed integer fiber is a rational linear program.

Bank--Mandel's rational globally quasiconvex polynomial attainment theorem
guarantees attainment of every finite mixed-integer infimum. Rational
threshold feasibility, a root-bound cutoff, bisection, and certified
algebraic recognition now give exact status and value with the claimed
cost. The unboundedness query must use the original unbounded model.

The complete optimizer-recovery proof in the convex optimization note
then transfers, for these reasons:

* At fixed optimal \(z\) and exact \(\theta\), the projected
  optimal set \(U_\theta\) is nonempty, closed, and convex. It is
  closed by its finite weak Farkas description and convex by sublevel
  projection. Its unique minimum-norm \(u^*\) is therefore defined by
  the same small-variable singleton formula. Quantifier elimination gives
  the same individual degree and height bounds.
* The field is \(K=\mathbb Q(\theta,u^*)\), including the value.
  The remaining minimum-norm linear fiber has a constant rational matrix,
  so its active-normal formula places every \(v_j^*\) in that field.
  Polynomial evaluation and rational minor bounds prove a uniform height
  bound and a common rational box for all canonical optimizers over the
  bounded optimal integer assignments.
* Keep this one compact box in every optimal-face query. Added rational
  affine boxes and the norm row \(\|u\|^2\le a\) remain within the
  class. Equality of the boxed exact optimum to \(\theta\) is
  equivalent to meeting the original optimal set. Integer interval
  bisection, norm bisection, and coordinate bisection recover certified
  approximations of the canonical \(u^*\).
* The outward rational right-hand-side approximation, exact rational
  minimum-norm QP, and Hoffman estimate recover approximations of the
  canonical \(v^*\). These use only a constant rational fiber matrix.
  Common-field algebraic recognition returns the exact optimizer, whose
  feasibility and objective are checked against every native input row.

The optimal set is a convex sublevel at its least value, even though the
objective need not be convex. The projection inequality for minimum norm
therefore remains valid. The recovery algorithm does not minimize a
nonconvex norm perturbation of the original objective. All subroutine
nesting has the same fixed depth as the convex optimization proof, so
the absolute input exponent is preserved.

## 6. Intrinsic directions

For an unpartitioned formulation \(g_i(z,x)\), a sufficient computable
space of eliminated directions is

\[
 K=\{a:\nabla^2 g_i(z,x)(0,a)=0
           \text{ identically for every native row and the objective}\}.
                                                               \tag{9}
\]

Rational coefficient linear algebra finds a basis. A rational change
\(x=T_1u+T_0v\) produces exactly (1), because the directional
derivatives in \(K\) are constant. The degree and coefficient bounds
for this change of variables are those in the convex note. Restriction
preserves quasiconvexity.

The common kernel can also be computed from the continuous Hessian blocks
alone, even though those blocks need not be positive semidefinite. The
following argument replaces the positive-semidefinite proof in the convex
case.

**Affine-direction lemma.** Suppose the continuous function
\(q(y,t)=a(y)t+b(y)\) is globally quasiconvex on its whole real
vector space. Then \(a\) is constant. If that constant is nonzero,
\(b\) is convex.

First suppose \(a(y_0)=0\) and \(a(y_1)\ne0\). Choose a
level \(c\ge b(y_0)\). Its closed convex sublevel contains the
complete line \(\{(y_0,t):t\in\mathbb R\}\) and some point
\((y_1,t_1)\). The convex-combination limit used in Section 3.1
then puts the entire parallel line at \(y_1\) in that sublevel,
contradicting its nonzero slope. Hence \(a\) is identically zero or
nowhere zero. The zero case is finished. In the remaining case,
continuity and connectedness make its sign constant.
After replacing \(t\) by \(-t\), assume \(a>0\).

For every real \(c\), the sublevel is the hypograph of
\(h_c(y)=(c-b(y))/a(y)\), so \(h_c\) is concave. Apply its
Jensen inequality at any two points and any weight. The inequality holds
for all positive and negative \(c\), so the coefficient of \(c\)
has zero Jensen defect. Thus \(1/a\) is affine. Its global positivity
forces it to be constant. Lemma 1 now gives convexity of \(b\).
This proves the lemma without a polynomial hypothesis.

If a continuous direction \(h\) belongs to the polynomial kernel of
every block \(\nabla^2_{xx}g_i(z,x)\), then each restriction along
that direction is affine: its second derivative is identically zero.
The affine-direction lemma makes its slope constant in all other variables,
including \(z\). Therefore the full Hessian annihilates \((0,h)\).
The reverse inclusion is immediate, proving equality of the two kernels.
The independently checked polynomial reciprocal-derivative proof in the
[projection review, Section 4](quasiconvex-polynomial-projection-review.md#4-a-stronger-affine-direction-statement)
gives an alternative route. This is a structural observation, with novelty
unestablished; it is not a new recognition algorithm for quasiconvexity.

## 7. Limits and prior comparison

The extension permits convex feasible sets described by globally
quasiconvex polynomial functions. It does not cover locally quasiconvex
functions, quasiconvexity only on an unspecified domain, arbitrary convex
sets defined by nonquasiconvex rows, or variable coefficients on the
eliminated variables. It is a parameterized bit-complexity statement;
practical constants and numerical performance remain unproved.

The qualitative extension should not be mistaken for an entirely new
quasiconvex integer method. Hildebrand--Koppe and Heinz already treat
globally quasiconvex polynomial integer optimization. The possible added
capability is exact mixed optimization and full algebraic output with
arbitrarily many linear continuous coordinates. The
[prior audit](quasiconvex-polynomial-nonlinear-dimension-prior.md)
also records a published mixed-integer FPT folklore statement by
Gavenciak--Koutecky--Knop. Its precise continuous-dimension and output
scope remains unresolved by the inspected passage, so it creates material
priority uncertainty.

The enlargement has concrete structural limits. Ahmadi--Olshevsky--Parrilo--
Tsitsiklis, Proposition 4.6, show that odd-degree globally quasiconvex
polynomials are monotone univariate polynomials of one linear coordinate;
their proper nonempty sublevels are halfspaces. Their Theorem 4.11 shows
that even homogeneous quasiconvex polynomials are convex. These precise
classification results limit what the wider representation can add.
By Lemma 1, every newly admitted nonconvex row must be independent of
the eliminated variables. Even a quasiconvex
nonconvex example can have a simple convex reformulation. Identifying
important applications that benefit from the additional representation
freedom remains open. The primary sources and exact comparisons are in
the prior audit. The result is best presented as an extension of the
convex theorem, with no separate major-breakthrough claim.

## 8. Verification record and limits

The [projection review](quasiconvex-polynomial-projection-review.md)
checked Lemmas 1--2, the strict LP alternative, and the need for a basic
dual optimum. The [oracle review](quasiconvex-polynomial-oracle-review.md)
independently reconstructed Section 3 and checked the changed interface
to the existing recursion. The
[full review](quasiconvex-polynomial-nonlinear-dimension-review.md)
checked Sections 2--6, including the radius and gap transfers, the separate
weak-slice hypothesis for optimal integer bounds, the common-field degree
refinement, and compact optimizer recovery. A further
[affine-direction review](quasiconvex-affine-direction-independent-review.md)
independently checked both the polynomial and continuous coefficient
lemmas. The author and parent researcher independently reread these
arguments and the substantive strengthening. No unresolved proof
correction remains in these reviews; that scrutiny is evidence rather
than a guarantee of correctness.

The reviewers ran targeted inline `python -` checks. Six exact SymPy
oracle cases covered both nearby-gradient branches, stationary cubic
and radial boundaries, a constant violation, and an inner-rounding
outcome. Exact fraction checks covered a nonconvex compact residual
epigraph with a positive gap, the zero-row multiplier decomposition,
and counterexamples to weaker affine-direction hypotheses. These checks
verify the displayed examples and identities. They do not implement the
full algorithm or establish its universal arithmetic bounds.

The author ran a separate targeted inline `python -` document check for
the main note and the modified prior audit, covering local links,
paired math delimiters, whitespace, control characters, and final
newlines. No project-wide verification, CI inspection, or Lean
formalization is claimed. The quantitative input theorems retain their
separate sources and verification limits.
