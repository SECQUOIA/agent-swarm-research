# Exact optimization with an unrestricted PSD objective

Date: 2026-09-28. Status: complete proof with a
[fresh adversarial review](common-range-optimization-fresh-review.md),
including exact optimizer recovery. An earlier
[adversarial investigation](common-range-optimization-review.md)
contributed repairs; the fresh review independently checked the combined
argument and used a separately staffed review of the output step. No
priority claim is made.

The common range of the **constraint** Hessians can control exact
optimization even when the objective has arbitrary positive-semidefinite
curvature. Adding the objective Hessian to that range would lose this
distinction. The algorithm instead retains the objective inequality
exactly, approximates only the native constraints, and invokes an
established algorithm for a polyhedron with one convex quadratic row.

## 1. Statements and parameters

Use the rational native convex quadratic and rational SOCP models from
[the feasibility theorem](common-range-fpt-frontier.md). Squared SOC rows
always retain their affine right-hand-side sign. All objective Hessians
in this note are jointly PSD. The objective is

\[
 q_0(w)=\tfrac12 w^TQ_0w+a_0^Tw+c_0,\qquad Q_0\succeq0.
\]

Let \(N\ge2\) be the explicit binary input length. For continuous
problems, \(r\) is the common range dimension of the native constraint
Hessians. With supplied bounds on \(z\in\mathbb Z^k\), use the
common range dimension \(r_x\) of their continuous Hessian blocks.
Without integer bounds, use

\[
 \rho=\operatorname{codim}\{v:H_i(0,v)=0\text{ for all native }H_i\}.
\]

The objective is excluded from all three parameters.

**Threshold theorem.** Exact feasibility with the additional rational
cut \(q_0\le t\) is decidable in \(f(r)N^C\) time in the continuous
case, \(f(k,r_x)N^C\) time with supplied integer bounds, and
\(f(k,\rho)N^C\) time without integer bounds. Here and below \(C\)
is absolute and \(f\) is computable. In the boxed-integer case a
polyhedron plus the single original PSD quadratic cut preserves precisely
the feasible original integer assignments. No new integer variables are
introduced.

**Continuous value theorem.** In \(f(r)N^C\) time one can classify
infeasibility, infimum \(-\infty\), or a finite infimum; in the finite
case one can return its exact algebraic value, decide whether it is
attained, and return an exact algebraic optimizer when one exists. This
includes SOC instances with a finite unattained infimum.
The finite value has degree at most \(f(r)\) and coefficient bit length
at most \(f(r)N^C\).

**Bounded-integer value theorem.** With supplied integer bounds, the same
classification, exact value, and attainment decision take
\(f(k,r_x)N^C\) time. If the optimum is attained, an optimal integer
assignment and an exact algebraic continuous optimizer can be returned.
Finiteness of the integer box is essential to the value proof
here; threshold feasibility alone is not a proof of unrestricted
mixed-integer optimization.

The [separate unbounded-integer composition](common-range-unbounded-optimization.md)
adds a general finite mixed-integer value bound and obtains full exact
optimization in \(f(k,\rho)N^C\) time without integer bounds.
For native PSD quadratic systems, \(\rho=r_x\); for general SOC
systems the larger parameter is necessary for the current unbounded
projection argument.

## 2. A parametric convex QP projection

Choose rational common-kernel coordinates \(x=T_1u+T_0v\), with
\(u\in\mathbb R^r\). Native quadratic rows, affine rows, sign rows,
and any box constraints have the form

\[
                 Cv\le d(u),                       \tag{1}
\]

where \(C\) is constant rational and \(d\) is quadratic. Retaining
integer coordinates or a residual variable replaces \(u\) in (1) by
the corresponding parameter tuple. In the unbounded-integer argument
the full-kernel definition of \(\rho\) ensures that \(C\) remains
constant. In the supplied-integer-box argument, fix \(z\) first;
\(C_z\) may depend on that assignment but has uniformly bounded bits.

The objective in these coordinates is

\[
 q(a,v)=\tfrac12v^TQv+b(a)^Tv+c(a),                 \tag{2}
\]

with constant \(Q\succeq0\), affine \(b\), and quadratic \(c\).
Suppose each nonempty fiber has a finite attained QP minimum. This is
automatic for boxed fibers. For every linearly independent row subset
\(I\) of \(C\), including the empty set, put

\[
 M_I=\begin{bmatrix}Q&C_I^T\\ C_I&0\end{bmatrix},
 \qquad
 \binom{v_I(a)}{\lambda_I(a)}
       =M_I^+\binom{-b(a)}{d_I(a)},                 \tag{3}
\]

where \(M_I^+\) is the Moore--Penrose inverse of the constant rational
matrix. Rational row reduction and minors bound its coefficient bits
polynomially. For example, if \(Z\) is a rational kernel basis and
\(A=M_I+ZZ^T\), then \(A\) is invertible and
\(M_I^+=A^{-1}M_IA^{-1}\). Consequently \(v_I\) is a rational
polynomial map of degree at most two. It is defined even when the
corresponding stationarity equations are inconsistent.

The minimum-norm fiber optimizer \(v_*\) equals \(v_I(a)\) for at
least one \(I\). To see this, choose a basis of **all** row normals
active at \(v_*\). Every direction in \(\ker C_I\) allows small
feasible motion in both signs, so first-order optimality supplies a
possibly signed multiplier making \((v_*,\lambda)\) solve the linear
system in (3). Positive semidefiniteness and row independence give

\[
       \ker M_I=(\ker Q\cap\ker C_I)\times\{0\}.  \tag{4}
\]

Indeed, multiplying \(Qh+C_I^T\mu=0\) by \(h^T\), with
\(C_Ih=0\), first gives \(Qh=0\), then \(\mu=0\). Small
feasible motions along this kernel preserve the objective exactly.
Minimum norm among optimizers therefore makes \(v_*\) orthogonal to
it. Thus \((v_*,\lambda)\) is the Moore--Penrose solution. This
argument includes singular matrices and active rows with zero multipliers.
Only choosing positive-multiplier rows would be insufficient.

Define

\[
 D_I=\{a:Cv_I(a)\le d(a)\},\qquad
 \phi_I(a)=q(a,v_I(a)).
\]

The rows defining \(D_I\) have degree at most two, and \(\phi_I\)
has degree at most four. The union of
\(D_I\cap\{\phi_I\le t\}\) is exactly the objective-threshold
projection. Every chart point gives an actual feasible original point;
conversely, the minimum-norm optimizer in every threshold-feasible fiber
belongs to one chart. This is why consistency and multiplier-sign guards
are unnecessary in these particular charts. The complete chart proof and
its independent review are in
[the optimizer encoding note](common-range-optimizer-witness.md).

Each chart has degree at most four and coefficient bit length
\((B+1)N^{C_0}\), where \(B\) bounds any appended scalar or box bits.
There are at most exponentially many charts, each with the original
polynomial number of rows. Denominators are cleared separately in each
row. The chart family is used only to prove bounds and is never enumerated
by the algorithm. All degree and coefficient bounds are uniform over it.

Quartic values cannot simply be replaced by quadratic values: minimizing
\(v^2\) over the fiber \(v\ge u^2\) gives \(u^4\).

### Unboxed fibers

A feasible threshold need not have a fiber minimizer when that fiber QP
is unbounded below. For example, \(v\ge0\) and \(q=-v\) admit
every finite threshold but have no KKT minimum.

Because the full objective is PSD, a vector in \(\ker Q\) is also
annihilated by every objective cross block involving the retained
parameters. A fiber has unbounded objective precisely when

\[
          Cd\le0,\qquad Qd=0,\qquad a_v^Td<0        \tag{5}
\]

has a solution, where \(a_v\) is the constant linear objective part.
This rational cone is independent of the parameter tuple. If it has a
solution, choose a rational solution with \(a_v^Td=-1\) and polynomial
bit length; every nonempty fiber is then unbounded below.

For completeness, absence of (5) proves finite attainment for all
nonempty fibers even with irrational parameter values. Split \(v\)
into the kernel of \(Q\) and a rational complement. The complement
has a positive definite quadratic objective. On the kernel, minimizing
the remaining linear objective over the polyhedral fiber is an LP. The
absence of (5) makes its dual feasible, and a fixed dual solution gives
an affine lower bound in the complement coordinates. The positive
definite quadratic plus this affine bound is coercive. Farkas projection
makes the feasible complement domain closed; the LP value is a finite
maximum of affine functions there. Its minimum is therefore attained,
and the kernel LP attains its value. This also proves the dichotomy
without applying a rational-input theorem to irrational right-hand sides.

If (5) holds, the objective-threshold projection is just the native
feasibility projection. Otherwise the quartic charts above apply.

## 3. A threshold-preserving radius and gap

The [Basu--Roy radius bounds](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf)
give, at fixed degree four in dimension \(d\), meeting and containing
radii whose logarithms are at most

\[
       (\tau+\log(S+1)+1)2^{O(d)}.                 \tag{6}
\]

Apply the meeting-radius theorem separately to a nonempty quartic
threshold chart in \(u\). Lift it by the degree-two map \(v_I(u)\). Its coefficients
have polynomial bit length, so this gives
some threshold-feasible original point in a rational box with bit length
\(2^{O(r)}(B+1)N^{C_1}\).

In case (5), first choose a small native feasible point by the existing
common-range radius theorem. Moving it a nonnegative distance
\(\max\{0,q_0-t\}\) along the normalized direction in (5) meets
the threshold. Its coordinate magnitude has the same type of bit bound.
For integer fibers in a supplied box all of these bounds are uniform.

Now impose a finite rational box and retain \(q_0\le t\) exactly.
If that intersection is empty, every outer-lift problem below is empty.
Otherwise let \(\alpha\) be the minimum, over that compact set, of
the maximum of zero and the native residuals. Introduce
\(0\le s\le U\), with \(U\) a rational upper bound for these
residuals, and replace each native row by its residual bound \(s\).
Section 2 describes the projected residual epigraph \(E\) in
\((u,s)\) as a finite union of basic closed quartic charts \(E_I\).
The whole projection is compact. Each chart is a closed subset of it,
and hence is compact too.

If the exact threshold system is infeasible, \(\alpha>0\). Each
nonempty reciprocal chart

\[
 H_I=\{(u,s,y):(u,s)\in E_I,\ sy=1,\ y\ge0\}
\]

is compact. The **containing** radius theorem bounds every \(y\),
including \(1/\alpha\) in a chart containing a residual minimizer.
Thus an effective bound is

\[
 \alpha=0\quad\hbox{or}\quad
 \alpha\ge2^{-2^{O(r)}(B+1)N^{C_2}}.               \tag{7}
\]

The high rank of \(Q_0\) does not enter the nonlinear dimension in
(6)--(7). A meeting radius alone would not prove the residual gap.

## 4. The exact threshold oracle

Print the threshold-preserving box from Section 3. Construct rational
polyhedral outer lifts of the native PSD quadratic or actual Lorentz-cone
rows with residual error strictly less than the gap in (7). Retain affine
rows and cone signs exactly. Retain \(q_0\le t\) as the sole exact
PSD quadratic row. Every true threshold point has a lift. A feasible
lifted point has native residual below the positive gap, so the exact
threshold system in that integer fiber is nonempty.

The lift has \(2^{O(r)}(B+1)^{C_3}N^{C_3}\) encoding length.
[Del Pia, Proposition 4, v2](https://arxiv.org/html/2311.00099v2#S4.SS2)
solves a rational polyhedron intersected with one PSD quadratic inequality
in FPT time parameterized by the number of integer coordinates. This is
an established subroutine, not a new one-quadratic algorithm. Its use
proves the continuous and supplied-integer-box threshold claims.

Without integer bounds, Section 2 gives a threshold-projection formula
\(\exists u\,\bigvee_I\Psi_I(z,u)\), with \(\rho\) quantified
variables, degree at most four, and polynomial coefficient bits. In the
recession case (5), use the native Farkas projection instead. Its free
\(z\)-set is convex because it projects the original convex sublevel.
The predicate-count-independent integer-witness theorem of
[Khachiyan--Porkolab, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
supplies a feasible integer assignment with \(f(k,\rho)N^C\) bits.
Print this box and invoke the preceding construction. This uses the
implicit formula only for its witness bound.

## 5. Finite values from established quantifier elimination

An important established result separates the number of input predicates
from the degree and coefficient size of each output predicate.
[Basu--Pollack--Roy (1996), Theorem 1.3.1](https://doi.org/10.1145/235809.235813)
and the well-behavedness condition immediately preceding it give this
separation. The coefficient statement is explicit in
[Basu's author survey, Theorem 2.27](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
For bounded degree and a bounded number of quantified and free variables,
output degree is bounded by a function of those dimensions, and output
coefficient bit length is at most that function times the input
coefficient-bit bound. These two bounds do not depend on predicate count.
The running time and number of output predicates do depend on it.

Apply this theorem only as a bound to the quartic objective epigraph
formula \(\exists u\,\bigvee_I\Psi_I(u,t)\). The scalar sublevel
projection is an upper interval, possibly open at its finite endpoint.
At a finite endpoint \(\theta\), some nonzero defining univariate
polynomial must vanish; otherwise all signs are locally constant.
Therefore

\[
 \deg\theta\le f(r),\qquad
 \operatorname{bit}(P_\theta)\le f(r)N^C,           \tag{8}
\]

for an integer annihilator. No attainment assumption is needed. The
objective-unbounded fiber case already gives \(-\infty\) whenever
the native system is feasible.

After checking native feasibility, a Cauchy bound from (8) gives a
computable \(M\) larger than the absolute value of every possible
finite infimum. The rational-threshold query at \(-M-1\) distinguishes
\(-\infty\) from a finite value. In the finite case, bisection and
standard algebraic-number recognition recover \(\theta\) exactly,
using precision polynomial in the degree and height bounds in (8).
If a midpoint equals an unattained infimum, the query is false; assigning
that midpoint to the lower interval endpoint still preserves the required
closed numerical enclosure. No query needs an algebraic input coefficient.

This argument imports an established QE size theorem. It does not run QE
on an exponentially long formula and does not prove a new elimination
bound. The local primary text at
`papers/pooling/revision-20260909/checks/whole-review4/basu1996-on-the-combinatorial-and-algebraic.txt`,
pp. 1004--1005, and the survey's Theorem 2.27 were inspected directly.

## 6. Attainment and bounded integer variables

Suppose the finite value \(\theta\) is attained. In a chart containing
an optimum, append \(P_\theta(t)=0\), a closed rational isolating
interval containing only the selected root, and \(\phi_I(u)\le t\).
This is a nonempty basic closed set in \(r+1\) variables, with degree
\(f(r)\) and coefficient bits \(f(r)N^C\). Its meeting radius,
followed by the polynomial chart map, gives an optimal original point in a
computable box of bit length \(f(r)N^C\). Only uniform degree and
height bounds are needed to print this box; the chart need not be known.
Enlarge it by the independent native feasible-point box.

Minimize \(q_0\) over the original problem in this box using Section 5.
The boxed set is compact and nonempty. Its minimum \(\beta\) satisfies
\(\beta\ge\theta\), and

\[
                 \beta=\theta
       \quad\Longleftrightarrow\quad
           \theta\text{ is attained originally}.              \tag{9}
\]

This proves continuous attainment classification without extending a
PSD-QCQP attainment theorem to general SOC constraints. The parameter
factor in the degree-\(f(r)\) radius call need not be \(2^{O(r)}\);
the full optimization statements deliberately use a generic \(f(r)\).

With supplied integer bounds, apply the same estimates uniformly after
substituting an integer assignment. There are finitely many assignments.
A finite global infimum is the infimum of one fiber and hence has the
same uniform degree/height bound, not a product over the number of fibers.
The threshold oracle in Section 4 performs value bisection and recognition
without enumerating assignments. A uniform conditional optimizer box and
the comparison in (9) decide global attainment.

In the attained case, recover an optimal integer assignment by interval
bisection on its coordinates. For each added rational integer-coordinate
box, compute the minimum over the fixed compact continuous box. The
restricted box contains a global optimizer exactly when its minimum equals
\(\theta\). Keep a half with that property. Once all integer coordinates
are fixed, the remaining continuous problem has an attained optimum and
retains the same range parameter. The supplied integer encoding bounds the
number of bisection steps by a polynomial in input bits.

## 7. Exact continuous optimizer

Work in the compact box retained by Section 6 and let \(F\) be its
nonempty convex optimal set.

For any \(x,y\in F\), the objective is constant on their segment.
Positive semidefiniteness gives \(Q_0(x-y)=0\). Thus

\[
                         g=Q_0x+a_0               \tag{10}
\]

has one fixed value on all of \(F\). Each coordinate can be approximated
by rational affine-cut queries. Such a cut meets \(F\) exactly when
the minimum of \(q_0\) on the cut problem equals \(\theta\).
All of these are rational-data problems covered by the threshold and
value theorem.

Project \(F\) onto its nonlinear coordinates \(u\). Its projection
is compact and convex, so it has a unique point \(u_*\) of minimum
Euclidean norm. A rational constraint \(\|u\|^2\le s\) has Hessian
range contained in the original common range; it does not increase \(r\).
Using the same oracle for the optimal set, first approximate the minimum
norm, then approximate \(u_*\) by coordinate bisection on a near-minimum-norm
slice. The projection inequality bounds every point of that slice close
to \(u_*\), as in
[the exact feasible-witness construction](socp-exact-witness-recovery.md).
Restart from the original compact box for each requested precision.

Low-dimensional quartic charts and the QE theorem bound the joint
algebraic degree of \((\theta,g,u_*)\) by \(f(r)\) and its height by
\(f(r)N^C\). For \(u_*\), use its unique minimizing-point formula in
the projected optimal set; for \(g\), any bounded-size optimal chart
point gives the same gradient. The two fields have a compositum of degree
bounded by the product of their parameter-only degree bounds. Approximation
oracles and the existing
[common-field recognition procedure](constructive-common-field-recovery.md)
therefore recover these values in one field \(K\).

After fixing \(u=u_*\), all native constraints are affine in \(v\),
with rational row normals and right-hand sides in \(K\). Objective
optimality can also be expressed with rational row normals. Write
\(b=g-a_0\), and obtain any solution \(x_0\in K^n\) of
\(Q_0x_0=b\) by elimination on the rational matrix \(Q_0\). Impose

\[
 Q_0x=b,\qquad
 a_0^Tx=\theta-c_0-\tfrac12x_0^TQ_0x_0.           \tag{11}
\]

Indeed, \(Q_0x=b\) implies \(x-x_0\in\ker Q_0\), so
\(x^TQ_0x=x_0^TQ_0x_0\). Together with feasibility, (11) is
equivalent to optimality on the chosen fiber. Every coefficient matrix
in this completion problem is rational; only right-hand sides lie in
\(K\). This distinction avoids a general algebraic-coefficient LP
subroutine.

[The common-range witness construction](common-range-witness-recovery.md),
Section 5, recovers a point in such a polyhedron by approximating its
right-hand sides outward, solving rational minimum-norm QPs, and using a
rational-matrix Hoffman bound to control the limit. Active Gram-matrix
formulas put the exact limit in \(K\) and bound its coefficient height.
These right-hand sides are rational polynomials of degree at most two in
\((\theta,g,u_*)\), with polynomial-bit rational coefficients.
Clearing the square of a common integralizing denominator and bounding
conjugates preserves the same field degree and the bound \(f(r)N^C\)
on coefficient height. Include the recovered primitive generator of
\(K\) when recognizing the final tuple. The completion therefore takes
\(f(r)N^C\) bit operations and produces an optimizer in the same field.
Exact substitution checks the original native rows, cone signs, affine
rows, and objective value. These output arguments received both the fresh
whole-proof review and a separately staffed review of the field and fiber
completion steps.

## 8. Prior comparison, significance, and limits

[The common-range prior audit](common-range-fpt-prior.md) compares
low-dimensional polynomial optimization, implicit convex descriptions,
and exact quadratic programming. The
[focused objective audit](common-range-optimization-prior.md) examines
the stronger parametric-QP precedents and the objective-excluded scope.
Del Pia already gives true FPT exact
optimization for a convex quadratic objective over a mixed-integer
polyhedron. The present direction would extend that parameter guarantee
to arbitrarily many native nonlinear rows sharing a small continuous
curvature subspace. Its use of parametric QP active sets, Farkas
projection, quantitative real algebraic geometry, and the one-quadratic
oracle must all be credited as established ingredients.

There is direct prior art for the chart mechanism.
[Spjøtvold--Tøndel--Johansen (ACC 2005)](https://skoge.folk.ntnu.no/prost/proceedings/acc05/PDFs/Papers/0149_WeB08_6.pdf),
Theorem 1 and Section IV, give piecewise affine optimizer selections for
constant-matrix parametric convex QPs, including singular Hessians and
secondary minimum-norm selection. Substituting quadratic monomial
parameters yields quadratic optimizer maps and quartic values. The proof
here supplies explicit rational bit bounds and covers all lower-dimensional
parameter cases; it does not introduce that representation mechanism.

The distinction from simply appending the objective is material: a model
can use only a few nonlinear aggregate features in its constraints while
its objective penalizes every individual continuous variable. The claimed
algorithmic exponent on the explicit input length remains absolute in
this setting. This is a theoretical exactness guarantee. The radius and
precision bounds may be far too conservative for an implementation;
faster certification or useful numerical tolerances require further work.

This note does not establish publication priority or an FPT algorithm for
arbitrary nonconvex representations of convex sets. Unbounded integer
assignments can create infima not represented by one finite fiber; the
bounded-integer argument cannot silently be reused there. The linked
unbounded extension uses a separate general convex semialgebraic value
theorem to handle precisely that issue.

## Verification record

Independent mathematical work reconstructed the singular-KKT projection,
the unbounded-fiber dichotomy, the compact reciprocal gap, and the QE
degree/height import. That investigation contributed repairs, so it is
not itself a fresh independent review of the final combined manuscript.
The separate fresh review reconstructed the final proof, checked the
primary imported theorems, and tested the output construction with
arbitrary objective rank. Its scope, exact examples, and commands are
recorded in the linked review. The mathematical argument does not rely
on those examples as a substitute for proof.
A targeted inline `python -` check passed for this manuscript and its
unbounded-integer extension: 14 local links, paired math delimiters,
trailing whitespace, control characters, and final newlines. These checks
do not establish the mathematical
claims. No project-wide verification or CI inspection is used.
