# Strictly feasible convex quartics can require exponentially large rational witnesses

Date: 2026-09-28. Status: quantitative theorem passed
[fresh independent review](strict-quartic-rational-witness-independent-review.md).
A [scoped primary literature comparison](strict-convex-quartic-witness-prior.md)
records the strongest checked neighboring bounds. Publication priority
is unestablished.

For every \(k\), a polynomial-size rational quartic in \(2k\)
variables can define a compact feasible set with nonempty interior,
while every rational feasible point needs exponentially many bits.
The polynomial is globally strongly SOS-convex, with a supplied rational
positive definite Hessian Gram. The obstruction is precision near an
irrational cubic coordinate, not a large coordinate magnitude or a
feasible set with empty interior.

This construction is independent of the PosSLP sign reduction. Its only
substantial dependency is the reviewed
[signed odd-root quartic realization](signed-odd-root-circuit-quartic.md).
Large rational-witness requirements for other convex systems are known;
the comparison section separates that prior from the restrictions here.

## Statement

**Theorem.** For every integer \(k\ge1\), one can construct in
deterministic polynomial time a rational quartic \(G_k\) in
\(n=2k\) variables, with polynomial coefficient bit length and a
polynomial-size rational full Hessian Gram at least the identity, such
that:

1. \(\nabla^2G_k\succeq I\) on all of \(\mathbb R^n\).
2. \(C_k=\{X:G_k(X)\le0\}\) is compact and has nonempty
   interior. In particular, it contains rational points.
3. Every \(X\in C_k\cap\mathbb Q^n\), writing its first
   coordinate in lowest terms as \(a/b\), with \(b>0\), satisfies
   \[
    \log_2 b>
       \frac{2^k-3}{3}(k+3)\log_2 1000
                        -\frac13\log_2 270.
    \tag{1}
   \]
   Thus every rational feasible point has bit length
   \(\Omega(k2^k)=\Omega(n2^{n/2})\).

All feasible points lie in a bounded region of constant coordinate
magnitude. One may clear denominators to obtain integer quartics with
the same feasible sets and the same polynomial bit-size bounds.
The lower bound is exponential in the number of variables and
superpolynomial relative to the constructed dense input size. It is
not asserted to be \(2^{\Omega(\text{total input bits})}\).

## A short root circuit for a very small positive number

Put
\[
 M=1000^{k+3},\qquad \delta_0=1/M,
 \qquad \delta_i=(1+3\delta_{i-1}^2)^{1/3}-1
                   \quad(1\le i\le k).
 \tag{2}
\]
Every \(\delta_i\) is positive. For \(t\ge0\),
\((1+t)^3\ge1+3t\), so
\[
                0<\delta_i\le\delta_{i-1}^2,
       \qquad \delta_k\le M^{-2^k}.
 \tag{3}
\]
The tiny number \(\delta_k\) is represented by \(k\) root
gates. It is never expanded as a rational approximation with that many
digits.

Let \(\xi_i=1+\delta_i\). The first gate has rational radicand
\(1+3/M^2\), and every later gate is
\[
                    \xi_i^3=3\xi_{i-1}^2-6\xi_{i-1}+4.
 \tag{4}
\]
Give gate \(i\) the positive rational box
\[
 w_i=1000^i/M,\qquad L_i=1-w_i,\qquad U_i=1+w_i.
 \tag{5}
\]
Here \(w_i\le1000^{-3}<1/3\), and every endpoint has
\(O(k)\) bits. On the predecessor box of width \(w\), signed
interval evaluation of (4) gives deviation from one at most
\(12w+3w^2\le13w\). Since \(w_i=1000w_{i-1}\),
\[
 (1-w_i)^3\le1-2w_i\le1-13w_{i-1},\qquad
 (1+w_i)^3\ge1+3w_i\ge1+13w_{i-1}.
\]
Thus the interval lies within \([L_i^3,U_i^3]\). The first
constant radicand satisfies this inclusion directly. These are exactly
the rational nonzero-box promises required by the signed-root theorem.

The normalization of that theorem is
\[
 \kappa=\frac1{1-w_k}=
             \frac{M}{M-1000^k}<2.
 \tag{6}
\]
In fact \(\kappa=10^9/(10^9-1)\) is independent of \(k\).
It returns a rational SOS quartic \(F\), in two variables per
gate, with unique zero
\[
                    p=(\kappa\xi_i,(\kappa\xi_i)^2)_{i=1}^k
 \tag{7}
\]
and a full positive definite rational Hessian Gram \(M_0\) on
\((v,X\otimes v)\). All output sizes and construction times are
polynomial in \(k\). Every coordinate of \(p\) lies in
\((0,4)\), since
\[
 0<\kappa\xi_i\le\frac{1+w_k}{1-w_k}<2.
\]

## A quadratic perturbation creates a small full-dimensional body

Let \(h=n+n^2\) be the Gram dimension, and put
\[
 \mu=\frac{\det M_0}{(\operatorname{tr}M_0)^{h-1}}>0,
 \quad \lambda=\left\lceil\frac3\mu\right\rceil,
 \quad u(X)=X_{k,1}-\kappa,
 \quad G_k(X)=\lambda F(X)-u(X)^2.
 \tag{8}
\]
The standard determinant bound gives \(M_0\succeq\mu I\).
The Hessian of \(u^2\) has Gram \(2ee^{\mathsf T}\), where
\(e\) selects the \(v_{k,1}\) coordinate in the constant
block of the Hessian basis. Therefore
\[
              \lambda M_0-2ee^{\mathsf T}\succeq I.
 \tag{9}
\]
This is the promised rational full Hessian Gram and proves global
strong convexity. Determinant computation, rational powers, and the
ceiling in (8) have polynomial bit complexity on this polynomial-size
rational matrix. Hence the quartic and its certificate remain of
polynomial size.

Write
\[
                         u_* =u(p)=\kappa\delta_k>0.
\]
At the known algebraic point \(p\),
\[
                   G_k(p)=-u_*^2<0,
                   \|\nabla G_k(p)\|=2u_*.
 \tag{10}
\]
Thus \(p\) is a strict feasible point and \(C_k\) has
nonempty interior. Global strong convexity implies coercivity, so the
closed sublevel set is compact. It also implies strict convexity of
the feasible body.

For any \(X\in C_k\), write \(r=\|X-p\|\).
The supporting quadratic inequality from \(\nabla^2G_k\succeq I\)
and (10) gives
\[
 0\ge G_k(X)\ge-u_*^2-2u_*r+\frac12r^2.
\]
Consequently
\[
                \|X-p\|\le(2+\sqrt6)u_*<5u_*
                         \le5\kappa M^{-2^k}.
 \tag{11}
\]
This localization concerns every feasible point, including boundary
points. Since \(5u_*<1\) and the coordinates of \(p\) lie
in \((0,4)\), all feasible coordinates lie in \((-1,5)\).
The first coordinate of \(p\) is below two, so a feasible first
coordinate has absolute value below three.

## The first coordinate cannot be approximated cheaply by a rational

Let \(\alpha=\kappa\xi_1\). By (2) and (6),
\[
 \alpha^3=\frac{M(M^2+3)}{(M-1000^k)^3}=\frac{A}{B},
 \quad A=M(M^2+3),\quad B=(M-1000^k)^3<M^3.
 \tag{12}
\]
Both integers have \(O(k)\) bits. The number \(\xi_1\),
and hence \(\alpha\), is irrational: \(M^2\) is an integer
cube, while \(M^2+3\) lies strictly between that cube and the
next integer cube. Since \(M^{2/3}\) is an integer, rationality
of \(\xi_1=(M^2+3)^{1/3}/M^{2/3}\) would force
\(M^2+3\) to be an integer cube. Thus \(\alpha\) has degree
three over \(\mathbb Q\).

Let \(a/b\) be a feasible first coordinate in lowest terms, with
\(b>0\). Irrationality implies \(Ba^3-Ab^3\ne0\), so
\[
 \left|B(a/b)^3-A\right|\ge\frac1{b^3}.
\]
Both \(\alpha\) and \(a/b\) have absolute value below three.
Factoring the difference of cubes gives
\[
 \left|B(a/b)^3-A\right|
       \le27B\,|a/b-\alpha|.
\]
Together with (11), \(B<M^3\), and \(\kappa<2\), this gives
\[
 \frac1{b^3}
   <135B\kappa M^{-2^k}
   <270M^{3-2^k}.
\]
Taking logarithms proves (1). No unproved Diophantine approximation
statement is used: the bound follows from an explicit integer cubic
and the fact that a nonzero integer has absolute value at least one.

For \(k\ge3\), \(2^k-3\ge2^{k-1}\), so (1) is
\(\Omega(k2^k)\). The inequalities remain valid for \(k=1,2\),
although the displayed lower bound can be weak at small \(k\).
Every nonempty open subset of \(\mathbb R^n\) contains rational
points; thus the lower bound concerns the size of existing rational
witnesses, not their absence.

## What the result establishes and does not establish

The supplied strict Hessian Gram removes any need to decide whether the
input is convex. Strict feasibility removes the irrational-singleton
obstruction to rational existence. Bounded coordinates remove the
possibility that the lower bound is caused only by a very large norm.
Even with these properties, rational point witnesses can require
exponentially many bits because the feasible body is extremely small
around a low-degree irrational coordinate.

The theorem does not prove that feasibility is outside NP. Other
certificates, including compact algebraic descriptions, can be small.
It does not obstruct approximate optimization with a prescribed error,
nor assert an inverse-polynomial Slater radius. Its rational interior
points exist but have no short ordinary binary coordinate description.

Large rational witnesses for convex systems are established prior.
The [primary comparison](strict-convex-quartic-witness-prior.md) records
Khachiyan's repeated-squaring inequalities, also discussed by
Pataki--Touzov: those are already strictly feasible convex quadratic
systems forcing exponentially large witnesses through very large
coordinates. The distinction here is a single globally strongly
SOS-convex quartic, a compact full-dimensional feasible set of bounded
coordinate magnitude, and a supplied strict rational Hessian certificate.

The same audit checks the general strict-set rational-height upper bound
\(\ell D^{O(n)}\), stated in Safey El Din--Zhi, Proposition 2.5,
with attribution to Basu--Pollack--Roy. It applies to the nonempty
basic open set \(G_k<0\). At fixed degree four and polynomial
coefficient bit length, the exponential dependence on dimension is
therefore qualitatively necessary even under the stronger promises here.
This is not a claim that all exponent constants match. An unsuccessful
search for an equivalent restricted example would not establish priority.

The focused exact checker is

```text
python research-20260927/check_strict_quartic_witness_lower_bound.py
```

It passed the interval promises for depths up to twenty, normalization,
cubic arithmetic, localization constants, scalar denominator inequalities,
and exact rank-one Gram perturbations on two rational matrices. The
universal construction and size bound depend on the proof and its
independent review; those finite examples are not a substitute. No
project-wide checks or CI inspection were used.
