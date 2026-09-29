# Succinct polynomial escape curves for convex quadratic systems

Date: 2026-09-27. Status: candidate consequence of the recession-elimination
argument. The initial fixed-integer-dimension construction passed an
[independent review](succinct-unboundedness-review.md). A stronger
integer-increment construction below passed a separate
[adversarial review](all-integer-escape-review.md).
No claim of publication priority is made.

## 1. What is being certified

An unbounded convex quadratically constrained problem need not have a
decreasing straight ray. For example, minimizing \(-z\) subject to
\(x\ge z^2\), with \(z\) integral, is unbounded below, but every feasible
recession direction has zero \(z\)-component. The
[recession-elimination proof](mixed-integer-attainment-frontier.md)
reveals a decreasing ray after suitable exact projections. This note lifts
that ray to a polynomial curve in the original variables.

The curve can have exponential degree. Its description nevertheless uses
a small arithmetic circuit: successive squaring is recorded without
expanding the resulting polynomial. The certificate records the local
projection and domination steps, so verification does not require a
general polynomial identity test on arbitrary arithmetic circuits.

Write \(w=(z,x)\in\mathbb R^{k+n}\), designate \(z\) as integral
when forming the mixed-integer restriction, and consider

\[
 q_0(w)=\tfrac12 w^TQ_0w+a_0^Tw+c_0,
 \qquad q_i(w)=\tfrac12w^TQ_iw+a_i^Tw+c_i\le0,
 \qquad Ew=e,                                      \tag{1}
\]

with rational data and \(Q_i\succeq0\), including \(i=0\). Affine
inequalities are allowed as rows with zero Hessian. Let \(N\) be the
binary input length. An arithmetic circuit below uses addition and
multiplication, a single indeterminate \(T\), and explicitly encoded
rational constants. Its output represents a polynomial, not a numerical
approximation.

**Proposition.** Suppose the continuous feasible set (1) is nonempty and
its objective is unbounded below. Given a rational \(R\ge1\), one can
construct a positive rational \(\gamma\) and a polynomial vector
\(p(T)\), represented by an arithmetic circuit, such that

\[
 p(0)=0,\qquad p(T)\in\mathbb Z[T]^{k+n},          \tag{2}
\]

and, for **every** continuously feasible anchor \(a\) with
\(\|a\|_\infty\le R\),

\[
 a+p(T)\text{ is continuously feasible for every real }T\ge1,
 \qquad q_0(a+p(T))=q_0(a)-\gamma T.                \tag{3}
\]

If the anchor has the designated integer coordinates integral, so does
the curve at every integer parameter. Every integer sample in fact
belongs to the same translate \(a+\mathbb Z^{k+n}\). If recession
elimination removes \(\ell\) variables before finding its decreasing
ray, then

\[
                  \deg p\le 2^{\ell+1}-1.         \tag{4}
\]

Construction time, circuit size, and the bit lengths of its constants are
polynomial in \(N+\operatorname{bits}(R)\), without restricting \(k\)
or the continuous Hessian span. The procedure assumes continuous
unboundedness and
feasibility as in the statement; recession elimination itself supplies
the indicated decreasing ray under those assumptions.

The output circuit need not have small expanded coefficients. It also does
not supply a rational anchor: rational convex quadratic systems can have
no rational feasible point.

**Conditional boundedness corollary.** If the mixed-integer feasible set
is nonempty, its objective is unbounded below if and only if the continuous
relaxation's objective is unbounded below. Conditional on this feasibility
promise, rational linear programming decides boundedness in polynomial
time, without fixing either parameter. This does not decide feasibility.
The forward implication follows by inclusion; the reverse implication
uses any mixed-integer feasible anchor in (3), with a sufficiently large
radius. Neither the radius nor the anchor needs to be known to the
conditional boundedness algorithm. Older literature explicitly studies
this equivalence and already supplies polynomial-time boundedness
procedures by linear programming. In particular,
[Obuchowska (2008), Algorithm A, Theorem 5.1 and Corollary 5.1](https://link.springer.com/content/pdf/10.1007/s00186-007-0196-3.pdf)
establish those conclusions, with the polynomial-time statement on p. 466
and the mixed-integer extension discussed on p. 447. Neither conclusion
is new here; the [prior audit](succinct-unboundedness-prior.md) compares
the assumptions. The proposed addition is the explicit integer-coefficient
circuit and its local verification format.

## 2. The projection trace

For any nonempty objective sublevel, its recession cone is

\[
 \{d:Q_i d=0,\ a_i^Td\le0\ (i\ge1),\ Ed=0,
                         Q_0d=0,\ a_0^Td\le0\}.   \tag{5}
\]

This is a rational polyhedral cone. If it contains a direction with
negative objective slope, rational linear programming finds such a
direction. Clearing all denominators makes every component integral.
Otherwise every direction has zero objective slope.

Treat every coordinate as continuous during these projections. A nonzero
rational zero-slope direction can be eliminated exactly over the reals.
At a single such step, write the old coordinates as

\[
                   w=A y+d s.                     \tag{6}
\]

Every inequality has the form

\[
                   r_i(y)+\alpha_i s\le0,
 \qquad \alpha_i\le0,                             \tag{7}
\]

and the objective and all equations are independent of \(s\). Retain
the rows with \(\alpha_i=0\) and delete the rows with
\(\alpha_i<0\). For every retained feasible \(y\), the deleted rows
hold for sufficiently large \(s\).

Choose any index \(j\) with \(d_j\ne0\), and use the literal section
\(w_j=0\). Then \(A\) is the zero-one coordinate insertion matrix,
and the removed scalar is \(s=w_j/d_j\). There are rational linear maps

\[
                    y=P w,\qquad s=b^Tw.          \tag{8}
\]

The projected anchor need not retain any integrality. This is harmless:
the construction below ultimately adds integer increments to the original
anchor. These continuous projections are not being used to preserve the
full set of mixed-integer objective values. That stronger property remains
the role of the lattice-preserving reductions in the linked finite-value
and attainment proof.

Continue until a decreasing direction is found. If instead the recession
cone becomes zero, a nonempty objective sublevel is compact, contradicting
unboundedness. Thus the process has at most \(n+k\) eliminations and
terminates with a rational direction \(d_*\) such that

\[
 Q_{0,*}d_*=0,\qquad a_{0,*}^Td_*=-\gamma<0.       \tag{9}
\]

Every elimination only deletes a variable from the retained polynomials,
so it creates no coefficient growth there. There are at most \(n+k\)
eliminations. Rational LP bounds therefore give polynomial bit length in
\(N\) for every direction, section, projection, and reduced polynomial
in this trace, without fixing \(k\).

The products of the matrices in (8) also have polynomial bit length.
Indeed, there are at most \(n+k\) matrices, each of
polynomial size and bit length; rational matrix products have bit length
bounded by the sum of these lengths plus the logarithms of the intervening
dimensions. Consequently the original radius \(R\) gives uniform
integer bounds, of polynomial bit length, on every projected anchor and
every removed anchor scalar. These bounds use absolute row sums and do
not require knowing an anchor's exact coordinates.

## 3. Lifting without losing integrality

Fix any feasible anchor \(a\) in the supplied box, and project it
through the trace. Denote the projected anchors at a particular step by
\(w^0=A y^0+d s^0\). The circuit construction uses bounds on these
quantities and is the same for every such \(a\).

At the terminal problem start with the increment

\[
                    p_*(T)=T d_*.
\]

Here \(d_*\) has already been multiplied by a positive common
denominator so that all its coordinates are integers; \(\gamma\) in
(9) is the corresponding scaled objective decrease.

Choose an integer \(M\ge1\) bounding both the terminal anchor's
coordinate magnitudes and those of \(d_*\), uniformly over the
original anchor box. Then

\[
                    B_*(T)=M(1+T)
\]

has nonnegative integer coefficients and bounds every terminal coordinate
in magnitude for real \(T\ge0\).

Now reverse one projection step. Suppose the current increment \(p_y\)
and an integer polynomial \(B\), with nonnegative coefficients, satisfy

\[
 B(T)\ge1,\qquad
 \|y^0+p_y(T)\|_\infty\le B(T)\quad(T\ge0).       \tag{10}
\]

Let \(M_s\ge1\) be an integer upper bound on \(|s^0|\). Expand
each deleted row \(r_i\) into its quadratic monomials and let \(H_i\)
be the sum of the absolute values of its rational coefficients. Since
\(B\ge1\),

\[
 |r_i(y)|\le H_i B^2
 \quad\text{whenever }\|y\|_\infty\le B.
\]

Write \(\beta_i=-\alpha_i>0\), and choose an integer

\[
 C\ge1+M_s+\max_{\alpha_i<0}H_i/\beta_i,           \tag{11}
\]

with maximum zero if no row is deleted. Choose a positive integer \(D\)
clearing all denominators of \(d\), and define

\[
 P_s(T)=D C T(1+B(T)^2),\qquad
 p_w(T)=A p_y(T)+d P_s(T).                         \tag{12}
\]

The reconstructed point is

\[
 w^0+p_w(T)=A(y^0+p_y(T))+d(s^0+P_s(T)).
\]

For every deleted row and real \(T\ge1\), its value is at most

\[
 H_i B(T)^2+\beta_i M_s
               -\beta_i D C T(1+B(T)^2)\le0.       \tag{13}
\]

Rows with zero slope and all equations hold by the induction hypothesis.
The increment \(p_w\) has integer coefficients in every coordinate:
\(A\) is an insertion matrix, \(p_y\) has integer coefficients by
induction, and \(dD\) is an integer vector. The removed scalar
\(s^0\) need not be integral; neither does the projected anchor.
Only the original anchor's designated integer coordinates matter.
Induction proves continuous feasibility and the integer-increment claim.

The output circuit can use only integer constants: precompute the integer
vector \(g=Dd\) and assemble the increment as
\(A p_y+g C T(1+B^2)\). The proof trace still contains the rational
recession direction and projection maps.

This integer polynomial majorant is essential. Substituting
\(C(1+\|y(T)\|^2)\) directly for an eliminated integer coordinate
would generally give an irrational number when the anchor is algebraic.

For the next bound, choose an integer

\[
 L\ge\max\{1,\max_j\sum_l|A_{jl}|,\max_j|d_j|\}.
\]

Then the polynomial

\[
 B_w(T)=L\bigl(B(T)+M_s+D C T(1+B(T)^2)\bigr)      \tag{14}
\]

has nonnegative integer coefficients and bounds every reconstructed
coordinate for all real \(T\ge0\). This bound does not assert
feasibility for \(0<T<1\), which is unnecessary.

Every increment has zero constant term, and every coefficient is integral.
Each reversed step preserves the
objective exactly. Equation (9) proves (3).

Starting with degree one, (12)--(14) increase the maximum degree from
\(D\) to at most \(2D+1\), proving (4). Each step adds a bounded
number of scalar arithmetic gates for its majorant and a polynomial
number of gates for its matrix-vector reconstruction. The constants
\(D,C,L,M_s,M\) have polynomial bit length, by the trace bounds and
(11). They do not include the expanded coefficients of
\(B\) or \(p\). This proves the asserted circuit bound.

## 4. Algebraic anchors and certificate scope

Let

\[
 h=\dim_{\mathbb Q}\operatorname{span}
                    \{\nabla^2_{xx}q_i:i\ge1\}.
\]

For fixed \(k,h\), the existing
[integer-witness theorem](unbounded-integer-frontier.md) and
[algebraic continuous recovery theorem](algebraic-witness-recovery.md)
provide an exactly feasible anchor: its integer coordinates have
polynomial bit length, its continuous coordinates belong to one real
number field of polynomial degree, and their individual minimal-polynomial
coefficient bit lengths are polynomial. Their Cauchy bounds supply an
appropriate radius \(R\) with polynomial bit length. The completed
[common-field recovery construction](constructive-common-field-recovery.md),
which passed an [independent review](constructive-common-field-review.md),
converts the canonical continuous point into a single real algebraic root
\(\alpha\), specified by an integer polynomial and a rational isolating
interval, and rational polynomials \(b_j\) such that
\(x_j=b_j(\alpha)\). This conversion has polynomial bit complexity
and output size for fixed \(k,h\).

**Complete unboundedness certificate.** For fixed \(k,h\), an unbounded
mixed-integer instance has a polynomial-size certificate that can be
constructed and independently verified in polynomial time. It consists
of an explicitly integral vector \(z\), the common-field representation
of a feasible continuous anchor, a rational anchor radius \(R\), the
rational projection trace, and the integer escape circuit. The verifier
does not need an optimization or feasibility oracle.

The algebraic field is needed only for the anchor. Every nonconstant
coefficient of the escape curve is integral, including in its continuous
coordinates. The proposition gives a stronger description than an
arbitrary curve with algebraic coefficients. A small exact anchor remains
the reason for fixing \(k,h\) in this complete certificate statement;
the construction of the increment circuit itself has no such restriction.

The local escape proof can be checked by rational linear algebra,
coefficient comparisons, PSD verification, and the inequalities defining
the recorded constants. In particular, the verifier checks the local
identities (6)--(9) at quadratic degree and checks that the submitted
circuits were assembled by (12)--(14). It does not expand the final
polynomials or invoke deterministic identity testing for unrestricted
circuits.

The common-field representation completes the remaining anchor check.
Substituting \(x_j=b_j(\alpha)\) into every original affine or
quadratic row gives univariate sign queries of polynomial degree and
coefficient bit length. Standard exact sign determination at the selected
root checks those rows and the radius bound in polynomial time, as proved
in Section 7 of the common-field note. The verifier checks the root
isolator and uses squarefree parts and polynomial gcds for exact zeros;
it need not trust an irreducibility or minimal-polynomial label supplied
with the certificate. The integer assignment is explicit and is checked
directly. These checks establish an exactly feasible anchor, after which
the verified local escape trace proves objective values tending to minus
infinity at integer parameter values. This is an unboundedness certificate;
it makes no claim about certificates of finite mixed-integer optimality.

## 5. Necessary qualifications

An entirely rational curve, including its constant term, need not exist.
Take the rational convex quadratic singleton described in the
[Hessian-span review](hessian-span-review.md), whose coordinates are
\((\sqrt[3]{2},\sqrt[3]{4})\), and take its product with an unrestricted
integer variable \(z\), minimizing \(-z\). Every feasible curve has
the same irrational first two coordinates. This example rules out a
rational-point or rational-constant promise, while permitting the anchored
rational increments above.

Rational problem data are essential for the integer-translation conclusion.
With two integer variables, the irrational-coefficient convex constraint
\((x-\sqrt2 z)^2\le0\) has only the feasible integer point \((0,0)\),
whereas minimizing \(-z\) over its continuous relaxation is unbounded
below. Thus even the conditional boundedness equivalence fails if the
data are allowed to be arbitrary real numbers.

Exponential degree can also be unavoidable. For one integer variable
\(z\) and continuous variables \(x_1,\ldots,x_m\), impose

\[
 z^2\le x_1,\qquad x_{j-1}^2\le x_j\ (2\le j\le m),
 \qquad\min -z.                                    \tag{15}
\]

Every row is jointly convex quadratic. A polynomial escape curve whose
objective is affine and strictly decreasing has
\(z(T)=a+bT\), \(b>0\). Feasibility for all sufficiently large
integer \(T\) gives \(x_j(T)\ge z(T)^{2^j}\), so
\(\deg x_m\ge2^m\). A straight-line circuit using repeated squaring
has only \(O(m)\) gates. This is a limitation of dense polynomial
output, not a hardness result. The continuous Hessian span in this
example grows with \(m\), so it does not establish such a degree
lower bound at fixed \(h\).

The construction explains one way to certify unboundedness when no
original decreasing ray exists. Its conditional boundedness algorithm
does not require fixed parameters, but feasibility remains a separate
problem. No computational speedup is established. The
[prior audit](succinct-unboundedness-prior.md) compares general
semialgebraic curve selection and existing polynomial escape-curve work,
and identifies the directly relevant older boundedness results. Priority
for the explicit circuit statement remains unestablished. This is a
supporting constructive refinement, not a new boundedness classification.

An open quantitative question is whether the degree of an escape curve
can be bounded using the integer dimension and continuous Hessian span,
instead of the total number of projection steps. The nested-chain example
does not rule this out. The present proof uniformly squares its majorant
at every step and establishes no sharper parameter-dependent degree bound.

## Verification record

The universal assertions rest on the explicit proof above and independent
reviews. The targeted command
`python research-20260927/check_succinct_unboundedness_curves.py` passed
exact checks of nested quadratic lifts, an integer coordinate shear, an
algebraic anchor, denominator clearing with a noninteger projected anchor,
and the degree recurrence. Its small-parameter example
confirms that the displayed envelope need not remain feasible for
\(0<T<1\). These checks do not prove the general theorem. No
project-wide tests, CI inspection, or Lean verification were performed.
A targeted inline Python document check also passed for this note and its
three review/audit notes: thirteen local links, final newlines, trailing
whitespace, and control characters.
