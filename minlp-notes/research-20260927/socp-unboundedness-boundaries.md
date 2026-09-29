# Two boundaries for unbounded rational mixed-integer SOCP

Date: 2026-09-28. Status: elementary supporting counterexamples; independently
checked by a reviewer. No novelty claim is made. The first phenomenon has
explicit prior examples in the literature, discussed below.

Rational second-order cone data do not give the unboundedness properties
available for native convex quadratic inequalities. Even two cone rows with
one squared-Hessian direction can separate integer and continuous
unboundedness. A closely related system is integer-unbounded but has no
nonconstant polynomial parametrization with rational coefficients. These are
scope limits for extending the
[convex quadratic escape-curve result](succinct-unboundedness-curves.md),
not objections to the separate
[unbounded MISOCP feasibility theorem](unbounded-misocp-frontier.md).

## 1. A rational cone system with an irrational feasible ray

Consider the rational SOC system in coordinates \((x,z)\):

\[
 \|(z,z)\|_2\le x,\qquad \|(x,x)\|_2\le 2z.       \tag{1}
\]

The first row implies \(x\ge0\), and the second implies \(z\ge0\).
With these signs, the two rows become

\[
 \sqrt2 z\le x,\qquad \sqrt2 x\le2z.
\]

Thus the continuous feasible set is exactly

\[
                  \{(\sqrt2 t,t):t\ge0\}.                  \tag{2}
\]

Minimizing the rational linear objective \(-z\) over (2) is unbounded
below. If both \(x\) and \(z\) are integral, the only feasible point
is \((0,0)\): a nonzero integer \(z\) would make
\(\sqrt2=x/z\) rational. Hence the integer problem is feasible and
has minimum zero, while its continuous relaxation is unbounded below.

The squared residuals are

\[
 q_1=2z^2-x^2,\qquad q_2=2x^2-4z^2=-2q_1.
\]

Their full Hessians, in the coordinate order \((x,z)\), are

\[
 H_1=\operatorname{diag}(-2,4),\qquad H_2=-2H_1.             \tag{3}
\]

The full squared-Hessian span therefore has dimension one. With both
coordinates designated integral, the continuous Hessian blocks have span
zero. A free continuous coordinate can be appended if a nonempty continuous
block is desired; the same objective conclusion holds.

The signs preceding the squaring step are essential. The quadratic
equalities alone also contain the opposite ray, which is not feasible for
(1). Both Hessians in (3) are indefinite. Thus (1) does not satisfy the
native positive-semidefinite Hessian assumptions of the convex quadratic
unboundedness theorem.

## 2. An integer-unbounded strip without polynomial escape

Now impose

\[
 z\ge1,\quad x\ge1,\quad
 \|(z,z)\|_2\le x,\quad
 \|(x-1,x-1)\|_2\le2z.                                  \tag{4}
\]

All coefficients remain rational. Since \(z\ge1\) and \(x\ge1\),
the absolute values in the norms have known signs. Consequently (4) is
equivalent to

\[
 z\ge1,\qquad \sqrt2 z\le x\le\sqrt2 z+1.                \tag{5}
\]

The separate bound \(x\ge1\) is redundant in (5), but makes the branch
choice in (4) explicit. For every positive integer \(z\), the integer
point

\[
                       x=\lceil\sqrt2 z\rceil             \tag{6}
\]

satisfies (5). Thus minimizing \(-z\) over the integer points is
unbounded below. The point \((x,z)=(3,2)\) strictly satisfies every
inequality in (4), so this obstruction does not require failure of strict
feasibility.

**Proposition.** Fix any real anchor \(a=(a_x,a_z)\), and let
\(P,Q\in\mathbb Q[T]\). If

\[
                    (a_x+P(T),a_z+Q(T))                  \tag{7}
\]

belongs to (5) for every sufficiently large integer \(T\), then both
\(P\) and \(Q\) are constant.

**Proof.** Feasibility bounds the real polynomial

\[
 R(T)=a_x-\sqrt2 a_z+P(T)-\sqrt2 Q(T)
\]

between zero and one on all sufficiently large integers. A nonconstant
real polynomial has unbounded absolute value along the positive integers,
so \(R\) is constant. For every positive degree \(j\), its coefficient
therefore gives

\[
                  p_j=\sqrt2 q_j,
                  \qquad p_j,q_j\in\mathbb Q.
\]

Irrationality of \(\sqrt2\) forces \(p_j=q_j=0\). This proves the
claim. \(\square\)

In particular, no integer-coefficient polynomial increment from any fixed
feasible anchor can certify objective escape, regardless of polynomial
degree or arithmetic-circuit size. Requiring feasibility for all large real
parameters is an even stronger condition and is also impossible.

There is no escape by using real polynomial coefficients while requiring
integer coordinates at every sufficiently large integer parameter. A
polynomial of degree at most \(d\) taking integer values at \(d+1\)
distinct integer arguments has rational coefficients, by inversion of the
rational Vandermonde matrix. Applying this to both coordinate polynomials
reduces that case to the proposition.

This is a limitation on polynomial parametrizations, not on all short
certificates. The explicit sequence (6) is already simple. It can also be
written using only an integer square root:

\[
                 x=\lfloor\sqrt{2z^2}\rfloor+1
                 \qquad(z\in\mathbb Z_{\ge1}).            \tag{8}
\]

The irrationality of \(\sqrt2 z\) makes (6) and (8) equal. A certificate
format permitting rounding operations could express this particular escape
sequence; the example does not establish a general certificate theorem
with such operations.

The squared residuals in (4) are \(2z^2-x^2\) and
\(2(x-1)^2-4z^2\), with the same negatively proportional Hessians as
in (3). The full span remains one, and the continuous span remains zero
when both coordinates are integral. Appending a free continuous variable
allows irrelevant nonconstant curves in that variable, but still cannot
give objective escape through polynomial changes in \((x,z)\).

## 3. Prior results and the precise distinction

[Morán, Dey, and Vielma, *Strong Dual for Conic Mixed-Integer Programs*
(2011), §4.1, Examples 1–2](https://optimization-online.org/wp-content/uploads/2011/07/3096.pdf)
already show failure of integer/continuous boundedness equivalence. Their
first example uses an irrational line. Their second has rational conic
quadratic representability and a full-dimensional feasible set. Thus the
general failure in Section 1 is established prior knowledge. The two-row
presentation here records it directly at squared-Hessian span one.

The same source's Proposition 2 restores equivalence for a convex set with
an interior mixed-integer feasible point. This is consistent with the
strip: both its integer and continuous objectives are unbounded. Section 2
shows that this interior-point condition alone does not supply polynomial
escape curves with rational coefficients.

The [convex quadratic note](succinct-unboundedness-curves.md) records the
older conditional boundedness equivalence for rational native convex
quadratics and its additional proposed polynomial-curve certificate.
Neither statement extends automatically to arbitrary rational SOC systems.
The distinction is structural: rational cone data can define an irrational
recession ray, whereas the recession cone of a rational native convex
quadratic system is rational polyhedral.

The source search examined §4.1, including Proposition 2, in the full
2011 primary preprint. Searches included “mixed integer sqrt{2} rational
cone recession” and “irrational boundedness second-order integer”. No claim
is made that the polynomial-strip observation is new. Its role is to prevent
an invalid transfer of the existing escape-curve theorem.

## 4. Verification and limits

An independent reviewer checked the sign branches, both unboundedness
claims, the Hessian proportionality, the rational-polynomial obstruction,
the arbitrary-real-anchor version, the final Vandermonde extension, and
the source comparison. Exact integer-square arithmetic
also checked the points (8) for \(1\le z\le10{,}000\). These finite
checks support the formula; the proofs above establish the infinite claims.

Targeted checks: an inline Python command checked those 10,000 integer
points, the two Hessian matrices, this file's local links, final newline,
and trailing whitespace. No project-wide verification or CI inspection was
performed. These examples do not settle the complexity of deciding
unboundedness or constructing suitable certificates for general MISOCP.
