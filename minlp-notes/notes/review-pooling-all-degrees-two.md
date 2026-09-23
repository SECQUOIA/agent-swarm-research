# Independent review: all four pooling degree bounds at most two

Date: 2026-09-05. Verdict: **PASS** for the mathematical reduction, strong
NP-hardness, and absence of a profit PTAS unless P=NP. No mathematical defect
was found. This review does not certify that the result is absent from all
previous literature.

Reviewed draft: [candidate investigation](pooling-all-degrees-two-investigation.md),
as present on 2026-09-05. The reviewer reconstructed the flow normalization,
integrality argument, and independent-set identity from the construction
before reading the draft proof, and then checked the complete draft.

## Flow algebra and deletion

For every pool, mass balance gives `a+d=s+b`, so its cost is exactly
`a-2s-b=-s-d`. This is an identity for every feasible flow, including mixed
intakes and clean flow sent to the lax output. It is not an inequality that
requires a pure-mode assumption.

At a strict output, every contributing positive-throughput pool has quality
in `[0,1]`. The zero quality upper bound forces each individual quality-flow
product to vanish. Hence a pool satisfies `s>0 => d=0`, or equivalently
`s*d=0`. Zero-throughput pools do not cause a sign problem because all their
outflows vanish, irrespective of their otherwise unconstrained qualities.

The deletion map is `(a,d,s,b) -> (s,d,s,d)`. Complementarity ensures at most
one of the two retained mode quantities is positive. The original flow has
`a>=s` and `b>=d`: if `s>0`, then `d=0` and `a=s+b`; if `s=0`, both
inequalities follow from nonnegativity and mass balance. Thus the map only
decreases each arc flow. Shared input capacities, shared output capacities,
pool capacities, and private output capacities all remain valid. New pool
qualities can be set to zero or one according to the retained mode. Profit
is unchanged because `s` and `d` are unchanged.

This argument depends on having upper capacities and no positive minimum
throughputs, which is exactly the model stated in the draft.

## Integral replacement

After fixing at most one allowed mode per pool, every pool is represented by
one edge joining its allowed input to its allowed output. All capacities
are one. The feasible mode throughputs form a fractional matching in a
bipartite graph. Each pool occurs once, so its capacity is the ordinary
upper bound one on its one edge; no omitted coupling constraint remains.

Bipartite matching integrality supplies an integral matching of at least
the fractional objective. Routing it through the corresponding pools
preserves the already fixed pure modes. This establishes existence of an
integral optimum and polynomial rounding from any rational feasible point.
It does not claim every optimal solution is integral, and such a stronger
claim is unnecessary.

An equivalent decomposition is useful for checking the resource roles:
clean edges join the `E1` resources to the `E2` resources, while dirty edges
join `E3` resources to private lax outputs. These resource classes are
distinct. The fact that the clean conflict graph is a union of even cycles
is consistent with the matching argument, but need not be used in the proof.

## Independent-set identity and approximation transfer

The only integral-mode conflicts are clean-clean conflicts from `E1` and
`E2`, dirty-dirty conflicts from `E3`, and the two modes at each pool.
Consequently the mode conflict graph is exactly the graph obtained by
replacing every `E3` edge by a path of length three.

For any independent set in this graph containing both original endpoints
of such a path, both internal vertices are absent. Replacing one original
endpoint by its adjacent internal vertex preserves independence and size.
Because `E3` is a matching, these changes do not interfere. The resulting
original vertices are independent in `G`, and the number of selected
internal vertices is at most `|E3|`. Conversely, any independent set of `G`
extends by one internal vertex per path. Therefore
`OPT_profit=alpha(H)=n/2+alpha(G)`.

The recovery procedure gives an independent set of `G` of size at least
`P-n/2` from any original feasible pooling point of profit `P`, because
normalization preserves profit and matching rounding can only increase it.
The greedy bound `alpha(G)>=n/4` implies `OPT_profit<=3 alpha(G)`.
Thus the draft's transfer from relative profit error `epsilon` to relative
independent-set error `3 epsilon` is valid. The distinction between
nonnegative profit and negative minimum cost is correctly stated.

## Degree counts and source theorem

A cubic graph with a supplied proper three-edge-coloring has exactly one
incident edge of each color at every vertex. Hence all inputs have
out-degree two, pools have exactly two inputs and two outputs, strict
outputs have in-degree two, and private lax outputs have in-degree one.
The three layer sizes are `n`, `n`, and `3n/2`; all capacities are one.
The threshold `-(n/2+k)` is integral with magnitude linear in the graph
size. Strong NP-hardness follows without any NP-membership assertion for
unrestricted pooling.

The reviewer independently read Section 5(A), printed pages 25–26, of
Chlebík and Chlebíková's
[primary author manuscript](https://pure.port.ac.uk/ws/portalfiles/portal/1887750/3DM_JOURNAL_revision_old.pdf).
It explicitly constructs proper three-edge-colorings of the cubic graphs
used in its independent-set gap reduction. It then transfers their unchanged
objective to three-dimensional matching. Thus the required independent-set
hardness holds with a supplied coloring; the reduction is not relying only
on a promise that a coloring exists. Its positive constant hardness gap
also supports the no-PTAS conclusion. A numerical gap constant is unnecessary.

## Independent computational check

The [reviewer's separate checker](../code/pooling_all_degrees_two/independent_review.py)
enumerates every quality disjunction `d=0 OR s=0` and solves the resulting
linear flow model, retaining clean-to-lax waste and mixed intakes in the
branches where they are feasible. This union of LPs is exactly the original
continuous model projected onto flows: if `s=0`, any intake mixture has
quality at most one; if `d=0`, the quality is zero. The check therefore
does not assume the candidate's normalization or integrality conclusions.

The run passed on 46 graph/coloring instances and 5,152 original-flow LP
branches: every coloring with the first matching fixed on four and six
vertices, and 12 seeded instances on eight vertices. In each branch the
checker reconstructed feasible pool qualities and checked the deletion
map's feasibility and profit preservation. Every graph optimum equaled
`n/2+alpha(G)`, where `alpha(G)` was independently computed by exhaustive
vertex-subset enumeration. The numerical tolerance was `1e-8`; these are
numerical checks supporting the exact proof, not formal certificates.

A deliberate negative control removes the quality disjunction on `K4`.
The relaxed profit becomes four, whereas the true optimum is three. This
confirms the check can detect the essential nonlinear mode restriction.

Run output:

```
PASS: 46 graph/coloring instances; 5152 original-flow LP branches.
Includes all colorings at n=4,6 with first matching fixed, plus 12 seeded n=8 instances.
Negative control K4: dropping quality disjunction gives 4, true optimum 3.
Every branch checked original pool quality, deletion feasibility, and exact profit preservation (tolerance 1e-8).
```
