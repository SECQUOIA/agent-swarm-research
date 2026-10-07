# Sparse quadratic hulls: local obstructions and a rejected star conjecture

Date: 2026-09-25. Status: exploratory research, with an independently checked
small counterexample and a consequence of published theorems. These are not
claimed as substantial original contributions. The primary result sought here
is a structural characterization of when continuous quadratic information can
be combined across a sparse graph without loss.

## What the repository already contains

A targeted search of the README, `results/`, `notes/`, and the September 22
scouting notes found substantial overlap with general separator arguments.
In particular,
[the September 22 novelty review](../notes/research-20260922-separator-novelty.md)
already explains why finite-feature moment matching, its approximation-duality
identity, and universal feature-count rates are established approximation and
optimal-transport ideas. Recasting them as sparse MINLP relaxations would not
supply the substantial advance requested. Existing network–simplex notes also
use common-simplex gluing. This investigation instead examines a more concrete
quadratic moment question, where common first and second moments look strong
but may carry insufficient information.

## Definitions

For a graph `G=(V,E)`, write

\[
 H_G=\operatorname{conv}\{(u_i,u_i^2,u_i u_j)_{i\in V,ij\in E}:
                  u\in[0,1]^V\}.
\]

This is the full quadratic graph hull, including equalities for the squares;
it differs from a hull that keeps only upper or lower square epigraphs.
A point belongs to `H_G` precisely when its coordinates are moments of one
probability law on the box. Compactness ensures that the ordinary convex hull
is closed, and finite-support laws suffice by Carathéodory's theorem.

Two relaxations matter:

1. `L_G` puts every edge's coordinates in the exact two-variable quadratic
   hull, adds the univariate quadratic hull at isolated vertices, and
   identifies the first and second moments of shared vertices.
2. `D_G` is the projection onto the coordinates of `H_G` of
   \[
   \begin{pmatrix}1&m^T\\m&M\end{pmatrix}\succeq0,\qquad
   \max\{0,m_i+m_j-1\}\le M_{ij}\le\min\{m_i,m_j\}
   \quad(i,j\in V).
   \]
   Crucially, `D_G` introduces moments and McCormick inequalities for
   **nonedges** as well as edges. Diagonal cases give `M_ii<=m_i`.

Always `H_G subseteq D_G subseteq L_G`. The second inclusion uses the known
exactness of PSD plus McCormick for the two-variable quadratic graph hull.

## Exact edge hulls fail on the three-vertex path

Let the path be `a-x-b`. The following local laws agree on
`E[x]=1/2` and `E[x^2]=5/16`:

| Local coordinates | Atoms | Probabilities |
| --- | --- | --- |
| `(x,a)` | `(1/4,0)`, `(3/4,1)` | `1/2`, `1/2` |
| `(x,b)` | `(0,0)`, `(5/8,1)` | `1/5`, `4/5` |

The remaining moments are

\[
 E[a]=E[a^2]=\tfrac12,\quad E[xa]=\tfrac38,
 \qquad
 E[b]=E[b^2]=\tfrac45,\quad E[xb]=\tfrac12.
\]

Thus these coordinates belong to `L_G`. They do not belong to `H_G`.
Indeed, any representing law would satisfy

\[
 E[(x-\tfrac14-\tfrac12a)^2]=0,
 \qquad E[(x-\tfrac58b)^2]=0.
\]

It would also have binary `a,b` almost surely, because the nonnegative
quantities `a-a^2,b-b^2` have zero expectations. The first identity forces
`x in {1/4,3/4}` and the second forces `x in {0,5/8}` almost surely.
Those supports are disjoint. This is a failure of common marginal information,
not a failure of local convexification.

There is a simple original-variable separating quadratic:

\[
\begin{aligned}
 P(x,a,b)
 &= (x-\tfrac14-\tfrac12a)^2+(x-\tfrac58b)^2
       +\tfrac14a(1-a)+\tfrac{25}{64}b(1-b)\\
 &=2x^2-\tfrac12x+\tfrac1{16}
       +(\tfrac12-x)a+(\tfrac{25}{64}-\tfrac54x)b.
\end{aligned}
\]

The minimum of `P` on the box is `1/128`, while the local moment point gives
expectation zero. To check the exact minimum, fix `x`; the last expression is
affine in each leaf, so some minimizing leaves are binary. At the four binary
leaf assignments the minimum over `x` is respectively

\[
 \tfrac1{32},\quad\tfrac9{128},\quad\tfrac9{32},\quad\tfrac1{128}.
\]

All four minimizing center values lie in the unit interval. In particular,
`P>=1/128` is a valid linear inequality in the sparse lifted coordinates and
is violated by the locally consistent point. The objective uses no leaf
square terms at all. Thus the example also concerns one shared convex square
and two bilinear products with binary or continuous bounded leaves.

Dense PSD plus nonedge McCormick detects this particular inconsistency.
The covariances are

\[
 \operatorname{Var}(x)=\tfrac1{16},\quad
 \operatorname{Cov}(x,a)=\tfrac18,\quad
 \operatorname{Cov}(x,b)=\tfrac1{10}.
\]

Both Cauchy–Schwarz inequalities with `x` are equalities. Any PSD completion
therefore forces `Cov(a,b)=1/5`, hence `E[ab]=3/5`.
This contradicts the nonedge McCormick bound `E[ab]<=E[a]=1/2`.
The example does **not** disprove a dense SDP formulation.

This small witness is independently reconstructed here, not asserted to be
new. In particular, the literature already studies the failure of summing
bivariate moment bounds, including numerical star examples.

## Three vertices are exact for the dense SDP projection

**Corollary of Burer–Natarajan–Willemsen.** If `G` is a forest on at most three
vertices, then `D_G=H_G`.

**Proof.** Any linear objective on the coordinates of `H_G` is a quadratic
objective whose off-diagonal interaction graph is contained in `G`.
Complement selected box variables, `u_i -> 1-u_i`, to make every nonzero
edge coefficient nonpositive. One can assign the complement choices
recursively on each tree. Diagonal coefficients and linear terms may have
arbitrary signs, which is allowed by the cited theorem.

The full PSD plus McCormick set is invariant under these affine box
symmetries: the moment matrix undergoes a congruence, and the four
McCormick inequalities for every pair permute. Burer–Natarajan–Willemsen,
Theorem 1, proves equality of the true optimum and the weaker relaxation
consisting of PSD and the upper McCormick bounds, for every submodular
quadratic objective in dimension at most three. Adding the other valid
McCormick bounds preserves equality. Thus every linear objective has the
same optimum over `D_G` and `H_G`. Both sets are compact convex sets, so
separation gives their equality. ∎

This is a useful exact formulation for a three-variable path, and it explains
precisely why adding nonedge moments can repair the local obstruction.
It is a short consequence of a strong prior theorem; its statement here
is not a claim to a major new hull result.

## Four-vertex paths already defeat finite linear-cut repairs

The preceding corollary cannot extend to arbitrary forests with the same
relaxation. Two very recent primary sources settle this point.

* Burer, Natarajan, and Willemsen,
  [arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3),
  Theorem 1 and Example 4 / Section 6.4, prove the low-dimensional result
  and give a four-dimensional counterexample. Its Hessian is tridiagonal,
  with off-diagonal entries `-14,-25,-14`: the interaction graph is a path.
  Earlier versions are materially different: v1 advertised general exactness,
  v2 retained an all-dimensional conjecture, and v3 contains a counterexample.
  The current version lists three authors and a changed title. The general
  exactness conjecture must not be reported as currently open.
* Zhang and Wang,
  [arXiv:2609.03617v1](https://arxiv.org/html/2609.03617v1),
  Sections 3–4, give a stronger obstruction. Their base objective can be
  written
  \[
  (a u_1-u_2)^2+(u_3-u_4/2)^2+a u_1
       +u_2(1-2u_3)+(2b-1)u_3(1-u_4),
  \quad a,b\in[1/2,1].
  \]
  Its only pair interactions are `12,23,34`. The perturbations used in their
  finite-cut theorem change diagonal and linear terms; their Lemma 2 keeps
  the Hessian fixed while moving the two relevant linear coefficients.
  Consequently the four-vertex-path sparsity survives the construction.

The correct quantified consequence is: **for every fixed finite family of
valid linear cuts in the full first/second-moment coordinates, there is a
quadratic objective supported on the four-vertex path for which basic PSD
plus those cuts has a positive gap.** The family may include all McCormick
inequalities. It is not one fixed objective defeating every possible valid
cut: the objective's exact supporting inequality would itself close its gap.

This excludes an objective-independent finite linear-cut repair of the basic
PSD architecture even at treewidth one and maximum graph degree two. It
says nothing by itself about richer SDP lifts, higher-degree moments,
second-order-cone lifts, adaptive objective-dependent cuts, or global
optimization complexity. The original finite-cut obstruction belongs to
Zhang and Wang; observing the retained path sparsity is an immediate
specialization, not a separate major lower bound.

## The arbitrary-star conjecture is false

The investigation next asked whether `D_G=H_G` for arbitrary stars.
The conjecture is **false**, already with five variables. A search under
copositive-matrix terminology exposed the missing obstruction. The
[separate construction](star-hull-proof-exploration.md) gives an exact rational
star instance on `[0,4]^5` with true minimum zero and a feasible dense
PSD-plus-all-McCormick point of objective `-9337/250000`. Rescaling each
variable by four gives the same conclusion on the unit box. All diagonal
quadratic coefficients are positive, and the quadratic matrix has exactly
one negative eigenvalue. The certificate is positive definite,
and every McCormick inequality has strictly positive slack.

The construction starts from Stephen Drury's
[The triangle graph T6 is not SPN](https://emis.de/ft/34748),
Electronic Journal of Linear Algebra 36 (2020), 90–93. Its analytic family
contains the rational choice `cos(theta)=24/25`, `sin(theta)=7/25`;
the [author's supporting page](https://www.math.mcgill.ca/drury/research/spn/index.html)
also states the corresponding integer matrix. A book graph with two hubs
and four leaves becomes a star after one hub is fixed as the homogenizing
coordinate. A doubly nonnegative matrix separating the copositive matrix
from the PSD-plus-nonnegative cone can be normalized and placed in a large
enough finite box so that every McCormick bound holds. This provides a
general obstruction-transfer principle, independently reviewed below.

This is an application of a strong existing copositive construction, not a
claim that Drury's obstruction itself is new. The further novelty screen
identified Qiu–Yıldırım,
[work on exact and inexact SDP–RLT box relaxations](https://doi.org/10.1007/s10898-024-01407-y),
Proposition 20 and Lemma 19, as an existing SDP–RLT optimality and
rank-one-certificate framework whose homogeneous specialization links
copositivity and SPN. The dehomogenized large-box transfer is not their
literal statement. Thus the general argument is close to established theory; dehomogenizing the book graph to a five-variable star
and constructing an explicit rational certificate are the useful specific
steps here. Whether this particular box
specialization has appeared before is not settled by the bounded search.
The immediate research value is that it decisively rejects an attractive
but false exactness conjecture. Dense first/second moments plus all box
product bounds can fail even when every interaction passes through a
single shared continuous variable.

The source history matters here too. Shaked-Monderer's 2016 claim that all
book graphs are SPN was corrected in 2017/2018. Drury disproved it for six
vertices in 2020. The
[2025 survey, CP graphs and SPN graphs](https://cot.mathres.org/issues/COT20253.pdf),
Section 4, records the corrected state. Using the original claim would
have produced a false proof. The four-variable star remains undecided in
this note; the fact that the five-vertex book graph is SPN does not by
itself prove exactness on a box.

## Consequence for every connected interaction graph with at least five vertices

**Corollary.** Let `G` be any finite connected graph on at least five vertices.
There is a rational quadratic on `[0,1]^V` with strictly positive diagonal
coefficients, strictly negative edge coefficients exactly on `E(G)`, and a
strict gap in the full PSD-plus-McCormick relaxation.

**Proof.** A spanning tree of `G` either has diameter at least three, hence
contains a four-vertex path, or is a star with at least four leaves.
Use the published submodular path counterexample in the first case, and
the submodular star counterexample above in the second. In both cases the
true minimum is zero, the square coefficients are positive, and there is
a feasible relaxation point of value `-g<0`.

Pad that point by setting all new random coordinates deterministically to
zero, and add `sum_i u_i^2` over the new vertices to the objective. The full
moment matrix remains PSD and all McCormick constraints remain valid.
The true minimum and witness value stay zero and `-g`, respectively.
Let `r` be the number of edges required by `G` that do not yet appear in
the objective. If `r>0`, add `-delta*u_i*u_j` on each such edge, with
`0<delta<g/r`. The true minimum is at least `-delta*r`, because every
product is at most one. The old witness has value at most `-g`, because
its product moments are nonnegative. Hence the gap remains positive,
and the prescribed support is now exact. Choose rational `delta` to
retain rational data. ∎

This corollary combines existing path obstructions and the explicit
book-to-star transfer. It rules out any universal exactness guarantee based
only on a connected sparsity pattern of five or more variables, even with
submodularity and positive coordinate curvature. It does not obstruct
stronger lifts, objective-dependent structure, or efficient optimization
algorithms. No claim of priority is made. The four-variable star is not
settled by this argument.

The independent reviewer checked the graph argument, padding, support
perturbation, coefficient signs, and strict-gap bound separately.

## Exact optimization remains easy for a star

A practical support oracle is elementary. Write a star objective as

\[
 q_0t^2+c_0t+\sum_{i=1}^{n-1}
             \{q_i y_i^2+(c_i+a_it)y_i\}.
\]

For fixed `t`, each leaf optimum is a clipped affine function if `q_i>0`,
and an endpoint choice if `q_i<=0`. At most two breakpoints per leaf
partition `[0,1]`; on each interval the reduced objective is a quadratic.
Its minimum is therefore found by checking interval endpoints and valid
stationary points. This gives a polynomial arithmetic algorithm for support
optimization, but does not itself yield an SDP extended formulation.
The arrangement depends on the queried objective, so treating its cells
as a fixed compact hull formulation would be unjustified.

An initial numerical probe compared this scalar elimination with dense
PSD plus McCormick using CVXPY/CLARABEL for 1,000 seeded random instances at
each of `n=4,5,6,8`. Coefficients were independently sampled with diagonal
terms uniform on `[-1,3]`, linear terms on `[-3,3]`, and edge coefficients
on `[-4,0]`. The largest reported positive gap was below `7e-9`.
A second 4,000-instance probe placed leaf-response transition intervals
throughout the box and balanced the two endpoint objective values; its
largest reported positive gap was below `6e-8`. Neither probe found the
subsequent exact counterexample. Some CLARABEL solves warned of possible
inaccuracy. This is only
counterexample-search evidence, not a correctness result or reliable
statistical estimate of exactness. The n=4 failures in the cited papers
were also hard to find by naive random sampling.

## Verification and literature scope

[The independent adversarial review](disjunctive-review.md) checks the
local witness, the symmetry/support-function argument, the finite-cut
quantifiers, and retention of path sparsity in the published perturbation.
It also caught the current-version update in the Burer paper.
[The separate transfer review](star-copositive-transfer-review.md) checks the
copositive-to-box argument, source overlap, and the star specialization.
The lead investigator additionally reconstructed the rational star witness
and every scalar quadratic piece in exact SymPy arithmetic, then ran
`python research-20260925/check_star_counterexample.py`; all checks passed.
The independent checker
`python research-20260925/check_star_independent_review.py` also passed,
including all 63 principal minors and an independently reconstructed leaf
elimination.

Exact `fractions.Fraction` arithmetic verified all moments, the four scalar
minimum values, and the forced missing moment `E[ab]=3/5`. Those checks
confirm the displayed rational calculations; they do not establish novelty
or general SDP exactness. No Lean proof was attempted: the retained finite calculations
have short exact certificates, and no major original theorem has been
established in this line. The star counterexample is also checked by a separate exact
script linked from its proof note; the scalar leaf-elimination proof avoids
relying on numerical copositivity tests.

Targeted commands run included:

* `rg` searches over the named README and research notes, followed by
  targeted `sed`/`cat` reads;
* a one-shot Python `fractions.Fraction` check of the rational witness;
* `python research-20260925/verify_disjunctive_review.py` (passed);
* `python research-20260925/check_star_counterexample.py` (passed);
* `python research-20260925/check_star_independent_review.py` (passed);
* `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python /tmp/minlp_star_gap_probe.py`
  and `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python /tmp/minlp_star_gap_targeted.py`
  for the limited randomized star probes (temporary exploratory code);
* `curl` retrieval and `pdftotext -layout` of Drury's open paper for
  source verification after a browser authentication error.

No project-wide verification or CI inspection was performed.

Primary literature inspected in this pass includes the current Burer paper,
Zhang–Wang, and Khajavirad,
[Tight semidefinite programming relaxations for sparse box-constrained
quadratic programs](https://arxiv.org/html/2601.18545v1), especially its
introduction and decomposition preliminaries. Khajavirad's sufficient
condition bounds connected components of vertices with positive loops to
size two, with additional conditions for polynomial formulation size.
The arbitrary-star counterexample with all square coordinates is not a direct
application of that sufficient condition. The paper distinguishes one-sided square
hulls from full equality graph hulls, a distinction that must be preserved.
Other search results concerning arrowhead and star quadratic forms did not
yield a checked matching theorem; this unsuccessful search is not evidence
of novelty.
