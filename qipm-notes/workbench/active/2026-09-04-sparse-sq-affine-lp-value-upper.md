# A dimension-independent SQ upper bound for the affine-slice LP value

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on novelty

## Main theorem

Let \(M\in\mathbb C^{N\times N}\) be invertible, with at most \(d\)
nonzeros per row and column, and

\[
 \|M\|\leq1,\qquad \sigma_{\min}(M)\geq K^{-1}.             \tag{1}
\]

Assume exact row-and-column sparse-location/value access to \(M\), exact
\(SQ(a)\) (coordinate queries, squared-coordinate sampling, and the norm),
and coordinate access to \(e\).  The zero-vector cases are trivial, so take
\(a,e\ne0\).  For \(0<\epsilon\leq1/2\) and
\(0<\zeta<1/2\), the scalar

\[
 z=a^*M^{-1}e                                              \tag{2}
\]

can be estimated to additive error

\[
 \epsilon\|a\|\,\|e\|
\]

with failure probability at most \(\zeta\), in ideal arithmetic, using

\[
 \boxed{
 \widetilde O\!\left(
 K^2\epsilon^{-2}\log(1/\zeta)\,
 (d+1)^{\,O(K\log(K/\epsilon))}
 \right).}                                                 \tag{3}
\]

The same estimate gives \(|z|\) to the same additive accuracy.  The
complexity is independent of \(N\).  No \(SQ(e)\) interface is needed.  The
algorithm uses only a subset of the stronger full-SQ matrix interface used
by the lower bound: sparse locations and values suffice, while row/column
norm and sampling queries to \(M\) are unused.

There is an instance-sensitive form.  If a public number \(R_e\) satisfies

\[
 \|M^{-1}e\|\leq R_e\|e\|,\qquad 1\leq R_e\leq K,           \tag{4}
\]

then (3) improves to

\[
 \boxed{
 \widetilde O\!\left(
 R_e^2\epsilon^{-2}\log(1/\zeta)\,
 (d+1)^{\,O(K\log(R_e/\epsilon))}
 \right).}                                                 \tag{5}
\]

For the cyclic affine-slice LP lower family, apply the theorem with the unit
objective vector \(a=\bar a\).  There \(\|e\|=\|\bar a\|=1\), and

\[
 R_e=\frac{\|M^{-1}e\|}{\|e\|}=\|M^{-1}e\|=R=\Theta(\sqrt K)
\]

is an exact public clock-only scalar.  Therefore
its value has the matching classical upper exponent

\[
 \exp\!\left(
 O\!\left(K\log(d+1)\log\frac{\sqrt K}{\epsilon}\right)
 \right),                                                  \tag{6}
\]

up to polynomial factors.  This matches the lower exponent in that note
within constants.

## Normal-equation inverse polynomial

Set

\[
 B=M^*M.
\]

Its spectrum lies in \([K^{-2},1]\).  Apply the relative Chebyshev residual
from the sparse-SQ conditioning theorem on this interval.  For any
\(0<\eta<1\), there is a degree-\((m-1)\) polynomial \(q\), with

\[
 m=O(K\log(1/\eta)),
\]

such that

\[
 \|I-Bq(B)\|\leq\eta.                                     \tag{7}
\]

Write \(r_m(\lambda)=1-\lambda q(\lambda)\).  Since
\(M^*e=M^*Mx=Bx\), where \(x=M^{-1}e\), the residual calculation below
does not require \(M\) to be normal.

Define

\[
 P=q(M^*M)M^*.                                             \tag{8}
\]

For \(x=M^{-1}e\), equation (8) gives the exact residual identity

\[
 Pe-x=-r_m(M^*M)x,
\]

and hence

\[
 \|Pe-M^{-1}e\|\leq\eta\|M^{-1}e\|.                       \tag{9}
\]

The singular values of \(P\) are

\[
 \frac{|1-r_m(\sigma^2)|}{\sigma},
\]

so

\[
 \|P\|\leq K(1+\eta).                                     \tag{10}
\]

For the generic theorem, choose

\[
 \eta=\frac{\epsilon}{4K}.
\]

Then

\[
 |a^*(Pe-M^{-1}e)|
 \leq\frac{\epsilon}{4}\|a\|\,\|e\|.                      \tag{11}
\]

Under (4), choose instead \(\eta=\epsilon/(4R_e)\), which proves the bias
part of (5).

## One-coordinate estimator

Sample \(I\) with probability

\[
 \Pr[I=i]=\frac{|a_i|^2}{\|a\|^2}
\]

and return

\[
 X=\|a\|^2\frac{(Pe)_I}{a_I}.                             \tag{12}
\]

Indices with \(a_i=0\) have zero sampling probability.  For every sampled
index, \(|a_i|^2/a_i=\overline{a_i}\), so

\[
 \mathbb E X=a^*Pe,\qquad
 \mathbb E|X|^2\leq\|a\|^2\|Pe\|^2.                       \tag{13}
\]

Equations (9)--(10) imply the generic bound

\[
 \mathbb E|X|^2
 \leq K^2(1+\eta)^2\|a\|^2\|e\|^2.                       \tag{14}
\]

Thus a median of means, applied separately to real and imaginary parts,
uses

\[
 O(K^2\epsilon^{-2}\log(1/\zeta))                         \tag{15}
\]

samples to achieve statistical error
\(\epsilon\|a\|\|e\|/2\).  If (4) is available, (9) directly gives
\(\|Pe\|\leq(1+\eta)R_e\|e\|\), replacing \(K^2\) by \(R_e^2\) in
(14)--(15).  Combining statistical and deterministic errors proves
(3)--(5).

Unlike the SPD quadratic-form estimator, no Kantorovich improvement is
available without an additional alignment promise: \(a^*M^{-1}e\) can
cancel even when \(\|M^{-1}e\|\) is large.  This is why the result is
additive rather than uniformly relative.

## Local sparse evaluation

One coordinate of \(Pe=q(M^*M)M^*e\) is a sum over alternating walks
through

\[
 M^*,M,M^*,\ldots .
\]

A walk has length at most \(2m-1\).  When expanding backward from the
requested output coordinate, the leftmost \(M^*\) step enumerates a column
of \(M\); the following \(M\) step enumerates a row, and the orientation
continues to alternate until an \(e\)-coordinate is queried.  Thus row access
to \(M\) handles an \(M\) step and column access handles an \(M^*\) step.
Identity terms and the sum over polynomial degrees can be represented by
self-loops.  Recursive evaluation or explicit path enumeration therefore
costs

\[
 (d+1)^{O(m)}                                             \tag{16}
\]

matrix and \(e\)-coordinate queries per sample.  It touches no length-\(N\)
vector.  Combining (16) with (15) proves the query bounds.

As in the companion decrement upper bound, the theorem is stated in ideal
arithmetic.  Chebyshev/Clenshaw evaluation gives a controlled finite-bit
implementation, but a complete statement requires a precise approximate-SQ
and input-bit model.

## Parameter match to the affine-slice LP lower family

The affine-slice LP has

\[
 \operatorname{OPT}
 =|\bar a^TM^{-1}e|,
\qquad
 \|\bar a\|=\|e\|=1,
\qquad
 R_e=\|M^{-1}e\|=R=\Theta(\sqrt K),                        \tag{17}
\]

where the theorem's vector \(a\) is the lower construction's \(\bar a\), and
\(R\) is exactly computable from the public clock.  Its lower theorem,
parameterized by requested additive value accuracy \(\epsilon\), gives

\[
 Q_{\rm lower}
 =\exp\!\left(
 \Omega\!\left(K\log s\log\frac{\sqrt K}{\epsilon}\right)
 \right)                                                   \tag{18}
\]

up to its explicit polynomial denominator.  Equation (5) gives

\[
 Q_{\rm upper}
 =\exp\!\left(
 O\!\left(K\log(s+1)\log\frac{\sqrt K}{\epsilon}\right)
 \right)                                                   \tag{19}
\]

up to polynomial factors in \(K/\epsilon\).  Since the cyclic family has
\(d=\Theta(s)\) with \(s\geq2\), the exponential
conditioning--sparsity--accuracy dependence agrees up to constants in the
exponent throughout the lower construction's admissible parameter range,
including the
constant-additive-error regime
\(\epsilon=\Theta(1)\), where both exponents are
\(\Theta(K\log s\log K)\).

This upper bound estimates only the scalar value.  It does not produce a
nullspace basis for the LP equality, an optimizer \(M^{-1}e\), or a dense
feasible point.  The separation therefore remains an output-sensitive
statement.

## Literature boundary

[Gharibian--Le Gall](https://arxiv.org/abs/2111.09079) already provide the
sampling identity behind (12) for overlaps with sparse low-degree polynomial
transforms.  [Cifuentes--Wang--Silva--Berta--Aolita](https://arxiv.org/abs/2410.13937)
give sparse-access inverse matrix-element algorithms based on polynomial
approximation.  [Montanaro--Shao](https://arxiv.org/abs/2311.06999) give
closely related dimension-independent sparse matrix-function entry upper
bounds and matching query lower bounds.  The normal-equation Chebyshev
construction itself is also standard.

The useful added statement is the norm-sensitive \(R_e\) ledger and its
parameter-matched application to the new constant-barrier affine-slice LP value
lower bound under the same SQ/vector-output contract.  It should be framed
as a matched corollary of known polynomial and importance-sampling
techniques, not as a new inverse-polynomial primitive.  A targeted search
found no prior statement of this affine-LP/full-SQ joint frontier, but
priority is not guaranteed.
