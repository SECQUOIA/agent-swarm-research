# Independent review of the completely positive obstruction

Date: 2026-09-25. Reviewer: `cp5_boundary_review`, with a separate focused
literature search by `box_hull_novelty`.

**Verdict.** The proposed obstruction is correct: the positive-diagonal box
moment upper hull has no finite semidefinite lift in dimension at least five.
The compact-base homogenization step is valid, with the boundedness argument
given below. This is a direct consequence of the established copositive-cone
obstruction and an explicit exposed face of this particular hull. Its novelty
as a formulation-level corollary is unestablished. It is a useful limitation
on a currently studied class of convexifications, but should not be described
as a new general method for proving nonrepresentability.

Let

\[
 H_n^+=\operatorname{conv}\{(x,Y):x\in[0,1]^n,\quad
 Y_{ij}=x_ix_j\ (i<j),\quad Y_{ii}\ge x_i^2\},
 \qquad e=(1,\ldots,1)^\top.
\]

Here \(Y\) is symmetric, convex hull means finite convex combinations, and a
finite semidefinite lift means a spectrahedral shadow, with arbitrary finite
matrix order and number of auxiliary variables.

**Closedness and the exposed face.** Write

\[
 K_n=\operatorname{conv}\{(x,xx^\top):x\in[0,1]^n\},\qquad
 D=\{(0,\operatorname{Diag}(s)):s\ge0\}.
\]

Then \(H_n^+=K_n+D\). The first set is compact and the second is a closed
cone, so the sum is closed. No replacement of convex hull by closed convex
hull is needed.

Define the affine function

\[
 L(x,Y)=1-2e^\top x+e^\top Ye.
\]

At each generating point, \(Y=xx^\top+\operatorname{Diag}(s)\) with \(s\ge0\),
and hence

\[
 L(x,Y)=(1-e^\top x)^2+e^\top s\ge0.
\]

Consequently \(F_n=H_n^+\cap\{L=0\}\) is an exposed face. In any finite
convex representation of a point of this face, every positive-weight atom
has \(s=0\) and \(e^\top x=1\). Conversely every mixture of such atoms lies in
the face. Thus, with \(\Delta=\{u\ge0:e^\top u=1\}\),

\[
 F_n=\operatorname{conv}\{(u,uu^\top):u\in\Delta\}.
\]

The statement that diagonal slack vanishes refers to the individual atoms.
It does **not** assert \(Y_{ii}=x_i^2\) for the averaged point: the mixture
of two distinct simplex vertices already has positive diagonal variance.
Also, the slice \(e^\top x=1\) alone does not impose simplex support on the
atoms and cannot replace \(L=0\).

**Identification with a completely positive base.** Define

\[
 \mathrm{CP}_n=\Big\{\sum_{k=1}^r v_kv_k^\top:
                    r<\infty,\ v_k\in\mathbb R_+^n\Big\},\qquad
 B_n=\{Y\in\mathrm{CP}_n:e^\top Ye=1\}.
\]

The projection of \(F_n\) onto \(Y\) is \(B_n\), and its inverse is

\[
 Y\longmapsto(Ye,Y).
\]

For the nontrivial inclusion, decompose \(Y=\sum_k v_kv_k^\top\), discard
zero terms, and put \(a_k=e^\top v_k>0\), \(u_k=v_k/a_k\), and

\[
 \lambda_k=a_k^2.
\]

Normalization gives \(\sum_k\lambda_k=e^\top Ye=1\), while

\[
 Y=\sum_k\lambda_k u_ku_k^\top,\qquad
 Ye=\sum_k\lambda_k u_k.
\]

This also proves \(B_n=\operatorname{conv}\{uu^\top:u\in\Delta\}\), so \(B_n\)
is compact directly. Every nonzero completely positive matrix has

\[
 e^\top Ye=\sum_k(e^\top v_k)^2>0,
\]

and therefore \(\operatorname{cone}(B_n)=\mathrm{CP}_n\). This compact-base
description also proves closedness of \(\mathrm{CP}_n\): for a convergent
sequence \(t_kB_k\), the scalars \(t_k=e^\top(t_kB_k)e\) converge, and the
compactness of \(B_n\) supplies a convergent subsequence of the base points.

**Why homogenization introduces no nonzero projected points at scale zero.**
This point should be proved rather than hidden in the phrase “take the
conical hull.” Suppose a nonempty bounded set \(B\) has a finite lift

\[
 B=\{y:\exists z,\ A_0+A(y)+D(z)\succeq0\},
\]

where \(A,D\) are linear maps. Consider

\[
 C=\{y:\exists t\ge0,z,\ tA_0+A(y)+D(z)\succeq0\}.
\]

For \(t>0\), division by \(t\) gives \(y\in tB\). If \(t=0\), choose any
feasible witness \((b,z_b)\) for \(B\). For every \(\alpha\ge0\),

\[
 A_0+A(b+\alpha y)+D(z_b+\alpha z)
 =[A_0+A(b)+D(z_b)]+\alpha[A(y)+D(z)]\succeq0.
\]

Thus \(b+\alpha y\in B\) for every \(\alpha\ge0\). Boundedness forces \(y=0\).
The zero vector itself is obtained by taking \(t=z=0\). Hence

\[
 C=\operatorname{cone}(B).
\]

This argument does not assume that the auxiliary variables are bounded or
that the lifted spectrahedron has an interior point. The inequality \(t\ge0\)
can be included as a scalar diagonal block, and affine equality constraints
can be encoded by paired scalar blocks.

If \(H_n^+\) were a spectrahedral shadow, its affine section \(F_n\), its
projection \(B_n\), and the homogenized cone \(\mathrm{CP}_n\) would all be
spectrahedral shadows. Closed-cone duality and the theorem of
Bodirsky–Kummer–Thom contradict this for \(n\ge5\). In the published version,
the relevant statements are **Remark 3.17** and **Corollary 3.18**; earlier
arXiv versions use different numbering.

**A stronger graph consequence, checked algebraically in this review.**
Let \(H(G)\) be the same hull with only the edge products recorded and with
positive square epigraphs at the vertices in \(V^+\). Other vertices may have
no loop or a negative square hypograph. If the graph induced by \(V^+\)
contains a \(K_5\) minor, then \(H(G)\) is not a spectrahedral shadow.

To prove this, take five disjoint connected branch sets \(S_1,\ldots,S_5\)
of positive-loop vertices realizing the minor. For each set select a
spanning tree. Intersect \(H(G)\) with the following affine equation
(the resulting face can be the whole hull when all branch sets are singletons):

\[
 T=\sum_{\{i,j\}\text{ in the selected trees}}
        (Y_{ii}+Y_{jj}-2Y_{ij})=0.
\]

Every summand is \((x_i-x_j)^2+s_i+s_j\ge0\) at a generating point. Therefore
the atoms in this first face have one common value \(t_a\) on each branch
set \(S_a\), and zero diagonal slack at every vertex of a nonsingleton
branch set. Select a representative \(r_a\in S_a\), and select one edge
joining each pair \(S_a,S_b\). On this first face, define the affine function

\[
 L'=1-2\sum_{a=1}^5 x_{r_a}
       +\sum_{a=1}^5Y_{r_ar_a}
       +2\sum_{a<b}Y_{\text{selected edge joining }S_a,S_b}.
\]

At every atom of the first face this is

\[
 (1-\sum_{a=1}^5t_a)^2+\sum_{a=1}^5s_{r_a}\ge0.
\]

Its zero section consequently projects, using the representative diagonal
and selected interbranch products, exactly onto \(B_5\). Surjectivity follows
by assigning each coordinate of a simplex vector to its whole branch set,
assigning zero outside the branch sets, and taking all loop slacks zero.
These assignments respect every original box, product, and loop condition.
Taking mixtures gives every element of \(B_5\).

It is not necessary that \(L'\) be nonnegative on the original hull: it is
nonnegative on the first face, and affine sections preserve finite SDP
lifts. Nor does this proof claim that edge contraction preserves the whole
diagonal upper hull; that claim would require care because the contraction
equalities kill diagonal slack. The direct construction of the \(B_5\)
section avoids that issue. A fresh agent, `minor_extension_review`,
independently checked this extension and found no mathematical gap.
It specifically checked singleton branches, mixtures, extra edges, and
outside vertices with negative loops. It also reported passing exact
symbolic checks for branch sizes \((3,1,2,1,1)\) and a rational two-atom
mixture. This is independent review evidence, not a formal proof
certificate. Priority remains unestablished.

For a concrete sparse example, take the Petersen graph with an outer
five-cycle, an inner five-star, and five corresponding spokes, and put a
positive loop on every vertex. Contracting the spokes gives \(K_5\): the
outer edges supply the five distance-one pairs and the inner edges supply
the five distance-two pairs. Consequently this ten-vertex graph of maximum
degree three already has a box moment upper hull with no finite SDP lift.
This is a stronger illustration than a five-clique; it does not establish
an obstruction for all sparse graphs.

**Prior results and significance.**

| Source examined | Comparison with the present statement |
| --- | --- |
| [Bodirsky–Kummer–Thom, published paper](https://ems.press/content/serial-article-files/52505), JEMS 28 (2026), 2233–2259; online 10 July 2024 | Corollary 3.18 excludes finite SDP lifts of the copositive cone for order at least five; Remark 3.17 transfers this to the dual completely positive cone. This supplies the substantive impossibility theorem used here. |
| [Khajavirad, 2026, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2) | Its introduction defines precisely this family as \(\mathrm{QP}(G)\). For a complete graph with all positive loops this is \(H_n^+\). Its sufficient SDP-representability condition excludes three positive-loop vertices inducing at least two edges. Both v1 and the revised v2 were examined. Thus the obstruction gives a negative boundary for an existing hull family. |
| [Burer–Dong, author manuscript](https://optimization-online.org/wp-content/uploads/2010/05/2621.pdf), revised 2011, published 2013 | Studies generalized completely positive cones over the homogenized box, including low-dimensional exactness, separation, and relaxation. Its framework establishes the longstanding connection between box moments and completely positive cones, but predates the arbitrary-lift impossibility theorem. Diagonal upward closure is the additional feature addressed by the exposed face here. |
| [Burer, 2009, local source](../literature/papers/burer2009-on-the-copositive-representation-of/paper.md) | Provides general completely positive reformulations and normalized matrix formulations. These make the simplex-base representation standard background rather than a novel contribution. |
| [Nishijima, 2026, arXiv:2602.23725v1](https://arxiv.org/html/2602.23725v1) | Extends nonrepresentability to completely positive and copositive cones over symmetric cones of rank at least five, using a section argument. This does not directly cover the homogenized box, but shows that transferring the known obstruction through sections is an established strategy. |
| [Hogben–Shaked-Monderer, SPN Graphs, 2019](https://www.aimath.org/~hogben/Hogben_Shaked-Monderer_SPNgraphs.pdf), examined in the separate minor subreview | Studies when sparse copositive matrices decompose as a positive semidefinite matrix plus a nonnegative matrix, including graph subdivisions. Failure of this decomposition does not imply absence of every finite SDP lift. A related earlier result has a [corrigendum](https://arxiv.org/abs/1712.05115), so comparisons with that graph literature require care. |

Searches included combinations of “box,” “hypercube,” “quadratic upper
hull,” “positive diagonal,” “positive loops,” “QP(G),” “spectrahedral
shadow,” “Bodirsky,” and “semidefinite representability.” No exact matching
box-upper-hull corollary was located in this search. This is limited search
evidence, not a novelty proof. A later dedicated screen for the graph
extension used combinations of “completely positive completion,”
“copositive,” “K5 minor,” “Petersen,” and “spectrahedral.” It found the SPN
graph literature above but no matching arbitrary-lift obstruction.
That additional negative search result still does not establish novelty.

The proved consequence excludes a single exact finite SDP description of
the joint hull, even with arbitrarily many auxiliary variables and without
a polynomial-size restriction. It does not show that every individual
quadratic epigraph lacks an SDP lift, exclude objective-dependent exact
formulations, preclude convergent SDP hierarchies, or settle the four-variable
case. Its likely value is to delimit structural classes for exact
convexification and guide attention toward approximation or additional
structure. Any solver benefit remains to be established.

**Targeted verification actually run.** The command
`python research-20260925/verify_cp5_face.py` passed. It expanded the
five-variable exposing identity exactly and checked a rational CP
decomposition with vectors \((1,2,0,0,0)\), \((0,1,1,0,1)\), and

\((0,0,0,2,0)\). The normalized weights were \(9/22,9/22,2/11\). Assertions
checked their sum, the normalized rank-one decomposition, \(Ye=x\), and

\(1-2e^\top x+e^\top Ye=0\). It also enumerated the Petersen graph edges,
checked degree three at every vertex, and verified that contracting the
five spokes gives precisely the ten pairs of \(K_5\). An earlier inline
`python - <<'PY'` command ran the same symbolic and normalization assertions
before the reusable script was created. These checks corroborate the
algebra, one normalization example, and the finite graph construction.
They do not verify the external
nonrepresentability theorem, establish novelty, or replace the proofs
above. No project-wide verification, CI inspection, or Lean proof was run.
