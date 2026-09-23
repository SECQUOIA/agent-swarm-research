# Positive multilinear gaps when every variable appears in at most two terms

Date: 2026-09-04.

Status: sharp theorem with a complete proof, independently reviewed; see [the audit](../notes/review-multilinear-frequency-two.md). Classical fractional matching structure is the main combinatorial ingredient. The gap-ratio application and odd-girth refinement require a separate novelty assessment. The box scope is the unit cube and boxes with zero lower bounds.

## 1. Result

Let

```
f(x) = sum_{v in V} a_v product_{i in S_v} x_i,
       a_v>0, |S_v|>=2, x in [0,1]^n,
```

with distinct monomial supports. Suppose every variable belongs to at most two supports. Affine terms can be ignored because they affect neither gap.

Form a loopless dual multigraph: monomials are vertices; a variable shared by two terms gives an edge joining those terms. A variable belonging to only one term gives an edge from that term to its own new dummy vertex of weight zero. Parallel edges are allowed. Let `g` be the length of a shortest odd cycle in this graph; write `g=infinity` if the graph is bipartite.

**Theorem.** At every point of the unit cube,

```
tbtgap_f(x) <= g/(g-1) chgap_f(x)                     (1)
```

for finite `g`, and the gaps are equal when the dual graph is bipartite. In particular,

```
tbtgap_f(x) <= (3/2) chgap_f(x).                      (2)
```

The constants are sharp: an odd cycle of length `g`, with unit weights and all its edge-variable marginals equal to `1/2`, has ratio exactly `g/(g-1)`. Thus the frequency-two worst ratio is `3/2`, not two. There is no bound on monomial degree or the number of terms.

The theorem concerns the scalar positive polynomial's gap. Bipartite exactness here does not assert that all individually feasible product-coordinate values can be realized simultaneously, or that the full lifted multilinear polytope equals its standard relaxation.

## 2. Coverage with the baseline retained

Use failure marginals `p_i=1-x_i`. For each dual vertex define

```
s_v(p) = sum_{i incident to v} p_i,
b_v(p) = max_{i incident to v} p_i,
c_v(p) = min{1,s_v(p)}.
```

The same definitions can be used at dummy vertices, whose weights are zero. Isolated irrelevant vertices contribute zero.

The single-term gap is

```
T_v = c_v(p)-b_v(p).
```

Indeed, its concave envelope is `1-b_v`, while its convex envelope is `max(0,1-s_v)`. For a random selected set of failure edges `F` with the prescribed edge marginals, let `I_v(F)` indicate that at least one edge incident to `v` is selected. The positive-coefficient concave envelope is the sum of the individual concave envelopes, attained by the common-threshold coupling. Consequently

```
tbtgap_f(x) = sum_v a_v [c_v(p)-b_v(p)],
chgap_f(x) = max_{P(i in F)=p_i}
                sum_v a_v [E I_v(F)-b_v(p)].          (3)
```

The baseline `b_v(p)` is essential. A generic approximation guarantee for the unshifted expected coverage would not prove the claimed gap bound.

## 3. A half-integral decomposition

Consider the degree-slab polytope

```
P(p) = {z in [0,1]^E:
          floor(s_v(p)) <= sum_{i incident to v} z_i
                         <= ceil(s_v(p)) for every v}.
```

The vector `p` belongs to this compact polytope. At every vertex `z` of `P(p)`, the fractional coordinates form vertex-disjoint odd cycles, and each fractional coordinate equals `1/2`. This is a standard fractional matching fact; the following direct proof also covers the lower/upper degree bounds and parallel edges used here.

Let `F_z` be the fractional edges, and let `R` be the vertices whose degree bound is tight and contains at least one such edge. Count a vertex only once when its lower and upper bounds coincide. At a polytope vertex these rows must have full column rank on `F_z`; otherwise a sufficiently small perturbation in their nullspace preserves every tight constraint and all box bounds, contradicting extremality. Thus `|F_z|<=|R|`.

Every tight row has an integer right-hand side and its other incident entries are integral. It cannot contain exactly one fractional edge; it contains at least two. Counting incidences therefore gives

```
2|R| <= number of fractional incidences at R <= 2|F_z|.
```

Both inequalities are equalities. Thus every fractional edge has both endpoints in `R`, and each vertex of the fractional subgraph has degree two. Its components are cycles. An even cycle would admit a nonzero alternating perturbation, contradicting full column rank. Every cycle is therefore odd. The two fractional entries at each of its vertices sum to an integer strictly between zero and two, so they sum to one. Alternating around an odd cycle forces both values to be `1/2`.

Decompose `p` as a finite convex combination of vertices of `P(p)`, and write `Z` for the resulting random vertex. Then `E Z=p`. Two properties will matter:

```
E c_v(Z) = c_v(p),
E b_v(Z) >= b_v(p).                                  (4)
```

For the first identity, if `s_v(p)<1`, its permitted degree interval is contained in `[0,1]`, where `min(1,s)=s`; if `s_v(p)>=1`, every permitted degree is at least one. The boundary cases follow as well. The second inequality is Jensen's inequality for the maximum of the incident coordinates.

## 4. Round each odd cycle

Condition on a vertex `z` of `P(p)`. Keep its integral edges fixed. On a fractional odd cycle of length `L`, choose uniformly among its `L` maximum matchings, each containing `(L-1)/2` edges. Independently choose with probability one half to use that matching or its complement within the cycle.

Every edge has marginal `1/2`, so this preserves `z`. A maximum matching leaves exactly one cycle vertex uncovered; its complement covers all cycle vertices. Uniform choice of the maximum matching makes the uncovered vertex uniform. Therefore every cycle vertex is covered by the cycle edges with probability

```
1-1/(2L).                                           (5)
```

Cycles can be rounded independently. If a cycle vertex has another integral edge equal to one, it is certainly covered. Otherwise its conditional baseline is `b_v(z)=1/2` and its conditional target is `c_v(z)=1`. Vertices not incident to fractional edges have `b_v(z)=c_v(z)` equal to zero or one and are handled exactly.

For finite odd girth `g`, put `alpha=1-1/g`. Since every fractional odd cycle has `L>=g`, these observations yield, for every vertex,

```
E[I_v(F) | Z=z] >= alpha c_v(z)+(1-alpha)b_v(z).       (6)
```

For a vulnerable cycle vertex the right-hand side is `1-1/(2g)`, bounded by (5); in all other cases the claim is exact.

Average (6) over `Z` and use (4):

```
E I_v(F) - b_v(p)
 >= alpha c_v(p)+(1-alpha)E b_v(Z)-b_v(p)
 >= alpha [c_v(p)-b_v(p)].                           (7)
```

This is the step that preserves the baseline. All failure marginals remain correct. Multiply (7) by the nonnegative term weights and sum; (3) proves (1).

If the dual graph is bipartite, there are no fractional cycles and every vertex of `P(p)` is integral. Its degree-slab decomposition directly attains coverage `c_v(p)` at every vertex in expectation. Thus every individual convex-envelope lower bound is simultaneously attained, proving equality of the two gaps. ∎

## 5. Sharpness

Let the dual graph be the odd cycle `C_L`, and give every term weight one and every variable marginal `x_i=1/2`. This corresponds to the positive bilinear cycle polynomial. The termwise gap is `L/2`, and the baseline total in (3) is `L/2`.

For every selected edge set `F` on this cycle,

```
number of covered vertices <= |F|+(L-1)/2.            (8)
```

If `|F|<=(L-1)/2`, use the bound `2|F|`; otherwise use the bound `L`. Since the prescribed edge marginals imply `E|F|=L/2`, (8) bounds expected coverage by `L-1/2`. The matching/complement construction attains this bound. Therefore

```
chgap_f = (L-1)/2,
tbtgap_f/chgap_f = L/(L-1).
```

All marginals are strictly interior. The triangle gives the sharp value `3/2`.

## 6. Primary-source comparison and scope

- Michael D. Barrus, *On fractional realizations of graph degree sequences*, Electronic Journal of Combinatorics 21(2), P2.18 (2014), Theorem 2.1 and its proof, gives the half-integral, vertex-disjoint odd-cycle structure for the bounded fractional fixed-degree polytope and identifies the matching foundations as classical. Our degree-slab variant has the same elementary incidence-count proof. [Open published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf/).
- Alberto Del Pia and Matthias Walter, *Simple odd beta-cycle inequalities for binary polynomial optimization*, Mathematical Programming 206, 203–238 (2024), studies odd-cycle inequalities for the full multilinear polytope and gives exact formulations for cycle hypergraphs with other inequalities. This is close structural prior work, but the reviewed abstract and introduction do not state the frequency-two scalar gap ratio proved here. [Open published paper](https://link.springer.com/article/10.1007/s10107-023-01992-y).
- Searches for multilinear read-twice relaxations, frequency-two monomial gaps, and odd-girth gap ratios found no direct statement of (1). This is not evidence sufficient to claim publication novelty. The ordinary bilinear odd-cycle example itself is established territory.

The result immediately extends to boxes with zero lower bounds by positive coordinate scaling. An arbitrary positive lower bound expands a monomial into many monomials and can destroy the frequency-two condition. Therefore the earlier generic nonnegative-box expansion must not be invoked to claim this structural theorem on all nonnegative boxes without another proof.

The [independently checked positive-box obstruction](../notes/multilinear-frequency-two-positive-box-obstruction.md) shows that bipartite exactness actually fails when positive lower bounds are allowed: its ratio is `7/6`. This does not disprove a universal `3/2` bound on those boxes; that broader question remains open here.

The proof constructs a simultaneous coupling with a sharp scalar gap guarantee.

A separate [independently reviewed algorithmic corollary](positive-multilinear-frequency-two-optimization.md) gives polynomial-time exact evaluation and separation for the scalar graph hull via classical prize-collecting edge cover. It makes no claim of a polynomial-size explicit formulation of the full lifted multilinear polytope.

## 7. Verification and remaining work

1. The [independent audit](../notes/review-multilinear-frequency-two.md) passed the full proof, including the degree-slab extreme-point structure, baseline averaging, dummy vertices, parallel edges, and sharpness. Its [exact supplemental verifier](../code/audit-frequency-two-cycle-rounding.py) checked the cycle marginals and coverage probabilities for lengths 3, 5, 7, 9, and 11, and the sharpness inequality over all 2,728 corresponding edge subsets.
2. The [verification script](../code/multilinear_frequency_two_verify.py) passed 200 seeded full binary-distribution LP comparisons with positive weights, unequal marginals, parallel edges, and single-incidence variables. All 94 bipartite cases attained equality. The sharp ratios were checked on odd cycles of lengths 3, 5, 7, and 9. Termwise calculations use exact rational arithmetic; the full distribution LP uses floating-point HiGHS. These checks complement the proof rather than certify it.
3. Broader novelty comparison with matching-based coverage rounding and multilinear-polytope theory.

## Lean verification

[Topic 19](../formal/topics/19-structural-multilinear/COVERAGE.md) formalizes the
`3/2` bound, the `g/(g-1)` odd-girth refinement, bipartite exactness and odd-cycle
sharpness. These are theorems about the original support family: its
frequency-two assumption supplies the degree-slab decomposition and cycle
rounding laws. The odd-girth condition concerns genuine cycles of distinct
factors and shared coordinates. Private variables and parallel dual edges are
included; a decomposition or rounding law is not an extra theorem hypothesis.
The sharpness family has proved frequency-two membership and exact odd girth.

The package also proves zero-lower-box transfer, the common-aspect positive-box
extensions through convex cardinality factors, and their sharp odd-cycle
witnesses. The exact unequal-aspect example has ratio `7/6`, disproving
bipartite exactness on arbitrary positive boxes. A universal `3/2` bound on
those arbitrary boxes remains unresolved here.

The [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md)
identifies the checks and reviewed source snapshots. The separate matching-based
optimization and separation algorithms, and their bit complexity, are not
part of this Lean verification.
