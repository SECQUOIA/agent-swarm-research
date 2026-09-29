# Prior for the cyclic determinant and exposing quadratic

Date: 2026-09-28. Status: scoped primary-source audit. The determinant
and graph-energy ingredients are established. Priority of their use in
the proposed convex quartic construction is not established.

Let \(m=n+1\ge3\), with indices modulo \(m\), and let the proposed
quadrics be

\[
 q_i(x)=x_i^2-c_i x_{i+1}x_{i+2},\qquad x_0=1,
\]

where a positive tuple \(p\), with \(p_0=1\), satisfies
\(p_i^2=c_i p_{i+1}p_{i+2}\). The candidate uses rational
\(c_i\in\{1,2,1/2\}\). The companion
[toric audit](cyclic-quadratic-toric-prior.md) treats the corresponding
binomial ideals and coefficient change.

## The determinant is a known directed spanning-tree count

The exponent matrix is

\[
 E=2I-P-P^2=(I-P)(2I+P),
\]

where \(P\) shifts the cyclic coordinates. It is the out-Laplacian
of the directed square cycle, with arcs \(i\to i+1\) and
\(i\to i+2\). Every principal cofactor equals

\[
 d_m=\frac1m\prod_{\substack{\zeta^m=1\\\zeta\ne1}}
        (2-\zeta-\zeta^2)
     =\frac{2^m-(-1)^m}{3}.
\]

Indeed \(\prod_{\zeta\ne1}(1-\zeta)=m\), while
\(\prod_{\zeta\ne1}(2+\zeta)=(2^m-(-1)^m)/3\). The resulting
sequence is the Jacobsthal sequence. Tree orientation conventions
cause no discrepancy here: reversal of this graph is isomorphic to
it through \(i\mapsto-i\).

Tanaka's *Spanning trees in directed square cycles*, Theorem 4.2,
states exactly that the number of directed spanning trees rooted at
any prescribed vertex is the Jacobsthal number \(J_m\). The paper
defines the sequence by \(J_0=0,J_1=1,J_{m+2}=J_{m+1}+2J_m\).
The inspected v2 is dated January 18, 2026, although the initial
submission is from March 2025. The graph definition assumes \(m\ge5\);
the displayed elementary determinant calculation also covers the
smaller distinct-step cases \(m=3,4\).
[Primary text](https://arxiv.org/pdf/2503.12561v2).

The same paper's Theorem 1.1 credits the eigenvalue-product count to
Wojciechowski and Fellows, *Counting spanning trees in directed regular
multigraphs*, Journal of the Franklin Institute 326 (1989), 889--896.
That original article was not obtained in this audit. Yong, Zhang, and
Golin also report that Lonc, Parol, and Wojciechowski, Networks 37
(2001), 129--133, gave the closed formula and showed that steps
\(1,2\) maximize the spanning-tree count among directed circulants
with two distinct positive steps. Their Lemma 1 supplies the general
two-step eigenvalue product. Their convention counts all choices of
root and therefore gives \(m\,d_m\).
[Inspected author text, pp. 2--4](https://www.cse.ust.hk/~golin/pubs/Networks_Double_Loop.pdf).

Thus neither the Jacobsthal formula nor the determinant's exponential
growth should be presented as a new result.

## The exposing quadratic is the energy of an undirected cycle

Put \(y_i=x_i/p_i\). Then

\[
 \begin{aligned}
 Q_*(x)&=\sum_{i=0}^{m-1}p_i^{-2}q_i(x)\\
 &=\sum_i(y_i^2-y_{i+1}y_{i+2})\\
 &=\tfrac12\sum_i(y_i-y_{i+1})^2.
 \end{aligned}
\]

This identity is direct reindexing. With \(y_0=1\), it vanishes
exactly at \(y_i=1\) for every \(i\), hence at \(x=p\).
Its Hessian in the free normalized coordinates is the grounded
Laplacian of an undirected cycle. Explicitly this is the
\((m-1)\times(m-1)\) tridiagonal matrix with diagonal entries two
and adjacent off-diagonal entries minus one. Its eigenvalues are

\[
 2-2\cos(j\pi/m),\qquad j=1,\ldots,m-1.
\]

In the original free coordinates the Hessian is its congruence by
\(\operatorname{diag}(p_1^{-1},\ldots,p_{m-1}^{-1})\). Positive
definiteness is therefore the standard grounded-Laplacian property,
not a new convexity theorem. Dörfler, Simpson-Porco, and Bullo state
this property in Proposition 5.1(iv) of *Electrical Networks and
Algebraic Graph Theory: Models, Properties, and Applications*.
[Inspected author text](https://www.control.utoronto.ca/~jwsimpson/papers/2017k.pdf).

The roles of the two graphs differ: the directed square cycle controls
the exponent lattice and its determinant, while the undirected cycle
controls the quadratic energy. They should not be identified as one
Laplacian matrix.

## What the combination may add

The potentially substantive step is combining a rational coefficient
change with this exposing quadratic and a quantitative rational
convexification argument. The desired output has a rational quartic
with a unique real zero of degree \(d_m\), a uniform positive Hessian
bound, and an input description polynomial in \(m\). Those properties
do not follow from a spanning-tree count alone. Conversely, the
exposing coefficients \(p_i^{-2}\) are generally irrational, so the
identity itself is not yet the required rational output.

For a rational SOS output with nondegenerate zero, the classical bound
is \(2^n-1\); see the [degree audit](quartic-zero-degree-prior.md).
Here \(d_{n+1}\sim(2/3)2^n\). A verified construction with the claimed
encoding would approach that bound within a factor tending to
\(3/2\). This comparison is an inference about the proposed combined
construction. It is not a novelty conclusion from the literature
search.

The Tanaka PDF and extracted text, and the Dörfler--Simpson-Porco--Bullo
PDF and text, are saved in `cyclic-prior-sources/`. The displayed
determinant factorization and energy identity were checked by direct
algebra. A targeted `python -` command using SymPy verified the exact
factorization and principal cofactors for \(m=3,\ldots,12\), and the
energy identity and grounded Hessian for \(m=3,\ldots,7\). All checks
passed. Scoped Markdown formatting and local-link checks also passed.
These finite checks do not replace the general identities above. This
audit does not substitute for review of the full quartic construction,
its coefficient bounds, or its exact witness degree.
