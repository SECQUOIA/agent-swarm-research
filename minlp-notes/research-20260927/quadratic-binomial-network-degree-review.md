# Independent review of the quadratic binomial network degree bound

Date: 2026-09-28.

The proposed Jacobsthal upper bound passes this review for all retained equations of a strongly connected two-outgoing-arc network. Positivity of the coefficients and of the real root is unnecessary. One boundary correction is required: the strict improvement for non-Eulerian networks holds for $n\geq2$, whereas at $n=1$ the two bounds coincide. The main construction already uses $n\geq2$.

This reviewer did not develop the extension from Eulerian graphs to arbitrary strongly connected networks. The reviewer did contribute to the preceding literature investigation and independently derived the same odd interlace-polynomial bound as the source-note author. Thus this is an independent review of the network extension, not a wholly uninvolved review of the interlace corollary. The review reconstructs the network argument from its statement and checks its special cases; it does not establish novelty or formal verification.

## Statement audited

Let $m=n+1\geq2$. The vertices are $0,\ldots,n$. Vertex $i$ has outgoing neighbors $a(i),b(i)$, with repetition and loops permitted, and the resulting directed multigraph is strongly connected. Fix $c_i\in\mathbb Q^\times$ and retain all $m$ equations

\[
x_i^2=c_i x_{a(i)}x_{b(i)},\qquad i=0,\ldots,n,
\qquad x_0=1.
\]

Suppose the equations have a real solution $p$. Let $A$ count arc multiplicities, $L=2I-A$, let $\tau_i$ be the number of directed spanning in-trees rooted at $i$, and put

\[
g=\gcd(\tau_0,\ldots,\tau_n),\qquad
J_m=\frac{2^m-(-1)^m}{3}.
\]

The claimed conclusions are correct:

- The complex affine solution set has exactly $g$ points, all with nonzero coordinates and full-column-rank Jacobian.
- The number of real solutions is $|\operatorname{Hom}(G,\{1,-1\})|$, where $G$ is the finite exponent quotient of order $g$ defined below. Therefore there is a unique real solution exactly when $g$ is odd.
- The joint field degree satisfies $[\mathbb Q(p_1,\ldots,p_n):\mathbb Q]\leq g$.
- With a unique real solution, $g\leq J_m$. If the network is not Eulerian, the stronger preliminary bound is $g\leq2^{n-1}$. For $n\geq2$ this is strictly below $J_{n+1}$.

Attainment of $J_{n+1}$ by the existing cyclic construction is a separate, previously reviewed construction. This review verifies that its graph lies inside the claimed network class; it does not repeat the quartic convexity proof.

## Nonzero coordinates and the role of all equations

Consider any complex solution. If $x_i\ne0$, its equation and $c_i\ne0$ imply that both outgoing neighbors have nonzero coordinates. Starting at $x_0=1$ and following directed paths therefore proves that every coordinate is nonzero. This is a forward propagation argument: the reverse assertion that a zero coordinate forces both neighbors to vanish would be false and is not used. Repeated neighbors and loops do not affect the forward implication.

The equation with index zero must be retained after substituting $x_0=1$. It is generally an additional constraint, not an equation to discard. Keeping only the other $n$ rows changes the lattice index from the gcd $g$ to the particular cofactor $\tau_0$. The proof and stated bound concern all $m$ equations. There is no claim here for a system obtained by dropping a row.

## The lattice index is the gcd of rooted cofactors

Delete column zero of $L$ to obtain the $m\times n$ exponent matrix $B$. Its row $i$ is the exponent vector of

\[
x_i^2x_{a(i)}^{-1}x_{b(i)}^{-1}
\]

after $x_0=1$ is substituted. Multiplicities are included: a repeated neighbor contributes $-2$, and a loop cancels one of the two diagonal contributions.

Strong connectivity implies $\operatorname{rank}L=m-1$, positivity of every $\tau_i$, and

\[
\operatorname{adj}(L)=\boldsymbol 1\tau^{\mathsf T}.
\]

Thus the signed maximal minor of $B$ obtained by deleting row $i$ is $\tau_i$. In particular $B$ has rank $n$. For the row lattice

\[
\Lambda=\langle B_0,\ldots,B_n\rangle_{\mathbb Z}
\subseteq\mathbb Z^n,
\]

Smith normal form gives

\[
|G|=[\mathbb Z^n:\Lambda]
=g,\qquad G=\mathbb Z^n/\Lambda.
\]

This uses the gcd of all maximal minors. A single grounded determinant is sufficient only in the Eulerian case, when all rooted cofactors agree.

## All complex roots, real roots, and nonsingularity

Normalize by the given real solution: $x_i=p_i y_i$, with $y_0=1$. All coordinates of $p$ are nonzero. Since $p$ satisfies the original equations, the normalized equations are

\[
y_i^2=y_{a(i)}y_{b(i)}.
\]

Their torus solution set is exactly $\operatorname{Hom}(G,\mathbb C^\times)$. A finite abelian group of order $g$ has exactly $g$ complex characters. Forward propagation already excluded affine solutions outside the torus, so these are all complex roots.

Because the normalizing solution is real, a normalized solution is real exactly when its character is real-valued. The finite subgroups of $\mathbb R^\times$ lie in $\{1,-1\}$. Consequently the real roots correspond precisely to $\operatorname{Hom}(G,\{1,-1\})$. This character group is trivial exactly when $g$ is odd. None of these steps needs positive coefficients or a positive root.

For the residual vector $F_i(x)=x_i^2-c_i x_{a(i)}x_{b(i)}$, its Jacobian at any root $z$ is

\[
DF(z)=\operatorname{diag}(z_0^2,\ldots,z_n^2)
B\operatorname{diag}(z_1^{-1},\ldots,z_n^{-1}).
\]

This formula includes the anchored row and is still correct when indices repeat. Both diagonal matrices are invertible and $B$ has rank $n$, so the Jacobian has full column rank. Each of the $g$ points is therefore a nonsingular isolated root of the overdetermined system. In particular the count has no hidden multiplicity from repeated arcs or loops.

## Field degree and non-Eulerian bound

Every coordinate is algebraic. An explicit reason is that $g e_j\in\Lambda$ for each standard basis vector $e_j$. Taking an integer combination of the monomial equations yields $p_j^g\in\mathbb Q^\times$. Let $K=\mathbb Q(p_1,\ldots,p_n)$. Every embedding $K\hookrightarrow\mathbb C$ sends $p$ to a root of the same rational system. Distinct embeddings give distinct coordinate tuples, because those coordinates generate $K$. Characteristic zero makes $K/\mathbb Q$ separable, hence

\[
[K:\mathbb Q]\leq g.
\]

This counts nonreal conjugates as well as real ones. It does not assume that a conjugate is positive or that individual coordinate degrees equal the joint degree.

Write $\tau_i=g w_i$, so $w$ is the primitive positive integer left-kernel vector of $L$. Each rooted tree chooses one of the two outgoing arcs at every nonroot vertex. Some choices fail to be trees, but this injection gives $\tau_i\leq2^n$, including for distinguished parallel arcs and loops.

The vector $w$ is all ones exactly when $L$ also has zero column sums, equivalently when the graph is Eulerian. If the graph is not Eulerian, some integer $w_i\geq2$, giving

\[
g\leq\frac{\tau_i}{2}\leq2^{n-1}.
\]

If the graph is Eulerian, all $\tau_i$ equal $g$. When the real root is unique, $g$ is odd. The [classical interlace-polynomial deduction](permuted-cycle-interlace-prior.md) therefore gives $g\leq J_{n+1}$. Its normalization counts cyclic Euler circuits, which BEST identifies with a fixed-root cofactor for two outgoing arcs. It applies with loops and distinguished parallel arcs; the associated interlace graph is still simple. For the general identity at $-1$, the correct sign is $(-1)^r$, where $r=\operatorname{rank}_{\mathbb F_2}(I+A_H)$. Oddness forces $r=m$, so the required value is $(-1)^m$.

At $n=1$, the non-Eulerian bound is $1=J_2$, not a strict improvement. For example,

\[
A=\begin{pmatrix}1&1\\2&0\end{pmatrix}
\]

is strongly connected and non-Eulerian, with $(\tau_0,\tau_1)=(2,1)$ and $g=1$. For $n\geq2$, direct comparison gives $2^{n-1}<J_{n+1}$. This correction was reported to the author before the main note was written.

## Exact computational checks

The independent check enumerated every row's unordered pair of outgoing neighbors, with repetition allowed, for $m=1,2,3,4$. It retained the strongly connected cases and used exact integer Bareiss determinants. The [retained checker](check_quadratic_binomial_network_degree_review.py) verifies the rooted-cofactor bound, positivity, primitive stationary vector, all signed maximal minors of $B$, the Eulerian equivalence, the non-Eulerian bound, and the odd-index Jacobsthal bound.

| Vertices $m$ | Strongly connected graphs | Odd index | Maximum $g$ | Maximum odd $g$ | Maximum non-Eulerian $g$ |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | none |
| 2 | 4 | 3 | 2 | 1 | 1 |
| 3 | 65 | 42 | 4 | 3 | 2 |
| 4 | 2325 | 1296 | 8 | 5 | 4 |

The initial exploratory command was `python -` with the exact enumeration supplied on standard input. Its logic was preserved in the retained checker. The targeted reproducible command is:

```sh
python research-20260927/check_quadratic_binomial_network_degree_review.py
```

This retained-file command was run and passed with exactly the counts in the table. It preserves the initial exploratory calculation; the rerun verified the saved artifact. It was not a rerun of the author's permutation search.

The finite checks support the cofactor conventions and special cases; they do not establish the general lattice, character, field-degree, or interlace arguments. Those arguments were checked separately as above. No Lean verification, project-wide verification, or CI inspection was performed.

## Scope and significance

The proof rules out improving the cyclic field degree by moving to any strongly connected network of this particular quadratic binomial form with a unique real root. Its mathematical ingredients are classical: directed matrix-tree theory, Smith normal form, finite characters, and the interlace-polynomial identities. This is a useful limit on the construction strategy, not a newly proved extremal graph principle or a universal degree bound for rational strongly convex quartics.

The network extension was first checked from the proposed statement before the final main-note text was available. The later [full-text review](cyclic-quartic-binomial-bound-review.md) covers the saved manuscript and its added weighted energy and connectivity claims. No gap remains in the extension apart from the corrected $n=1$ strictness claim.
