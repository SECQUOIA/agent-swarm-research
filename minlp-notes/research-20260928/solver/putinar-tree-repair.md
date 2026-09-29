# Quantitative total-variation repair on a junction tree

Date: 2026-09-28. Status: supporting lemma, with an independent adversarial
proof review and exact finite checks. No novelty claim is made. This note
provides a quantitative interface for local kernel densities; it is not a
theorem about positivity certificates by itself.

## Setting and convention

Let a finite tree `T=(V,E)` index bags `B_b` covering a finite coordinate set
`I`. Assume running intersection: the bags containing each coordinate induce
a connected subtree. Each coordinate space `X_i` is nonempty and standard
Borel, and each bag has the full product space
`X_b = product_{i in B_b} X_i`. Closed boxes are the intended application.
Let `nu_b` be an actual probability law on `X_b`.

For an edge `e=bc`, write `S_e=B_b intersection B_c` and let

\[
 \varepsilon_e=
 \operatorname{TV}((\operatorname{pr}_{S_e})_\#\nu_b,
                   (\operatorname{pr}_{S_e})_\#\nu_c),
 \qquad
 \operatorname{TV}(\alpha,\beta)=\sup_A|\alpha(A)-\beta(A)|.
\]

Thus TV lies in `[0,1]` for probability laws and is one half of the `L1`
distance when densities exist. The empty separator has discrepancy zero.
For bounded measurable `f_b`, set
`w_b=osc(f_b)=sup f_b-inf f_b` and `W=sum_b w_b`. Expectations below require
only boundedness, not continuity or polynomiality.

## The repair theorem

Root the tree at any bag `r`. Let `P(r,b)` be the edge set on its path to
`b`, and put

\[
 E_b^r=\{e\in P(r,b):S_e\cap B_b\ne\varnothing\}.
\]

**Theorem 1.** There is a probability law `mu` on the global product space
whose bag marginals `mu_b` satisfy

\[
 \operatorname{TV}(\mu_b,\nu_b)
 \le \min\!\left\{1,\sum_{e\in E_b^r}\varepsilon_e\right\}
 \le \min\!\left\{1,\sum_{e\in P(r,b)}\varepsilon_e\right\}.
 \tag{1}
\]

In particular the root law is preserved. If `f=sum_b f_b`, then

\[
 \left|\int f\,d\mu-\sum_b\int f_b\,d\nu_b\right|
 \le\sum_b w_b\min\!\left\{1,\sum_{e\in E_b^r}\varepsilon_e\right\}.
 \tag{2}
\]

For the untruncated version, let `C_e^r` be the component of `T-e` not
containing the root. Exchanging sums gives the useful expression

\[
 \sum_b w_b\sum_{e\in E_b^r}\varepsilon_e
 =\sum_e\varepsilon_e
       \sum_{\substack{b\in C_e^r\\B_b\cap S_e\ne\varnothing}}w_b.
 \tag{3}
\]

**Proof.** For every edge, maximally couple its two separator marginals.
For probability laws `alpha,beta`, this coupling is obtained by matching the
common measure with density `min(d alpha/d lambda,d beta/d lambda)` under
`lambda=alpha+beta`, and independently coupling the two remaining measures
after normalization. The latter measures have disjoint supports modulo
null sets. The probability of unequal separator values is exactly their
TV distance. If the residual mass is zero, only the common part is used.

Disintegrate each bag law on its separator projection and lift the separator
coupling using the two conditional bag laws. Standard Borel spaces supply
these regular conditional distributions. This produces an edge pair law
`gamma_e` with the original two bag marginals and separator-disagreement
probability exactly `epsilon_e`. Conditional kernels on null sets are only
sampled against their original marginals, so their arbitrary versions cause
no problem.

All these edge pair laws can be realized by a joint law of separate bag
copies `(Z_b)`: sample the root with law `nu_r`, then sample each child
conditionally on its parent using a disintegration of `gamma_e`. Induction
shows that every bag has its original law and every edge has the prescribed
pair law. This construction relies on the index graph being a tree.

For each coordinate `i`, let `a_i` be the unique bag containing `i` that is
closest to the root, and define `X_i=(Z_{a_i})_i`. Running intersection
implies that `a_i` is an ancestor of every bag containing `i`, and `i`
belongs to every separator on the path from `a_i` to such a bag. Thus

\[
 \{X_{B_b}\ne Z_b\}
 \subseteq \bigcup_{e\in E_b^r}
       \{\text{the two bag copies disagree on }S_e\}.
\]

The union bound and the coupling bound for TV prove (1) for
`mu=Law(X)`. All selected coordinates belong to their coordinate domains,
so `X` belongs to the global product. Finally,
`|int h d alpha-int h d beta| <= osc(h) TV(alpha,beta)` for bounded real
`h`, giving (2), and finite summation gives (3). This proves the theorem.

The construction matters. Directly extending a repaired parent by the
original child's conditional law proves the full-path bound, but need not
prove the refinement `E_b^r`. For example, on bags `{1,2},{2,3},{3,4}`,
let the first law have `X_2~Bernoulli(p)`, the second have
`X_2=X_3~Bernoulli(q)`, and the third have
`X_3=X_4~Bernoulli(q)`. Ordinary conditional extension propagates the first
edge's discrepancy into the third bag. The separate-copy construction in
the proof leaves the third law unchanged.

## A simple optimized bound and its sharpness

For a set `A` of bags, write `W(A)=sum_{b in A} w_b`. If `A_e,B_e` are the
two components of `T-e`, choose a weighted median root: every component
after deleting that root has weight at most `W/2`. Such a root exists for
every finite tree with nonnegative vertex weights. If `W=0`, any root works.
For every edge, the component away from this root has the smaller weight.
Consequently (1)--(2) imply

\[
 \left|\int f\,d\mu-\sum_b\int f_b\,d\nu_b\right|
 \le \sum_e\varepsilon_e\min\{W(A_e),W(B_e)\}
 \le {W\over2}\sum_e\varepsilon_e.
 \tag{4}
\]

The first expression is exactly the minimum over roots of the full-path
sum `sum_b w_b sum_{e in P(r,b)} epsilon_e`: any root pays one of the two
component weights for each edge, and a weighted median pays the smaller
one simultaneously on every edge. The median can be characterized using
vertex weights alone, independently of the edge discrepancies. The clipped
bound in (2) and the refined bound in (3) can improve (4); no pointwise
optimality is claimed for any of them.

The dependence on tree size cannot generally be removed. Take a path with
`t=2k` bags, all containing a common `x in [0,1]`. Private coordinates may
be added to make the bags distinct. Number the bags `j=0,...,2k-1`, give
bag `j` the Bernoulli law with parameter `j epsilon`, and take
`0 < epsilon <= 1/(2k-1)`. Each adjacent discrepancy is `epsilon`. Set
`f_j(x)=x` for `j<k` and `f_j(x)=-x` otherwise. Every local oscillation is
one, the global objective is identically zero, but

\[
 \sum_j\int f_j\,d\nu_j=-k^2\varepsilon,
 \qquad
 \sum_{i=1}^{2k-1}\varepsilon\min(i,2k-i)=k^2\varepsilon.
 \tag{5}
\]

Thus (4) can be attained even for a linear scalar objective. This is a
limitation of a bound based only on generic marginal discrepancies. It is
not a lower bound for errors arising from a particular polynomial kernel,
which may have additional structure.

For weighted TV repair itself there is a stronger sharpness statement.
Fix arbitrary nonnegative weights and edge discrepancies with
`E=sum_e epsilon_e <= 1`. Give every bag one common categorical coordinate,
with distinct labels `0` and `(e,A_e),(e,B_e)` for each edge. Let its bag law
put mass `1-E` on `0` and mass `epsilon_e` on the side label of edge `e`
containing that bag. Adjacent laws differ only in their common edge block,
so their TV discrepancy is exactly the specified `epsilon_e`.

For any common repaired law `q`, apply weighted absolute-deviation
minimization separately to the two coordinates in each edge block. Each
coordinate contributes at least
`epsilon_e min(W(A_e),W(B_e))` before the factor `1/2` in TV. Summing the
two coordinates gives

\[
 \sum_b w_b\operatorname{TV}(q,\nu_b)
 \ge\sum_e\varepsilon_e\min\{W(A_e),W(B_e)\}.
\]

The median bag's own law attains equality. All labels can be embedded as
distinct points of a real interval; discreteness does not restrict this
example to discrete coordinate spaces.

## Hard local supports: a different bound

The coordinate extraction in Theorem 1 need not preserve nonproduct local
constraints. It must not be used to claim such preservation.

There is a separate support-preserving statement. Suppose each original
bag law is supported on a measurable local feasible set `K_b`. Retain the
joint original bag copies in the proof and let `A` be the event that every
edge separator agrees. Then

\[
 \mathbb P(A)\ge 1-\sum_e\varepsilon_e.
\]

If `E=sum_e epsilon_e<1`, condition on `A`. Running intersection yields
a global assignment satisfying all local constraints almost surely. Its
bag marginal `mu_b` satisfies `TV(mu_b,nu_b)<=P(A^c)<=E`, because
`nu_b=P(A)mu_b+P(A^c)Law(Z_b|A^c)`. There is no factor `1/(1-E)` in this
TV estimate. Its objective error is at most `W E`. This conditional law
is generally different from the law in Theorem 1; their guarantees must
not be combined as if a single law automatically satisfied both.

The condition `E<1` cannot be weakened to `E<=1` as a universal feasibility
claim. Take `m>=2` bags sharing a categorical coordinate
`x in {1,...,m}`. Bag `j` forbids label `j` and is uniform on all remaining
labels. Every edge discrepancy equals `1/(m-1)`, hence `E=1` on any tree,
but no global label satisfies all the local constraints.

## When a common density shift avoids repair

The tree discrepancy bounds are unnecessary in an important special case.
Suppose normalized signed local densities `h_b` already have exactly
consistent separator marginals against compatible product probability laws
`lambda_b`, and suppose `h_b >= -delta` everywhere for one common
`delta>=0`. Define

\[
 q_b={h_b+\delta\over1+\delta}.
\]

These are genuine normalized nonnegative densities. Integrating out bag
coordinates preserves both the constant one and the assumed signed
marginals, so the `q_b lambda_b` remain exactly consistent. The zero-error
case of Theorem 1 therefore glues them exactly. Moreover,

\[
 h_b\lambda_b=(1+\delta)q_b\lambda_b-\delta\lambda_b
\]

implies

\[
 \left|\int f_bq_b\,d\lambda_b-\int f_bh_b\,d\lambda_b\right|
 =\delta\left|\int f_b\,d\lambda_b-\int f_bq_b\,d\lambda_b\right|
 \le\delta w_b.
\]

Thus the total objective correction is at most `delta W`, with no
accumulation along the tree. A bound only on the integral of the negative
part does not justify this shift: pointwise domination by a common,
compatible reference probability measure is the required hypothesis.
Bag-dependent pointwise bounds can be replaced by their maximum. This is
an elementary alternative to use when a kernel argument supplies the
stronger pointwise information.

## Verification and provenance

The tree gluing and maximal-coupling tools are standard; this note makes
their quantitative use explicit without claiming priority. The earlier
repository note [repair-probe.md](../structural/repair-probe.md) studies
related Wasserstein repair under a deterministic error bound. The present
argument uses full product domains for its finer TV bound and does not
assume that deterministic premise.

An independent adversarial reviewer checked the construction, the refined
edge set, the weighted median bound, the categorical sharpness construction,
the hard-support qualification, and the common density shift. The reviewer
identified the distinction between the two gluing constructions, which is
recorded explicitly above.

Targeted command run:

```text
python research-20260928/solver/check_putinar_tree_repair.py
```

Result:

```text
PASS: 80 exact rooted coupling checks; weighted-cut identity; six sharp objective examples
```

The script uses exact rational arithmetic to construct maximal separator
couplings, lift them, glue original bag copies, and perform the stated
coordinate extraction. It checks all roots of 24 finite examples, including
chains with repeated and changing separators and a branching tree, verifies
the weighted-cut identity, and checks six exact instances of (5). These
checks test the construction on finite instances; the measurable-space
proof and universal claims are established by the argument above. No
project-wide verification or CI status inspection is part of this check.
