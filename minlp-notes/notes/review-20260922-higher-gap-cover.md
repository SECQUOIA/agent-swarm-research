# Independent review: higher gaps, VC dimension, and parameter covers

Date: 2026-09-22. Reviewer: `review_higher_gap_cover`.

**Verdict.** Both proposed probabilistic arguments are correct under the assumptions stated below. The VC-dimension argument is simpler and gives a useful finite-grid extension directly. This review approves the envelope cardinality theorem, not an entire treewidth dynamic program: exact message construction and bit complexity require separate proofs. Novelty remains qualified because generalized winner gaps and their rank-conditioning proof are established prior work.

## Model and conditioning check

Let nonempty \(Z\subseteq\{0,1\}^m\), let \(g:Z\to\mathbb R\) be arbitrary and deterministic, and let \(\xi_i\) be independent random variables with densities bounded by \(\phi\). Put

\[
 F(z)=g(z)+\xi^Tz,\qquad
 A_\delta=\{z:F(z)\le\min_wF(w)+\delta\}.
\]

For fixed coordinates \(I\) and pattern \(a\in\{0,1\}^I\), condition on all noise outside \(I\) and define

\[
 C_a=\min_{z_I=a}\left(g(z)+\sum_{j\notin I}\xi_jz_j\right).
\]

Empty classes can be discarded. The numbers \(C_a\) are fixed under this conditioning. If pattern \(a\) is represented in \(A_\delta\), its entire-class minimum \(C_a+\xi_I^Ta\) lies between the global minimum and that minimum plus \(\delta\). This is the essential step: the representative support may depend on all noise, but the class minimum before adding \(\xi_I^Ta\) does not depend on the conditioned coordinates.

## VC-dimension proof

Write \(V=\operatorname{VCdim}(A_\delta)\). If a fixed \(k\)-coordinate set \(I\) is shattered, the patterns \(0,e_1,\ldots,e_k\) are represented. Thus

\[
 |C_{e_i}+\xi_i-C_0|\le\delta\quad(i\in I).
\]

Each inequality restricts one independent coordinate to an interval of length \(2\delta\). Consequently

\[
 \Pr(V\ge k)\le {m\choose k}(2\phi\delta)^k.
\tag{1}
\]

The fact that a shattered coordinate set is selected after observing the noise causes no problem: (1) takes a union over all deterministic choices of \(I\).

Sauer's lemma yields \(|A_\delta|\le\sum_{j=0}^V{m\choose j}\le(m+1)^V\). The last inequality also holds when \(V=0\). For any real \(p\ge1\), put \(a=(m+1)^p\). Tail summation gives

\[
\begin{aligned}
 \mathbb E|A_\delta|^p
 &\le\mathbb E a^V\\
 &=1+\sum_{k=1}^m(a^k-a^{k-1})\Pr(V\ge k)\\
 &\le(1+2a\phi\delta)^m
 \le\exp(2ma\phi\delta).
\end{aligned}
\tag{2}
\]

For \(m\ge1\), choosing \(\delta=[2m\phi(m+1)^p]^{-1}\) makes (2) at most \(e\). When \(m=0\), there is at most one support and no probabilistic argument is necessary.

## Parameter covering

Let \(q_z\) be deterministic, uniformly \(L\)-Lipschitz functions on a metric space \(T\), and let \(K\) count the distinct supports attaining the envelope minimum at at least one point of \(T\). Suppose a deterministic \(\delta/(2L)\)-net has \(J\) points. Any support active at \(t\) is \(\delta\)-near-optimal at the nearest net point: both its value and the envelope value change by at most \(L\) times the distance. Hence, pointwise,

\[
 K\le\sum_{j=1}^J |A_\delta(t_j)|.
\]

Convexity, without any independence between net points, gives

\[
 \mathbb E K^p\le J^{p-1}\sum_j\mathbb E|A_\delta(t_j)|^p
 \le eJ^p.
\tag{3}
\]

For \(T=[-M,M]^d\) in Euclidean distance, a Cartesian mesh of spacing at most \(\delta/(2L\sqrt d)\) gives

\[
 J\le\left(2+\frac{4ML\sqrt d}{\delta}\right)^d.
\]

Thus every fixed moment is polynomial in \(m,\phi,LM\), for fixed \(d,p\). When \(L=0\), one net point suffices. No convexity, polynomial degree, or regularity of equality sets is needed.

This counts **distinct supports**, including supports optimal only on a boundary or at a tie. It does not bound the number of connected regions for arbitrary Lipschitz functions: even two Lipschitz branches can alternate infinitely often. For bounded-degree polynomials in fixed dimension, an additional arrangement bound can convert support cardinality into a region-complexity bound.

## Finite-grid extension: polynomial grid size suffices

Suppose instead that every coordinate satisfies the interval bound

\[
 \Pr(\xi_i\in B)\le\phi\,\operatorname{length}(B)+1/N.
\]

Independent uniform sampling from \(N\ge2\) equally spaced points in \([-\sigma,\sigma]\) has this property with \(\phi=1/(2\sigma)\). Repeating the same proof gives

\[
 \mathbb E|A_\delta|^p
 \le\exp\left(m(m+1)^p(2\phi\delta+1/N)\right).
\tag{4}
\]

In particular, choose

\[
 \delta=\frac1{4m\phi(m+1)^p},\qquad
 N\ge2m(m+1)^p.
\]

Then (4) is at most \(e\), and (3) follows unchanged. Choosing the next power of two for \(N\) uses \(O_p(\log(m+1))\) random bits per coordinate. All tied supports are included, so no jitter limit or deduplication is needed for this cardinality theorem. The grid size must match the fixed moment order required by the algorithm; one fixed grid is not asserted to satisfy every moment order with this same bound.

## Independent affine-rank route

An affine subspace of dimension \(s\) contains at most \(2^s\) binary vectors. Indeed, some \(s\) coordinate projections are injective on its direction space and hence on the affine subspace. Thus \(|A_\delta|\ge2^{r-1}+1\) implies affine rank at least \(r\).

Choose \(r+1\) affinely independent supports and \(r\) coordinates whose projected difference matrix is nonsingular. Condition on the remaining noise and use their \(r+1\) pattern-class minima. All \(r\) differences from the first class lie in \([-\delta,\delta]\). The map from the chosen noise coordinates to these differences has an integer determinant of absolute value at least one. Its preimage has volume at most \((2\delta)^r\), hence probability at most \((2\phi\delta)^r\). A union over coordinate sets and ordered pattern tuples gives the valid coarse bound

\[
 \Pr(|A_\delta|\ge2^{r-1}+1)
 \le m^r2^{r(r+1)}(2\phi\delta)^r.
\]

Together with a parameter mesh, this also gives polynomial fixed moments by choosing a fixed \(r>d(p+1)\). The VC proof avoids tail integration and has the cleaner finite-grid extension.

## Prior work and significance

[Röglin and Teng, FOCS 2009](https://www.roeglin.org/publications/FOCS09.pdf), Section 6.1, Lemma 6.1 and its appendix proof, already study generalized winner gaps. Their threshold is \(2^{r-1}+1\); their proof selects coordinates and binary patterns using rank, conditions on other coefficients, and applies a volume bound. Their displayed estimate has exponent \(r-1\) in the gap, for a perturbed linear objective. Section 6.2 already derives expected polynomial smoothed running time from suitable randomized pseudopolynomial algorithms. These mechanisms must be credited explicitly. The present arbitrary deterministic offsets, affine-rank refinement, VC-dimension moment bound, and parameter-covering application are the specific comparisons to investigate further.

[Sauer, 1972](https://www.sciencedirect.com/science/article/pii/0097316572900192) is the source for the finite-family cardinality theorem. The publisher's open-archive abstract identifies its exact-bound Theorem 2; the standard statement is used above. No novelty is claimed for this combinatorial ingredient.

[Brunsch and Röglin](https://arxiv.org/abs/1111.1546) already obtain polynomial higher moments for smoothed Pareto sets, and discuss polynomial objectives under zero-preserving perturbations. Their model is an important overlap check. Its abstract concerns perturbed linear criteria plus an arbitrary objective, which does not immediately settle arbitrary Lipschitz parameter families with only additive binary-coordinate noise. This review did not establish a definitive novelty separation from every variant of that work.

Queries examined included `"isolation lemma" "VC dimension"`, `"smoothed analysis" "Sauer"`, `"generalized winner gap" arbitrary`, and smoothed parametric optimization with Lipschitz objectives. These searches found no immediate equivalent to the complete VC-plus-cover statement. That is not evidence sufficient to establish novelty.

The theorem removes a real obstruction to a fixed-treewidth algorithm: polynomial operations on random envelope sizes require higher moments, not just their first moments. It does not by itself provide the algorithm. Candidate enumeration, exact pruning, separator consistency, rational coefficient growth, and a uniform support-independent Lipschitz bound still require their own proofs.

## Verification scope

This is an independent mathematical review of the supplied arguments and the extension in (4). No numerical experiments, Lean proof, project-wide verification, or CI checks were used. Every conditioning step, moment summation, net argument, and degenerate case above was rederived directly. The finite-grid extension was sent to the parent and theorem author for independent rechecking before integration.
