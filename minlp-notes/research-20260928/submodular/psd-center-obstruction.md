# Positive definite center blocks do not preserve SDP exactness

Date: 2026-09-28. Status: verified negative boundary, derived from a prior
counterexample. This is not proposed as an original main contribution.

The [stable-positive theorem](../../research-20260927/stable-positive-submodular-exactness.md)
proves exactness of PSD plus upper RLT for a submodular box quadratic when the
positive-diagonal vertices form a stable set. It is tempting to replace
that condition by positive semidefiniteness of the positive-diagonal principal
block. That extension is false, even when that block is positive definite,
contains only two variables, and the support graph is a path.

## A short derivation from an existing example

Burer, Natarajan, and Willemsen,
[*On the Semidefinite Representability of Continuous Quadratic Submodular
Minimization With Applications to Pricing and Moment Problems*, v3](https://arxiv.org/html/2504.03996v3),
Example 4 and Proposition 12, provide

\[
 Q_0=\begin{pmatrix}8&-14&0&0\\-14&25&-25&0\\
 0&-25&25&-14\\0&0&-14&8\end{pmatrix},\qquad
 c_0=(12,29,0,0)^T.
\]

Their quadratic \(q_0(x)=x^TQ_0x+c_0^Tx\) is nonnegative on
\([0,1]^4\) and vanishes at the origin. Define

\[
 q(x)=q_0(x)+8x_1(1-x_1)+8x_4(1-x_4)
                  +\frac{x_2^2+x_3^2}{16}.                 \tag{1}
\]

Every added term is nonnegative on the box, so \(\min q=0\). In
quadratic form its coefficients are

\[
 Q=\begin{pmatrix}0&-14&0&0\\-14&401/16&-25&0\\
 0&-25&401/16&-14\\0&0&-14&0\end{pmatrix},\qquad
 c=(20,29,0,8)^T.                                         \tag{2}
\]

The positive-diagonal set is \(C=\{2,3\}\). Its principal block has
eigenvalues \(1/16\) and \(801/16\), so it is positive definite.
The full quadratic is submodular and its interaction graph is the four-node
path. The full quadratic is not convex; only its center block is positive
definite. The remaining variables are affine separately and can be rounded
to binary endpoints when minimizing over the box.

Use the prior paper's explicit rational relaxed point

\[
 \mu=(3/32,3/16,9/16,3/4)^T,
 \quad
 X=\begin{pmatrix}
 3/32&3/32&3/32&61/1024\\
 3/32&125/1024&3/16&3/16\\
 3/32&3/16&231/512&9/16\\
 61/1024&3/16&9/16&3/4
 \end{pmatrix}.                                           \tag{3}
\]

The moment matrix \(\left(\begin{smallmatrix}1&\mu^T\\\mu&X
\end{smallmatrix}\right)\) is positive definite and (3) satisfies every
full RLT inequality. The prior objective value is \(-109/1024\).
Since \(X_{11}=\mu_1\) and \(X_{44}=\mu_4\), the first two added
terms in (1) have zero relaxed value. Hence

\[
 Q\mathbin\bullet X+c^T\mu
 =-\frac{109}{1024}+\frac1{16}
      \left(\frac{125}{1024}+\frac{231}{512}\right)
 =-\frac{1157}{16384}<0.                                  \tag{4}
\]

Thus even full SDP–RLT is inexact. The conclusion applies to global objective
exactness, and therefore also rules out a universal fixed-mean convex-closure
identity for this larger class. It does not rule out polynomial optimization
by another method. Eliminating the convex center block still gives a
submodular value function of the two binary endpoint variables.

The modification (1) is elementary. The original gap, its explicit witness,
and the central phenomenon belong to Burer–Natarajan–Willemsen. The new
observation merely places that known example on the proposed structural
boundary. It should not be presented as a new general SDP-gap result.

## Independent numerical discovery and an additional exact example

Before finding the short derivation above, a targeted screen found another
four-node path with a positive definite two-variable center. Its independently
stored rational witness is in
[psd_center_exact_certificate.json](psd_center_exact_certificate.json),
verified by [check_psd_center_obstruction.py](check_psd_center_obstruction.py).
The matrix in center-first order is

\[
 Q=\begin{pmatrix}11&-5&-7/2&0\\-5&6&0&-5\\
 -7/2&0&-5&0\\0&-5&0&-6\end{pmatrix},
 \qquad
 c=(9,-1,11567/1804,10825/984)^T,
\]

with constant \(1/24\). Its center determinant is 41. After minimizing
that center, its four binary endpoint values are zero for
\((0,0),(0,1),(1,1)\), and \(2547/1804\) for \((1,0)\).
Both remaining diagonal coefficients are negative; coordinatewise concavity
therefore proves nonnegativity on the whole box. The exact saved moment point
has full RLT and a positive definite moment matrix, with objective

\[
 -704315984787773/202950000000000000<-0.00347.
\]

This example is retained as a separate certificate, not as evidence of a
stronger result or priority. The earlier screen initially reported false gaps
because an all-free stationary vector was stored in an integer array. That
bug was identified, corrected by requiring floating-point arrays, and the
initial reported gaps were discarded. Only the later rational certificates
support the conclusions here.

## Verification and interpretation

Commands actually run:

```text
python research-20260928/submodular/screen_psd_center.py
python research-20260928/submodular/screen_psd_center_path.py
python research-20260928/submodular/check_psd_center_obstruction.py
python research-20260928/submodular/check_psd_center_prior_obstruction.py
```

The first two are numerical discovery screens and are not certificates.
The third verifies the independent saved witness using rational LDL
factorization, all RLT inequalities, and exact convex center minimization.
The fourth independently checks all 81 face-stationary patterns of the
prior example, checks that its four singular stationarity systems are
inconsistent, and verifies (2)–(4) with exact rational arithmetic and positive
leading principal minors. No project-wide tests or CI inspection were run.
Lean was not used.

A broader exact SDP theorem will need a condition beyond positive
semidefiniteness of the center principal matrix. The negative example does
not undermine the stable-positive theorem: its two positive-diagonal vertices
are adjacent. Nor does it identify computational hardness or measured solver
performance.

The [independent review](obstruction-independent-review.md) verified both
certificates and independently minimized all four endpoint fibers of (2),
without relying on the source assertion about the original quadratic. It
found no substantive error.
