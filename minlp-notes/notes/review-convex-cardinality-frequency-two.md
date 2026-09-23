# Independent audit: convex cardinality factors of frequency two

Date: 2026-09-04. Reviewer: `review_common_factor`, independent of the theorem's author.

**Verdict: the theorem and common-aspect-ratio box corollary pass the mathematical audit.** This review covers [the master result](../results/convex-cardinality-frequency-two-gap.md). It does not establish novelty. The individual envelope formulas and fractional degree-polytope structure are classical ingredients.

## Scope checked

The factors are the **multiaffine interpolants** of binary cardinality values `φ_v(k)`, with nonnegative discrete second differences. They are not arbitrary continuous functions `φ_v(Σ x_i)`. Each coordinate belongs to at most two factor supports. The sequences may be negative, decreasing, or nonmonotone: the proof requires convexity, not monotonicity or nonnegativity. Affine additions do not affect either gap.

The theorem concerns the scalar graph-hull gap relative to the sum of individual factor gaps. Bipartite exactness here does not imply equality of the full polytope carrying a separate value coordinate for every factor. Zero gaps cause no difficulty for the inequality; ratios are interpreted only when the denominator is positive.

## Envelope and common-maximum audit

Multiaffinity permits replacement of any interior graph point by independent Bernoulli vertex interpolation, preserving both its mean and value. Thus binary distributions suffice for both envelopes, locally and globally.

For one factor, Jensen gives the lower bound `ψ(Σp_i)`, where `ψ` is the convex interpolation of `φ` between consecutive integers. The cube restricted to one integer degree slab is integral: two fractional coordinates permit an opposite perturbation, and one fractional coordinate cannot make the integer sum bound tight. This proves attainability even when `Σp_i` is an integer or some means are zero or one.

Discrete convexity implies supermodularity of the cardinality set function. In the uncrossing proof, choose a maximizing distribution, then one maximizing `E|X|²` among the primary maximizers. Uncrossing incomparable support sets cannot improve the primary objective beyond its maximum; therefore it preserves that maximum and strictly improves the secondary objective, a contradiction. The maximizing support is a chain. Its distribution is determined by the coordinate marginals and is the common-threshold law. This argument does not require the sequence to increase. In particular, the same threshold law maximizes every factor simultaneously.

An equivalent explicit formula, useful for checking the baseline, is

```
cav f_v(p) = φ_v(0) + Σ_{k=1}^{d_v} [φ_v(k)−φ_v(k−1)] p_(k),
```

where the means are sorted in nonincreasing order. The draft correctly retains this common upper envelope when comparing gaps.

## Degree-slab and rounding audit

At a degree-slab vertex, let `F` be the strictly fractional edges and count each tight vertex degree row once. Full column rank requires `|F|≤|R|`. Each tight row incident to a fractional edge has at least two fractional incidences, because its residual degree is an integer. Every edge has two endpoints, so `2|R|≤2|F|`. Equality forces a union of cycles with every participating degree row tight. Even cycles admit a sufficiently small alternating perturbation; on an odd cycle, the tight equations force every edge to one half.

This counting covers parallel edges: a two-edge cycle is even and cannot be fractional at an extreme point. Private-coordinate dummy vertices have degree one, so cannot lie on a fractional cycle. Constant factors and isolated factor vertices are harmless. Unused coordinates can be omitted and given their prescribed marginals independently.

The slab is chosen using the original mean. Since each local lower envelope is affine on its allowed degree slab, its expectation under a vertex decomposition is exactly its value at that original mean. The local upper envelope is concave, so the crucial inequality is

```
E T(Z) ≤ T(p).
```

The draft uses this direction correctly.

On a half-valued odd cycle of length `L`, uniform maximum-matching/complement rounding preserves every edge marginal. At each factor vertex it selects zero or two cycle edges with probability `1/(2L)` each and one otherwise. If `m` other incident coordinates equal one, the local gap is

```
T_v(z) = [φ_v(m)+φ_v(m+2)]/2 − φ_v(m+1).
```

Consequently its expected rounding cost is exactly `vex f_v(z)+T_v(z)/L`. Nonnegative curvature permits replacing `1/L` by `1/g`. Averaging and subtracting from the shared concave envelope proves `H≥(1−1/g)T`. In a bipartite graph the slab is integral and attains all individual lower envelopes simultaneously. The sharp odd-cycle examples are valid.

## Positive-box corollary

On `x_i∈[l_i,r l_i]`, with `l_i>0` and one common `r>1`, normalization gives the original factor's binary values `a_v(∏l_i)r^k`. Their discrete second differences are nonnegative. The theorem therefore applies to the original factor without expanding it into separately relaxed monomials; the original occurrence count is preserved.

Different connected components may use different ratios. Fixed coordinates can be substituted first. The unit-box AND sequence is also convex and gives the earlier theorem directly. For every fixed `r>1`, an odd cycle of bilinear products has the same gap ratio as its unit-box counterpart: affine terms contribute no gap and the nonlinear parts share the positive multiplier `(r−1)²`.

Unequal aspect ratios within a component are outside this corollary. The known positive-box bipartite obstruction therefore remains consistent with it.

## Supplemental validation reviewed

The author supplied [a reproducible verifier](../code/multilinear_convex_cardinality_verify.py). I independently inspected its formulas and its full binary-distribution LP formulation. Its rational tests check the cycle curvature identity, while its LP tests use independently enumerated binary objective values with prescribed marginal constraints. The random sequences include negative entries and slopes, and the graphs include private and parallel edges. The parity-lift breadth-first search correctly computes odd girth as the minimum odd closed-walk length.

The LP calculations use floating-point HiGHS and are numerical corroboration, not proof certificates. The mathematical verdict above rests on the independently checked proof.

The author reports 175 exact curvature checks and 240 full-distribution LP comparisons, including 181 bipartite equality cases.

## Subsequent optimization corollary audit

**The matching reduction and scalar-envelope optimization corollary also pass.** I reviewed the added construction and the explicit rational dual bound after completing the core theorem audit.

For an original edge, its two mandatory gadget vertices can be covered either by their common inactive edge or by two endpoint-slot edges. If one uses a slot, the other cannot use the inactive edge and must also use a slot. Thus every matching covering the mandatory vertices represents one original binary vector. Conversely, every binary vector can be represented because each endpoint has as many slots as incident edges. Since all incident gadget vertices have the same slot neighbors, occupied slots can always be reassigned to the cheapest available increments. Discrete convexity makes these the first `k` increments, whose sum is `φ_v(k)−φ_v(0)`.

Negative slot increments and negative original linear costs do not affect this argument. If `W` is the sum of absolute unmodified gadget edge costs, two matchings differ in unmodified cost by at most `2W`. A coverage bonus `M=2W+1` per mandatory endpoint therefore forces complete mandatory coverage; the all-inactive matching supplies a feasible completely covered comparison. This proves the claimed reduction to unconstrained weighted matching.

I added and ran [an independent exact verifier](../code/audit_convex_cardinality_matching.py). All 100 seeded tests passed. The verifier compares exhaustive original binary minimization with a separate exhaustive recursion over all unconstrained gadget matchings, using integer arithmetic throughout. Cases include signed convex sequences, negative original edge costs, zero-cost dummy factors, isolated factors, and parallel edges. This verifies the reduction on small instances; it does not implement the polynomial-time matching algorithm.

For the envelope LP, matching minimizes `f(z)−π·z` and therefore separates the dual constraints. The rows `(1,z)` span the full dual variable space, so the dual has no lines; its nonempty optimal face contains a vertex. With `A` bounding the absolute binary function values, Cramer's rule bounds every coordinate of such a vertex by `(n+1)! A`, using a nonsingular zero-one matrix. The added explicit bounding box therefore preserves an optimum and has polynomial encoding length. This justifies rational separation-to-optimization also at boundary means. Sorting gives the common concave-envelope value and a globally valid supporting affine upper function. Together these yield exact scalar-envelope evaluation and scalar graph-hull separation, without a claim about a polynomial-size formulation of all factor values.

The optimization statement is presented appropriately as a consequence of classical matching and separation machinery, not as a new matching algorithm.
