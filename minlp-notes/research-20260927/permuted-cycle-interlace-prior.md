# Permuted cycle cofactors: a consequence of classical interlace identities

Date: 2026-09-28.

The proposed Jacobsthal bound for arbitrary admissible permutations follows from classical interlace-polynomial identities. It should not be presented as a new general determinant theorem. The short deduction below also explains why oddness of the cofactor is the relevant restriction.

## Statement and conventions

Let $m\geq3$, let $S$ be the permutation matrix with row $i$ supported in column $i+1\pmod m$, and let $P$ be a permutation matrix with row $i$ supported in column $p(i)$. Assume

\[
p(i)\notin\{i,i+1\pmod m\}.
\]

Set $B=2P-I-S$. Every cofactor of $B$ has the same absolute value, denoted $t(B)$, and

\[
\boxed{t(B)\leq J_m:=\frac{2^m-(-1)^m}{3}.}
\tag{1}
\]

Equality is attained by $P=S^2$. Thus the cycle used in the quartic construction maximizes this cofactor throughout the admissible permutation class, not just among circulants. The proof is a direct consequence of established identities, independent of finite enumeration.

Here a rooted arborescence is an in-tree: every nonroot vertex has one outgoing arc, and following outgoing arcs leads to the root. Euler tours are counted modulo cyclic rotation, with distinct arcs distinguished. For an Eulerian 2-in/2-out digraph, the BEST theorem identifies this Euler-tour count with the arborescence count at any fixed root. There is no extra factor of $m$.

## The classical ingredients and what was inspected

1. Richard Arratia, Béla Bollobás, and Gregory B. Sorkin, *The Interlace Polynomial of a Graph*, Journal of Combinatorial Theory, Series B 92 (2004), 199–233. The [author preprint, arXiv:math/0209045v2](https://arxiv.org/pdf/math/0209045) was inspected directly. Theorem 9 identifies the number of Euler circuits of a 2-in/2-out digraph with $q_H(1)$, where $H$ is the interlace graph of any Euler circuit. Theorem 12 gives the deletion/pivot recurrence and edgeless-graph initial condition. These imply nonnegative integer coefficients and zero constant term for a nonempty graph. Remark 17 gives $q_H(2)=2^{|H|}$. Sections 11.2–11.3 were also inspected: Propositions 51 and 52 concern the largest and second-largest values without the oddness restriction and do not themselves give (1).

2. Paul N. Balister, Béla Bollobás, Jonathan Cutler, and Luke Pebody, *The Interlace Polynomial of Graphs at −1*, European Journal of Combinatorics 23 (2002), 761–767. The [author PDF](https://www.memphis.edu/msci/people/pbalistr/interlace.pdf), dated July 3, 2002, was inspected directly. Theorem 1 states

   \[
   q_H(-1)=(-1)^r2^{m-r},\qquad
   r=\operatorname{rank}_{\mathbb F_2}(I+A_H),\quad m=|H|.
   \tag{2}
   \]

   The sign in the general formula is $(-1)^r$, not $(-1)^m$. These agree when the rank is full, which is precisely the case needed below. The paper identifies earlier circle-graph versions in work of Martin and Las Vergnas; the present deduction does not claim that the identity originated with the graph-polynomial notation.

3. Zbigniew Lonc, Krzysztof Parol, and Jacek M. Wojciechowski, *On the Number of Spanning Trees in Directed Circulant Graphs*, Networks 37 (2001), 129–133. The [publisher abstract](https://onlinelibrary.wiley.com/doi/10.1002/net.2) distinguishes $g_k(m)$, the maximum for directed circulants, from $f_k(m)$, the maximum for all regular digraphs. It states $g_2(m)=\lfloor(2^m+1)/3\rfloor=J_m$, whereas the stated result for $f_k$ is asymptotic. The abstract alone does not establish (1).

4. Jacek Wojciechowski and coauthors, *Heuristic Maximization of the Number of Spanning Trees in Regular Graphs*, Journal of the Franklin Institute 343 (2006), 309–325. The [publisher abstract and section excerpts](https://www.sciencedirect.com/science/article/abs/pii/S0016003206000615) describe heuristic construction of suboptimal directed and undirected regular graphs. No exact arbitrary-permutation bound was identified in the accessible material. The complete article was not inspected.

The source search included maximum arborescences of regular digraphs, maximum Euler-tour counts in 2-in/2-out digraphs, and extremal and odd evaluations of interlace polynomials. No priority claim follows from the failure to find the displayed corollary verbatim. In particular, a three-line consequence of these classical identities has little basis for a separate novelty claim.

## Odd interlace evaluations satisfy the Jacobsthal bound

Let $H$ be any nonempty simple graph on $m$ vertices, and suppose $q_H(1)$ is odd. Write

\[
q_H(x)=\sum_{j\geq1}a_jx^j,\qquad a_j\in\mathbb Z_{\geq0}.
\]

Integer polynomials take congruent values at $1$ and $-1$ modulo 2. Thus $q_H(-1)$ is odd. Equation (2) forces $r=m$, and consequently $q_H(-1)=(-1)^m$. Since

\[
2^j-(-1)^j\geq3\qquad(j\geq1),
\]

we obtain

\[
3q_H(1)
\leq\sum_{j\geq1}a_j\bigl(2^j-(-1)^j\bigr)
=q_H(2)-q_H(-1)
=2^m-(-1)^m.
\tag{3}
\]

Equality in (3) holds exactly when $\deg q_H\leq2$, because the scalar inequality is strict for $j\geq3$. This equality condition is stated only in polynomial terms; no classification of the extremizing interlace graphs is used.

Combining (3) with the Euler-circuit interpretation and BEST gives the following useful formulation: **every Eulerian 2-in/2-out digraph with an odd rooted arborescence count has at most $J_m$ arborescences at each fixed root**. The directed graph may have distinguished parallel arcs; the associated interlace graph remains a simple graph. The permutation application below is loopless and has distinct outgoing neighbors.

## Applying the identities to $2P-I-S$

Left multiplication by $P^{-1}$ gives

\[
L=P^{-1}B=2I-P^{-1}-P^{-1}S.
\]

Under the stated support restriction, $L$ is the row Laplacian of a simple 2-in/2-out digraph $D$. The two negative entries in row $p(i)$ occur in columns $i$ and $i+1$, so they are distinct and neither is diagonal. Both row and column sums of $L$, and of $B$, vanish.

Modulo 2, $B=I+S$. A grounded principal minor of $I+S$ has determinant 1: after deleting the last row and column it is upper triangular with diagonal entries 1. Hence $B$ has rank $m-1$ over the rationals. Its left and right kernels are both spanned by the all-ones vector, so its adjugate is a nonzero scalar multiple of the all-ones matrix. In particular all signed cofactors are equal, and they are odd.

Row permutation changes a cofactor into another cofactor, up to sign. Therefore every grounded cofactor of $L$ has absolute value $t(B)$, and is odd. The directed matrix-tree theorem makes these cofactors nonnegative rooted arborescence counts. Their nonvanishing gives arborescences at every root, hence $D$ is strongly connected. It has an Euler tour and the interlace construction applies. Equation (3) now gives (1).

For $P=S^2$,

\[
B=2S^2-I-S=(S-I)(2S+I).
\]

The usual cycle eigenvalue product or a grounded determinant recurrence gives the cofactor $J_m$, as recorded in the [cyclic construction](cyclic-quartic-exponential-degree.md). Equivalently this is the rooted spanning-tree count in the directed square cycle. This last count and its circulant extremality are already classical; the important conclusion for the search is that arbitrary admissible permutations cannot improve it.

## Verification and scope

The deduction of (3), the exact sign in (2), and the matrix-to-digraph mapping were checked directly against the cited primary sources. A second agent independently reached and checked the same scalar inequality and parity argument while searching the general regular-digraph literature. That agent contributed to the argument; this is a parallel mathematical check, not a claim of a wholly uninvolved final review.

Targeted verification: `python -` with an inline `pathlib`/regular-expression check passed for balanced display delimiters, control characters, trailing whitespace, and the local Markdown link in this file. No project-wide verification or CI inspection was performed. The companion search note records exact permutation/cofactor computations, which support examples and implementation details but are unnecessary for the proof in all dimensions above.

This closes the attempt to improve the quartic degree by permuting the assignment of diagonal squares to edges of one cycle. It does not prove a universal degree bound for strongly convex rational SOS quartics, nor an upper bound $J_m$ for regular digraphs with an even arborescence count.
