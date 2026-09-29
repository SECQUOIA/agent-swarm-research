# Independent review of the quantitative convexification constants

This review checks only the root separation, derivative bounds, and bit
lengths proposed for the univariate convexification construction. It does
not verify the construction or its significance and novelty. No defect
was found in the constants below. The proof is elementary; no numerical
root approximation is used.

Let \(P\in\mathbb Z[x]\) be primitive and irreducible of degree
\(d\geq1\), with coefficients of absolute value at most \(2^\tau\),
where \(\tau\geq1\) is an integer. Suppose \(P\) has exactly one real
root \(\alpha\). Write \(f=P^2\), and set

\[
\begin{aligned}
R_0&=2^{\tau+1},&
\sigma&=2^{-4d^2(\tau+1)},&
m&=\sigma^{2(d-1)},\\
C_0&=(d+1)2^{2\tau},&
Q&=(2d+1)^2C_0,&
R&=4(R_0+Q+1),\\
H&=(2d+1)^4C_0R^{2d},&
r&=\frac m{2H},&
a&=r^2(\sigma/2)^{2(d-1)},\\
b&=\frac{ar^2}{(1+4R^2)^2},&&&
N&=2+\left\lceil\frac{3H+1}{b}\right\rceil.
\end{aligned}
\]

## Root separation

The Cauchy bound gives \(|\alpha_i|\leq1+2^\tau\leq R_0\) for every
complex root. Irreducibility in characteristic zero implies that all
roots are simple. For \(d\geq2\), choose any pair at distance \(s\).
The discriminant is a nonzero integer, and hence

\[
1\leq |\operatorname{disc}(P)|
\leq 2^{\tau(2d-2)}s^2
       (2R_0)^{d(d-1)-2}.
\]

Consequently

\[
s\geq
2^{-\tau(d-1)-(\tau+2)(d(d-1)-2)/2}
\geq 2^{-d(d-1)(\tau+1)}
\geq\sigma.
\]

The middle inequality uses \(d\geq2\), so that
\(\tau(d-1)\leq\tau d(d-1)/2\), and discards a nonnegative
improvement from the term \(-2\). For \(d=1\) there is no pair of
distinct roots, so the assertion is vacuous.

Two useful consequences are also valid. First,
\(|P'(\alpha)|^2\geq m\), because the leading coefficient has absolute
value at least one. Second, every nonreal root has imaginary part of
absolute value at least \(\sigma/2\): its conjugate is a distinct root.
Therefore, for every real \(x\) with \(|x-\alpha|\geq r\),

\[
 f(x)\geq r^2(\sigma/2)^{2(d-1)}=a.
\]

The second consequence uses the assumption of exactly one real root.

## Derivatives on the bounded interval

Put \(n=2d\) and write \(f(x)=\sum_{i=0}^n c_ix^i\). Then
\(|c_i|\leq C_0\), and \(c_n\geq1\). Since \(R\geq1\), for
\(0\leq j\leq3\) and \(|x|\leq R\),

\[
 |f^{(j)}(x)|
 \leq(n+1)C_0 n^j R^n
 \leq(n+1)^4C_0R^n=H.
\]

Derivatives whose order exceeds the degree are zero. In particular,
\(f''(\alpha)=2|P'(\alpha)|^2\geq2m\). Since \(r\leq1/2\) and
\(|\alpha|\leq R_0\), the interval \([\alpha-r,\alpha+r]\) lies
inside \([-R,R]\). The mean value theorem therefore yields
\(f''(x)\geq 2m-Hr=3m/2\) throughout that smaller interval.

## Derivatives outside the interval

Let \(t=|x|\geq R\). Then \(t\geq2\) and \(t\geq4C_0\). Since
\(n\) is even, the leading term of \(xf'(x)\) is positive, while

\[
\left|\sum_{i=1}^{n-1} i c_i x^i\right|
\leq2C_0(n-1)t^{n-1}
\leq\frac n2 t^n.
\]

Thus \(xf'(x)\geq(n/2)t^n>0\).

When \(n=2\), \(f''(x)=2c_2\geq2\). When \(n\geq4\), its lower
terms satisfy

\[
\left|\sum_{i=2}^{n-1}i(i-1)c_i x^{i-2}\right|
\leq2C_0(n-1)(n-2)t^{n-3}
\leq\frac{n(n-1)}2t^{n-2}.
\]

Its leading term is at least \(n(n-1)t^{n-2}\), so
\(f''(x)\geq n(n-1)t^{n-2}/2\geq1\). Both conclusions hold at the
endpoints \(|x|=R\) as well.

## Binary encoding lengths

Let \(E=8d^2(d-1)(\tau+1)\). Direct substitution gives the exact
identities

\[
\begin{aligned}
m&=2^{-E},\\
r&=\frac1{2^{E+1}H},\\
a&=\frac1{2^{3E+2d}H^2},\\
b&=\frac1{2^{5E+2d+2}H^4(1+4R^2)^2}.
\end{aligned}
\]

Since \(H\) and \(R\) are integers, \((3H+1)/b\) is an integer.
Thus

\[
N=2+(3H+1)2^{5E+2d+2}H^4(1+4R^2)^2.
\]

Moreover,
\(\log_2 R=O(\tau+\log(d+1))\) and
\(\log_2 H=O(d(\tau+\log(d+1)))\). These formulas show that every
listed integer or rational constant, including the binary integer
\(N\), has encoding length
\(O(d^3(\tau+\log(d+1)))\). Reduction of rational fractions can only
decrease that length. This is a bound on the encoding of \(N\), not a
polynomial bound on its numerical value or on the size of an expanded
polynomial of degree proportional to \(N\).

## Verification scope

The inequalities and encoding identities above were checked directly,
including \(d=1\), and compared with the displayed statements in
[the quantitative draft](compressed-univariate-convex-zero-realization.md).
The height parameter \(\tau\) must be an integer; this should be stated
explicitly when the formulas are claimed to define rational constants.
One may always choose an integer coefficient-height bound from the input.

A targeted inline Python command verified the final newline, absence of
trailing whitespace and control characters, and balanced math delimiters.
The same command used `fractions.Fraction` to check the exact formulas for
\(r,a,b\) and integrality of \((3H+1)/b\) in the 20 cases
\(1\leq d\leq5\), \(1\leq\tau\leq4\); all checks passed. These
finite checks only corroborate the identities proved above. No
project-wide tests or CI checks were run.
