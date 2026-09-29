# Exact optimizers for a convex quadratic divided by an affine function

Date: 2026-09-28. Status: proof and fresh field and algorithm reviews
completed; no unresolved gap was found in the stated composition.
The value theorem is developed separately in
[common-range-quadratic-fractional.md](common-range-quadratic-fractional.md).

A convex quadratic numerator can have arbitrary rank without entering the
common-range parameter of the native constraints. Retaining the
denominator's linear direction leaves rational quadratic-programming
charts for the remaining variables. These charts bound a canonical
optimizer, while exact fractional-value comparisons recover it.

## 1. Statement and assumptions

Let \(F\subseteq\mathbb R^k\times\mathbb R^n\) be a rational closed
convex set described by native affine SOC constraints or PSD quadratic
constraints and arbitrary affine rows. The integer variables are
\(z\in\mathbb Z^k\). Consider

\[
             \inf\left\{\frac{q_0(z,x)}{d(z,x)}:
                           (z,x)\in F,\ z\in\mathbb Z^k\right\},          \tag{1}
\]

where \(q_0\) is a rational convex quadratic, with positive semidefinite
Hessian in all \((z,x)\) variables, and \(d\) is rational affine and
strictly positive throughout the real set \(F\). The numerator can be
negative. Its Hessian may have arbitrary rank.

Let \(H_i\) be the full Hessians of the native quadratic constraints
or squared cone residuals; retain cone right-hand-side signs. Define

\[
 K_*=\{v\in\mathbb R^n:H_i(0,v)=0\ \text{for every }i\},
 \qquad \rho=n-\dim K_* .                                  \tag{2}
\]

The numerator Hessian is excluded from (2). The denominator is excluded
as well; the proof retains at most one additional direction for it.
Let \(N\ge2\) be the total explicit rational input length.

**Complete optimization consequence.** Combined with the separate value
theorem, the construction below gives an algorithm with bit complexity
\(f(k,\rho)N^C\), for an effective function \(f\) and an absolute
constant \(C\). It decides infeasibility or unboundedness below, returns
an exact finite infimum otherwise, decides its attainment, and returns
an optimal integer assignment and an exact algebraic continuous optimizer
when attained. The output has one primitive integer polynomial, a real
root isolator, and rational coordinate polynomials in that root.

No boundedness, Slater condition, rational optimizer, or positive uniform
denominator lower bound is assumed. Section 7 treats the explicitly
positive domain \(F\cap\{d>0\}\) when positivity is not promised on
all of \(F\). The result concerns one quadratic numerator, not a
maximum of unrestricted quadratic numerators.

The value theorem supplies three inputs to this output argument:
an exact rational-threshold algorithm, a finite-value degree and height
bound \(f(k,\rho)N^C\), and a conditional bound of that form for some
attaining integer assignment. Its threshold is
\(q_0-t d\le0\); for rational \(t\), this is one convex quadratic
with the original numerator Hessian. The
[common-range quadratic-objective theorem](common-range-optimization.md)
keeps that Hessian outside the native range parameter.

## 2. Fix an integer fiber and retain the denominator direction

First prove the continuous encoding and recovery statement. Fix a rational
integer assignment and include its encoding length in the data size.
Use the notation

\[
 q_0(x)=\tfrac12x^TQx+a^Tx+c,\qquad Q\succeq0,\qquad
 d(x)=d_x^Tx+d_c.                                           \tag{3}
\]

Choose a rational invertible split

\[
 x=T_1u+T_0v,\qquad
 \operatorname{range}T_0=K_*\cap\ker d_x^T,\qquad
                   r:=\dim u\le\rho+1.                     \tag{4}
\]

For a continuous-only input, use the common kernel of its native Hessians.
For mixed inputs, one can fix this split before integer substitution.
All transformation entries have polynomial bit length.

The native rows and cone signs become

\[
                         Cv\le b(u),                        \tag{5}
\]

where \(C\) is constant rational and \(b\) is quadratic. The
denominator becomes \(d_0(u)\), independent of \(v\).
Suppose the continuous ratio has finite attained minimum \(\theta\).
Every feasible fiber in (5) has a finite numerator minimum: an unbounded
numerator in one fiber would make the ratio unbounded there, since
\(d_0(u)\) is a fixed positive number. A convex quadratic bounded below
on a nonempty polyhedron attains its minimum.

The reviewed [constant-matrix QP chart lemma](common-range-optimizer-witness.md#2-constant-matrix-quadratic-programming-charts)
therefore applies. There is a finite family of rational maps
\(v_I(u)\) of degree at most two, with polynomial coefficient length,
such that the minimum-norm numerator optimizer in each feasible fiber
equals some \(v_I(u)\). Define

\[
 D_I=\{u:Cv_I(u)\le b(u)\},\qquad
                    g_I(u)=q_0(T_1u+T_0v_I(u)).             \tag{6}
\]

The set \(D_I\) has quadratic defining rows and \(g_I\) has degree
at most four. Every chart point admitted by \(D_I\) is feasible.
The number of charts can be exponential; neither this proof's selected
chart nor the whole family is enumerated by the algorithm.

## 3. The optimal projection is closed and has a small canonical point

The continuous optimal set is

\[
 O=\{x\in F:q_0(x)-\theta d(x)\le0\}.                         \tag{7}
\]

The ratio is everywhere at least \(\theta\), so the inequality in (7)
is an equality. The defining function is convex quadratic, hence \(O\)
is closed and convex. By the chart coverage,

\[
 U_\theta=\operatorname{proj}_u O
   =\bigcup_I\{u\in D_I:g_I(u)\le\theta d_0(u)\}.             \tag{8}
\]

This finite union is closed, since every constituent is a basic closed
quartic set. It is convex as the projection of \(O\). Thus it has a
unique point \(u_*\) of minimum Euclidean norm. In the optimal fiber
over \(u_*\), choose the unique minimum-norm point \(v_*\).

There is a chart \(I_*\) with

\[
                         v_*=v_{I_*}(u_*).                  \tag{9}
\]

Indeed, because \(d_0(u_*)\) is fixed, the optimal ratio points in this
fiber are exactly its numerator minimizers. The chart lemma selects the
minimum-norm member of those minimizers. Moreover, \(u_*\) is the
unique norm minimizer on
\[
 \Omega_{I_*}=\{u\in D_{I_*}:g_{I_*}(u)\le\theta d_0(u)\}.
\]
This set contains \(u_*\) and is contained in \(U_\theta\); any
other point with the same minimum norm would contradict uniqueness on
the convex set \(U_\theta\).

Let \(D\) and \(H\) bound the degree and representation bits of
the supplied \(\theta\). A coefficient-sensitive low-dimensional
argument gives

\[
 [\mathbb Q(\theta,u_*):\mathbb Q]\le f(r,D),\qquad
 \operatorname{encoding}(\theta,u_*)\le f(r,D)(N+H)^C.       \tag{10}
\]

Here and below \(C\) is absolute. One direct proof uses the minimal
polynomial and isolator for \(\theta\), describes the unique minimizer
of \(\|u\|^2\) on \(\Omega_{I_*}\) by comparison with all
\(u'\in\Omega_{I_*}\), and eliminates all but one coordinate in turn.
Each resulting univariate formula defines a singleton, so one of its
nonzero polynomials vanishes there. Coefficient-sensitive quantifier
elimination bounds its degree and height using \(O(r)\) variables,
degrees at most \(\max(4,D)\), and coefficient bits polynomial in
\(N+H\). Multiplying the degree bounds for only the \(r\) retained
coordinates, together with \(D\), still gives a parameter-only bound
\(f(r,D)\). A bounded primitive element and trace-pairing conversion
then give the common representation in (10). This product is taken over
the retained coordinates, not over the possibly many original or
gradient coordinates. The separate field review details these bounds.

By (9), \(v_*\) is a rational quadratic polynomial in \(u_*\).
It therefore lies in the same field, with height of the form (10).
The complete canonical tuple and the original coordinates consequently
have common-field degree at most \(f(r,D)\), total representation
length \(f(r,D)(N+H)^C\), and a computable transformed box

\[
                 (u_*,v_*)\in[-B,B]^n,\qquad
                 \operatorname{bit}B\le f(r,D)(N+H)^C.      \tag{11}
\]

This encoding conclusion is for an attained **optimal** level. It must
not be replaced by a same-field assertion for arbitrary nonempty
quadratic sublevels. For example, with no native constraints,
\(d=1\), \(q_0(v)=(v-2)^2\), and threshold \(2\), the minimum-norm
point of the sublevel is \(2-\sqrt2\), even though the retained
dimension is zero and the threshold field is rational. At the actual
minimum zero, its optimizer is the rational point \(2\).

## 4. A common gradient makes the optimal fiber linear

For any \(x,y\in O\), the midpoint belongs to \(F\) and has ratio
at least \(\theta\). On the other hand, (7) and the quadratic identity
give

\[
 (q_0-\theta d)((x+y)/2)
    =-\tfrac18(x-y)^TQ(x-y)\le0.
\]

Thus \((x-y)^TQ(x-y)=0\), and positive semidefiniteness gives
\(Q(x-y)=0\). The raw numerator gradient

\[
                            g=Qx+a                           \tag{12}
\]

is constant throughout this continuous optimal set. This statement is
made after fixing the integer assignment. It need not hold across
different optimal integer assignments.

Evaluating (12) at the point in (9) shows that \(g\) lies in
\(\mathbb Q(\theta,u_*)\), with the degree and height bounds (10).
Appending its possibly many coordinates introduces no product of field
degrees.

Put \(b_g=g-a\). Rational row reduction of the fixed matrix \(Q\)
gives a rational linear operator \(R\) on its range such that

\[
                  x_0=Rb_g,\qquad Qx_0=b_g.                 \tag{13}
\]

On the affine space \(Qx=b_g\), write \(x=x_0+w\) with \(Qw=0\).
Symmetry gives \(x^TQx=x_0^TQx_0\). Therefore the exact optimal fiber
at \(u=u_*\) is described by the original native fiber rows and

\[
 \begin{split}
 Qx&=g-a,\\
 a^Tx&=\theta d_0(u_*)-c-\tfrac12x_0^TQx_0.
 \end{split}                                               \tag{14}
\]

Both coefficient matrices in (14) are rational. In \(v\) coordinates
the added matrices are \(QT_0\) and \(a^TT_0\); all algebraic data
occur on the right-hand sides. These right-hand sides are polynomials
of degree at most two in \((\theta,g,u_*)\), with polynomial-bit
rational coefficients.

The first equation alone is insufficient when the numerator has a linear
component on \(\ker Q\); the scalar equation in (14) retains its
objective level. If \(Q=0\), use \(x_0=0\). The argument covers this
case and all singular positive semidefinite \(Q\).

## 5. Approximation uses rational fractional-value queries

Keep the full rational box (11) in the fixed transformed coordinates.
For any rational affine cuts and rational threshold on \(\|u\|^2\),
the resulting native subdomain is compact. Its positive-denominator
ratio is continuous and attains a minimum if nonempty. Thus its exact
value equals \(\theta\) if and only if the domain meets \(O\).

The new norm row has the rational SOC form
\[
                       \|(2u,t-1)\|_2\le t+1
\]
for \(t\ge0\), or the native PSD form \(\|u\|^2\le t\).
It annihilates the eliminated kernel in (4). Affine cuts add no curvature.
All these value queries have native common range at most \(\rho+1\);
the numerator Hessian remains excluded.

Use this optimal-set oracle to approximate \(u_*\) by squared-norm
bisection and coordinate bisection. The box contains \((u_*,v_*)\),
so its optimal projection retains the same minimum-norm point. A feasible
norm threshold at most \(\eta^2/16\) above \(\|u_*\|^2\) restricts
every projected optimal point to distance at most \(\eta/4\), by the
convex projection inequality. Coordinate bisections preserve nonemptiness
and then give coordinate error below \(\eta\). Restart with the
original box at every new requested precision.

The same oracle approximates each coordinate of \(g\). For a rational
threshold \(t\), the row \((Qx+a)_j\le t\) is rational affine.
Since (12) is constant on every optimal point, the oracle returns yes
exactly when \(g_j\le t\). Rational interval bisection on a bound
computed from \(Q,a,B,T_1,T_0\) supplies arbitrary precision. No square root
or algebraic coefficient is introduced into an optimization query.

Refine the selected input root for \(\theta\), and evaluate the
right-hand sides of (14) and the native rows at \(u_*\). They define
a nonempty polyhedron in \(v\) with rational coefficient matrix and
algebraic right-hand side. Approximate that right-hand side outward
and solve an exact rational minimum-norm QP. The
[rational-QP and Hoffman recovery estimate](common-range-witness-recovery.md#5-recover-the-affine-fiber-through-rational-quadratic-programs)
gives a certified approximation to its unique minimum-norm point \(v_*\).
It needs only an absolute polynomial number of precision bits in the
input, magnitude bound, and requested output accuracy.

Finally apply [constructive common-field recovery](constructive-common-field-recovery.md)
to \((\theta,g,u_*,v_*)\), with the joint degree and height bounds
already established. Its bit overhead is polynomial in those bounds.
Transform back and verify the original native rows, cone signs,
denominator positivity, and \(q_0(x)=\theta d(x)\) exactly.
The output contains the selected value embedding.

Each queried value is compared with \(\theta\) by ordinary univariate
real-algebraic comparison and then discarded. No compositum of all
query-value fields is formed. With the coefficient-sensitive FPT value
oracle, query count, input length, rational QP cost, and recognition
overhead compose to \(f(r,D)(N+H)^C\), with an absolute exponent.

## 6. Attainment and integer recovery

Let the original mixed-integer problem have known finite infimum
\(\theta\). The value theorem gives \(D,H\le f(k,\rho)N^C\)
and a conditional integer bit bound \(M\le f(k,\rho)N^C\) for some
attaining assignment, if one exists.

Fix one global rational split (4). For each integer assignment in that
box, substitution has length polynomial in \(N+M\). If its
\(\theta\)-level is nonempty, then \(\theta\) is its attained
continuous minimum: the original mixed-integer infimum is a lower bound
on every such fiber. Thus the encoding argument of Sections 2--3
applies exactly where needed. It gives one uniform transformed box of
bit length \(f(r,D)(N+M+H)^C\) containing the canonical point of
every attaining fiber in the integer box. No assertion about arbitrary
nonoptimal quadratic sublevels is used.

Intersect the rational problem with both boxes. A nonempty resulting
mixed-integer domain is a finite union of compact continuous fibers,
so its fractional infimum \(\beta\) is attained. Therefore the
original finite infimum is attained if and only if the boxed domain is
nonempty and \(\beta=\theta\). The forward implication uses one
small attaining assignment and its uniformly bounded canonical point;
the reverse implication uses compact attainment.

When equality holds, integer-coordinate bisection retains halves whose
boxed value equals \(\theta\). Each retained domain contains an
actual optimizer. Polynomially many comparisons fix an attaining
integer assignment; Section 5 then returns its canonical continuous
optimizer. Every input length remains \(f(k,\rho)N^C\), and all
subroutines have absolute input exponents, proving the complete bound.

With a supplied integer box, use uniform fixed-fiber value bounds and
bounded-integer quadratic-threshold feasibility. A finite global infimum
over that finite set of assignments equals one of their continuous
infima. This gives the same recognition and compact-attainment argument
with the corresponding continuous common-range parameter.

## 7. An explicitly positive domain

If the stated domain is \(F\cap\{d>0\}\), add a continuous variable
\(s\) and the rational cone

\[
                         \|(2,d-s)\|_2\le d+s.              \tag{15}
\]

Its projection is exactly the positive domain, and its feasible points
all satisfy \(d>0\). The original objective is independent of \(s\).
The [reviewed shared reciprocal lift](common-range-positive-domain-review.md)
proves preservation of feasibility, infimum, and attainment, with
new cross-aware common-range codimension at most \(\rho+2\).
The numerator Hessian is extended by a zero row and column, so it remains
positive semidefinite and is still excluded from the native parameter.
Apply the complete theorem to the lifted closed system and discard
\(s\). The FPT parameter family is unchanged.

Compact tests must include this auxiliary coordinate; an
original-coordinate box in the open domain alone does not supply
attainment. The returned original point need not minimize the norm of
the original open domain.

## 8. Prior, significance, and limitations

The threshold conversion, parametric convex QP charts, and
minimum-norm and algebraic recovery tools have substantial classical
precedents. The chart mechanism and its singular cases were compared with
Spjøtvold--Tøndel--Johansen and Patrinos--Sarimveis in
[the common-range objective prior note](common-range-optimization-prior.md).
The [quadratic-fractional prior audit](common-range-quadratic-fractional-prior.md)
compares the assembled result with quadratic fractional programming and
mixed-integer convex optimization.

In particular, [Chandrasekaran--Tamir (1984), pp. 327 and 334](https://www.math.tau.ac.il/~atamir/opt_84.pdf)
already establish polynomial-time exact algebraic infimum computation and
attainment decisions on an unbounded rational polyhedron for a nonnegative
convex quadratic numerator and a positive concave quadratic denominator.
An affine denominator is included. Thus exact continuous polyhedral
fractional values and attainment are established capabilities. Their
literal assumptions do not include a numerator of arbitrary sign or
integer variables.

Del Pia's one-PSD-cut result supplies rational threshold feasibility in
the mixed-integer polyhedral case. The additions at issue here are the
native conic or quadratic constraint class controlled by \(\rho\),
unbounded integer domains controlled by \(k\), finite-value and
canonical-output bounds, and their exact FPT composition. The inspected
sources did not state this complete theorem; that search finding does
not establish novelty or priority.

The capability is exact optimization of a normalized convex quadratic
cost while allowing arbitrary numerator rank and many continuous
directions that enter the native constraints only linearly. Possible
models include a convex operating cost divided by a positive affine
throughput measure. This is a theoretical capability and parameterized
bit-complexity result; no practical runtime or numerical precision benefit
has been demonstrated.

Convexity of the numerator is substantive both for rational threshold
optimization and for the common-gradient identity. Denominator positivity
is enforced or assumed. The common-range parameter concerns the supplied
native representation. The proof neither enumerates its implicit QP
charts nor assumes that a numerical approximation is an exact optimizer.
With several unrestricted quadratic numerators, threshold feasibility
would contain several arbitrary-rank PSD constraints; the one-quadratic
interface used here would no longer apply.

## Verification record

The [field review](common-range-quadratic-fractional-field-review.md)
independently checks the optimal projection, the choice of one chart,
the low-dimensional singleton formula, common-field representation, and
the uniform conditional box. The
[algorithm review](common-range-quadratic-fractional-algorithm-review.md)
checks gradient constancy after integer substitution, rational-normal
recovery, compact value comparisons, attainment, integer recovery, and
the absolute input exponent. Both read the final manuscript and found
no unresolved gap, conditional on the separately reviewed value and
threshold theorems. A narrow reviewer also checked the gradient and
affine-fiber identities.

Two clarifications were incorporated. Multiplying degree bounds for only
the \(r\) retained coordinates is sufficient for a parameter-only joint
degree; the ambient coordinates are then rational chart evaluations.
The gradient magnitude bound includes the rational transformation because
the containing box is in transformed coordinates. The nonoptimal
sublevel counterexample remains explicit.

Exact inline SymPy checks by the reviewers covered objective ranks
\(1,2,7,12\), a positive-dimensional optimal set, singular numerator
Hessians, the necessity of the scalar objective equation, kernel
preservation, nonattainment in an unboxed query, and the distinction
between a continuous-fiber gradient and mixed-integer gradients.
The field review also checked a quartic chart and a sharper optional
perturbation bound. These finite calculations do not prove the general
degree, height, or complexity claims.

The primary prior audit inspected the 1984 assumptions and nonattainment
passage; the author independently reread those passages. A targeted inline
Python check covers this note and its three supporting reports: final
newlines, whitespace, control characters, paired math delimiters, and
local Markdown links. No project-wide checks, CI inspection, or Lean
formalization are asserted.
