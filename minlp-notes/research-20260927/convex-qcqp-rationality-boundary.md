# Rational feasible points are not guaranteed for native convex quadratics

Date: 2026-09-27. Status: exact counterexample and elementary consequences;
the singleton construction has been independently checked. The
[independent review](convex-qcqp-rationality-review.md) also checks the
ellipsoid variant and the distinction from the one-dimensional Hessian-span
case. No publication-priority claim is made for this example.

A rational system of globally convex quadratic inequalities can have exactly
one feasible point, with irrational coordinates. This already occurs for
three rank-one PSD Hessians in two variables. It also occurs for the
intersection of three full-dimensional rational ellipsoids. Consequently,
the algebraic feasible-point output in the Hessian-span results cannot in
general be replaced by a rational feasible point.

## 1. A cubic irrational singleton

Set

\[
 r=\sqrt[3]{2},\qquad p=(r,r^2),
\]

and define the rational quadratic polynomials

\[
 q_1(x,y)=x^2-y,\qquad
 q_2(x,y)=y^2-2x,\qquad
 q_3(x,y)=(x-y)^2-2x-y+4.                 \tag{1}
\]

**Proposition 1.** The feasible set

\[
 F=\{(x,y)\in\mathbb R^2:q_1(x,y),q_2(x,y),q_3(x,y)\le0\}
\]

is exactly \(\{p\}\). Each native quadratic is globally convex, and
the Hessian-span dimension is exactly three.

**Proof.** The Hessians, after dividing by two, are

\[
 \begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
 \begin{pmatrix}0&0\\0&1\end{pmatrix},\quad
 \begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\]

They are PSD, have rank one, and are linearly independent. The identities
\(r^3=2\) and \(r^4=2r\) show that all three polynomials vanish at
\(p\). Define the strictly positive weights

\[
 \lambda_1=2r-1,\qquad \lambda_2=r^2-1,\qquad \lambda_3=1.
\]

Direct expansion gives

\[
 \begin{aligned}
 \sum_{i=1}^3\lambda_iq_i(x,y)
 &=2rx^2+r^2y^2-2xy-2r^2x-2ry+4\\
 &=\begin{pmatrix}x-r&y-r^2\end{pmatrix}
   \underbrace{\begin{pmatrix}2r&-1\\-1&r^2\end{pmatrix}}_{M}
   \begin{pmatrix}x-r\\y-r^2\end{pmatrix}.       \tag{2}
 \end{aligned}
\]

The first principal minor of \(M\) is positive, and
\(\det M=2r^3-1=3\), so \(M\) is positive definite.
Every feasible point makes the left side of (2) nonpositive. The right
side is nonnegative and vanishes only at \(p\). This proves the claim.
\(\square\)

The polynomial \(T^3-2\) is irreducible over \(\mathbb Q\), for
example by Eisenstein's criterion at two. Thus the feasible point has
field degree three, and \(F\cap\mathbb Q^2=\varnothing\). In
particular, even the affine hull of a rational native convex quadratic
feasible set need not be a rational affine space.

## 2. The same obstruction for three rational ellipsoids

The rank-one Hessians are not essential. Define

\[
 R_i=3q_i+q_1+q_2+q_3\quad(i=1,2,3).
\]

Explicitly,

\[
 \begin{aligned}
 R_1&=5x^2-2xy+2y^2-4x-5y+4,\\
 R_2&=2x^2-2xy+5y^2-10x-2y+4,\\
 R_3&=5x^2-8xy+5y^2-10x-5y+16.        \tag{3}
 \end{aligned}
\]

Their quadratic-part matrices are respectively

\[
 \begin{pmatrix}5&-1\\-1&2\end{pmatrix},\quad
 \begin{pmatrix}2&-1\\-1&5\end{pmatrix},\quad
 \begin{pmatrix}5&-4\\-4&5\end{pmatrix}.
\]

Each is positive definite with determinant nine. The minimum values of
\(R_1,R_2,R_3\) are respectively
\(-53/36,-101/9,-449/36\), so each set \(R_i\le0\) is a
full-dimensional compact ellipsoid with rational coefficients and rational
center.

Let \(S=\lambda_1+\lambda_2+\lambda_3=2r+r^2-1\), and set

\[
                  \eta_i=\frac{\lambda_i-S/6}{3}.
\]

All three numbers are positive. For the only close case,

\[
 6\lambda_2-S=5r^2-2r-5>0,
\]

because \(r>5/4\) and \(5t^2-2t-5\) is increasing for
\(t\ge5/4\), with value \(5/16\) at \(5/4\). The other two
inequalities follow immediately from \(5/4<r<4/3\).
Since the coefficient matrix transforming \((q_1,q_2,q_3)\) into
\((R_1,R_2,R_3)\) is \(3I+\mathbf1\mathbf1^T\),

\[
                   \sum_i\eta_iR_i=\sum_i\lambda_iq_i.       \tag{4}
\]

Equation (2) therefore proves

\[
                  \{R_1\le0,R_2\le0,R_3\le0\}=\{p\}.
\]

The invertible transformation also preserves the three-dimensional
Hessian span. The ellipsoids individually have interior; their common
intersection has no interior.

## 3. Why rational exposing multipliers are insufficient

**Proposition 2.** For the original system (1), no nonzero vector
\(w\in\mathbb Q_+^3\) makes \(g=\sum_iw_iq_i\) globally
nonnegative.

**Proof.** Since every \(q_i(p)=0\), a globally nonnegative
aggregate would have \(g(p)=0\), hence \(\nabla g(p)=0\).
Write \(g(z)=z^TAz+b^Tz+c\) with rational coefficients.
The equations \(2Ap+b=0\), together with the linear independence of
\(1,r,r^2\) over \(\mathbb Q\), force every entry of \(A\)
and \(b\) to vanish. The nonnegative combination of the native PSD
Hessians is then zero. Since each input Hessian is nonzero PSD, its trace
is positive, and taking traces forces \(w=0\). \(\square\)

The same argument applies to (3). Thus an exposing step based on a
nonnegative aggregate with minimum zero may require irrational
multipliers. The rationality of the *direction* of the aggregate's
minimizer set does not imply rationality of its affine offset.

This does not contradict the
[rational infeasibility-certificate theorem](rational-infeasibility-certificates.md).
That theorem rounds multipliers while preserving a strictly positive
minimum. The positive margin is absent in an exposing aggregate. Nor does
Proposition 2 exclude other kinds of rational certificates, such as
certificates that encode algebraic numbers by rational polynomials and
isolating intervals.

## 4. What is true when the Hessian span has dimension one

Suppose the rational PSD matrices \(Q_i\) have span dimension one.
Choose a nonzero member \(Q\succeq0\). Then
\(Q_i=\gamma_iQ\) for rational \(\gamma_i\ge0\), and write

\[
 q_i(x)=\gamma_i q(x)+\ell_i(x),\qquad
 q(x)=\tfrac12x^TQx,
\]

with rational affine \(\ell_i\). Feasibility is equivalent to

\[
 q(x)-t\le0,\qquad \gamma_it+\ell_i(x)\le0\quad\text{for all }i,
                                                               \tag{5}
\]

together with the original affine rows. In one direction take
\(t=q(x)\). In the other direction use \(\gamma_i\ge0\).

System (5) has one quadratic inequality and otherwise only affine rows.
The classical rational small-solution theorem of Vavasis applies; it is
also covered by Del Pia, Dey, and Molinaro's mixed-integer extension.
Therefore every nonempty rational native PSD system with \(h\le1\)
has a rational feasible point of polynomial binary length. The same
statement holds with any subset of its original variables required to
be integer when the **full** native Hessian span has dimension at most
one. This is a reduction to a prior theorem, not a new small-solution
theorem. Fixing only continuous Hessian blocks does not justify this
mixed-integer reduction.

The subsequent [two-span rationality theorem](two-span-rationality-frontier.md)
settles the intermediate case: every nonempty rational native PSD system
with \(h\le2\) has a polynomial-size rational feasible point. It also
has dense rational points and a rational affine hull. Its separate proof
and independent review therefore establish that the obstruction here at
\(h=3\) is sharp. The one-span reduction above remains the simpler
classical special case.

## 5. Comparison with general SOCP and examined sources

General rational SOCP already permits an irrational singleton at squared
Hessian-span dimension one. For example,

\[
                \|(1,1)\|_2\le t,\qquad \|(t,t)\|_2\le2
\]

forces \(t=\sqrt2\). Squaring gives \(2-t^2\le0\) and
\(2t^2-4\le0\), with the required nonnegative right-hand sides.
The first squared polynomial has negative Hessian. Proposition 1 is a
different boundary: **every native polynomial itself has PSD Hessian**.

Sources examined for this audit:

- Stephen A. Vavasis, *Quadratic programming is in NP*, Information
  Processing Letters 36(2), 73–77 (1990),
  [DOI](https://doi.org/10.1016/0020-0190(90)90100-C). Its rational
  small-solution result is stated in the two primary papers below; the
  original article was not separately retrieved for this audit.
- Alberto Del Pia, Santanu S. Dey, and Marco Molinaro, *Mixed-integer
  quadratic programming is in NP*, Mathematical Programming 162,
  225–240 (2017),
  [DOI](https://doi.org/10.1007/s10107-016-1036-0). The local full text,
  Theorem 1 and Section 2.2, was inspected. Theorem 1 supplies the
  polynomial-size rational witness for one quadratic inequality with
  arbitrary affine rows and integrality restrictions.
- Daniel Bienstock, Alberto Del Pia, and Robert Hildebrand,
  *Complexity, exactness, and rationality in polynomial optimization*,
  Mathematical Programming 197, 661–692 (2023),
  [DOI](https://doi.org/10.1007/s10107-022-01818-3),
  [open preprint](https://arxiv.org/abs/2011.08347). The local published
  full text was inspected. Example 2.1 uses the same cubic irrational
  point through a cubic inequality; Example 6.1 gives a native convex
  quadratic chain requiring exponentially many bits; Example 6.3 gives
  an irrational-only SOCP. These examples do not themselves state the
  three-native-PSD presentation (1).

Searches also covered the phrases “convex quadratic rational feasible
point,” “convex quadratic irrational solutions,” and “intersection of
ellipsoids rational point.” No equivalent native-PSD example was located
in this targeted search. That is not evidence sufficient to establish
novelty. The result is retained as a verified boundary and a safeguard
against simplifying away algebraic output, not as a main contribution.

## 6. Targeted verification

The independent reviewer verified the positive aggregate directly.
An additional exact SymPy calculation reduced (2) modulo \(r^3-2\),
obtained zero remainder, checked \(\det M=3\), checked the Hessian
independence, and computed the determinants, rational centers, and minimum
values of all three ellipsoids in (3). After the initial one-off symbolic
calculation, these checks were retained in
[the targeted script](check_convex_qcqp_rationality.py), together with
exact endpoint and monotonicity checks for the positive ellipsoid weights.
The command actually run was:

```sh
python research-20260927/check_convex_qcqp_rationality.py
```

Result: passed.

These calculations verify the displayed identities and matrix data. The
proof of uniqueness uses positive definiteness and positive weights as
given above. No project-wide checks or CI checks were run, and no Lean
formalization is claimed.
