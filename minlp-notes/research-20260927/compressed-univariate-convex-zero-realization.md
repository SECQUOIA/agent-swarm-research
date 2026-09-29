# Polynomial-size circuits for exact univariate convex zero realization

Date: 2026-09-28. Status: complete proof, independently reviewed in the
[full review](compressed-univariate-convex-zero-realization-review.md)
and [constants subreview](compressed-univariate-constants-subreview.md).
This note makes the constants in the
[univariate multiplier lemma](univariate-convex-zero-realization.md)
effective. It does not replace the separate
[exponential expanded-degree lower bound](univariate-convex-degree-lower-bound.md).

## 1. Result and output convention

Let \(P\in\mathbb Z[X]\) be irreducible of degree \(d\ge1\),
with positive leading coefficient and exactly one real root \(\alpha\).
Suppose every coefficient has absolute value at most \(2^\tau\),
where \(\tau\in\mathbb Z_{\ge1}\). The coefficients are densely encoded.

**Theorem.** A deterministic algorithm, polynomial in \(d+\tau\),
constructs \(c\in\mathbb Q\), \(\kappa\in\mathbb Q_{>0}\),
and an integer \(N\ge2\), such that

\[
 G(X)=\kappa P(X)^2\bigl(1+(X-c)^2\bigr)^N,
 \qquad G''(x)\ge1\quad(x\in\mathbb R),\qquad
                         G^{-1}(0)=\{\alpha\}.       \tag{1}
\]

The binary lengths of \(N,c,\kappa\) are
\(O(d^3(\tau+\log(d+1)))\). Consequently a rational arithmetic
circuit for \(G\), with binary addition and multiplication gates and
shared intermediate values, has polynomial size and can be constructed
in polynomial time. Its degree and dense expansion can be exponential.

The theorem concerns construction of a circuit description. It does
**not** give polynomial-time exact rational evaluation of that circuit:
even at a rational argument with polynomial bit length, the exact value
can have exponentially many bits. It also supplies no general separation
oracle or optimization algorithm for convex arithmetic-circuit input.

A rational input polynomial can first be normalized to a primitive
integer polynomial. Its new degree and coefficient length are polynomial
in the original dense rational input length. Irreducibility and the
one-real-root property are the stated input assumptions; the construction
does not need to recover every complex root.

## 2. Explicit rational constants

Put

\[
\begin{aligned}
 R_0&=2^{\tau+1},&
 \sigma&=2^{-4d^2(\tau+1)},&
 m&=\sigma^{2(d-1)},\\
 C_0&=(d+1)2^{2\tau},&
 Q&=(2d+1)^2C_0,&
 R&=4(R_0+Q+1),\\
 H&=(2d+1)^4C_0R^{2d},&
 r&=\frac{m}{2H},&
 a&=r^2(\sigma/2)^{2(d-1)},\\
 b&=\frac{a r^2}{(1+4R^2)^2},&
 N&=2+\left\lceil\frac{3H+1}{b}\right\rceil,&
 \kappa&=\frac2m.
\end{aligned}                                                    \tag{2}
\]

Every quantity is rational or integer, and their order of construction
contains no dependence on the center \(c\). The constants are
deliberately conservative. Set \(f=P^2\).

### Root and coefficient bounds

Cauchy's bound gives \(|\gamma|<R_0\) for every root \(\gamma\)
of \(P\). Separability gives a nonzero integer discriminant. Isolating
one pairwise distance in its product formula and bounding all other
distances by \(2R_0\) gives, for \(d\ge2\),

\[
 |\gamma_i-\gamma_j|
 \ge2^{-\tau(d-1)}(2R_0)^{-d(d-1)/2+1}
                                      >\sigma.             \tag{3}
\]

The much smaller dyadic \(\sigma\) in (2) is sufficient. For
\(d=1\), there are no distinct pairs to check. Since the leading
coefficient is a positive integer,

\[
 |P'(\alpha)|\ge\sigma^{d-1},\qquad
                         f''(\alpha)\ge2m.                \tag{4}
\]

Each coefficient of \(f\) has absolute value at most \(C_0\).
The coefficients of \(f'\) and \(f''\) have absolute value at
most \(Q\). Summing at most \(2d+1\) monomials, with the
derivative factors bounded by \((2d)^3\), gives

\[
       |f^{(j)}(x)|\le H
          \quad(|x|\le R,\ 0\le j\le3).                  \tag{5}
\]

Derivatives above the polynomial's degree are zero, so (5) includes
the linear-input case.

### Inner interval, middle region, and tails

We have \(0<m\le1\), \(H\ge1\), and \(r\le1/2\).
The interval \(|x-\alpha|\le r\) lies inside \([-R,R]\).
By (4)--(5),

\[
     f''(x)\ge2m-Hr\ge m,\qquad f''(x)\le H
                         \quad(|x-\alpha|\le r).          \tag{6}
\]

For every nonreal root \(\gamma\), its conjugate is another root.
Equation (3) gives \(|\operatorname{Im}\gamma|\ge\sigma/2\).
There are no other real roots. Hence for any real \(x\) with
\(|x-\alpha|\ge r\), the root product gives

\[
              f(x)\ge r^2(\sigma/2)^{2(d-1)}=a.            \tag{7}
\]

In particular this bounds the compact middle region used in the
qualitative proof. It avoids minimizing \(f\) on that region.

For the tails, the leading coefficients of \(f'\) and \(f''\)
are at least two. The former has odd degree and the latter has even
degree. If a polynomial of degree \(s\) has lower coefficients bounded
by \(Q\), the absolute value of their sum at \(|x|>1\) is at
most \(Q|x|^s/(|x|-1)\). Since \(R>4(Q+1)\), this is
less than \(|x|^s/4\) in the tails. Thus

\[
               f''(x)\ge1,\qquad xf'(x)>0
                                \quad(|x|\ge R).           \tag{8}
\]

The constant second derivative when \(d=1\) is at least two and
needs no lower-term estimate. Also \(R>|\alpha|+r+1\), as
required by the multiplier proof.

## 3. Choose the rational center after the exponent

Use rational bisection to choose \(c\) with

\[
 \delta=|c-\alpha|\le r/2,
              \qquad \delta^2\le\frac{m}{8NH}.             \tag{9}
\]

No square root or exact representation of \(\alpha\) is required.
Start with the interval \([-R_0,R_0]\). There is exactly one real
root, it is simple, and the positive leading coefficient implies opposite
signs at the endpoints. If a midpoint is a root, take that rational
midpoint as \(c\). Otherwise retain the sign-changing half. It
suffices to stop when the interval width \(w\) satisfies
\(w\le r/2\) and \(w^2\le m/(8NH)\), then take its midpoint.
These rational stopping tests are stronger than necessary but imply (9).

For \(|c-\alpha|\le r/2\) and \(|x|\le R\), we have
\(|x-c|\le2R\). Therefore the constants (2) satisfy exactly the
qualitative proof's middle-region condition, with
\(B_0=B_1=M=H\):

\[
                         b(N-1)\ge3H+1.                   \tag{10}
\]

That proof gives the following explicit bounds for
\(g=f(1+(X-c)^2)^N\), because its positive multiplier is at least
one:

- On \(|x-\alpha|\le r\), \(g''(x)\ge m/2\).
- On \(|x|\le R\), \(|x-\alpha|\ge r\),
  \(g''(x)\ge N(H+1)-H\ge1\).
- On \(|x|\ge R\), the three differentiated terms and (8)
  give \(g''(x)\ge1\).

As \(m\le1\), these bounds imply \(g''\ge m/2\)
everywhere. Scaling by \(\kappa=2/m\) proves (1) with modulus one.
The multiplier is positive, so the real zero set stays unchanged.

## 4. Bit lengths and construction cost

The displayed formulas give

\[
\begin{aligned}
 \log_2(1/\sigma)&=O(d^2(\tau+1)),\\
 \log_2(1/m)&=O(d^3(\tau+1)),\\
 \log_2R+\log_2H&=O(d(\tau+\log(d+1))),\\
 \log_2(1/r)+\log_2(1/a)+\log_2(1/b)+\log_2N
                         &=O(d^3(\tau+\log(d+1))).
\end{aligned}                                                     \tag{11}
\]

The numerator and denominator lengths obey the same polynomial bounds;
all the quantities are formed by products, fixed displayed powers, and
one rational ceiling. No expanded polynomial of degree \(N\) is
ever constructed.

The number of bisection iterations needed for (9) is bounded by a
constant times

\[
 \log R_0+\log(1/r)+\log N+\log H+\log(1/m)+1,
\]

and therefore by the same polynomial. Exact signs of \(P\) at
these dyadic midpoints are evaluated by Horner's rule. Their intermediate
numerators and denominators have polynomial length in \(d,\tau\)
and the midpoint length. Thus center construction has polynomial bit
cost, not merely a polynomial number of idealized real operations.

Represent \(P(X)\) by Horner's rule, square it, form
\(1+(X-c)^2\), and raise that base to \(N\) by binary powering.
The last step needs \(O(\log(N+1))\) multiplication gates if
intermediate powers are shared. The rational constants have polynomial
bit length. This proves the circuit construction bound. It is a directed
acyclic circuit, not an unshared formula that copies each previously
computed power at every squaring.

## 5. Why circuit construction does not supply a cheap oracle

Consider the integer argument \(x_0=R+1\). It has polynomial bit
length. Since \(|c|\le R_0+1/4<R-1\),
\(1+(x_0-c)^2\ge2\). Also \(P(x_0)\) is a nonzero integer,
because \(x_0\ne\alpha\), and \(\kappa\ge1\). Hence

\[
                              G(x_0)\ge2^N.                \tag{12}
\]

Writing this exact rational number as a reduced numerator and denominator
requires at least \(N+1\) numerator bits. When \(N\) is
exponential, no polynomial-time algorithm can write that exact value in
the ordinary rational representation.

The [cubic lower-bound family](univariate-convex-degree-lower-bound.md)
forces this situation for some inputs: every convex realization has
exponential degree, whereas (1) has degree exactly \(2d+2N\).
For those inputs the exponent \(N\) in any successful construction
of this form must be exponential. Thus the warning concerns actual
necessary growth on that family, not only loose constants in (2).

Some simpler queries about this particular polynomial are cheap.
Zero-sublevel membership \(G(x)\le0\) is exactly \(P(x)=0\).
Differentiation gives

\[
 G'(x)=\kappa P(x)(1+(x-c)^2)^{N-1}
 \left[2P'(x)(1+(x-c)^2)+2N(x-c)P(x)\right].
\]

The power is strictly positive. Thus the derivative sign at a rational
argument is computable by polynomial-bit arithmetic after factoring out
that power. The exact-value output obstruction proves no hardness for
root finding, zero-sublevel membership, or these sign queries.

The construction supplies no general polynomial-cost epigraph, value,
or derivative-value oracle for convex arithmetic circuits. It also does
not justify treating \(N\) as a small degree parameter. Logarithmic
value encodings, controlled approximate evaluation, or more general
sign comparisons require separate analysis before further solver
consequences.

## 6. Prior comparison and verification scope

The geometric multiplier method is established prior, as documented in
the [qualitative review](univariate-convex-zero-realization-review.md)
and the [degree-prior audit](univariate-convex-degree-lower-bound-prior.md).
Root separation from an integer discriminant, coefficient bounds,
rational bisection, and binary powering are standard tools. This note
combines them to distinguish polynomial-size circuit output from
necessarily large expanded degree. It makes no priority claim for
convexification or polynomial arithmetic circuits.

The new quantitative obligations are the simultaneous constants in (2),
the bounds (3)--(10), and the bit accounting in (11). The fresh adversarial
review and separate constants subreview reconstructed them independently
and found no gap. The full reviewer also checked 24 exact rational
normalized-curvature values, without expanding the enormous power; the
constants reviewer checked 20 exact constant identities. The linked
reviews record the commands and their scope. Those finite checks test
the formulas and arithmetic handling, not the universal curvature or
complexity claims. No project-wide check, CI inspection, or Lean
formalization is claimed.

After those reviews, a targeted inline `python - <<'PY'` command checked
this note and the two linked reviews for existing local links, balanced
math delimiters, control characters, trailing whitespace, and final
newlines. All three files passed. These document checks do not verify
the mathematics.
