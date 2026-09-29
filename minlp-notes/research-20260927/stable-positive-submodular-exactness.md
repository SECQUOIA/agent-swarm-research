# Exact SDP with upper RLT when the positive diagonal vertices are stable

Research date: 2026-09-27. Status: proved below using the independently
reviewed [submodular star theorem](binary-leaf-star-hull.md), with a fresh
[adversarial review](stable-positive-submodular-review.md) and targeted
checks. Priority remains unestablished.

The first-order SDP relaxation with only upper RLT inequalities is exact
for a submodular box quadratic whenever no two variables with positive square coefficients
interact. The interaction graph may have cycles and unbounded degree.
A feasible SDP point also gives at most \(|B|+1\) explicit box points,
one of which has objective no greater than its relaxed value; here \(B\)
is the set of variables with nonpositive square coefficients.

## Precise statement

Write the quadratic on \([0,1]^V\) as

\[
q(x)=c_0+\sum_{i\in V}(d_i x_i^2+b_i x_i)
          -\sum_{ij\in E}w_{ij}x_ix_j,
\qquad w_{ij}>0.
\tag{1}
\]

Thus every nonzero mixed coefficient is negative, which is the usual
quadratic submodularity condition. Zero interactions are omitted from
\(E\). Put \(C=\{i:d_i>0\}\) and \(B=V\setminus C\).

**Theorem.** Suppose \(C\) is a stable set of \((V,E)\). Then the
unit-box SDP relaxation with upper RLT inequalities has the true box minimum.
Consequently full SDP–RLT is exact as well. More strongly,
for every feasible moment point \((\mu,X)\), the rounding procedure below
produces a box point with objective at most \(L_{\mu,X}(q)\).

The relaxation used in the stronger statement is

\[
\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}\succeq0,
\qquad X_{ij}\leq\mu_i\quad(i,j\in V).
\]

Symmetry supplies both upper bounds. The diagonal inequalities and PSD
imply \(\mu_i^2\leq X_{ii}\leq\mu_i\), hence \(0\leq\mu\leq1\).
No lower RLT inequality or binary diagonal equality is required.

The theorem concerns this sign-restricted family of objectives. It does
not assert an exact mixed binary moment hull for arbitrary graphs or for
arbitrary signs. The [forest hull theorem](binary-separator-forest-hull.md)
has that stronger projection conclusion on its more restricted graph class.

## Standard coupling fact, with proof

Let \(f:2^D\to\mathbb R\) be submodular, and fix binary means
\(u\in[0,1]^D\). Among all distributions of a random subset \(S\subseteq D\)
with \(\Pr(i\in S)=u_i\), the expectation of \(f(S)\) is minimized by

\[
S(U)=\{i:u_i\geq U\},\qquad U\sim\mathrm{Uniform}[0,1].
\tag{2}
\]

This is the classical Lovász convex-closure property. A finite-dimensional
argument suffices here. The distributions form a compact polytope on the
\(2^{|D|}\) subsets. Among its expectation minimizers choose one maximizing
\(\mathbb E|S|^2\). If incomparable sets \(A,B\) both have positive mass,
move an equal positive mass \(\delta\) from each to \(A\cap B,A\cup B\).
This preserves total mass and every marginal probability. Submodularity
does not increase expected cost; optimality therefore preserves that cost.
But the second cardinality moment increases by

\[
2\delta\,|A\setminus B|\,|B\setminus A|>0,
\]

a contradiction. The selected minimizer has nested support. A nested
binary law with the prescribed means is exactly (2), up to zero-mass
outcomes and tied means. This proves the fact.

In particular, the same coupling (2) minimizes the expectation of every
submodular function of any subset of the binary coordinates, provided
its corresponding marginal means are fixed. This simultaneous property
allows cyclic interaction graphs in the theorem.

## Conditional center minimization

Since \(C\) is stable, every \(c\in C\) interacts only with vertices
in \(B\). Set

\[
q_c(t,z)=d_c t^2+b_c t-t\sum_{b\in N(c)}w_{cb}z_b,
\qquad z\in\{0,1\}^{N(c)},
\]

and define

\[
g_c(s)=\min_{0\leq t\leq1}\{d_c t^2+(b_c-s)t\},
\qquad
f_c(S)=g_c\left(\sum_{b\in S}w_{cb}\right).
\tag{3}
\]

The function \(g_c\) is concave: it is the pointwise infimum, over
\(t\in[0,1]\), of affine functions of \(s\). A concave function of a
nonnegative modular sum is submodular. Explicitly, concavity makes
\(g_c(s+w)-g_c(s)\) nonincreasing in \(s\) for every \(w\geq0\),
which is exactly the diminishing-returns inequality for \(f_c\).

For each binary neighbor configuration, a minimizing center value is

\[
t_c(z)=\operatorname{clip}_{[0,1]}
 \left(\frac{\sum_{b\in N(c)}w_{cb}z_b-b_c}{2d_c}\right).
\tag{4}
\]

To transfer (3) to a feasible upper-RLT SDP point, order \(N(c)\) by
nonincreasing \(\mu_b\). Let \(S_j\) be the first \(j\) neighbors in
that order, set \(\beta_c=f_c(\varnothing)\), and set
\(\alpha_b=f_c(S_j)-f_c(S_{j-1})\) for the neighbor in position \(j\).
Submodularity gives the elementary greedy affine minorant

\[
\beta_c+\sum_{b\in S}\alpha_b\leq f_c(S)\qquad(S\subseteq N(c)).
\]

Indeed, add the elements of \(S\) in the chosen order. At each step the
preceding selected set is contained in the preceding full prefix;
diminishing returns makes the former marginal at least \(\alpha_b\).
The inequality is an equality for every prefix \(S_j\), and hence for
every positive-probability outcome of the common-uniform coupling.

It follows that
\(q_c(t,y)-\sum_b\alpha_b y_b\geq\beta_c\) on the entire local box:
the minimum over the affine leaf variables occurs at binary leaves,
where the inequality follows from (3). This is still a submodular star
with arbitrary leaf linear coefficients. Proposition 3 of the linked
star note applies. Restricting the global PSD matrix to this star and
retaining its upper RLT bounds therefore gives

\[
\begin{aligned}
L_{\mu,X}(q_c)
 &\geq\beta_c+\sum_{b\in N(c)}\alpha_b\mu_b\\
 &=\mathbb E[f_c(\{b\in N(c):\mu_b\geq U\})].
\end{aligned}
\tag{5}
\]

This argument uses local objective exactness, not a local representing
distribution for the weaker upper-RLT region. The arbitrary-sign star
moment-hull theorem requires full RLT and is not being extended here.

## One coupling for the whole graph

Use one uniform \(U\) for all vertices in \(B\), and define an actual box
point by

\[
\widehat x_b(U)=\mathbf1\{\mu_b\geq U\}\quad(b\in B),
\qquad
\widehat x_c(U)=t_c(\widehat x_{N(c)}(U))\quad(c\in C).
\tag{6}
\]

This is globally feasible regardless of cycles, because every continuous
center is defined after the binary vector and there are no interactions
between centers. Its binary coordinates satisfy

\[
\mathbb E\widehat x_b=\mu_b,
\qquad
\mathbb E[\widehat x_b\widehat x_{b'}]=\min(\mu_b,\mu_{b'}).
\]

For \(b\in B\), the diagonal RLT inequality and \(d_b\leq0\) imply
\(d_bX_{bb}\geq d_b\mu_b\). For a binary–binary edge,
\(-w_{bb'}X_{bb'}\geq-w_{bb'}\min(\mu_b,\mu_{b'})\).
Thus the part of the objective involving only \(B\) has relaxed value
at least its expected value under (6). Adding (5) for every center yields

\[
L_{\mu,X}(q)\ \geq\ \mathbb E[q(\widehat x(U))]
\ \geq\ \min_{x\in[0,1]^V}q(x).
\tag{7}
\]

Actual rank-one points are relaxation-feasible, so (7) proves exactness.
It also proves the asserted rounding guarantee: at least one outcome
of (6) has objective no greater than the average in (7).

Only the sorted distinct values of \((\mu_b)_{b\in B}\) matter. The
binary vector, and hence every center response, is constant between
consecutive values. There are at most \(|B|+1\) outcomes with positive
probability. Evaluate those points and choose the best. Ties and means
equal to zero or one merely remove outcomes. If \(B\) is empty, stability
of \(C\) makes the objective separable, and (4) gives its single candidate.
If \(C\) is empty, the proof reduces to standard submodular binary
rounding. \(\square\)

The rounding conclusion is an exact-arithmetic statement for a feasible
relaxation point. No claim is made about numerical solver tolerances or
certification from an approximately feasible point.

## Equality with the convex closure at every binary mean

The same argument gives more than equality of unconstrained minima.
For \(S\subseteq B\), define the value after fixing the binary vector and
optimizing every continuous center:

\[
F(S)=c_0+\sum_{b\in S}(b_b+d_b)
 -\sum_{bb'\in E:\ b,b'\in S}w_{bb'}
 +\sum_{c\in C}g_c\left(\sum_{b\in S\cap N(c)}w_{cb}\right).
\tag{8}
\]

It is submodular by (3) and the signs of the binary–binary interactions.
For \(u\in[0,1]^B\), let \(\widehat F(u)\) denote its Lovász extension,
including the constant \(F(\varnothing)\); equivalently,

\[
\widehat F(u)=\mathbb E[F(\{b:u_b\geq U\})].
\]

**Corollary.** For every \(u\in[0,1]^B\),

\[
\min\{L_{\mu,X}(q):(\mu,X)\text{ satisfies PSD and upper RLT},\ \mu_B=u\}
=\widehat F(u).
\tag{9}
\]

Indeed, (7) gives the lower bound with fixed \(u\). Conversely, the
common-uniform law (6) with those binary means and the center responses
(4) produces an actual feasible full moment matrix of objective exactly
\(\widehat F(u)\). This also proves (9) with full SDP–RLT in place of
the weaker system. Compactness gives attainment: diagonal upper bounds
and PSD bound every moment matrix entry.

Thus adding an epigraph coordinate \(\eta\geq L_{\mu,X}(q)\) and
projecting out all continuous means and moment variables gives precisely
the convex epigraph of the eliminated binary value function over
\([0,1]^B\). This is an SDP representation of a particular known
submodular convex closure. It is not a hull description retaining all
continuous coordinates, nor a convexification of arbitrary additional
constraints involving them.

## Coordinate complementation and the forest consequence

Suppose an objective has arbitrary mixed coefficients, but there are
signs \(s_i\in\{-1,1\}\) such that complementing the coordinates with
\(s_i=-1\) makes every mixed coefficient nonpositive. The quadratic
coefficient of each individual square is unchanged, while linear and
constant terms may change. Full SDP–RLT is invariant under this affine
coordinate transformation. Its exactness therefore follows whenever the
positive diagonal vertices are stable in the transformed objective.
That stability condition is unchanged by complementation as well.
Individual coordinate complements need not preserve the upper-only
relaxation, so this extension asserts exactness of full SDP–RLT or of
the upper-only system after performing the chosen transformation.

Every signed forest admits such a choice of signs: root each component
and choose a child's sign to make its edge to the parent negative.
Consequently the arbitrary-sign forest exactness corollary also follows
from this theorem. The forest moment-hull theorem remains stronger than
this implication because it preserves all retained moments at once.

## Literature comparison and significance

The coupling and concave-composition facts are established results,
not contributions here. Bach,
[*Learning with Submodular Functions: A Convex Optimization Perspective*](https://arxiv.org/pdf/1111.6453),
Section 5.1, identifies the convex closure with the Lovász extension;
Proposition 6.1 states submodularity of a concave function of a nonnegative
modular sum. Those passages were inspected directly on 2026-09-27.
The finite uncrossing proof and calculation (3) make their use self-contained.

Burer, Natarajan, and Willemsen,
[*On the Semidefinite Representability of Continuous Quadratic Submodular
Minimization With Applications to Pricing and Moment Problems*,
arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3),
prove exactness for submodular quadratics in at most three
variables using precisely the upper-RLT relaxation above. Their general-dimensional
counterexample precludes removing all additional structure. The claim
here has no dimension bound, but imposes the stable-positive-diagonal
condition. Its proof depends on the candidate upper-RLT star theorem,
which is not supplied by the low-dimensional theorem alone.

Dey–Khajavirad's stable-positive-loop result provides an SOC-representable
hull for arbitrary interaction signs, with a formulation that can be
exponential. Their polynomial-size statements impose further structural
conditions. Khajavirad's later SDP results similarly control size using
graph structure. Precise current-version references and degree assumptions
are recorded in the [forest comparison](binary-separator-forest-hull.md).
The theorem here instead claims exactness of the existing polynomial-size
upper-RLT SDP system for the submodular sign class, without degree or
treewidth bounds. It does not provide a full arbitrary-sign hull or a
polynomial-size SOC representation.

Independent center minimization already reduces this class to minimizing
a submodular set function on \(B\). New polynomial-time solvability is
therefore not the proposed advance. The candidate contribution is a
structural exactness theorem for a standard relaxation, together with the
explicit threshold rounding guarantee and its fixed-mean value-function
identity (9). It could justify treating certain large quadratic blocks
exactly within MINLP relaxations. Arbitrary side
constraints are not covered, and no computational speedup is established.

There is also a direct older tractability precedent: Tardella,
[*Connections between continuous and combinatorial optimization problems
through an extension of the fundamental theorem of Linear Programming*](https://doi.org/10.1016/j.endm.2004.03.054),
Theorem 3, covers submodular box minimization when the residual problem
after fixing coordinatewise quasiconcave variables at endpoints is
polynomially evaluable. Here those variables include \(B\), and the
residual problem on \(C\) is separable. The independent
[priority audit](binary-star-prior-review.md) inspected this theorem in
the open [CTW04 proceedings](https://www.lix.polytechnique.fr/~liberti/ctw04proc.pdf),
page 225. Its theorem does not state exactness of the particular SDP–RLT
relaxation used here.

Priority remains open. A search failing to locate an equivalent result
under these words is not evidence of novelty. In particular, exact SDP
relaxations for mixed binary submodular models and common-factor moment
problems need a focused comparison.

## Verification status

The root investigator `/root` independently checked the initial full-RLT
proof outline: local star laws, concave elimination, common-uniform
coupling, and the signs in (7). The priority reviewer
`/root/binary_star_prior_review` identified the upper-only strengthening
and the fixed-mean consequence. The author checked both deductions;
`/root/forest_hull_review` then independently audited the saved stronger
proof, including its greedy affine minorant, fixed-mean equality, and
sign-switching restriction. That reviewer found no defect. Its fresh
subordinate `/root/forest_hull_review/upper_star_audit` separately checked
the upper-RLT star dependency. Its fresh subordinate
`/root/forest_hull_review/upper_star_audit/modular_minorant_check`
independently checked the affine-minorant and global-coupling argument,
including ties, endpoint means, and empty neighborhoods. The star note records additional reviews
of the endpoint corrections. These checks are evidence, not formal
verification or a finding of novelty.

Targeted commands actually run by the author were

```sh
python research-20260927/check_binary_leaf_star.py
python research-20260927/check_stable_positive_fixed_means.py
```

The first passed its exact identities, rational clipping cases, and
upper-RLT scope checks. The second uses a five-vertex cyclic example:
two positive centers joined to three binary vertices, plus negative
interactions between every pair of binary vertices. The fixed binary
means are \((1/5,1/2,4/5)\); both centers exhibit lower, interior, and
upper clipping. Its exact common-threshold expectation is
\(-3251/2400\), and the actual finite moment lift is checked exactly.

A numerical full SDP–RLT solve differed from that value by about
\(-3.10\times10^{-12}\), with largest constraint residual about
\(1.15\times10^{-11}\) and solver status `optimal`. The upper-only solve
differed by about \(4.24\times10^{-13}\), with largest residual about
\(1.84\times10^{-9}\) and status `optimal_inaccurate`. Those floating-point
comparisons do not certify optimality; the exact lift certifies an upper
bound, and the analytic proof gives the matching lower bound. The finite
checks do not prove the universal theorem, priority, or practical value.
No project-wide verification or CI inspection was performed.
