# Rational lifted approximations of Lorentz cones: source and encoding audit

Date: 2026-09-27. Status: established approximation machinery, with an explicit
integer implementation and two source edge cases repaired below. This note
makes no novelty claim for polyhedral cone approximation.

## Primary sources examined

Burak Kocuk, *Rational polyhedral outer-approximations of the second-order cone*,
Discrete Optimization 40 (2021), 100643,
[DOI](https://doi.org/10.1016/j.disopt.2021.100643),
[open manuscript, dated March 11, 2021](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf),
[arXiv version](https://arxiv.org/abs/1912.00256).
The relevant locations are equations (1), (6), (10), and (13),
Propositions 1, 3, 4, and 5, and Sections 2.3 and 3.3.
The construction uses integer Pythagorean triples, then a binary tree of
three-dimensional cones. This gives a multiplicative outer approximation with
polynomial encoding length. The same-size existence construction in Section 2
does not itself give the coefficient bound needed here; use Section 3.

Aharon Ben-Tal and Arkadi Nemirovski, *On polyhedral approximations of the
second-order cone*, Mathematics of Operations Research 26 (2001), 193–205,
[author-hosted manuscript](https://www2.isye.gatech.edu/~nemirovs/ApprLor_fin.pdf).
This is the antecedent lifted approximation and tree construction. Its
trigonometric coefficients are generally irrational.

The conclusions below are an explicit bit-complexity audit of this prior work,
not a new approximation theorem or a claim that approximation decides exact
SOCP feasibility without an additional separation bound.

Kocuk's Proposition 7 is also direct prior art for integer-point preservation:
for an intersection \(S\) of balls with integral centers and positive integral
radii, under Section 5's standing assumption \(S\cap\mathbb Z^N\ne\varnothing\),
it constructs a rational outer polytope \(T\supseteq S\) satisfying
\(T\cap\mathbb Z^N=S\cap\mathbb Z^N\). Section 5 also states applicability
to integral ellipsoid data, without a separate detailed statement. The ball
proof uses the unit gap between distinct
integer squared distances. It does not supply a gap for infeasible continuous
fibers over integer decisions. An extension using such fibers must identify
that extra gap argument, rather than claim integer preservation itself is new.

## A safe statement with an exact construction

Write

\[
K_d=\{(u,t)\in\mathbb R^d\times\mathbb R:\|u\|_2\le t\}.
\]

Given an integer \(d\ge2\) and rational \(0<\epsilon\le1\), one can construct a
homogeneous rational linear system in \((u,t,z)\), whose projection
\(P_{d,\epsilon}\) satisfies

\[
K_d\subseteq P_{d,\epsilon}
\subseteq\{(u,t):t\ge0,\ \|u\|_2\le(1+\epsilon)t\}. \tag{A}
\]

Put \(K=\lceil\log_2d\rceil\). The numbers of auxiliary variables and rows are

\[
O\!\left(d\,[1+\log(K/\epsilon)]\right),
\]

and every integer coefficient has
\(O(1+\log(K/\epsilon))\) bits. Construction time is polynomial in \(d\)
and the binary encoding length of \(\epsilon\). The output can be sparse;
each folding row has at most three nonzero entries. Clearing denominators
of rational affine input maps preserves polynomial encoding length.
For \(d=0,1\), the cone itself has an exact linear description.

Here is a version that avoids evaluating logarithms, trigonometric functions,
or algebraic numbers during coefficient generation.

### Three-dimensional building block

For rational \(\delta>0\), use the following integer triples from Kocuk's
equation (13):

\[
(a_1,b_1,c_1)=(120,119,169),\qquad
h_j=2^{j-2}+2,
\]
\[
(a_j,b_j,c_j)=(2h_j-1,\,2h_j^2-2h_j,\,2h_j^2-2h_j+1)
\quad(j\ge2).
\]

Choose the first integer \(J\ge2\) for which \(\delta b_J\ge1\).
This stopping test is exact rational arithmetic. Define the lift in variables
\((u,v,t,\xi_0,\eta_0,\ldots,\xi_J,\eta_J)\) by

\[
\xi_0\ge\pm u,\quad \eta_0\ge\pm v,
\]
\[
c_j\xi_j=b_j\xi_{j-1}+a_j\eta_{j-1},\qquad
c_j\eta_j\ge\pm(-a_j\xi_{j-1}+b_j\eta_{j-1})
\quad(1\le j\le J),
\]
\[
\xi_J\le t,\qquad b_J\eta_J\le a_J\xi_J. \tag{B}
\]

The \(\pm\) notation denotes both inequalities, not an independent sign choice.
There are \(2J+2\) auxiliary variables, \(J\) equalities, and
\(2J+6\) inequalities.

For completeness, the geometric facts needed from the source can be checked
directly. Let \(\theta_j\in(0,\pi/2)\) have sine \(a_j/c_j\) and cosine
\(b_j/c_j\). Then \(\theta_1\ge\pi/4\),
\(\theta_2=\theta_1/2\), and

\[
\tfrac12\theta_{j-1}\le\theta_j\le\theta_{j-1}\qquad(j\ge3).
\]

For the lower inequality, write \(h=h_{j-1}\ge3\) and
\(h_j=2h-2\); the half-angle comparison reduces to

\[
\frac{4h-5}{8h^2-20h+12}\ge\frac1{2h-1},
\]

whose positive-denominator cross-product difference is \(6h-7>0\).
For the upper inequality, \((2h-1)/(2h^2-2h)\) decreases for \(h\ge2\).
Consequently, repeatedly rotating by \(-\theta_j\) and reflecting the second
coordinate maps the initial first quadrant into the angular interval
\([0,\theta_j]\). Taking the inequalities defining each absolute value at
equality therefore lifts every point of \(K_2\) into (B).

Conversely, all \(\xi_j,\eta_j\) are nonnegative, and the rotations preserve
Euclidean norm before each absolute-value slack is added. Thus every point of
(B) satisfies

\[
\sqrt{u^2+v^2}\le\sqrt{\xi_J^2+\eta_J^2}
\le\frac{c_J}{b_J}\xi_J
\le(1+\delta)t.
\]

In particular \(t\ge0\). If \(t=0\), all original and auxiliary coordinates
are zero: the positive coefficients in each preceding equality propagate
\(\xi_J=0\) backwards, and the final inequality forces \(\eta_J=0\).

### Coefficient and tree audit

For \(j\ge2\), \(c_j=b_j+1\). Also
\(b_{j+1}<4b_j\). If \(J>2\), minimality gives
\(b_{J-1}<1/\delta\), hence \(c_J<4/\delta+1\). If \(J=2\), then
\(c_J=13\). Including the first triple, every coefficient has magnitude at
most

\[
\max\{169,\,4/\delta+1\}. \tag{C}
\]

Moreover, \(b_j\ge2^{2j-3}\), so the stopping rule uses
\(J=O(1+\log^+(1/\delta))\) stages. These estimates prove the bit and
construction-time bounds without exact evaluation of the source's displayed
stage-count formula.

For the general cone, pad \(u\) with zero coordinates to \(2^K\) leaves and
use (B) at every internal vertex of a balanced binary tree. Set
\(\delta=\epsilon/(2K)\). There are \(2^K-1<2d\) building blocks.
Induction up the tree gives outer norm factor \((1+\delta)^K\).
Since \(0<\epsilon\le1\),

\[
(1+\epsilon/(2K))^K\le e^{\epsilon/2}\le1+\epsilon.
\]

The last inequality follows from
\(\log(1+\epsilon)\ge\epsilon/2\). This analytic estimate certifies the
rational construction; exponentials and logarithms need not be computed.
The exact cone admits the lift obtained by placing the true subtree norm at
each internal vertex. This proves (A), including the origin.

## Source edge cases and application boundaries

The source's notation \((1+\epsilon)L^N\) denotes enlargement of the norm
bound; literal scalar multiplication of a cone would leave it unchanged.
Use (A) to avoid that ambiguity.

Equation (15) in the examined manuscript can return a nonpositive stage count
for part of the advertised range \(0<\delta<1/4\): at \(\delta=1/5\),
\(\lceil\log_2(-6+2\sqrt{11})\rceil=0\). In addition, the fixed first
triple has coefficient 169, which exceeds the bound \(4/\delta\) at
\(\delta=1/10\). Thus the literal maximum-coefficient statement in
Proposition 4 needs a constant term or a smaller tolerance range. The stopping
rule \(J\ge2\) and bound (C) remove both issues. They do not affect the
asymptotic claim used here. These observations concern the examined open
manuscript; no assertion is made about an independently checked publisher
proof version.

For an affine cone constraint \(\|Ax+b\|_2\le c^Tx+d\), substitution into
the lift enforces \(c^Tx+d\ge0\) automatically and enforces
\(Ax+b=0\) when that right side is zero. Squaring the original constraint
without retaining this sign would introduce a spurious negative branch.
The homogeneous approximation creates no such branch.

The approximation alone does not preserve exact feasibility. A polyhedron may
intersect every positive-tolerance outer cone while missing the cone itself.
An exact-decision argument needs a proved quantitative infeasibility gap or
another exact structural argument. Also, multiplicative norm error only gives
a bounded squared-residual error when the affine right sides have a proved
bound on the domain under consideration.

## Targeted verification

The open PDF was downloaded to `/tmp/minlp-kocuk-2021.pdf` and extracted using
`pdftotext -layout`; Sections 2 and 3 were checked against the source text.
The exact integer checks recorded below verify finite instances and algebraic
identities; the preceding argument supplies the uniform proof. No project-wide
verification or CI inspection was performed.

Two targeted commands of the form `python - <<'PY' ... PY` were run using
`fractions.Fraction`, with `sympy` for symbolic identities. The first checked:

- The Pythagorean identity, the half-angle cross-product difference \(6h-7\),
  the coefficient-growth difference \(4b_j-b_{j+1}=12h_j-12\), and the
  negative derivative of \((2h-1)/(2h^2-2h)\): four symbolic identities.
- Every tolerance \(\delta\in\{1,3,7\}/2^p\), \(1\le p\le80\): exact
  stopping, final factor, coefficient bound, and stage-growth checks; 240 cases.
- Every \(d\in\{2,3,4,7,8,9,32,100,1024\}\) and
  \(\epsilon=2^{-p}\), \(p\in\{0,1,3,10,40,80\}\): exact rational
  verification of \((1+\epsilon/(2K))^K\le1+\epsilon\); 54 cases.

The second command folded the rational unit-circle points
\(((1-r^2)/(1+r^2),2r/(1+r^2))\), \(r=k/4\), \(-16\le k\le16\),
at scales 0, 1, and 7, for tolerances \(1/2,1/5,1/10,1/100,2^{-40}\).
All 495 cases passed exact norm preservation, final-angle and height tests,
the apex check, and rejection at height \(-1\) for the constructed lift.
This finite test does not by itself rule out all other lifts at negative
height; the nonnegativity proof above does.

Final outputs were `PASS: 4 symbolic identities; 240 exact stage/coefficient
checks; 54 exact tree-factor checks` and `PASS: 495 exact
signed-circle/scale/apex/negative-RHS folding cases`. An initial symbolic
harness assertion compared structurally different equivalent SymPy
expressions; simplifying their difference fixed the harness. No mathematical
statement changed.

Independent review: the SOCP adversarial reviewer separately checked the
triples, half-angle bound, coefficient growth, stopping rule, tree factor,
homogeneity, and apex argument against the source on 2026-09-27 and found no
gap. The parent investigator also read the construction and found no issue.
These reviews are additional evidence, not formal verification.
