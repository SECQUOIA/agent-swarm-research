# Oracle-complexity conjectures: current scope and a feasibility transfer lemma

Date: 2026-09-22. Status: supporting investigation with
[independent adversarial review](review-20260922-oracle-transfer.md).
The lemma is correct under its stated assumption, but its main geometric
mechanism already appears in Basu's earlier work. It is not a resolution of
the general constrained transfer conjecture or a publishable main contribution.

**Attribution correction.** Basu,
[Complexity of optimizing over the integers, Section 4.1](https://arxiv.org/html/2110.06172v6),
already uses independent cube fibers, rotated separating cuts, retirement,
fractional YES points, and a final convex hull. The addition below is an
explicit arbitrary-source-adversary formulation and a bound preserving all
previous YES points. The review also checks the July 2026 revision of
arXiv:2511.02082, now titled *Tight Lower Bounds for Binary First-Order
Oracles*. Historical title and conjecture references below describe the
versions originally inspected.

## Literature check changes the target

The repository copies of Basu–Jiang–Kerger–Molinaro, *Information Complexity of Mixed-integer Convex Optimization* (Mathematical Programming 210, 2025), and Basu–Kerger–Molinaro, *Tight Lower Bounds for the Bit and Inner Product Oracle for Constrained Convex Optimization* (arXiv:2511.02082, 2025), were examined, especially their introductions, model definitions, and conjectures. Primary open copies:

- <https://optimization-online.org/wp-content/uploads/2023/08/information_complexity_of_convex_mixed_integer_opti.pdf>
- <https://arxiv.org/abs/2511.02082>

The first paper's Conjecture 1 asks for a generic continuous-to-mixed-integer lower-bound transfer incorporating constraints. Its proved Theorem 7 concerns unconstrained source problems with a common optimal value and hereditary permissible queries. Conjecture 2 asks for a quadratic continuous-dimension lower bound with a general binary first-order oracle, including an accuracy logarithm. Conjecture 3 concerns converting full-information upper bounds into general binary upper bounds. These are distinct questions.

A primary-source search on 2026-09-22 found a material intervening result: Phillip Kerger, *Closing the Oracle-Complexity Gap in Derivative-Free Convex Optimization: A Near-Quadratic Lower Bound from Exact Function Values*, arXiv:2607.13335v1, 14 July 2026, <https://arxiv.org/html/2607.13335v1>. Its Theorem 4 proves a deterministic exact-value lower bound of order d²/log(d+1) on a Euclidean ball, at one universal constant times d^(-1/2) accuracy. It also transfers to binary integer variables with a factor 2^n. This settles the previously missing near-quadratic dimension dependence for that exact-value model at the stated accuracy. It does not establish a multiplicative log(1/epsilon) lower bound or a lower bound for binary subgradient access. Exact function values and binary first-order information are incomparable oracle resources.

The latter distinction matters: weakening a value oracle to value bits preserves a value-only lower bound, but adding subgradient bits produces a different, stronger resource that cannot be covered by that argument.

The search also checked the authors' primary publication pages, <https://phillipkerger.github.io/research/> and <https://www.ams.jhu.edu/~abasu9/>, and located the separate ICML 2024 paper *A Universal Transfer Theorem for Convex Optimization Algorithms Using Inexact First-order Oracles*, <https://proceedings.mlr.press/v235/kerger24a.html>. Its presence is not evidence that the constrained lower-bound conjecture is resolved. No general resolution was identified in this search; that is not a novelty proof.

## A restricted transfer result with an explicit assumption

Let B=[-R,R]^d, with R>0. Let K be a family of nonempty compact convex subsets of B, every member containing an infinity-norm ball of radius rho>0. A full separation response at y is either YES or a unit vector a satisfying

    a · (z-y) < 0 for every z in the unknown set.

The oracle returns the normal, with the query point specifying the hyperplane. Repeated queries must receive the same response.

Assume an L-step resisting adversary for K, where L is a nonnegative integer. This means that for every adaptive sequence of at most L distinct query points in B the adversary supplies only nonzero full separation normals, consistently on repetitions, and after every prefix the surviving family K_t is nonempty and

    intersection { K : K in K_t } = empty.

Here survival means consistency with all strict separating responses already supplied. This assumption states the exact adversarial property needed. It follows from a deterministic full-separation query lower bound greater than L on a class of nonempty sets (with fixed consistent charts included in the instance description). Here is the decision-tree argument. If the current surviving family cannot be solved with k further queries, then for every next query some possible response leaves a family that cannot be solved with k-1 further queries. Otherwise selecting, separately for every response, a successful residual strategy gives a k-query strategy. Start with k=L and iterate, retaining the stronger residual lower bound. The residual family always has no common feasible point, because a common point is a zero-query solution. A YES response cannot be chosen because it supplies such a point. This argument uses the unrestricted deterministic information model, where decision rules and selections need not be computationally effective. For source classes also containing the empty set, this particular implication needs separate care: empty-instance uncertainty can prevent an output even when all nonempty survivors share a feasible point.

**Proposition.** Under this assumption, for every n>=1 and every deterministic algorithm using at most

    2^n (L+1) - 1

full separation queries, there is a nonempty compact convex set C in [0,1]^n × B and a fixed valid separation chart on C such that:

1. C has an integer fiber containing an infinity-norm ball of radius rho;
2. the algorithm fails to output a point of C intersected with (Z^n × R^d).

Queries may be fractional. The integer variables in the known box are binary. No bound on the numerical magnitude of unnormalized cut coefficients is asserted.

The quantifier order is `for every algorithm, there exists a body and a
valid chart`. The resulting chart may depend on the algorithm. This does
not produce a single chart for an entire instance class against all
algorithms. The distinction between those information models is detailed
in the review; the proposition should not be silently transferred between
them.

### Proof

Write V={0,1}^n. For v in V set

    d_v(x) = sum_i [v_i(1-x_i) + (1-v_i)x_i].

On [0,1]^n, d_v is affine, nonnegative, and vanishes only at v. At every other vertex it is at least one. Its gradient is s_v=(1-2v_i)_i.

Run an independent copy of the source adversary at each vertex. A vertex is active until its (L+1)st distinct query; at that query it is retired and its eventual fiber will be empty. Cache the answer at every full query point and use the cached answer on repetitions. Thus retirement never changes the chart at an earlier query point.

Maintain a finite set P of fractional query points answered YES, together with all previously returned separating halfspaces. A halfspace is stored in strict form, with the original query point on its boundary.

For a previously unseen fractional query q=(x,y), x not in V, inspect all earlier halfspaces. If q violates at least one of their strict inequalities (including equality), return that earlier normal. Otherwise answer YES and insert q into P. This inspection uses full information and is the principal restriction of the proposition.

At a previously unseen query (v,y) in an active fiber with at most L-1 earlier distinct queries in that fiber, request a source normal a. Choose

    H > 2R sqrt(d) max(1, max_{p in P} 1/d_v(p_x)),

where the second maximum is omitted if P is empty. Return the normal proportional to (-H s_v, a), namely the cut

    a · (z-y) < H d_v(x).                         (1)

The source survivor sets at v satisfy (1). Every point in {w}×B for a different vertex w satisfies (1), since the left side is at most 2R sqrt(d) and d_v(w)>=1. Every previous fractional YES point also satisfies (1) by the choice of H. Normalizing the returned vector does not change these inequalities.

On the (L+1)st distinct query in a fiber, retire v and return the unit normal proportional to (-s_v,0). Its strict halfspace is d_v(x)>0. All other vertex fibers and all fractional YES points lie strictly inside it. At any later new query in that retired fiber the same outward integer normal is valid. Repetitions still return their cached answers.

Queries outside the known product box, if the model permits them, receive fixed box-separation cuts and play no role. They can be omitted from the remaining argument.

Because fewer than 2^n(L+1) queries have occurred, at least one vertex remains active. For each active vertex v, choose a surviving source set K_v. For each retired vertex put K_v=empty. Define

    C = conv( P union union_{v in V} ({v}×K_v) ). (2)

There are finitely many compact constituents, so C is compact and convex. Every stored strict halfspace contains every constituent: source constraints ensure this on their own surviving fibers; the tilt ensured it on the other fibers and earlier YES points; later YES points were admitted only when they satisfied every preceding strict cut. Retirement cuts contain all surviving fibers. A strict affine inequality remains strict under every finite convex combination. Hence every returned separating normal is valid for C. Every YES point belongs to C by construction.

Since at least one active K_v is nonempty and rho-fat, C is nonempty and has a rho-fat integer fiber. Moreover, extremality of each cube vertex gives exactly

    C intersected with ({v}×B) = {v}×K_v.

Indeed, a convex combination with x-coordinate v can use only constituents whose x-coordinate equals v, and P contains no such points.

Finally, consider the algorithm's output. If it is not in V×B it fails. If its vertex is retired, it fails. If its vertex v is active, the no-common-point assumption allows choosing the surviving K_v to omit its continuous output. Choose the other surviving sets arbitrarily and form (2). If the algorithm instead announces infeasibility, nonemptiness of C refutes that answer. At the finitely many queried points define the chart to equal the supplied cached answers; at other points use zero on C and any normalized strict separating normal outside C. Compact convex separation ensures such normals exist. Thus one fixed instance and one fixed chart realize the whole transcript. This proves the candidate proposition.

## What this establishes and what it does not

The proof gives a reusable way to prevent fractional separation queries from coupling independent vertex fibers: retain fractional YES points and increase the tilt of later vertex cuts as necessary. The construction is adaptive, but the final transcript belongs to one fixed compact convex set with one fixed chart. It does not require a uniform separation gap in the continuous source.

This is a restricted feasibility result. It does not resolve the paper's arbitrary-oracle, constrained-optimization transfer conjecture. In particular:

- For binary/coordinate access, testing whether a new fractional point satisfies every earlier cut may require unavailable full normals. Treating them as known would invalidate the reduction. The current proof has no simulation bound in that model.
- The source assumption follows from a deterministic lower bound for a nonempty source class by the decision-tree argument above. Any use with an emptiness-detection lower bound must separately verify the residual-family property and the fatness of each nonempty survivor.
- The result allows unbounded integer-direction coefficients. A rational input-size statement or uniform conditioning statement would require additional work.
- It gives a lower bound, not a solver speedup. Its potential value is to transfer structural continuous impossibility results without redoing the mixed-integer geometry. Classical full-information lower bounds already have the principal 2^n d log(R/rho) form, so obtaining that bound again would not be a significant advance.

## Failed fixed-tilt shortcut

An initially tempting construction uses inequalities

    dist(y,K_v) <= H d_v(x)

with one large fixed H. Its fiber geometry is correct, but arbitrary source separation access does not supply distance values or a separation gap. A point arbitrarily close to a source boundary can have a valid strict source separator with arbitrarily small gap. There is no uniform positive gap available to justify a one-call simulation at a fractional x near v. The adaptive retained-point construction avoids this particular gap for full normals, while introducing the partial-information limitation above.

## Research priorities

The most consequential unresolved targets suggested by this inspection are the general binary first-order unconstrained lower bound and a constrained transfer theorem that genuinely preserves partial information. A useful intermediate target would be a transcript representation that supports the fractional-cut decision using O(1) permissible source queries, without fixing hidden full normals. A proof must account for adaptive real-valued query points and the fixed-chart requirement.

The exact-value accuracy dependence is also a meaningful separate target: Kerger's near-quadratic bound at accuracy Theta(d^(-1/2)) does not automatically multiply by log(1/epsilon). Repeating a scale-dependent hard instance requires exact transcript consistency across scales; a direct-sum slogan does not provide that.

## Verification record

The proposition was checked manually and independently reviewed for strict
separation, compactness, retention of fractional YES responses, exact integer
fibers, and repeated-query consistency. The review narrowed its originality
claim and made the chart quantifiers explicit. No project-wide checks, CI
inspection, numerical experiments, or Lean proof were run for this note.
Search absence is not used as a novelty claim.
