# An analytic cubic family certifying R(3) ≥ 1610000/743033

The [focused cubic paper and Lean package](../paper-cubic-gap/README.md)
collects the universal upper bound, optimality among fixed mixtures of the
three stated rounding laws for uniform termwise guarantees, the analytic lower
family, and exact finite witnesses. Its [coverage map](../paper-cubic-gap/formal/COVERAGE.md)
and [verification record](../paper-cubic-gap/formal/VERIFICATION.md) identify
the formal statements and completed checks.

Date: 2026-09-04. Status: theorem with an exact symbolic certificate and completed independent written audit; see `notes/review-positive-cubic-analytic-family.md`. This strengthens the finite cubic lower certificates in `positive-cubic-gap.md`.

## Result

The worst positive multilinear ratio in degree at most three satisfies

\[
R(3)\ge\frac{1610000}{743033}\approx2.166795.
\]

The bound is proved by an explicit family of positive integer-coefficient cubic polynomials and an affine minorant valid for every normalized group-count vector in [0,1]³. The certified lower bounds converge to 1610000/743033; convergence of the actual family ratios or attainment of this value by a finite member is not asserted. The proof below first derives the simpler bound 483/223, then incorporates the positive Bernstein slack to obtain the headline bound.

## A scalar polynomial inequality

For every (a,b,c)∈[0,1]³,

\[
F(a,b,c):=6c^3+27bc^2+18b^2+30ac+20ab+9a^2
\ge37a+\frac{79}{2}b+38c-\frac{103}{3}.
\tag{1}
\]

Let h be the left side minus the right side. For fixed c, its Hessian in (a,b) is

\[
\begin{pmatrix}18&20\\20&36\end{pmatrix},
\]

which is positive definite: its leading diagonal entry is positive and its determinant is 248.

For 0≤c≤3/10, the minimum over (a,b)∈[0,1]² occurs at

\[
a=1,\qquad b_*(c)=13/24-3c^2/4.
\]

Indeed, b_* lies strictly between zero and one; the derivative with respect to b is zero; and the derivative with respect to a is

\[
-49/6+30c-15c^2\le-31/60<0.
\]

The latter expression increases on this interval and attains the displayed upper bound at c=3/10. These are the optimality conditions for the upper a boundary and an interior b value of a convex quadratic. Thus

\[
h(a,b,c)\ge p(c):=-\frac{972c^4-576c^3-1404c^2+768c-101}{96}
\quad(0\le c\le3/10).
\]

For 3/10≤c≤1, minimize the same positive-definite quadratic over unrestricted real a,b. This can only lower its value and gives

\[
h(a,b,c)\ge r(c):=-\frac{78732c^4-212256c^3+203796c^2-82032c+11275}{2976}.
\]

The following exact Bernstein certificates prove the required nonnegativity of p and r. On an interval [ℓ,u], set t=(c−ℓ)/(u−ℓ). The row gives positive integers v_0,...,v_4 and a positive denominator D such that the relevant polynomial is

\[
\frac1D\sum_{i=0}^4v_i\binom4i t^i(1-t)^{4-i}.
\]

Every Bernstein basis term is nonnegative for 0≤t≤1.

| Polynomial | Interval | D | (v_0,v_1,v_2,v_3,v_4) |
|---|---|---:|---|
| p | [0,1/5] | 60000 | (63125,39125,20975,9395,4133) |
| p | [1/5,3/10] | 240000 | (16532,6008,1802,3788,11597) |
| r | [3/10,1/2] | 7440000 | (215357,1285415,1434125,1250375,1008125) |
| r | [1/2,3/4] | 190464 | (25808,18056,7964,9230,15869) |
| r | [3/4,1] | 190464 | (15869,22508,34520,45920,31040) |

All identities are rational polynomial identities. They establish (1) over the full continuous cube, not only at sampled points.

## A positive multilinear family

Let m be a positive multiple of nine, with m≥9. Use three disjoint groups U,V,W of m variables. Write A,B,C for their respective coordinate sums, and E_k for their elementary symmetric multilinear polynomials. Define

\[
f_m(x)=2E_3(W)+3B E_2(W)+2mE_2(V)
+\frac{5m}{3}AC+\frac{10m}{9}AB+mE_2(U).
\tag{2}
\]

Every monomial has degree two or three and a positive integer coefficient. Evaluate every variable of U at 1/4, every variable of V at 1/2, and every variable of W at 3/4.

At a binary vertex, let a=A/m, b=B/m, and c=C/m denote the normalized success counts. Direct expansion gives

\[
\frac{18}{m^3}f_m
=F(a,b,c)-\frac{18c^2+27bc+18b+9a}{m}+\frac{12c}{m^2}
\ge F(a,b,c)-\frac{72}{m}.
\tag{3}
\]

For any binary coupling with the prescribed individual marginals, the mean normalized counts are (1/4,1/2,3/4). Taking expectations in (1) and (3) gives

\[
\frac{18}{m^3}\operatorname{vex}f_m
\ge\frac{139}{6}-\frac{72}{m}.
\]

This uses only a globally valid affine minorant, so it does not require solving the convex-envelope LP or assuming any conditional independence.

The concave envelope and term-by-term gap have exact scaled formulas:

\[
\begin{aligned}
\frac{18}{m^3}\operatorname{cav}f_m
&=\frac{167}{4}-\frac{153}{4m}+\frac9{m^2},\\
\frac{18}{m^3}\operatorname{tbtgap}f_m
&=\frac{161}{4}-\frac{135}{4m}+\frac6{m^2}.
\end{aligned}
\]

These follow by counting monomials and using their individual envelope formulas. Only the E_3(W) terms have a nonzero termwise convex envelope. Therefore

\[
\frac{18}{m^3}\operatorname{chgap}f_m
\le\frac{223}{12}+\frac{135}{4m}+\frac9{m^2},
\]

and

\[
\frac{\operatorname{tbtgap}f_m}{\operatorname{chgap}f_m}
\ge
\frac{161/4-135/(4m)+6/m^2}
{223/12+135/(4m)+9/m^2}
\longrightarrow\frac{483}{223}.
\]

The hull gap is positive because all coordinates are interior and the polynomial contains positive nonlinear monomials. Passing to the supremum over positive multiples of nine proves the simpler lower bound 483/223. The displayed finite lower bound already exceeds two at m=36.

The positive Bernstein coefficients give a uniform slack of at least δ=901/120000 in (1). Raising its affine right side by δ strengthens the finite ratio certificate to

\[
\frac{\operatorname{tbtgap}f_m}{\operatorname{chgap}f_m}
\ge
\frac{161/4-135/(4m)+6/m^2}
{223/12-901/120000+135/(4m)+9/m^2}.
\]

The denominator is positive for every positive m. Along positive multiples of nine, these lower certificates converge to

\[
\frac{161/4}{223/12-901/120000}
=\frac{4830000}{2229099}=\frac{1610000}{743033}.
\]

Thus the supremum is at least this value. The Lean theorem [`cubic_boxDegreeSupremum_sandwich`](../formal/Formal/CubicGap/AnalyticResults.lean) combines it with the universal upper bound on finite nonnegative boxes. Its proof uses the positive hull gaps and membership of the actual family ratios in the supremum set; it does not assume convergence of those ratios.

## Verification and scope

`code/multilinear_ratio/verify_cubic_analytic_family.py` checks the Hessian determinant, the boundary optimality identities, both eliminated quartics, every Bernstein expansion, the exact finite-family polynomial expansion, and the limiting gap calculation in rational symbolic arithmetic. Its output is preserved in the matching `.log` file. These identities provide the proof; a numerical global optimizer is not used as a certificate.

This lower bound does not determine R(3). The [three-distribution coupling](positive-cubic-rounding-upper-bound.md) supplies the independently audited universal upper bound 31/12. The coefficient-removal lemma shows that the same degree-three supremum can be approached with unit-coefficient homogeneous polynomials, at the cost of increasing dimension; that statement is separate from the explicit integer-coefficient family (2).
