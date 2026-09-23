# Independent audit of the McCormick density bound

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed file: [McCormick-versus-hull gap bounds](../results/mccormick-gap-degeneracy-bound.md),
especially the signed cut identity and Steps 3b, 3c, and 4.

Verdict: the bound `c*(b)<=4 sqrt(rho(G))` is correct, with
`rho(G)=max_{nonempty U} |E(G[U])|/|U|`. All factors of two, the fractional
orientation construction, and the induced-subgraph transfer check out.
This audit establishes mathematical correctness, not literature priority.

## Core proof checked independently

Let `H` be an induced weighted support graph with zero-diagonal symmetric
weighted adjacency matrix `A`, and define

```
L = sum_{ij in E(H)} |a_ij|,
N = sum_i (sum_j a_ij^2)^(1/2),
R = maximum signed cut weight - minimum signed cut weight.
```

For `f(s)=sum_{ij}a_ij s_i s_j`, cut weights equal a fixed constant minus
`f(s)/2`. Thus `R=(max f-min f)/2`. Writing two sign vectors as `s=u+v`,
`s'=u-v`, with `u,v` supported on complementary vertex sets `T,S`, gives
`f(s)-f(s')=2 v^T A_(S,T) u`. Every such complementary-support pair occurs.
Therefore

```
R = max_S ||A_(S,T)||_(infinity -> 1).
```

Choose a cut locally optimal for the nonnegative weights `a_ij^2`.
For each vertex, its crossing squared weight is at least half its total
squared weight, including vertices with zero total weight. If `X` and `Y`
are the sums of crossing row norms on the two sides, this gives
`X+Y>=N/sqrt(2)`. Sharp real Khintchine gives
`R>=max(X,Y)/sqrt(2)>=(X+Y)/(2sqrt(2))>=N/4`.
The local optimum is only an existence device here; the proof does not
claim that arbitrary local improvement takes polynomially many steps.

The network in Step 3c correctly constructs edge shares
`theta_ij+theta_ji=1`, with each vertex load at most `rho(H)`. Its finite
edge-to-endpoint capacity `|E(H)|+1` is large enough because the all-edge
source cut has capacity `|E(H)|`. A smaller cut cannot sever one of these
arcs. If `U` is its set of vertex nodes on the source side, minimizing
over admissible edge nodes gives capacity
`|E(H)|-|E(H[U])|+rho(H)|U|>=|E(H)|`. Max-flow/min-cut therefore supplies
the claimed shares. The same proof covers an edgeless graph.

At each vertex, weighted Cauchy–Schwarz gives

```
sum_j theta_ij |a_ij|
 <= sqrt(sum_j theta_ij) sqrt(sum_j theta_ij a_ij^2)
 <= sqrt(rho(H)) sqrt(sum_j a_ij^2).
```

The second inequality uses both the load bound and `theta_ij<=1`.
Summing its left side counts each edge exactly once, giving
`L<=sqrt(rho(H)) N<=4sqrt(rho(H)) R`. This is the desired cut inequality.
When there are edges, `rho(H)>0` and `R>0`; without edges one must use
the undivided inequality and the convention `c*=0`.

The same `rho(G)` controls every induced subgraph. Corollary 1 of
[Boland et al., *Bounding the gap between the McCormick relaxation and
the convex hull for bilinear functions*](https://arxiv.org/pdf/1507.08703)
then gives the global envelope-gap statement. The primary manuscript
was opened independently. The half-integral-point reduction and the
cut-range normalization agree with the result file.

## Boundaries and literature check

This density parameter is half maximum average degree, also called
fractional pseudoarboricity. It is not fractional arboricity, which has
denominator `|U|-1`. Density/orientation duality is established literature;
for example, the primary manuscript
[Kowalik, *Approximation Scheme for Lowest Outdegree Orientation and
Graph Density Measures*](https://www.mimuw.edu.pl/~kowalik/papers/orient.pdf)
discusses maximum density and the relaxed orientation problem. The proof
here is self-contained and needs no novelty claim about that duality.

The searches `McCormick convex hull gap arboricity density degeneracy`,
`graph Sidon constant arboricity bilinear polynomial discrepancy`, and
related exact phrases did not locate a matching density gap theorem.
They did locate the earlier multilinear-relaxation paper studying graph
density empirically. These limited searches do not establish novelty,
especially under alternative harmonic-analysis terminology.

## Additional elementary bipartite corollary

For a bipartite support graph with fixed sides `P,Q`, let `Delta_P` and
`Delta_Q` be the maximum degrees on those respective sides. When the
support is nonempty,

```
c*(b) <= sqrt(2 min{Delta_P,Delta_Q})
       <= sqrt(2 min{|P|,|Q|}).
```

Indeed `R>=||A_(P,Q)||_(infinity -> 1)` by the signed cut identity.
Khintchine gives `R>=(1/sqrt(2)) sum_(i in P)||a_i||_2`.
Cauchy–Schwarz on the at most `Delta_P` entries in each row gives
`R>=L/sqrt(2 Delta_P)`. Transpose for `Delta_Q`. Each induced graph
inherits the bipartition and side-degree bounds, so the same gap transfer
applies. Empty sides mean no edges and are handled separately.

The frustrated four-cycle, with three positive unit weights and one
negative unit weight, has `L=4`, `R=2`, and both side degrees equal two;
it attains equality in this bound at the centre of the box. Thus the
constant `sqrt(2)` multiplying the square root of the smaller side degree
cannot be improved uniformly. This is a direct consequence of standard
bilinear-norm inequalities and should not be claimed novel without a
separate search. It improves the generic bound for the common bipartite
flow/intensive-variable interaction graph.
