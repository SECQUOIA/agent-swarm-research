# Rational optimizer height forces long maximal-rank Gram and face certificates

Date: 2026-09-28. Status: passed
[independent review](rational-circle-optimal-gram-height-review.md).
Publication priority is unestablished.

The [rational unit-circle quartics](rational-convex-quartic-minimizer-height.md)
have short rational SOS certificates, but every rational optimal Gram
of maximal rank requires an exponentially long entry. Every nonzero
rational matrix exposing their optimal Gram face also requires an
exponentially long entry. These conclusions follow from rational linear
algebra and the reviewed
[strict-Hessian moment theorem](strict-hessian-moment-arithmetic.md).
They distinguish finding some rational certificate from finding one
that has maximal rank or explicitly identifies its smallest face.

## Setting and consequences

Let \(F_k\) be the quartic from the circle construction, in
\(N=2(k+1)\) variables, with unique rational zero \(p\).
Let \(b(X)\) list the monomials of degree at most two, starting
with the constant monomial, and set
\[
 S=\binom{N+2}{2},\qquad e=b(p),\qquad
 H_k=2^k\log_2 5.
 \tag{1}
\]
Every coordinate of \(p\) belongs to \([-1,1]\), and either
terminal coordinate has reduced denominator \(5^{2^k}\).
The quartic and its full positive definite rational Hessian Gram have
polynomial input length.

The strict-Hessian moment theorem gives the following facts.

- The unconstrained order-two moment relaxation has the unique optimal
  moment matrix \(ee^{\mathsf T}\), and its value is zero.
- An optimal rational polynomial Gram \(Q\succeq0\) of rank
  \(S-1\) exists. Every such Gram has
  \(\ker Q=\mathbb R e\).
- Every nonzero PSD matrix exposing the feasible set of optimal Grams
  has the form \(Z=c\,ee^{\mathsf T}\), \(c>0\).
- The moment and SOS optimization programs have strictly feasible
  points and a strictly complementary optimal pair. The optimal-level
  Gram feasibility problem has real singularity degree one.

Rationality of the maximal-rank Gram follows by integrating the rational
Hessian certificate after translating by the rational point \(p\).
This asserts existence, not a short expanded rational matrix.

For a rational matrix, say its entries have **height at most \(B\)**
if every entry in reduced form has numerator of absolute value at most
\(2^B\) and positive denominator at most \(2^B\).
The following bounds are unconditional:

1. Every rational optimal Gram of rank \(S-1\) has an entry-height
   bound satisfying
   \[
    B\geq\frac{H_k-\log_2((S-1)!)}{S^2-1}.
    \tag{2}
   \]
   Thus some entry requires \(\Omega(2^k/N^4)\) bits.
2. Every nonzero rational PSD exposing matrix for the optimal Gram
   feasible set has an entry-height bound satisfying
   \[
                      B\geq H_k/2.
    \tag{3}
   \]
3. The unique optimal moment matrix has an entry with denominator
   exactly \(5^{2^k}\), since its constant-versus-linear entry
   is the corresponding coordinate of \(p\).

These are exponential bounds in the dimension \(N\), and
superpolynomial bounds relative to the constructed total input size.

## Proof of the maximal-rank Gram bound

Partition a rational optimal Gram according to the constant monomial:
\[
 Q=\begin{pmatrix}q_{00}&c^{\mathsf T}\\c&A\end{pmatrix},
       \qquad e=(1,w)^{\mathsf T}.
\]
The matrix \(A\) is positive definite. Indeed, a nonzero vector
\((0,u)\) cannot belong to \(\ker Q=\mathbb Re\), because
\(e_0=1\); positivity of \(Q\) then gives
\(u^{\mathsf T}Au>0\). The equation \(Qe=0\) implies
\[
                            Aw=-c.
 \tag{4}
\]
There are \(S-1\) equations, each with \(S\) rational
coefficients when the right-hand side is included.

Suppose every entry of \(Q\) has height at most \(B\).
Clear denominators separately in each row of (4), using their product.
Each row multiplier is at most \(2^{SB}\), and each resulting
integer entry has absolute value at most \(2^{(S+1)B}\).
The integer square coefficient matrix \(A'\) is nonsingular.
The determinant expansion yields
\[
 0<|\det A'|
    \leq(S-1)!\,2^{(S-1)(S+1)B}.
 \tag{5}
\]
By Cramer's rule, the reduced denominator of every entry of \(w\)
divides \(|\det A'|\). One such entry is a terminal coordinate
of \(p\), whose denominator is \(5^{2^k}\). Taking logarithms
of (5) proves (2). For all sufficiently large \(k\),
\(\log_2((S-1)!)\) is negligible compared with \(H_k\).

The same argument also gives an exponential lower bound on the total
bit length without the polynomial divisor: the logarithmic height of
each cleared row is at most the sum of denominator bit lengths in that
row plus the largest numerator bit length in the row. Summing those
bounds and applying the determinant expansion bounds the denominator
logarithm by the total encoding length of the entries used in (4), plus
\(\log_2((S-1)!)\). The per-entry statement (2) is independent of
minor choices in total encoding conventions.

## Proof of the exposing-matrix bound

Let \(Z=c\,ee^{\mathsf T}\ne0\) be rational and PSD.
Its constant entry \(Z_{00}=c\) is positive. For a linear monomial
corresponding to a terminal coordinate \(p_i\),
\[
                      p_i=Z_{0i}/Z_{00}.
 \tag{6}
\]
If both rational entries have height at most \(B\), their quotient
has a reduced denominator at most \(2^{2B}\): before cancellation,
that denominator is a product of one entry denominator and the other
entry numerator. Since \(p_i\) has denominator \(5^{2^k}\),
(3) follows. The arbitrary positive scaling of an exposing matrix
cannot remove this bound.

Such a rational exposing matrix does exist, namely
\(ee^{\mathsf T}\). It gives a valid one-step facial reduction,
but its ordinary rational entries are long.

## What remains short, and what the result does not establish

The construction supplies \(N+1\) rational quadratic square
factors of polynomial total size. Their Gram is an optimal rational
certificate of rank at most \(N+1<S-1\). Thus the lower bound does
not apply to all optimal Grams. It applies to maximal-rank optimal
Grams, to every optimal moment matrix, and to nonzero PSD matrices
exposing the full real optimal Gram feasible set.

The phenomenon does not require irrational coefficients, failure of
Slater's condition for the optimization programs, nonattainment, or
failure of strict complementarity. It also does not give a running-time
lower bound for finding some exact certificate: a short certificate is
explicitly supplied. Compact arithmetic circuits describe the optimizer
and consequently its moment and exposing matrices. The lower bounds
concern expanded rational entries.

The general strict-Hessian moment, rank, and facial-reduction statements
are dependencies, not new results claimed here. The application is
an explicit rational bounded optimizer family forcing large rational
heights despite short lower-rank certificates. The companion
[literature comparison](rational-minimizer-height-prior.md) covers the
optimizer-height context. Publication priority is unestablished.

## The general rank distinction already follows from Khachiyan's example

There is an elementary predecessor for the broad phenomenon of short
feasible PSD points but long maximal-rank points. Homogenize the
classical repeated-squaring construction discussed by
[Pataki and Touzov](https://arxiv.org/pdf/2103.00041v2). Consider the
block diagonal matrix with blocks
\[
 \begin{pmatrix}x_1&2t\\2t&t\end{pmatrix},\qquad
 \begin{pmatrix}x_j&x_{j-1}\\x_{j-1}&t\end{pmatrix}
             \quad(2\leq j\leq k).
 \tag{7}
\]
It has constant integer input coefficients and a short rank-one feasible
point \(t=x_1=\cdots=x_{k-1}=0,x_k=1\). Full-rank feasible
points exist: take \(t=1\), \(x_1>4\), and recursively
\(x_j>x_{j-1}^2\). At every full-rank point, \(t>0\), and
\[
 x_1/t>4,\qquad x_j/t>(x_{j-1}/t)^2,
                 \qquad x_k/t>2^{2^k}.
\]
If the two rational entries \(x_k,t\) have height at most \(B\),
their positive ratio is at most \(2^{2B}\). Thus \(B>2^{k-1}\).
This derivation shows that the general rank-versus-height distinction
should not be claimed as a new SDP phenomenon. The restricted quartic
realization, and its relation to a bounded rational optimizer, are the
additional features established here.

## Verification

The fresh reviewer reconstructed the Cramer bounds, the exposing-matrix
scaling argument, and the dependencies on the strict-Hessian moment
theorem. The review also checked the deduction (7). No substantive
correction was needed.

The independent checker was extended to verify, at \(k=1\), a
Taylor optimal Gram's polynomial identity, maximal rank, prescribed
kernel, principal-system recovery, and scaled exposing ratios:

```text
python research-20260927/check_rational_circle_minimizer_review.py
```

The reviewer and author ran this extended checker successfully. These
finite checks do not prove the asymptotic height bounds, which follow
from the exact arguments above. No project-wide or CI checks were run.
