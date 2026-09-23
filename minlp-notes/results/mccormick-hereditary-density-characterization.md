# Maximum induced density characterizes the worst McCormick gap on every graph

Status: theorem and prior-art transfer independently reviewed on 2026-09-04;
see `notes/review-mccormick-hereditary-density.md`.
Novelty reassessed: the square-root density order follows from classical
Schur-multiplier theorems through the transfer below. Retain this as an explicit
McCormick consequence with an elementary proof and improved constant, not as a
new graph-norm order characterization.

## Statement

Let G=(V,E) be a finite simple undirected graph with at least one edge. For
real edge coefficients a, let

```
b_a(x) = sum_{ij in E} a_ij x_i x_j,       x in [0,1]^V,
```

and let c*(a) be the smallest nonnegative factor such that the vertical gap
between the two McCormick envelopes is at most c*(a) times the vertical gap
between the convex and concave envelopes, at every x in the box.
Coefficients may be zero unless explicitly restricted. Set

```
rho(G) = max_{nonempty U subset V} |E(G[U])| / |U|,
Gamma(G) = sup_{a in R^E, a != 0} c*(a),
Gamma_pm(G) = max_{a in {-1,1}^E} c*(a).
```

Then

```
max{1, sqrt(rho(G)/(2 log 2))}
    <= Gamma_pm(G) <= Gamma(G) <= 4 sqrt(rho(G)).                 (1)
```

The same supremum Gamma(G) results if every edge coefficient is required to
be nonzero. In particular, there are absolute constants bounding the worst
McCormick gap above and below by sqrt(rho(G)) **for each individual graph**.
The lower bound already holds for a signing with every coefficient equal to
+1 or -1, at a box point having coordinates in {0,1/2}.

The upper bound is established in
[`mccormick-gap-degeneracy-bound.md`](mccormick-gap-degeneracy-bound.md),
Step 3c and Step 4. This note proves the matching lower bound, its localization,
and the precise consequences. The density is half the maximum average degree;
it counts unweighted edges of the allowed interaction graph. It is not the
sum of coefficient magnitudes divided by the number of vertices, and is not
fractional arboricity, which uses denominator |U|-1.

For an edgeless graph, define c*(0)=Gamma(G)=Gamma_pm(G)=0. The nonempty-edge
hypothesis in (1) avoids both an empty coefficient supremum and the lower bound 1.

## Cut-range and face identities

For a nonempty vertex subset U, use only the coefficients on its induced
edge set, and write

```
f_{a,U}(s) = sum_{ij in E(G[U])} a_ij s_i s_j,   s in {-1,1}^U,
L_U(a) = sum_{ij in E(G[U])} |a_ij|,
R_U(a) = (max_s f_{a,U}(s) - min_s f_{a,U}(s))/2.
```

R_U is the difference between the maximum and minimum signed cut weights.
A zero coefficient vector gives L_U=R_U=0, and its ratio is interpreted as 0.
For any other vector, R_U>0: the degree-two Walsh characters are orthogonal,
so their nonzero linear combination is nonconstant and has mean zero.

The induced-subgraph gap formula is

```
c*(a) = max_{U subset V} L_U(a)/R_U(a).                         (2)
```

Its upper direction is Corollary 1 of
[Boland, Dey, Kalinowski, Molinaro, Rigterink](https://arxiv.org/abs/1507.08703).
The matching lower direction can be checked directly, as follows.

Take x_i=1/2 for i in U, and x_i=0 otherwise. Any convex combination of box
vertices with barycenter x has outside coordinates identically zero.
For the active coordinates write z_i=(1+s_i)/2. Their means are 1/2, so
E[s_i]=0, and

```
E[b_a(z)] = (sum_{ij in E(G[U])} a_ij + E[f_{a,U}(s)])/4.
```

Every possible expectation of f lies between its minimum and maximum.
Both extremes are attained with the required barycenter: mix s and -s
with equal probability, using f(s)=f(-s). Thus the convex-hull vertical gap
at x is R_U(a)/2. The individual McCormick product intervals have width
1/2 on U-edges and width zero on every other edge. Their weighted total
width is L_U(a)/2. The ratio is therefore L_U/R_U whenever L_U>0.

This argument legitimately uses box vertices: multilinearity expresses
every graph point (x,b_a(x)) as a convex combination of vertex graph points,
by taking independent Bernoulli coordinates of mean x.

## Random signs on an arbitrary graph

**Lemma.** For every n-vertex m-edge graph H with m>0, there is a signing
sigma in {-1,1}^{E(H)} such that

```
||f_sigma||_infinity <= sqrt(2 m n log 2).                      (3)
```

**Proof.** Choose the m edge signs independently and uniformly. For fixed
vertex signs s and lambda>0, independence and cosh(lambda)<=exp(lambda^2/2)
give

```
E[exp(lambda f_sigma(s))] <= exp(m lambda^2/2).
```

The same bound holds with -lambda. Fix one vertex sign to +1; global sign
reversal leaves every edge product unchanged, so the resulting 2^(n-1)
vertex configurations still represent every value of f_sigma. Let
Z=||f_sigma||_infinity. Pointwise,

```
exp(lambda Z)
 <= sum_{s: s_1=1} (exp(lambda f_sigma(s)) + exp(-lambda f_sigma(s))).
```

Taking expectations and then using Jensen's inequality yields

```
E[Z] <= (n log 2)/lambda + m lambda/2.
```

Choose lambda=sqrt(2 n log(2)/m). This gives E[Z]<=sqrt(2mn log 2).
At least one signing has Z no larger than its expectation. This proves (3).
No asymptotics, independence among different vertex configurations, or
assumption of graph connectivity is needed. ∎

The lemma is the elementary finite Walsh version of a classical random-sign
supremum estimate. No novelty is claimed for it.

## Proof of the lower bound in (1)

Choose U attaining rho(G), and put H=G[U], n=|U|, m=|E(H)|.
Since G has an edge, m>0 and n>=2. Apply the lemma to H. Because
R_U(sigma)<=||f_sigma||_infinity and L_U(sigma)=m,

```
L_U(sigma)/R_U(sigma)
 >= m/sqrt(2 m n log 2)
 = sqrt(rho(G)/(2 log 2)).
```

Extend sigma to **every** edge of G by giving each edge outside E(H)
any value in {-1,1}. Equation (2), or the explicit face construction above,
shows that the same lower bound holds for c*(sigma) on G. Coefficients
outside the induced subgraph do not affect the witnessing face.
This proves the stated lower bound for Gamma_pm, with full support and no
limiting argument.

Finally R_U<=L_U because |f_{a,U}(s)|<=L_U. Any nonzero coefficient vector
has some U with L_U>0, so (2) gives c*(a)>=1. Together with the cited upper
bound, this completes (1). ∎

## Zero coefficients and the whole-graph norm

Define

```
C(G) = sup_{a != 0} L_V(a)/R_V(a).
```

Then Gamma(G)=C(G). Indeed, the full-center point gives c*(a)>=L_V/R_V,
so Gamma>=C. Conversely, each ratio in (2) is a full-graph center ratio
for the vector obtained by keeping only the U-edges and zeroing all other
coefficients. Hence c*(a)<=C, proving equality.

This also handles the strict-support issue rigorously. Restrict to
L_V(a)=1. The function R_V is continuous and strictly positive on this
compact set, so L_V/R_V attains its finite maximum at some a*. Perturb
any zero components to nonzero values to obtain full-support vectors
a^(k) converging to a*. Continuity of the **whole-graph** center ratio gives

```
lim_k L_V(a^(k))/R_V(a^(k)) = C(G).
```

Since c*(a^(k)) is at least that ratio and at most Gamma(G), the supremum
over full-support vectors is also Gamma(G). This proof does not assume
continuity of c*(a) across disappearing coefficients, which need not hold.
The full-support supremum is not asserted to be attained.

For a particular coefficient vector, the upper bound can of course use
its effective graph G_a=(V,{ij:a_ij!=0}), giving c*(a)<=4sqrt(rho(G_a)).
A corresponding lower bound does **not** hold for every fixed coefficient
vector: positive coefficients can have bounded gap on very dense graphs.
Equation (1) is a worst-over-coefficients characterization of a topology.

## Consequences and interpretation

**Graph families.** For any family of finite graphs, the McCormick factors
are uniformly bounded over all real coefficients and all box points if
and only if rho is uniformly bounded over the family. Necessity already
follows by restricting to coefficients +/-1. No hereditary closure
assumption on the family is required: each individual graph exposes its
densest induced subgraph by fixing outside coordinates to zero.

**Degeneracy and arboricity.** If d is degeneracy and alpha is arboricity,
then d/2<=rho<=d and rho<=alpha<=2rho for graphs with an edge. The first
comparison follows from a subgraph of minimum degree d and a degeneracy
orientation. For the second, partitioning into alpha forests gives rho<=alpha;
label the outgoing edges of a degeneracy orientation with distinct labels
from 1,...,d to partition the graph into d forests, giving alpha<=d<=2rho.
Each label class is a forest because its orientation is acyclic and has
outdegree at most one. Thus (1) equivalently characterizes the worst
factor by sqrt(d) or sqrt(alpha), with universal constants. It is rho
that enters the sharpest upper bound proved here.

**No bound from average density alone.** A dense core can be diluted by
arbitrarily many leaves while rho and a bad face persist. For example,
start with K_{q,q} and attach q^2 leaves to a core vertex. Its global
edge/vertex ratio remains below 2, while rho>=q/2 and (1) gives an
unbounded worst factor. This example is connected and uses full-support
signings.

**No unnormalized weighted-density substitution.** Scaling a by t!=0
leaves c*(a) unchanged. A single edge of magnitude epsilon has c*=1 but
weighted density epsilon/2. Therefore replacing rho with
max_U sum_{e in E(U)}|a_e|/|U| cannot give a scale-invariant bound of this
form. The coefficient-sensitive row-norm certificate in the companion
note is the appropriate separate weighted statement.

**Scope for process systems engineering.** The theorem concerns the
vertical McCormick-versus-convex-hull gap of one bilinear function over a
box. It explains why sparsity of the densest local interaction pattern,
rather than the total number of process variables or global average
density, controls the worst possible gap. It does not assert a
multiplicative objective approximation ratio for a constrained MINLP or
for a simultaneous collection of nonlinear constraints.

## Relation to Sidon constants and novelty limits

Let S(G)=sup_a L_V(a)/||f_a||_infinity be the real Sidon constant of the
edge-supported degree-two Walsh system. Since f_a has mean zero,

```
||f_a||_infinity/2 <= R_V(a) <= ||f_a||_infinity,
S(G) <= Gamma(G) <= 2S(G).
```

For bipartite G, flipping one vertex part negates f_a, so R_V=||f_a||_infinity
and Gamma(G)=S(G). The lemma applied to a densest induced subgraph, with
zero coefficients elsewhere, also gives

```
sqrt(rho(G)/(2 log 2)) <= S(G) <= 4sqrt(rho(G)).
```

The dense Walsh-system square-root order, random-sign lower bounds,
Littlewood mixed norms, and decoupling are classical. Finite unions of
independent character systems also make qualitative boundedness for
bounded arboricity unsurprising. The transfer below establishes that the square-root density order was
already a consequence of classical operator theory. The possible remaining
contribution is the constant 4, the elementary proof, and the explicit
consequence for bilinear McCormick gaps; their publication value and novelty
require further assessment.
See [`sidon-gap-novelty.md`](../notes/sidon-gap-novelty.md) for checked
sources and remaining audit priorities.

## Existing Schur-multiplier theorem already implies the density order

The following transfer was located late in the audit and independently
checked. It materially limits the novelty claim.

Davidson and Donsig, *Norms of Schur multipliers* (2007),
[Theorems 2.4 and 1.2](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavDon_schur.pdf),
give, for any matrix T with entries bounded by the adjacency pattern P,

```
||T||_Schur <= 2 sqrt(beta(P)),
beta(P) = max_{R,C: |R|+|C|>0} |P intersect (R x C)|/(|R|+|C|),
pi(T) <= K_G ||T||_Schur,
```

where pi is the real projective tensor norm and K_G the real Grothendieck
constant. The paper attributes the underlying theory to Varopoulos and Pisier.

For the symmetric adjacency pattern, elementary counting gives

```
|P intersect (R x C)|
 <= |E(G[R union C])| + |E(G[R intersect C])|
 <= rho(G)(|R|+|C|).
```

Taking R=C equal to a densest subset proves beta(P)=rho(G).
For weighted adjacency A and T=sign(A), tensor duality gives

```
2 L_V(a) = <A,T> <= pi(T) ||A||_(infinity->1).
```

For vertex signs u,v, put p=(u+v)/2, q=(u-v)/2. Then

```
u^T A v = 2(f_a(p)-f_a(q)),
||A||_(infinity->1) <= 2 osc(f_a) = 4R_V(a).
```

The second line holds because p,q lie in the cube and multilinearity puts
their f-values between its vertex extrema. Combining yields

```
L_V(a) <= 4 K_G sqrt(rho(G)) R_V(a).
```

Thus the density order follows from existing results; our upper constant 4
improves the constant in this particular transfer. This does not establish
that 4 is the best previously available constant.
