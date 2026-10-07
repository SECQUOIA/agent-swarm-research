# Prior-art audit: exact active-bound recognition and Square Root Sum

Date: 2026-10-02. This focused comparison concerns the reduction in
[`convex-active-set-radical-comparison.md`](../new-direction/convex-active-set-radical-comparison.md).
It is an output-contract comparison, not an NP-hardness claim or a claim that
convex optimization itself is hard on these instances.

## Finding

The construction reduces canonical Square Root Sum directly to exact
recognition of whether a specified coordinate of the unique minimizer is at a
box bound. Given positive binary integers `a_i` and an integer `B`, it builds a
rational cubic objective on a rational box for which

\[
 y^*=0\quad\Longleftrightarrow\quad \sum_i\sqrt{a_i}\le B.
\]

The constructed objective is uniformly strongly convex, has bounded
coordinate curvature and a supplied tree decomposition of bag size three.
Thus an exact polynomial-time active-bound decision routine for this promised
class would put Square Root Sum in P. The implication is a many-one reduction:
it already holds for a yes/no answer to the active-bound predicate; it does
not require an algorithm to print the minimizer or its algebraic coordinates.

This aligns with a longstanding exact-comparison problem. It does not imply a
lower bound for approximate minimization, for computing the optimal value to
polynomial precision, or for returning a compact implicit convex problem.
The reduction supplies such a compact descriptor explicitly. The unresolved
step is deciding whether one coordinate is exactly equal to its bound when
the alternative has positive slack but the reduction supplies no lower bound
on that slack in terms of the input bit length.

## Exact comparison and known complexity status

Etessami and Yannakakis define SQRT-SUM as deciding, on positive integers
`d_1,…,d_n` and an integer `k`, whether `sum_i sqrt(d_i) <= k`. They note that
it is equivalent to comparing sums of Euclidean distances with a threshold,
for example the length of a specified spanning tree or TSP tour. They state
that the problem is in PSPACE and leave membership in NP or P open. This is the
same input predicate as the reduction above, including the equality case.
See Etessami and Yannakakis, [“On the Complexity of Nash Equilibria and Other
Fixed Points”](https://doi.org/10.1137/080720826), §1, p.4 of the retrieved
peer-reviewed author version; the direct SRS-to-equilibrium comparison is
also discussed in the proof on pp.33–34. The local primary-text package is
[[etessami2010-on-the-complexity-of-nash]].

The known upper bound can be stated more strongly as membership in the
counting hierarchy (and hence PSPACE). Allender, Bürgisser,
Kjeldgaard-Pedersen, and Miltersen prove PosSLP is in the counting hierarchy
and derive the same upper bound for Sum-of-square-roots in Corollary 1.5.
See [“On the Complexity of Numerical Analysis”](https://doi.org/10.1137/070697926),
Theorem 1.4 and Corollary 1.5, pp.5–6 of the published article; its open
author manuscript is in [[allender2009-on-the-complexity-of-numerical]].
These upper bounds are not polynomial-time algorithms.

The 2024 SoCG paper of Eisenbrand, Haeberle, and Singer restates the sign
problem as deciding whether `E = sum_i x_i sqrt(a_i) >= 0`; it says this is
not known to be in P or NP and gives PSPACE as an upper bound via the
existential theory of the reals. It improves a separation bound for a fixed
radicand set, but the constant from the Subspace Theorem is nonexplicit, so
that result does not give an effective polynomial precision guarantee for
general binary inputs. See [“An Improved Bound on Sums of Square Roots via
the Subspace Theorem”](https://doi.org/10.4230/LIPIcs.SoCG.2024.54), abstract,
§1, and Theorems 1 and 6, pp.1–6; the local primary text is
[[eisenbrand2024-an-improved-bound-on-sums]].

The Open Problems Project continues to list its Problem 33, the minimum
nonzero gap between two sums of square roots, as open. The page explicitly
states that a polynomial bound on the number of precision bits would imply a
polynomial-time sign algorithm, while failure of that bound would not rule
out a different polynomial-time algorithm. This distinction matters here:
the reduction uses the exact active predicate, and does not rely on a claim
that every polynomial-time algorithm must come from a separation bound. See
[TOPP Problem 33](https://topp.openproblem.net/p33), “Status/Conjectures” and
“Motivation.”

Existing separation-bound methods do give finite exact sign tests. The Open
Problems Project summarizes known root-separation bounds with exponentially
many precision bits in the number of radicals. Burnikel et al. also give a
constructive separation bound for real-algebraic expression DAGs, including
radical expressions, and use adaptive precision to determine signs. These
are exact-computation baselines, not polynomial-time SRS results. See [TOPP
Problem 33](https://topp.openproblem.net/p33), “Partial and Related
Results,” and Burnikel et al., [“A Separation Bound for Real Algebraic
Expressions”](https://doi.org/10.1007/3-540-44676-1_21), §§1–3 and Theorem
1; the local source is
[[burnikel2001-a-separation-bound-for-real]].

## Equality, sign, and output-contract distinctions

Three closely related arithmetic problems should not be conflated:

- **Non-strict threshold comparison:** `sum_i sqrt(a_i) <= B`, the canonical
  SRS form used in the reduction. The answer handles equality on the bound
  side.
- **Signed strict sign:** decide whether `sum_i delta_i sqrt(a_i) > 0` for
  `delta_i in {-1,+1}`. Gaillard and Jindal formulate this as SSR and report
  the general sign problem remains open. The canonical positive-sum threshold
  problem reduces to this signed form in one direction: for `B>0`, append
  the term `-sqrt(B^2)=-B`, then complement the strict-positive answer.
  Thus `sum_i sqrt(a_i) <= B` is true exactly when the resulting signed sum
  is not positive. Equality is included on the true side. This observation
  does not show that arbitrary signed SSR reduces back to integer-threshold
  SRS.
- **Zero testing:** decide whether a signed radical sum equals zero. This is
  easier than sign comparison in the cited literature. Blömer's 1991 FOCS
  extended abstract gives a polynomial-time **Monte Carlo** zero/field
  membership test with arbitrarily small error; it explicitly does not give
  an efficient sign test. Gaillard and Jindal describe SSReq as in P, but the
  underlying Blömer source calls its algorithm Monte Carlo, so this audit
  does not restate that result as a deterministic P algorithm. See Blömer,
  [“Computing Sums of Radicals in Polynomial Time”](https://doi.org/10.1109/SFCS.1991.185434),
  pp.1–2, 5–8; and Gaillard and Jindal,
  [“On the Order of Power Series and the Sum of Square Roots Problem”](https://doi.org/10.1145/3597066.3597079),
  §§1–1.1, pp.1–2. Both local primary texts are available as
  [[blomer1991-computing-sums-of-radicals-in]] and
  [[gaillard2023-on-the-order-of-power]].

In the constructed optimization problem, the full-box optimum value equals
the optimum value on the face `y=0` exactly when the coordinate is active.
Thus the predicate can also be viewed as exact equality of two convex
polynomial optimum values. Approximate value or optimizer access does not by
itself decide that equality. The reduction gives no polynomial-bit lower
bound separating `y^*=0` from `y^*>0`.

The known comparison sources establish that radical-sum predicates already
appear in geometric length comparisons, zero testing, exact real arithmetic,
and equilibrium computation. In the targeted search, I found no prior
source giving this particular reduction to one active bound of a uniformly
strongly convex, rational, bounded-treewidth cubic program. That is a scoped
search result, not a novelty conclusion. The strongest supported statement
is the direct implication from a polynomial exact active-bound oracle on the
stated class to polynomial-time Square Root Sum.

## Source access and ingestion

The Etessami–Yannakakis, Allender et al., Gaillard–Jindal, Blömer,
Eisenbrand–Haeberle–Singer, and Burnikel et al. primary texts are already
present and marked read in the local literature KB. Their local package
locators are given above. The official TOPP page was checked directly for
the current status of Problem 33. No new source or KB ingestion was needed.
