# A small quadratic vanishing space can force rational SOS descent

Date: 2026-09-28. Status: proof reconstructed by the author and root;
fresh adversarial review pending. The cyclic applications below are
exactly verified in specified finite dimensions; no all-dimension
combinatorial assertion is made. Publication priority is unestablished.

The [three-variable descent counterexample](ternary-rational-sos-convex-counterexample.md)
uses five independent rational quadratics at its zero. Its four-square
convex baseline leaves a direction in that vanishing space available
for a negative perturbation. The following criterion explains when
this route, and indeed every stationary quartic perturbation preserving
convexity, must fail.

For a point \(p\in\mathbb R^n\), let

\[
 \begin{aligned}
 I_2(p)&=\{q\in\mathbb Q[X]_{\leq2}:q(p)=0\},\\
 J_4(p)&=\{F\in\mathbb Q[X]_{\leq4}:
                   F(p)=0,\ \nabla F(p)=0\},\\
 W(p)&=\operatorname{span}_{\mathbb Q}
                      \{q r:q,r\in I_2(p)\}.
 \end{aligned}
 \tag{1}
\]

Always \(W(p)\subseteq J_4(p)\).

## The descent criterion

**Theorem.** Assume \(\dim_{\mathbb Q}I_2(p)=n+1\) and
\(J_4(p)=W(p)\). Suppose a rational SOS polynomial \(G\) of
degree exactly four is globally convex, has \(G(p)=0\), and
has \(\nabla^2G(p)\succ0\). Then every rational globally convex
polynomial \(F\) of degree exactly four satisfying

\[
 F(p)=0,\qquad\nabla F(p)=0,
                   \qquad\nabla^2F(p)\succ0
 \tag{2}
\]

has a positive definite rational Gram matrix in any rational basis of
\(I_2(p)\). In particular, it is rational SOS.

The positive definite matrix is on the vanishing-quadratic basis, not
the full degree-at-most-two monomial basis. A positive definite Gram
matrix on the full monomial basis would contradict \(F(p)=0\).
The baseline assumption is rational SOS, not merely real SOS or
rational SOS-convexity.

**Proof.** Let \(q=(q_1,\ldots,q_{n+1})\) be a rational basis of
\(I_2(p)\). Every rational square factor of \(G\) has degree at
most two and vanishes at \(p\), so

\[
             G=q^{\mathsf T}S_0q,
             \qquad S_0\in\mathbb S_+^{n+1}(\mathbb Q).
\]

In fact \(S_0\succ0\). Otherwise a real factorization of this
matrix would express \(G\) as at most \(n\) real quadratic
squares. This contradicts the
[minimum SOS length theorem](convex-quartic-minimal-sos-length.md),
which requires at least \(n+1\) squares for a globally convex quartic
with a zero and positive definite Hessian there.

Because \(F\in J_4(p)=W(p)\), choose a symmetric rational matrix
\(S\) with \(F=q^{\mathsf T}Sq\). Suppose \(S\) is not
positive definite. The segment

\[
 S_t=(1-t)S_0+tS,\qquad
 F_t=(1-t)G+tF=q^{\mathsf T}S_tq
 \tag{3}
\]

has a first point \(t_*\in(0,1]\) at which \(S_{t_*}\) is
positive semidefinite and singular. Its rank is at most \(n\), so
\(F_{t_*}\) is a sum of at most \(n\) real quadratic squares.

On the other hand \(F_{t_*}\) is globally convex, vanishes at
\(p\), and has positive definite Hessian there. It has degree
exactly four. To check the last point, both fourth-degree leading
forms are nonnegative: evaluate the globally convex polynomials along
rays, using that their stationary value at \(p\) is a global minimum.
For \(t_*<1\), the nonzero nonnegative leading form of \(G\)
cannot be canceled by that of \(F\). For \(t_*=1\), the assumed
degree of \(F\) applies. The minimum-square theorem now gives a
contradiction. Hence \(S\succ0\).

Rational LDL factorization and rational square decompositions of its
positive weights give rational polynomial squares. This proves the
claim. No injectivity of the product map was assumed. \(\square\)

## A product-independence consequence

The rational SOS baseline and the dimension assumption alone imply
that the map

\[
 \mathbb S^{n+1}(\mathbb Q)\longrightarrow W(p),
                         \quad S\longmapsto q^{\mathsf T}Sq
 \tag{4}
\]

is injective. Indeed, if a nonzero symmetric matrix \(K\) mapped
to zero, choose a sign of \(K\) having a negative eigenvalue and
move from \(S_0\succ0\) along that direction. At the first singular
positive semidefinite matrix the unchanged polynomial \(G\) would
have at most \(n\) real squares, contradicting the same theorem.
Consequently

\[
 \dim W(p)=\frac{(n+1)(n+2)}2.
 \tag{5}
\]

Under all the theorem's hypotheses, the Gram matrix on \(I_2(p)\)
is unique. Thus a counterexample at a point with a rational convex SOS
baseline must exploit either more than \(n+1\) rational vanishing
quadratics or a stationary quartic outside their product span. Merely
choosing a larger perturbation does not evade the theorem.

## Exact finite evidence for the cyclic family

The [cyclic family](cyclic-quartic-exponential-degree.md) has

\[
 d=\frac{2^{n+1}-(-1)^{n+1}}3,
 \qquad p_i=a^{s_i},\quad
 s_i=\frac{(-2)^i-1}3,\quad a^d=2.
 \tag{6}
\]

Its rational SOS strongly convex quartic supplies the required
baseline. The [retained exact checker](check_cyclic_quartic_stationary_space.py)
computes the dimensions in (1) over \(\mathbb Q\), without
approximating \(a\) or building a degree-\(d\) number-field matrix.
It gave the following results:

| \(n\) | \(d\) | \(\dim I_2\) | \(\dim W\) | \(\dim J_4\) |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 3 | 6 | 6 |
| 3 | 5 | 5 | 15 | 15 |
| 4 | 11 | 5 | 15 | 15 |
| 5 | 21 | 6 | 21 | 21 |
| 6 | 43 | 7 | 28 | 28 |
| 7 | 85 | 8 | 36 | 36 |
| 8 | 171 | 9 | 45 | 45 |
| 9 | 341 | 10 | 55 | 55 |
| 10 | 683 | 11 | 66 | 66 |
| 11 | 1365 | 12 | 78 | 78 |
| 12 | 2731 | 13 | 91 | 91 |
| 13 | 5461 | 14 | 105 | 105 |
| 14 | 10923 | 15 | 120 | 120 |
| 15 | 21845 | 16 | 136 | 136 |
| 16 | 43691 | 17 | 153 | 153 |

Because \(W\subseteq J_4\), equality of the computed dimensions
proves equality of those spaces in each listed case. Thus the criterion
rules out rational SOS failure for any globally convex quartic satisfying
(2) at these specific cyclic points in dimensions 4 through 16. The
three-variable example escapes exactly through its larger \(I_2\).
The two-variable case also meets the criterion.

Here is why the finite calculations are exact. A monomial \(X^e\)
at \(p\) evaluates to \(2^h a^r\), where

\[
 \sum_i e_i s_i=hd+r,\qquad0\leq r<d.
\]

The powers \(1,a,\ldots,a^{d-1}\) are rationally independent by
Eisenstein irreducibility. Quadratic monomials therefore split into
evaluation classes indexed by \(r\); each class of size \(t\)
contributes exactly \(t-1\) independent binomial vanishing relations.

For the stationary quartic calculation, multiply derivative equation
\(j\) by the nonzero coordinate \(p_j\). A monomial then has
evaluation vector proportional to

\[
                  (1,e_1,\ldots,e_n)\,a^r.
\]

The nonzero rational proportionality factor is \(2^h\). Each
residue class can consequently be ranked separately using these
integer exponent vectors. The kernel dimension is \(\dim J_4\).
Finally the checker multiplies the exact binomial basis of \(I_2\),
groups products by the same residues, and computes their ranks using
Python's exact `Fraction` arithmetic. It uses neither modular rank
heuristics nor floating-point tolerances.

Command actually run:

```text
python research-20260927/check_cyclic_quartic_stationary_space.py
```

All listed ranks were computed successfully. The finite computation
does not prove the pattern for arbitrary \(n\). A uniform description
of the low-degree cyclic exponent collisions would be required for
that claim. No project-wide verification or CI checks were run.

## Consequence for the research direction

The desired stronger construction would force every real field carrying
an exact SOS certificate to contain an algebraic field of degree
exponential in a short input. The cyclic singleton family supplies the
large field, but the evidence above blocks its simplest stationary
quartic perturbations in many dimensions. A useful next route must
change the coordinate configuration, enlarge its quadratic vanishing
space, or produce a stationary quartic outside the product span. This
criterion is a proved obstruction to a method under its hypotheses,
not a lower bound for arbitrary lifted representations or certificate
systems. Its novelty has not been checked against the SOS-length and
convex Gram-slice literature.
