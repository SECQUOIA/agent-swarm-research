# Independent review of the compressed univariate construction

Date: 2026-09-28. Scope: the complete proof in
[the quantitative circuit construction](compressed-univariate-convex-zero-realization.md),
including all displayed constants, the center algorithm, the circuit
encoding, and the exact-value output warning. This reviewer did not
develop that construction. A fresh
[second reviewer](compressed-univariate-constants-subreview.md)
independently checked the root, coefficient, tail, and bit-length estimates.

**Finding.** No mathematical gap was found. The construction yields a
polynomial-size rational arithmetic circuit for a polynomial with the
prescribed unique real zero and second derivative at least one. This is
an effective representation theorem. It does not establish a general
optimization algorithm for convex arithmetic-circuit input or priority
over the established convexification literature.

## 1. Root and coefficient estimates

Write the leading coefficient as \(A\ge1\), and put
\(D=2d\). The height bound \(\tau\) must be an integer, as it
can always be chosen from the dense input; this ensures that the
displayed constants are rational. Cauchy's root bound is strictly below
\(R_0=2^{\tau+1}\). For \(d\ge2\), the discriminant is a
nonzero integer. If \(\rho\) is any selected pairwise root distance,
its product formula gives

\[
 1\le |\operatorname{disc}P|
 \le 2^{\tau(2d-2)}\rho^2
                    (2R_0)^{d(d-1)-2}.
\]

Taking square roots yields the draft's bound (3), which is stronger than
\(\sigma=2^{-4d^2(\tau+1)}\). The case \(d=1\) requires no
root separation. In all cases,
\(|P'(\alpha)|\ge\sigma^{d-1}\), so
\((P^2)''(\alpha)\ge2m\).

Each coefficient of \(f=P^2\) is a sum of at most \(d+1\)
products and has absolute value at most \(C_0\). The first and
second derivative coefficients are bounded by \(Q=(D+1)^2C_0\).
For derivatives of order at most three, at most \(D+1\) terms,
factors at most \(D^3\), and \(R\ge1\) give
\(|f^{(j)}|\le (D+1)^4C_0R^D=H\) on \([-R,R]\).
Terms whose derivative order exceeds their degree contribute zero.

For a degree-\(s\) polynomial, lower coefficients bounded by \(Q\)
contribute less than \(Q|x|^s/(|x|-1)\) when \(|x|>1\).
At \(|x|\ge R\), this is below \(|x|^s/4\). The leading
coefficients of \(f'\) and \(f''\) are at least two, and their
degrees are odd and even, respectively. This proves both tail signs and
the uniform bound \(f''\ge1\). When \(d=1\), the second
derivative is a constant at least two, so the same conclusion holds.

The stronger tail conclusion matters: mere pointwise positivity of
\(f''\) would not by itself supply the explicitly claimed modulus.

## 2. The three curvature regions

The radius \(r=m/(2H)\) is at most \(1/2\), and its neighborhood
of \(\alpha\) lies in \([-R,R]\). The derivative bound gives

\[
 f''(x)\ge 2m-Hr=3m/2\ge m
                   \quad\text{if }|x-\alpha|\le r.
\]

For every nonreal root \(\gamma\), its conjugate is a distinct
root, hence \(|\operatorname{Im}\gamma|\ge\sigma/2\).
The root product therefore gives
\(f(x)\ge r^2(\sigma/2)^{2(d-1)}=a\) whenever
\(|x-\alpha|\ge r\). This lower bound is valid for all real
\(x\) in question, not only the compact middle region.

Let \(z=x-c\), \(w=(1+z^2)^N\), and \(g=fw\).
The exact identity is

\[
 \frac{g''}{w}
 =f''+\frac{4Nz}{1+z^2}f'
  +\left(\frac{2N}{1+z^2}
    +\frac{4N(N-1)z^2}{(1+z^2)^2}\right)f.
\]

The center is selected after \(N\), so its required accuracy has no
circular dependence.

- On the root neighborhood, the middle term can be negative only
  between \(c\) and \(\alpha\). There both \(|z|\) and
  \(|x-\alpha|\) are at most \(\delta\), and
  \(|f'(x)|\le H\delta\). Thus
  \(g''/w\ge m-4NH\delta^2\ge m/2\).
- On the middle region, \(r/2\le |z|\le2R\). The last term is
  at least \(bN(N-1)\), whereas the first two are at least
  \(-H-2NH\). The choice \(b(N-1)\ge3H+1\) gives
  \(g''/w\ge N(H+1)-H\ge1\).
- In both tails, \(z\) has the sign of \(x\). The cross term is
  nonnegative, and the first term is at least one. Thus \(g''/w\ge1\).

These regions cover the line, including their boundaries. Since
\(w\ge1\) and \(m\le1\), multiplying by \(2/m\) gives
\(G''\ge1\) globally. The strictly positive multiplier preserves
the real zero set.

## 3. Effective center and circuit encoding

The positive leading coefficient and the unique simple real root imply
opposite signs at \(-R_0\) and \(R_0\). Exact rational bisection
therefore applies. An exact midpoint root can be used immediately;
otherwise retaining the sign-changing half preserves the root.

The draft's rational stopping conditions are stronger than necessary.
If the final width is \(w\), the midpoint error is at most \(w/2\).
Thus its stated tests certainly imply both bounds on \(\delta\),
without computing an irrational square root. The number of iterations
is polynomial, and Horner evaluation has polynomial intermediate bit
length. This verifies a Turing-time construction, not just an arithmetic
operation count.

One can check the bit accounting particularly directly by putting
\(E=8d^2(d-1)(\tau+1)\). Then

\[
 \begin{aligned}
 m&=2^{-E},\\
 r&=\frac{1}{2^{E+1}H},\\
 a&=\frac{1}{2^{3E+2d}H^2},\\
 b&=\frac{1}{2^{5E+2d+2}H^4(1+4R^2)^2}.
 \end{aligned}
\]

In particular, \((3H+1)/b\) is already an integer. The ceiling is
harmless. Every numerator and denominator used in the construction,
including the binary integer \(N\), has
\(O(d^3(\tau+\log(d+1)))\) bits.

Horner's rule uses \(O(d)\) gates for \(P\); shared binary powering
uses \(O(\log N)\) gates. The bit length of the full explicit DAG
encoding remains polynomial, including gate references and rational
constants. An unshared formula could duplicate previous powers and is
not the output representation proved here.

## 4. Exact values and simpler oracles must be separated

At the polynomial-bit-length integer \(x_0=R+1\), the base is at
least two, \(P(x_0)\) is a nonzero integer, and \(\kappa\ge1\).
Consequently \(G(x_0)\ge2^N\). A reduced rational numerator must
then have at least \(N+1\) bits. The previously reviewed cubic degree
lower bound forces exponential \(N\) for some inputs in this form,
so this is an actual output-length obstruction for exact rational values.

This obstruction does not apply to every useful query about this
particular polynomial. Zero-sublevel membership is exactly
\(P(x)=0\). Also

\[
 G'(x)=\kappa P(x)(1+(x-c)^2)^{N-1}
 \left[2P'(x)(1+(x-c)^2)+2N(x-c)P(x)\right].
\]

The outside factors other than \(P(x)\) are positive. For rational
\(x\), the sign of \(G'(x)\) can therefore be computed by
polynomial-bit arithmetic without evaluating the large power. This
distinction was sent to the author as a scope clarification and is now
included in the main note. A large
exact value alone proves no hardness result for root finding, membership,
or derivative-sign separation. General convex circuit optimization and
other value or epigraph queries require separate analysis.

## 5. Verification and limits

The universal assertions above were checked by proof reconstruction.
A fresh reviewer independently reconstructed the numerical constants and
their bit lengths. The established qualitative multiplier proof and cubic
degree lower bound were read as dependencies; this review does not claim
to establish novelty or to redo their literature searches.

A targeted inline `python - <<'PY'` command using exact `Fraction`
arithmetic checked the constructed constants, rational bisection, and
24 normalized-curvature values for \(P=X-1\), \(P=X^3-2\), and
\(P=X^3-X+1\). For each polynomial it checked the center, both nearby
points, zero, both tail boundaries, and points beyond both boundaries.
The corresponding \(N\) values had 173, 2723, and 1925 binary bits.
It also checked the positive-base and nonzero-integer facts at \(R+1\).
Every check passed without expanding a power of exponent \(N\).
These finite checks test the formulas and their arithmetic handling;
they do not establish global curvature or complexity by themselves.

The final author edits were reread directly: the integer height
assumption, rational constant types, derivative factorization, and
narrowed oracle conclusions are correct. A separate targeted inline
Python command checked this review's local links, math delimiters,
whitespace, control characters, and final newline; all checks passed.

No project-wide verification, CI inspection, or Lean formalization was
performed. The positive review is evidence for the stated proof, not a
guarantee of correctness or priority.
