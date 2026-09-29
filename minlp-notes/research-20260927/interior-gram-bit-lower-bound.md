# Strictly positive strongly SOS-convex quartics with only long interior Gram certificates

Date: 2026-09-28. Status: complete proof passed
[fresh adversarial review](interior-gram-bit-lower-bound-review.md)
without a mathematical correction. Publication priority is unestablished.

There are polynomial-size rational quartics with a supplied strict
rational Hessian Gram, a short rational SOS certificate, and strictly
feasible ordinary Gram spectrahedra, for which every rational
**positive definite** polynomial Gram needs exponentially many bits.
The short SOS certificate has a singular Gram. Thus this result
separates interior Gram witnesses from general SOS certificates; it
does not give a lower bound for all rational PSD Grams.

All polynomial Grams below use the ordinary full monomial vector
\(z(X)\) containing every monomial of degree at most two, once each.
Its dimension is \(D=\binom{n+2}{2}\). This basis convention matters
for an encoding bound.

## Theorem

For every \(k\ge1\), one can construct a rational quartic \(f_k\)
in \(n=2k\) variables, together with rational certificates of
polynomial size in \(k\), such that:

1. \(f_k\) is strictly positive on \(\mathbb R^n\), and has a
   rational full Hessian Gram at least the identity.
2. \(f_k=z^{\mathsf T}Q_0z\) for a rational PSD matrix \(Q_0\)
   of polynomial bit length and rank at most \(n+2<D\).
3. There exists a rational positive definite matrix \(Q\) with
   \(f_k=z^{\mathsf T}Qz\).
4. Every such positive definite rational \(Q\), with reduced
   upper-triangular entry denominators \(b_{ij}\ge1\), satisfies
   \[
   \sum_{i\le j}\log_2 b_{ij}
   >
   2^k\log_2 M-1-\frac{D-1}{2}\log_2 T_+,
   \qquad
   M=1000^{k+3},\quad
   T_+=\max\{1,15(n+1)\|f_k\|_1\}.
   \tag{1}
   \]

Here \(\|f_k\|_1\) is the sum of absolute monomial coefficients.
Its logarithm is polynomially bounded in \(k\). Consequently every
positive definite rational Gram has total denominator length
\(\Omega(k2^k)=\Omega(n2^{n/2})\). This lower bound is exponential
in dimension and superpolynomial in the polynomially bounded
constructed input size. It is not stated as
\(2^{\Omega(\text{total input bits})}\).

## 1. A strictly positive quartic with a very small value

Use the reviewed construction from
[the rational-witness lower bound](strict-convex-quartic-rational-witness-lower-bound.md).
Its circuit is
\[
 \delta_0=M^{-1},\qquad
 \delta_i=(1+3\delta_{i-1}^2)^{1/3}-1,\qquad
 0<\delta_i\le\delta_{i-1}^2.
 \tag{2}
\]
It provides, in polynomial time, a rational quartic
\[
 F=\sum_{\ell=1}^{n+1}q_\ell^2
\]
with rational quadratic factors, unique zero \(p\), and a supplied
rational positive definite full Hessian Gram \(M_0\).
All coefficient lengths are polynomial in \(k\).
Its rational normalization satisfies \(1<\kappa<2\).
The rational affine polynomial
\[
 u(X)=X_{k,1}-\kappa
\]
satisfies
\[
 0<u(p)=\kappa\delta_k\le\kappa M^{-2^k}.
 \tag{3}
\]
The dependency note verifies the circuit boxes, construction sizes,
and this quantitative estimate. No high-precision rational
approximation to \(\delta_k\) is printed in the instance.

Let \(h=n+n^2\), and set
\[
 \mu=\frac{\det M_0}{(\operatorname{tr}M_0)^{h-1}},\qquad
 \lambda=\left\lceil\frac3\mu\right\rceil,\qquad
 f_k=\lambda F+u^2.
 \tag{4}
\]
The rational Hessian Gram
\(\lambda M_0+2ee^{\mathsf T}\) is at least \(3I\), where
\(e\) selects the constant Hessian-basis coordinate associated with
\(X_{k,1}\). All data in (4) have polynomial bit length.

Since \(F\ge0\) with its only zero at \(p\), and \(u(p)>0\),
the polynomial \(f_k\) is positive everywhere. Strong convexity
makes it coercive, so its attained minimum is strictly positive.
At the particular algebraic point \(p\),
\[
                 f_k(p)=u(p)^2<4M^{-2^{k+1}}.
 \tag{5}
\]
No estimate of the actual minimizer or its arithmetic degree is used.

If \(c_\ell\) and \(a\) are the rational coefficient vectors of
\(q_\ell\) and \(u\) in \(z\), then
\[
 Q_0=\lambda\sum_{\ell=1}^{n+1}c_\ell c_\ell^{\mathsf T}
                         +aa^{\mathsf T}
 \tag{6}
\]
is a polynomial-size rational PSD Gram. Its rank is at most \(n+2\),
strictly smaller than \(D\) because \(n=2k\ge2\).
Positive rational scalar weights can be split into polynomially many
rational squares by binary expansion. Thus there is also a short
ordinary rational polynomial SOS, not merely a weighted certificate.

## 2. Positive definite rational Grams do exist

We give the existence argument to avoid a vacuous lower bound.
It is the reviewed Taylor-Gram lemma from
[the unconstrained sign reduction, Section 5](unconstrained-quartic-posslp-reduction.md#5-rational-sos-membership-is-hard-in-the-same-strict-class).

Let a rational quartic \(f\) have a rational full Hessian Gram
\(A\succeq I\) and a positive attained minimum. Choose a rational
point \(q\) sufficiently close to its minimizer that
\[
 c=f(q)-\tfrac12\|\nabla f(q)\|^2>0.
 \tag{7}
\]
Put \(d=X-q\) and \(g=\nabla f(q)\). Rational Taylor SOS
integration, after subtracting \(\tfrac12\|d\|^2\), gives
\[
 f=S_q+\tfrac12\|d+g\|^2+c,\qquad
 S_q=f-f(q)-g^{\mathsf T}d-\tfrac12\|d\|^2
       \in\Sigma\mathbb Q[X]^2.
 \tag{8}
\]
In detail, rational PSD Hessian Grams give rational weighted squares;
the identity
\[
 \int_0^1(1-t)(U+tV)^2\,dt
       =\tfrac12(U+V/3)^2+(V/6)^2
 \tag{9}
\]
integrates their affine dependence on \(t\). Rational positive
weights require no coefficient-field extension.

Moreover
\[
 A-\operatorname{diag}(I,0)
                  \succeq\operatorname{diag}(0,I_{n^2}).
 \tag{10}
\]
The explicit lower block in (10) contributes Taylor square factors
\(d_id_j/6\) for all \(i,j\). They span the homogeneous quadratic
terms in \(d\); the completed squares in (8) and its positive constant
span the affine terms. The rational factor coefficient vectors
therefore span the full degree-at-most-two polynomial space, yielding
a rational positive definite Gram. Translation from \(d\) to \(X\)
is an invertible rational basis change.

This proves existence for \(f_k\). It places no upper bound on the
bit length of \(q\), \(c\), or the resulting Gram.

## 3. Every PSD Gram has a uniform norm bound

Let \(B=\mathbb E[z(X)z(X)^{\mathsf T}]\), for the uniform
probability measure on \([-1,1]^n\). We claim
\[
                       B\succeq \frac{1}{15(n+1)}I.
 \tag{11}
\]
Indeed, for a quadratic polynomial
\[
 a_0+\sum_i b_iX_i+\sum_i c_iX_i^2+\sum_{i<j}d_{ij}X_iX_j,
\]
orthogonality of the centered square monomials gives its squared
\(L^2\) norm as
\[
 \left(a_0+\frac13\sum_i c_i\right)^2
       +\frac13\sum_i b_i^2
       +\frac4{45}\sum_i c_i^2
       +\frac19\sum_{i<j}d_{ij}^2.
 \tag{12}
\]
Writing the first parenthesis as \(a'\), we have
\[
 a_0^2\le2(a')^2+\frac{2n}{9}\sum_i c_i^2.
 \tag{13}
\]
Comparison of (12) with (13) proves (11):
\(2/[15(n+1)]\le1\),
\((1+2n/9)/[15(n+1)]\le4/45\), and the other two
coefficient bounds are immediate.

For any PSD Gram \(Q\) of \(f_k\),
\[
 \frac{\operatorname{tr}Q}{15(n+1)}
       \le\operatorname{tr}(QB)
       =\mathbb E[f_k(X)]\le\|f_k\|_1.
 \tag{14}
\]
Hence \(\|Q\|_{\rm op}\le\operatorname{tr}Q\le T_+\).
This bounds all feasible Grams, not only the constructed \(Q_0\).
The Gram spectrahedron is therefore bounded and closed, hence compact.

## 4. A small determinant forces large denominators

Let \(Q\succ0\) be any rational Gram of \(f_k\).
Since \(z(p)\) contains its constant entry one,
\[
 \lambda_{\min}(Q)
   \le \frac{z(p)^{\mathsf T}Qz(p)}{\|z(p)\|^2}
   \le f_k(p).
 \tag{15}
\]
Combining (5), (14), and (15) gives
\[
             0<\det Q<4M^{-2^{k+1}}T_+^{D-1}.
 \tag{16}
\]

Write the upper-triangular entries in reduced rational form with
positive denominators \(b_{ij}\). The positive integer
\[
                         B_Q=\prod_{i\le j}b_{ij}^2
 \tag{17}
\]
clears every denominator in the determinant expansion: an
upper-triangular entry occurs at most twice in a permutation product.
Thus \(B_Q\det Q\) is a positive integer, and
\[
                 \det Q\ge B_Q^{-1}
                     =2^{-2\sum_{i\le j}\log_2 b_{ij}}.
 \tag{18}
\]
Taking logarithms of (16)--(18) proves (1).
Because \(D=O(k^2)\) and \(\log T_+\) is polynomial in \(k\),
the exponential term dominates the subtracted polynomial.
This establishes the asserted encoding lower bound.

The strict positivity of \(\det Q\) is essential. For the short
singular Gram \(Q_0\), its determinant is zero, so (18) has no positive
integer to bound. A small polynomial value only forces a small
Rayleigh quotient; without positive definiteness it need not force
long rational entries.

The separately reviewed
[upper bound](interior-gram-single-exponential-upper.md) gives total
encoding length \(\operatorname{poly}(L)2^{O(n)}\) for some
positive definite rational Gram whenever the quartic is strictly
positive and a full positive definite rational Hessian Gram is supplied.
Thus exponential dependence on dimension is qualitatively necessary
and sufficient in this class. Exponent constants and polynomial
factors are not matched.

## Prior comparison and scope

The [primary-literature audit](gram-bit-size-prior.md) distinguishes
known SDP and constrained-SOS coefficient lower bounds from ordinary
polynomial Grams. It also records corrected versions of relevant
rational SOS upper bounds. This theorem concerns interior points
only; the audit's stronger all-PSD target remains unresolved here.

Compactness of ordinary Gram spectrahedra is established prior
theory: [Chua, Plaumann, Sinn, and Vinzant, Lemma 1.5](https://arxiv.org/pdf/1608.00234).
The elementary cube argument above supplies the explicit norm bound
needed by this encoding proof. Compactness itself is not a new claim.

[Gärtner, Magron, and Vallentin, Corollary 1.3](https://arxiv.org/html/2606.25118v1),
give a polynomial-time exact rational Gram construction when an
ordinary positive Gram margin is supplied, counting its rational
encoding length. Our family has no short ordinary margin:
(15) forces every positive definite Gram's smallest eigenvalue to be
less than \(4M^{-2^{k+1}}\). This does not conflict with that
quantitative theorem or its weak-membership result.

The full Hessian Gram has a uniform positive margin and polynomial
size, while every interior polynomial Gram has long expanded rational
entries. Those are different matrix representations of different
polynomials. The result does not bound the size of general PSD Grams,
and the explicit short certificate (6) rules out that stronger claim
for this family. It does not imply an NP lower bound, rule out compact
arithmetic-circuit representations, or obstruct approximate
certification at a specified tolerance.

Strict feasibility and boundedness of the Gram spectrahedron do not
ensure a short rational interior point. The possibly much smaller
ordinary Gram margin must be distinguished from the supplied strict
Hessian margin.

## Verification

Fresh independent review checked the dependency, positive definite
Gram existence, moment inequality, determinant arithmetic, and
encoding quantifiers. The author independently reread the complete
review and its checker. No mathematical correction was required.
The reviewer's retained targeted command was:

~~~text
python research-20260927/check_interior_gram_bit_lower_bound_review.py
~~~

It passed exact centered cube moments and rational LDL checks of
\(B-I/[15(n+1)]\) for \(n=1,2,3,4\). These finite checks assess
the constants and indexing; the proof above establishes all
dimensions. The author inspected the checker without rerunning the
same computation. No project-wide verification, CI inspection, or
Lean formalization was performed.
