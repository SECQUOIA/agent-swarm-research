# Exact SDP–RLT on forests with nonadjacent continuous vertices

Research date: 2026-09-27. Status: proof below, using the independently
reviewed [binary-leaf star theorem](binary-leaf-star-hull.md). The independent
[forest review](binary-separator-forest-bound-bridge-review.md) found no defect.
Priority remains unestablished.

The star theorem extends to forests by gluing distributions across binary
vertices. This gives an exact polynomial-size semidefinite representation
without a bound on the degree of a continuous vertex.

## Moment-hull theorem

Let \(F=(V,E)\) be a finite forest and let \(C\subseteq V\) be a stable
set: no edge has both endpoints in \(C\). Put \(B=V\setminus C\), and define

\[
H(F,C)=\operatorname{conv}\left\{
\big((x_i)_{i\in V},(x_c^2)_{c\in C},(x_ix_j)_{ij\in E}\big):
x_C\in[0,1]^C,\ x_B\in\{0,1\}^B\right\}.
\]

Take the full unit-box SDP–RLT system on all vertices, with moment matrix
\(\left(\begin{smallmatrix}1&\mu^T\\\mu&X\end{smallmatrix}\right)\succeq0\),
all pairwise McCormick inequalities, and \(X_{bb}=\mu_b\) for every
\(b\in B\).

**Theorem.** Its projection onto the coordinates defining \(H(F,C)\)
equals \(H(F,C)\). Auxiliary products outside \(E\) are not required to
be preserved by a representing distribution.

The full SDP–RLT region has the same projection even without the binary
diagonal equalities: increasing \(X_{bb}\) to \(\mu_b\) adds a nonnegative
diagonal matrix, preserves all RLT constraints, and changes no retained
coordinate. Thus those equalities are optional in the projected formulation.

There is also an exact formulation using separate local blocks:

- For every \(c\in C\), use one full SDP–RLT block on the star
  \(\{c\}\cup N(c)\), with binary diagonal equalities for all neighbors.
  Keep its center square, all its first moments, and its center–neighbor
  products. Leaf–leaf products in that block are auxiliary.
- For every edge \(uv\in E\) with \(u,v\in B\), impose the four
  McCormick inequalities on \((\mu_u,\mu_v,X_{uv})\).
- Identify all copies of each first moment. Include \(0\leq\mu_b\leq1\)
  for isolated binary vertices.

No PSD constraint linking distinct blocks is needed for this formulation.
Each star of degree \(d\) uses a PSD matrix of order \(d+2\), including
the constant coordinate. An isolated continuous vertex is the case \(d=0\).
The total number of scalar variables and linear constraints is
\(O(|V|+|E|+\sum_{c\in C}(\deg(c)+1)^2)=O(|V|^2)\).
This bound concerns an explicit finite conic representation; it makes no
claim about exact arithmetic running times for semidefinite optimization.

## Proof by binary separators

For each continuous-center block, the star theorem supplies a finitely
supported distribution of that center and its binary neighbors with the
specified retained moments. A point of a compact convex hull has a finite
representing distribution, so no measure-theoretic limiting construction is
needed.

For a binary–binary edge, the four probabilities are

\[
\begin{array}{ll}
p_{11}=X_{uv},&p_{10}=\mu_u-X_{uv},\\
p_{01}=\mu_v-X_{uv},&p_{00}=1-\mu_u-\mu_v+X_{uv}.
\end{array}
\]

McCormick makes them nonnegative, and they sum to one. They therefore
define the required edge distribution. An isolated binary vertex has its
Bernoulli distribution of mean \(\mu_b\).

To organize the gluing, build an incidence graph with one node for each
local bag and one node for every binary vertex. Join a bag node to each
binary vertex it contains. The continuous-center bag replaces its original
center node; a binary–binary edge is subdivided by its edge-bag node.
Thus this incidence graph is obtained from \(F\) by subdivisions and
relabeling, and is still a forest. Isolated continuous-center bags and
isolated binary vertices cause no problem.

Root each nontrivial incidence component at a bag. Draw its variables
according to its local distribution. When a child bag is reached through
a binary vertex \(b\), draw the new variables using that bag's conditional
distribution given the already drawn value of \(b\). Every bag has the
same Bernoulli marginal at \(b\), because its mean is \(\mu_b\).
Consequently this operation preserves the child's complete local
distribution as well as every distribution already realized. If one value
of \(b\) has zero probability, choose an arbitrary conditional distribution
on that unused branch. Distinct child branches may be drawn conditionally
independently.

The incidence forest ensures that a new bag shares only this already drawn
binary vertex with the preceding bags. The construction therefore never
has to reconcile different laws on a continuous separator, or on a tuple
of binary variables. Continuing through the finitely many bags yields a
finite distribution matching all retained first moments, continuous squares,
and edge products. Different forest components can be drawn independently.

This proves that the local-block formulation projects into \(H(F,C)\).
Conversely, every actual mixed binary point has feasible rank-one local
blocks and edge moments; taking convex combinations proves the reverse
inclusion. The local formulation is exact.

Every point in the full SDP–RLT face restricts to feasible local blocks.
The just-proved inclusion therefore applies to its retained coordinates.
The reverse inclusion follows again from actual rank-one moment matrices.
This proves the full-system projection statement. \(\square\)

## Consequence for continuous box quadratic optimization

Consider

\[
q(x)=c+\sum_{i\in V}b_i x_i+\sum_{i\in V}d_i x_i^2
       +\sum_{ij\in E}f_{ij}x_ix_j,
\qquad x\in[0,1]^V,
\]

where \(F=(V,E)\) is a forest. Suppose the vertices with \(d_i>0\)
form a stable set. All linear coefficients and interaction signs are
arbitrary.

**Corollary.** Full SDP–RLT is exact for this objective. There is no degree
restriction on the vertices with positive square coefficients.

**Proof.** Set \(C=\{i:d_i>0\}\) and \(B=V\setminus C\). For any
feasible full relaxation point, increase each \(X_{bb}\), \(b\in B\),
to \(\mu_b\). This adds a nonnegative diagonal matrix to the moment
matrix, so PSD is preserved; all RLT inequalities remain valid. The
linearized objective does not increase because \(d_b\leq0\).

The theorem supplies a distribution in \([0,1]^C\times\{0,1\}^B\)
matching every objective moment of the modified point. Its expected
objective is at least the minimum of \(q\) on the full box. The original
relaxation value is therefore at least that minimum as well. An actual
minimizer supplies a rank-one feasible point proving equality. \(\square\)

Equivalently, the nonpositive-square variables can be put at endpoints
without increasing a fixed point's objective, because the objective is
concave or affine in each such variable separately. The explicit remainder
is \(d_b x_b^2-d_b x_b=(-d_b)x_b(1-x_b)\), a valid diagonal RLT term.

## Prior results and the additional claim

The gluing principle is established theory. Khajavirad,
[*Tight semidefinite programming relaxations for sparse box-constrained
quadratic programs*, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2),
Lemma 4, states a decomposition result when the overlap is a complete
hypergraph with no positive loop. A singleton binary separator satisfies
that premise. Corollary 2 gives a polynomial-size SOC formulation when
positive-loop vertices form a stable set, treewidth is \(O(\log |V|)\),
and every positive-loop degree is \(O(\log |V|)\). The current v2 statement
was inspected directly on 2026-09-27.

Dey and Khajavirad,
[*A second-order cone representable class of nonconvex quadratic programs*,
arXiv:2508.18435v2](https://arxiv.org/html/2508.18435v2),
Proposition 8, gives a polynomial-size SOC formulation for forests whose
positive-loop vertices are stable and have degree \(O(\log |V|)\).
Their general stable-positive-loop result allows a larger formulation.
The current v2 proposition and its proof were inspected directly on
2026-09-27.

The added claim here is polynomial-size SDP representation and exactness
of the existing full SDP–RLT relaxation for forests with stable positive-loop
vertices of arbitrary degree. It follows from the new candidate star
projection theorem plus the established separator argument. The result is
an SDP statement; it does not remove the degree condition from the cited
polynomial-size **SOC** statements. Nor does it cover their full class of
bounded-treewidth graphs. The present compact hull retains exact continuous
squares, while their positive-loop sets use epigraph square coordinates;
an epigraph version here follows by adding nonnegative slack to the retained
continuous-square coordinates.

These comparisons do not establish priority. In particular, equivalent
mixed binary moment or graph formulations may exist outside the sources
inspected. The star note records the remaining common-factor covariance
and mixing-set comparisons needed before any publication claim.

## Limits and verification

The statement does not permit two adjacent continuous vertices in the
mixed binary hull. It also does not claim that pairwise moment matching
on a continuous separator is sufficient; that is false in general.
For graphs with cycles, the incidence graph of these bags need not be
acyclic, and matching only binary singleton marginals need not give a
joint distribution.

The theorem provides an exact local relaxation for a potentially useful
class of MINLP substructures. Adding arbitrary side constraints to the
convex hull need not yield the convex hull of the constrained problem.
No computational speedup or new general complexity classification is claimed.

The proof is analytic and uses no numerical optimization. The star theorem's
targeted checks are recorded in its own note. The independent reviewer
`/root/frontier_cube/four_star_route/four_star_bound_bridge` checked the
incidence graph, conditional gluing, zero-probability branches, projection,
degree bound, and the two current primary sources. The
[review record](binary-separator-forest-bound-bridge-review.md) found no defect;
the fresh `/root/forest_hull_review` audit is recorded separately in
[forest-hull-review.md](forest-hull-review.md). These are evidence, not
formal verification or a novelty finding. No
project-wide verification or CI inspection was performed.
