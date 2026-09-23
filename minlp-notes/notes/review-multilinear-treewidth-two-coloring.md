# Independent audit of the incidence-treewidth-two coloring theorem

Date: 2026-09-04. Reviewer: audit_mccormick, independently of new_directions.
Status: the analytic graph proof, positive-multilinear transfer, and sharpness
example in [the theorem draft](../results/positive-multilinear-treewidth-two-exact.md)
pass this full written audit. This verifies correctness, not publication priority.
The result concerns zero-lower-bound boxes; arbitrary nonnegative local payoffs
and arbitrary positive lower bounds are separate questions.

## What the graph invariant records

I checked the stronger property actually proved: every cycle using only one
factor color has an even number of factor vertices. Paths count factor vertices
at both endpoints when those endpoints are factors. This convention explains
both composition corrections and is essential for the proof.

For a network with fixed terminal types, the invariant specifies one parity,
shared by its two color-swapped active witnesses. Different active, blocked,
and unequal-endpoint witnesses may use different internal colorings. Nothing
requires all those witnesses to coexist in a single coloring. A blocked witness
has no monochromatic terminal path, but may contain cycles wholly within the
network; those cycles are already controlled by goodness.

For variable-variable terminals the active witness excludes every path of the
other color. For mixed terminals the factor endpoint itself excludes the other
color. For equally colored factor-factor terminals the same observation applies.
With differently colored factor terminals no terminal path is monochromatic.
These distinctions supply the compatibility needed at every composition.

## Series cases checked

Let the identified vertex have factor indicator `δ∈{0,1}`. A terminal path
is the concatenation of one path in each component, so its factor parity is
`ε_1 XOR ε_2 XOR δ`. The last correction removes the twice-counted shared
factor when present. Every cycle in a series composition lies wholly in one
component. Thus no additional cycle condition is hidden in the series cases.

Active witnesses concatenate with the same desired color. I checked each
required extra witness:

| Outer types; identified type | Reason the required witness exists |
| --- | --- |
| V,V; V | Opposite active colors prevent a monochromatic path from crossing both components. |
| V,V; F | Blocking is required only for output parity zero, hence unequal component parities. The even mixed component has no direct edge and can be blocked with the prescribed shared factor color. |
| V,F; V, or reversed | Use the opposite color in the V,V component from the prescribed outer factor color. |
| V,F; F, or reversed | Give the shared factor the opposite color from the outer factor. The F,F component admits those distinct endpoint colors and blocks every monochromatic terminal path. |
| F,F, equal colors; V | Blocking is required only for output parity one, hence unequal component parities. Block the even mixed component, whose direct edge is absent. |
| F,F, equal colors; F | Color the shared factor oppositely. Both components use their distinct-endpoint alternatives. |
| F,F, different colors; either type | For a shared variable use compatible active witnesses with the two prescribed colors. For a shared factor choose its color and use equal-endpoint active or distinct-endpoint witnesses separately. |

These exhaust all terminal-type triples, including reversals. A nontrivial
series composition has no direct terminal edge, and both mixed-terminal cases
supply the therefore-required blocking alternative. The argument using even
mixed parity is valid because the invariant separately guarantees that a direct
edge forces odd parity.

## Parallel cases checked

Component interiors are disjoint. Every new simple cycle uses exactly one
terminal path in each component. Its factor parity is the XOR of the two path
parities and the number of factor terminals modulo two. A cycle cannot use
three different component paths: it would have to revisit a terminal.

For V,V terminals, even components have blocking witnesses. Activate both
components when their parities agree; otherwise activate the odd component and
block the even one. The resulting active parity is the Boolean OR. A blocking
witness is required only when both parities are even, and then both components
can be blocked.

For F,F terminals with a common prescribed color, odd components have blocking
witnesses. Activate both when their parities agree; otherwise activate the even
component and block the odd one. The resulting parity is the Boolean AND.
A blocking witness is required only when both parities are odd. With distinct
endpoint colors, use those prescribed colors in both components. A cross-component
monochromatic cycle would contain both differently colored endpoints, which is
impossible.

For mixed terminals without a direct edge, both components can be blocked with
the same factor-endpoint color. Activate either one and block the other, or block
both. For mixed terminals with a direct edge, precisely one component can contain
that edge in a simple graph. Activate its odd witness and block the other
component. These choices create no cross-component monochromatic cycle.

The simple-graph restriction is substantive. Two parallel direct edges would
form a length-two cycle with one factor vertex, which cannot meet the stronger
cycle claim. A usual monomial incidence graph has no parallel incidence edges,
so this restriction does not exclude the intended application. Repeated scopes
as different factor nodes also do not create parallel graph edges.

## Coverage of all graphs of treewidth at most two

The induction applies to every simple bipartite two-terminal series-parallel
network. In a series-parallel expression for a final simple bipartite graph,
each component network is a subgraph of the final graph and therefore is also
simple and bipartite. It is unnecessary to assume that an edge-contraction
recognition process preserves the bipartition labels.

I independently checked a primary source for the extension through blocks:
Hassin and Tamir, [Efficient algorithms for series-parallel graphs](https://www.math.tau.ac.il/~hassin/sp.pdf),
SIAM Journal on Computing (1986), printed p.381, Theorem 3.1. It gives the
series-parallel characterization of biconnected components via exclusion of a
subgraph homeomorphic to `K_4`, attributing the structural result to Dirac and
Duffin. The definitions and terminal composition rules are on printed p.380-381.
I visually checked those scanned pages. A graph with no `K_4` minor certainly
has no subdivision of `K_4`, so the stated direction covers all graphs of
treewidth at most two.

Root the block-cut forest. A new block intersects the processed part in one
articulation vertex. If that vertex is a factor, a global color swap in the new
block matches its prescribed color without affecting goodness. If it is a
variable, there is no color to match. Every graph cycle lies in one block.
Bridges and isolated vertices cause no difficulty: use the base edge or choose
an isolated factor's color arbitrarily. The block extension is therefore valid.

## Balanced-matrix transfer and the stronger TU consequence

The graph lemma excludes every monochromatic odd-factor cycle, so in particular
it excludes the induced cycles corresponding to odd-order two-ones-per-row-and-
column submatrices. Each color's scope matrix is balanced.

I independently checked Cornuéjols,
[Combinatorial Optimization: Packing and Covering](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf),
Theorem 6.13, printed p.82 (PDF page 84). For a balanced matrix it establishes
integrality of the unit-cube polytope with any partition of its rows into the
stated packing, equality, and covering constraints. For a 0/1 matrix the right
hand sides are one. Thus the draft uses the theorem with the correct right hand
sides; it does not infer mixed-row integrality merely from separate packing and
covering integrality.

For failure means `p`, the selected row inequalities all hold at `p`. Its
convex decomposition into binary feasible points gives a common joint law.
A packing row allows at most one failure, so union probability equals its sum
of failure means; a covering row has union probability one. This also covers
the threshold case `Σp_i=1`, assigned to packing in the draft. The lower
monomial envelope is therefore attained simultaneously within each color.

For a term `e`, choose a coordinate with smallest prescribed success mean.
The random deficiency `X_k−∏_{i∈e}X_i` is pointwise nonnegative. A color's law
achieves its full termwise deficiency for terms in that color and cannot make
other deficiencies negative. Mixing the two laws yields half the total termwise
gap. The sum of individual concave-envelope values is itself the full concave
envelope, because one comonotone law attains all upper intersections. Therefore
the maximum total deficiency is exactly the true hull gap. This proves the
claimed factor two. Empty or affine scopes contribute zero and may be discarded.

There is also a stronger structural consequence of the proved graph property:
**each color's 0/1 scope matrix is totally unimodular.** For any submatrix with
even row and column sums, its support graph is Eulerian and decomposes into
edge-disjoint simple cycles. Every such cycle has length divisible by four, so
the number of ones in the submatrix is divisible by four. Camion's criterion
then gives total unimodularity. The criterion is stated in the same Cornuéjols
source as Theorem 6.5, printed p.76 (PDF page 78). This argument was independently
derived during this audit and sent to the author and second reviewer for checking.
It may provide a useful alternative source vocabulary for the novelty search:
partitioning rows into two totally unimodular matrices when the bipartite support
has treewidth at most two.

## Sharpness and boundary checks

For the draft's flower polynomial with `n≥2`, each anchor-leaf term has upper
value `1/n` and lower value zero; the all-leaf term has upper value `1−1/n` and
lower value zero. Thus the termwise gap is `2−1/n`.

Writing `R` for the leaf-failure count gives `ER=1`, and the anchor has mean
`EA=1/n`. The total expected deficiency is

```
E[AR]+Pr(R≥1)−1/n.
```

The pointwise inequality `AR+1[R≥1]≤R+A` is valid for both anchor values and
all integer `R≥0`. It bounds the deficiency by one. A law with exactly one
uniformly chosen failed leaf and an independent anchor attains one. Hence the
full hull gap is exactly one and the ratios approach two.

After deleting the anchor vertex the incidence graph is a tree. Adding that
anchor to every edge bag of a width-one tree decomposition gives bags of size
three and proves treewidth at most two directly. For `n≥2`, two leaf branches
and the all-leaf factor form a cycle, proving treewidth at least two. Merely
having a small feedback vertex set was not used as an unexplained general
bound on treewidth.

If the termwise gap is zero the theorem states an inequality, not an undefined
ratio. Scaling a box `[0,u]` with positive finite upper bounds changes only the
positive coefficients. A coordinate with zero upper bound makes its incident
monomials identically zero, so it can first be deleted. The zero-lower-bound
extension is therefore valid, including degenerate boxes.

## Computation and status

I read the exact discovery script's transition functions and independently
reran it. It reached 73 signature types, with no new types in round eight and
no empty attainable-state set. Its parity corrections agree with the analytic
proof. This is supplementary evidence; the full case analysis above does not
depend on accepting finite computation as a proof.

No mathematical correction was required in the analytic theorem draft audited
here. The separately established arbitrary-payoff ratio-three example remains
consistent: its nonnegative multilinear factors have signed monomial expansions,
and it does not admit the positive-monomial deficiency argument used here.
Publication novelty still requires a separate literature audit.
