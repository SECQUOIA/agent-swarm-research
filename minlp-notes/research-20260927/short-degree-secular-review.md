# Review of the short-instance specialization argument

Date: 2026-09-27. Reviewed Sections 5–6 of
[the effective Hilbert audit](sharp-degree-effective-hilbert-audit.md),
including the corrected value resultant. No substantive gap remains in
the degree, height, specialization, or dense-output argument.

The raw resultant normalization is correct. With
\(f=tA^2-N\), its roots \(\lambda_k\), and
\(g=(Y+\lambda t)A+W\), the product formula gives

\[
 [Y^{2r}]\operatorname{Res}_\lambda(f,g)
 =t^{r+1}\prod_k A(\lambda_k)
 =t\operatorname{Res}_\lambda(f,A).
\]

At \(t=0\), both polynomials lose their highest homogeneous terms, so
their homogenizations have a common root at infinity. Thus the raw
resultant is divisible by \(t\). The quotient has constant leading
coefficient

\[
 c=(-1)^r\left(\prod_i b_i^2\right)
   \prod_{i<j}(d_i-d_j)^4\ne0.
\]

If this quotient is \(cY^{2r}+a_{2r-1}Y^{2r-1}+\cdots+a_0\),
then substituting \(Y/c\) and multiplying by \(c^{2r-1}\) gives a
monic polynomial for \(c\beta_j\). This scaling preserves the stated
polynomial degree and logarithmic-height bounds. Integrality of the sum,
together with the integral closure of \(\mathbb Z[T]\) in
\(\mathbb Q(T)\), puts its monic minimal polynomial in
\(\mathbb Z[T,Y]\).

The root bounds on the unit circle and at infinity justify both estimates
in (8). The elementary symmetric function of order \(k\) is bounded by
\(\binom Dk M^k\) when all conjugates of the sum are bounded by \(M\).
Cauchy's coefficient estimate then bounds its coefficient height. Growth
\(O(|T|^{kL})\) bounds its polynomial degree by \(kL\).

For \(m=\deg_TP\), use the explicit transformed polynomial

\[
 Q(U,Y)=U^mP(1+1/U,Y).
\]

Its leading coefficient in \(Y\) is \(U^m\), and
\(Q(0,Y)=[T^m]P\ne0\). Consequently it has no polynomial content,
and every positive integer specialization retains degree \(D\).
The coefficient of \(U^mY^D\) is one, so its integer content is also
one. Direct expansion gives
\(H(Q)\le(m+1)2^mH(P)\). The hypothesis \(m\ge1\) follows from
\(\gamma'=-c\sum_j\lambda_j\ne0\) on the optimizer branch:
an algebraic function satisfying a polynomial over \(\mathbb Q\)
has zero derivative in characteristic zero.

[Dèbes–Walkowiak, Theorem 3.3 and Section 4.1](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/pierre_debes/A44-DebesWalkowiakHITBounds.pdf)
have the hypotheses used in the audit. In particular, the theorem does
not require a monic polynomial. Its group-sensitive bound, including the
elementary subgroup-count substitute in the audit, supplies an integer
\(u>0\) within the stated bit bound. The root after specialization is
\(c\beta\); since \(c\in\mathbb Q^\times\), the true optimal
value has the same field and degree.

The absolute input-length exponent can be seen directly. Put \(n=hr\).
Then \(D=(2r)^h\le2^n\), so (8) implies
\(\log m,\log\log H(Q)=O(n)\). The elementary subgroup bound and
\(\log|G|=O(n\log(n+1))\) give

\[
 \log u=O(n^2\log^2(n+1)).
\]

The dense constraint matrices require \(O(hn^2)\) constant-size
entries, the objective coefficients have \(O(\log(n+1))\) bits,
and there are \(h\) right-hand sides with
\(O(\log u+\log(n+1))\) bits. Hence even
\(N=O(n^3\log^2(n+1))\) is sufficient. All implicit constants here
are absolute. The fixed-\(h\), growing-\(r\) argument in Section 6
therefore establishes the stated obstruction for dense minimal-polynomial
output.

Targeted verification run:

```text
python research-20260927/check_short_degree_secular.py
PASS: exact branch, derivative, and value-resultant checks for r=[1, 2, 3, 4]
```

These finite checks support the resultant identities; the proofs above
and the cited theorem supply the general argument. No project-wide or CI
checks were run.
