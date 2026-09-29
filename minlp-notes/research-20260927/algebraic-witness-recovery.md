# Exact algebraic feasible points at fixed Hessian span

Date: 2026-09-27. Status: candidate theorem; independent
[proof](algebraic-witness-review.md) and
[source](algebraic-recognition-source-review.md) reviews found no gap.
The recovery step uses an established algebraic
recognition algorithm. Priority for the combined optimization statement
has not been established.

## 1. What the result adds

The [exact-feasibility theorem](hessian-span-exact-feasibility.md) decides
whether a rational convex quadratic system has a feasible point, even
when its feasible set has empty interior or contains no rational point.
Its numerical output need only satisfy relaxed inequalities. This note
upgrades that decision theorem to construction of an exactly feasible
point, described by real algebraic coordinates.

Let

\[
 F=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0\ (i=1,\ldots,m)\},
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
\]

where all data are rational and every \(Q_i\succeq0\). Let \(N\ge2\)
be the explicit binary input length and

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

No coordinate bounds, Slater condition, or rational-point promise are
required. If \(F\ne\varnothing\), let \(x^*\) be its unique point of
minimum Euclidean norm.

**Proposed theorem.** For every coordinate \(j\), the number \(x_j^*\)
has degree and minimal-polynomial coefficient bit lengths at most
\(N^{O(h+1)}\). There is a deterministic algorithm, polynomial in \(N\)
for fixed \(h\), which decides whether \(F\) is empty and otherwise
returns every coordinate of \(x^*\) as a primitive integer minimal
polynomial and a rational interval containing exactly its selected real
root. A conservative bound for the complete algorithm is
\(N^{O((h+1)^2)}\) bit operations.

The output is an exact coordinatewise description of one common feasible
point. It does not claim that the rational approximations used during the
algorithm belong to \(F\). It also does not yet supply an exact optimizer
for an arbitrary convex objective.

## 2. Coordinate degree and height without a boundedness assumption

The nonempty closed convex set \(F\) has a unique minimum-norm point:
existence follows by intersecting a norm sublevel set through any feasible
point, and strict convexity gives uniqueness. Minimize
\(f(x)=\|x\|_2^2\).

Apply the active affine restriction in Steps 1 and 2 of the
[Hessian-span value proof](hessian-span-reduction.md). At \(x^*\), turn
active affine inequalities into equations, retain active native quadratic
inequalities, and delete the inactive inequalities. The segment argument
in that proof preserves the minimum value. Next express every retained
Hessian in a retained basis of at most \(h\) Hessians and impose the
affine differences between the corresponding whole polynomials. All
these differences vanish at \(x^*\), so the optimum is unchanged.

Rational elimination gives an affine chart

\[
 x=x_0+Vu,\qquad u\in\mathbb R^d,
\]

whose coefficients have polynomial bit length in \(N\), independently
of the unknown coordinates of \(x^*\). The matrix \(V\) has full column
rank. The retained convex quadratic polynomials satisfy

\[
 \widetilde q_i=\sum_{j\in B}c_{ij}\widetilde q_j,
 \qquad |B|\le h,
\]

as identities including their affine and constant terms. If \(d=0\),
the chart is a rational point and the result is immediate. Otherwise

\[
 \widetilde f(u)=\|x_0+Vu\|_2^2
\]

is coercive and strictly convex, with positive definite Hessian
\(2V^TV\). Its unique minimizer over the restricted system maps to
\(x^*\).

For \(0<\varepsilon<1\), relax every retained native row to
\(\widetilde q_i(u)\le\varepsilon\), and minimize the same
\(\widetilde f\). The old optimizer is strictly feasible. Coercivity
gives a unique optimizer \(u_\varepsilon\); Slater's condition gives
nonnegative KKT multipliers. Moreover,

\[
 \|x_0+Vu_\varepsilon\|_2^2\le\|x^*\|_2^2.
\]

This is a uniform compact bound for the purpose of a convergence proof;
its numerical value need not be known. Every accumulation point as
\(\varepsilon\downarrow0\) is feasible for the restricted system and
has norm at most \(\|x^*\|\). Uniqueness then gives
\(x_0+Vu_\varepsilon\to x^*\). No auxiliary ball and no objective
regularization are needed here.

The same conic support reduction as in the value proof keeps at most
\(h\) native multipliers. Choose one support \(J\), \(|J|\le h\),
occurring along a sequence \(\varepsilon\downarrow0\). Stationarity
is

\[
 M u=-a_f-\sum_{i\in J}\lambda_i a_i,
 \qquad
 M=2V^TV+\sum_{i\in J}\lambda_i\widetilde Q_i\succ0.
\]

Set \(\Delta=\det M>0\) and
\(p=-\operatorname{adj}(M)(a_f+\sum_{i\in J}\lambda_i a_i)\),
so \(u=p/\Delta\). Clearing denominators in all retained primal
inequalities and in complementarity gives a polynomial KKT formula
\(\mathcal K_J(\varepsilon,\lambda)\), including \(\Delta>0\) and
\(\lambda_i\ge0\). It contains every retained
primal row, including those outside \(J\). Every solution reconstructs
the unique relaxed optimum, since the problem is convex. Degrees are
\(O(N)\), coefficient bit lengths are polynomial in \(N\), and the
number of polynomials is polynomial in \(N\).

For original coordinate \(j\), put

\[
 P_j=x_{0,j}\Delta+(Vp)_j.
\]

The formula

\[
 \forall\gamma\;\left[\gamma\le0\ \lor\
   \exists\varepsilon,\lambda\;
   \left(0<\varepsilon<1,\ \varepsilon<\gamma,
     -\gamma\Delta<P_j-a\Delta<\gamma\Delta,
     \mathcal K_J(\varepsilon,\lambda)\right)\right]
                                                        \tag{1}
\]

defines exactly the singleton \(\{x_j^*\}\). One direction uses the
fixed-support sequence, and the other uses convergence of every relaxed
optimizer to \(x^*\). Divergence of the multipliers causes no difficulty.

There are two quantified blocks of sizes \(1\) and at most \(h+1\),
and one free scalar. The coefficient-sensitive block quantifier
elimination theorem used in the value proof, Basu--Pollack--Roy
Theorem 14.16, therefore gives an integer annihilating polynomial for
\(x_j^*\) of degree and coefficient bit lengths \(N^{O(h+1)}\).
After removing zero polynomials, at least one polynomial in the resulting
singleton formula must vanish at its point: otherwise all signs would be
locally constant. This does not require discovering the unknown chart or
support algorithmically.

An elementary factor bound transfers this conclusion to the primitive
minimal polynomial. If an integer annihilator has degree at most \(D\)
and coefficient magnitudes at most \(2^B\), all its roots have modulus
at most \(1+2^B\). The primitive minimal polynomial divides it over
the integers after removal of content, by Gauss's lemma. Its leading
coefficient is at most \(2^B\) in absolute value, and its roots are a
subset of the annihilator's roots. Expanding their product bounds its
coefficients by

\[
 2^B\,2^D(1+2^B)^D.
\]

Thus its coefficient bit lengths remain \(N^{O(h+1)}\).

The same Cauchy bound supplies a computable universal radius

\[
 F\ne\varnothing\quad\Longrightarrow\quad
 x^*\in[-R,R]^n,\qquad R=2^{N^{C(h+1)}},             \tag{2}
\]

for a sufficiently large absolute constant \(C\). This is also a
small-point proof for removing continuous boundedness assumptions. The
constants are effective consequences of the elimination theorem; the
statement is a complexity bound, not a calibrated numerical estimate.

## 3. Certified approximation from rational feasibility queries

Append the box in (2). The bounded exact-feasibility algorithm decides
whether it intersects \(F\), and hence whether \(F\) is empty. Assume
it is nonempty, and write \(\theta=\|x^*\|_2^2\).

For a supplied rational \(0<\tau\le1\), the following procedure
returns a rational vector \(c\) with
\(\|c-x^*\|_\infty<\tau\).

First binary-search \(\theta\) in \([0,nR^2]\), using exact
feasibility queries for

\[
 F\cap[-R,R]^n\cap\{x:\|x\|_2^2\le s\}
                                                        \tag{3}
\]

at rational thresholds \(s\). Maintain a feasible upper threshold
\(b\). Stop when the enclosing value interval has width at most
\(\tau^2/16\), and define \(K\) by (3) with \(s=b\). Then
\(K\ne\varnothing\) and \(b\le\theta+\tau^2/16\). The new
norm inequality increases the Hessian-span dimension by at most one.

The minimum-norm projection inequality is

\[
 \langle x^*,x-x^*\rangle\ge0\quad(x\in F).
\]

It follows by differentiating the norm squared along the feasible
segment from \(x^*\) toward \(x\). Consequently,

\[
 \|x-x^*\|_2^2
 \le\|x\|_2^2-\|x^*\|_2^2\le\tau^2/16
 \qquad(x\in K).                                   \tag{4}
\]

Next bisect rational coordinate intervals inside the original box,
always preserving nonempty intersection with \(K\). At a midpoint
\(m\) for coordinate \(j\), query feasibility with \(x_j\le m\)
in the current box. If feasible, keep its lower half. Otherwise keep its
upper half, whose closed boundary is harmless. Repeat until every
interval has width at most \(\tau\), and let \(c\) be the box
midpoint. Some \(y\in K\) belongs to that box, even though no such
point has been explicitly constructed. Therefore

\[
 |c_j-x_j^*|\le |c_j-y_j|+|y_j-x_j^*|
 \le\tau/2+\tau/4<\tau
\]

for every \(j\). All feasibility queries use only rational data,
affine added bounds, and the one norm Hessian. They need no interior
promise. Their number and input bit lengths are polynomial in
\(N^{O(h+1)}+\log(1/\tau)\). For fixed \(h\), the approximation
procedure is polynomial in the requested number of accuracy bits.

## 4. Turning approximations into exact coordinates

The classical algorithm of Kannan, A. K. Lenstra, and Lovász supplies
the remaining step. Their 1988 paper, *Polynomial Factorization and
Nonrandomness of Bits of Algebraic and Some Transcendental Numbers*,
[Theorem 1.19, printed p. 241](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf),
recovers the minimal polynomial of an algebraic number from sufficiently
accurate rational approximation and bounds on its degree and height.
If these bounds are \(D\) and \(A\), it suffices to choose an integer
\(s\) with

\[
 2^s>2^{D^2/2}(D+1)^{(3D+4)/2}A^{2D}
\]

and supply approximation error less than \(2^{-s}/(12D)\). The
algorithm is deterministic and polynomial in \(D\) and \(\log A\)
in the bit model. The theorem also handles numbers of modulus greater
than one, by reciprocal transformation within its proof.

Here \(D,\log A\le N^{O(h+1)}\), so Section 3 supplies the required
approximations in polynomial time for fixed \(h\). Apply the algorithm
to every coordinate.

A polynomial alone does not choose a real conjugate. This can be fixed
with another certified approximation. Let the returned primitive minimal
polynomial have degree at most \(D\) and coefficient magnitudes at most
\(2^H\), with \(H\ge1\). Its roots have modulus at most
\(1+2^H\). If its degree is at least two, its nonzero integer
discriminant, expressed as its leading coefficient to power \(2d-2\)
times the product of all squared root differences, yields the conservative
separation bound

\[
 |\alpha-\beta|>\delta:=2^{-4D^2(H+2)}
 \quad\text{for distinct roots }\alpha,\beta.         \tag{5}
\]

For degree one the conclusion about a selected root is immediate. Obtain
a rational approximation \(a\) with error less than \(\delta/8\)
and return

\[
 \left(p,[a-\delta/4,a+\delta/4]\right).
\]

The coordinate lies strictly inside this interval, and (5) excludes every
other root. The interval and polynomial thus specify the exact intended
coordinate. All outputs refer to the same \(x^*\), because the common
approximation procedure was proved to converge to that unique point.

Combining the polynomial-size degree and height bounds with the bounded
decision oracle gives the conservative overall bound
\(N^{O((h+1)^2)}\). A sharper dependence on \(h\) would require
retaining separate coefficient-height parameters throughout the oracle
analysis; it is not asserted here.

## 5. A common-field degree bound

For this particular canonical point, a further argument bounds the degree
of the whole field

\[
 K=\mathbb Q(x_1^*,\ldots,x_n^*).
\]

Apply formula (1) to a rational linear form \(c^Tx^*\), replacing
\(P_j\) by \(c^T(x_0\Delta+Vp)\). The coefficient magnitudes now
depend on \(c\), but the number of polynomials, their degrees, and the
quantifier-block sizes do not. The degree conclusion of quantifier
elimination is independent of coefficient magnitudes. Thus one uniform
bound \(D=N^{O(h+1)}\) bounds the degree of every rational linear
combination of the coordinates, without a bound on the bit length of
\(c\).

Since characteristic zero is separable, the primitive element theorem
provides such a linear combination generating \(K\). Hence

\[
 [K:\mathbb Q]\le D.                                  \tag{6}
\]

This uses the uniform linear-form bound, rather than inferring (6) from
the degrees of the coordinates separately.

A primitive element can also be identified in polynomial time for fixed
\(h\), with no number-field factorization needed. Consider

\[
 \alpha_k=\sum_{j=1}^n k^{j-1}x_j^*,\qquad
 k=0,\ldots,(n-1)D(D-1)/2,
\]

where \(k^0=1\). If \(d=[K:\mathbb Q]\), the field has \(d\)
distinct complex embeddings. For each pair of distinct embeddings, the
difference between their images of \(\alpha_k\) is a nonzero polynomial
in \(k\) of degree at most \(n-1\): otherwise they agree on every
coordinate and hence on \(K\). At most \((n-1)d(d-1)/2\) values of
\(k\) fail to separate some pair. Thus at least one candidate has
\(d\) distinct conjugates and generates \(K\).

The candidate coefficient bit lengths are polynomial in \(N\) and
\(\log D\). The height bound obtained from (1) remains
\(N^{O(h+1)}\) for these candidates. Section 3 supplies arbitrarily
accurate approximations to them by rational linear arithmetic, so KLL
recovers each minimal polynomial. A candidate of largest degree is a
primitive element, and Section 4 selects its intended real embedding.

This additionally produces a primitive generator as a specified rational
linear combination of the coordinates and as a real algebraic number.
The subsequent [common-field construction](constructive-common-field-recovery.md)
converts every coordinate into a rational polynomial in that generator in
polynomial time for fixed \(h\). Its independent review checks the
conversion and the bit bounds needed to verify feasibility by univariate
sign evaluation. The proof above supplies the degree, height, and certified
approximation inputs for that construction.

## 6. Scope, significance, and open work

The point of this result is exact construction on degenerate convex
quadratic systems. It closes the gap between deciding feasibility and
returning an exactly feasible point for this structural parameter. The
coordinates need not be rational: the irrational singleton in the
[independent Hessian-span review](hessian-span-review.md) demonstrates
why a rational-output promise would be false.

For a bounded-integer mixed-integer system whose convex continuous
Hessians have fixed span, any exactly feasible integer assignment can
be followed by this continuous recovery procedure on its rational slice.
Combined with the fixed-integer-dimension algorithm in the
[MILP projection note](mixed-integer-span-frontier.md), this returns
an exact mixed-integer feasible point. Its continuous output uses real
algebraic coordinates and is not the approximate lifted MILP solution.

The algebraic recognition algorithm, projection inequality, bisection,
and the use of a minimum-norm canonical point are established methods.
The candidate addition is the uniform coordinate degree and height bound
controlled by the span of the native Hessians, together with its use in
the exact-feasibility oracle. No source search so far establishes
publication priority for that combination. The closest comparisons remain
those recorded in [the Hessian-span prior-art audit](hessian-span-prior.md).

There is an older exact-optimization antecedent to the use of algebraic
degree and height bounds followed by decision bisection: Chandrasekaran
and Tamir, *Optimization problems with algebraic solutions: quadratic
fractional programs and ratio games*, Mathematical Programming 30 (1984),
326--339, [pp. 326--328](https://www.tau.ac.il/~atamir/opt_84.pdf).
That mechanism is not claimed as new here. Their stated problem classes
differ from the present arbitrary-dimensional convex quadratic systems
with bounded Hessian-span dimension. The local prior-art scout inspected
these pages; this note relies on that recorded comparison rather than a
claim that the 1984 paper has been exhaustively screened.

An individual-coordinate representation does not in general bound a
vector's joint number-field degree or make arbitrary multivariate sign
evaluation efficient. Section 5 supplies an additional argument for the
degree bound in this setting; the subsequent
[common-field construction](constructive-common-field-recovery.md) supplies
the coordinate conversion and polynomial-time feasibility verification.
Exact optimization of
a general convex objective
also requires a further argument: an irrational optimal-value threshold
cannot simply be passed to the rational-input feasibility oracle.

Verification for this theorem consists of symbolic proof review and
inspection of the cited primary algorithm. No computational experiment or
Lean formalization is claimed to certify the universal theorem.
The author ran a targeted Python document check on this note and its two
linked review notes: all ten local links, math delimiters, final newlines,
control characters, and trailing whitespace passed. No project-wide
verification or CI inspection was run.
