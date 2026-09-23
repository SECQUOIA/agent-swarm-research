# Second independent review: pooling with all degree bounds two

Date: 2026-09-05. Reviewer: `potential_flow_review`, independently of the author and first reviewer.

Reviewed draft: [pooling-all-degrees-two-investigation.md](pooling-all-degrees-two-investigation.md), including its weighted-capacity and positive-tolerance extensions. The main proof was read before the first review; the first review was consulted afterward.

**Verdict: PASS.** The main strong NP-hardness reduction, exact objective identity, polynomial rounding from arbitrary rational feasible solutions, and profit inapproximability transfer are mathematically correct. The two structural extensions also pass. This review does not certify novelty.

## Nonconvex feasibility and purification

Write a pool's clean and dirty intake as `a,d`, strict and lax outflow as `s,b`, and throughput as `t=a+d=s+b`. Its profit is exactly `s+d`, by mass balance and the four specified costs.

If `t>0`, the mixing equation gives quality `p=d/t` in `[0,1]`. If `t=0`, every incident flow is zero, so its quality has no effect. Consequently all summands `p_v s_v` in each zero-bound strict output constraint are nonnegative, and each summand must vanish. Hence `s>0` implies `d=0`.

The purification can be written in one line:

```
(a,d,s,b) -> (s,d,s,d).
```

The implication above ensures this tuple has at most one active mode. It also gives `s<=a` and `d<=b`: if `s>0`, then `d=0` and `a=s+b`; if `s=0`, then `b=a+d`. Thus **every arc flow decreases or remains equal**. All shared input and output capacities and all pool capacities remain satisfied. Setting the new active quality to zero in the clean mode or one in the dirty mode makes both pool and output quality equations explicit. Profit remains exactly `s+d`.

This checks the entire continuous feasible region, including mixed intake sent only to a lax output and pure clean flow split between strict and lax outputs. It does not assume optimality, integrality, or prior purification.

## Exact polynomial rounding from rational points

For each pool choose the clean mode if its given strict flow is positive; otherwise choose the dirty mode. A zero-throughput pool may therefore be assigned the dirty mode without affecting the argument. Construct the bipartite graph with the physical inputs on one side, the physical outputs on the other, and one edge for each pool's chosen mode. Associate the purified throughput to that edge.

These edge values are a feasible fractional matching: incidence sums are bounded by the unit physical vertex capacities, and each edge value is bounded by the unit pool capacity. Conversely, every fractional matching of this graph routes feasibly through the selected pure pool modes. There is only one edge per pool, so no pool constraint has been lost.

Compute a maximum-cardinality matching of this graph and route one unit through each selected pool. Bipartite matching integrality guarantees that its cardinality is at least the original fractional throughput sum, which is exactly the original profit. This is a direct constructive rounding algorithm.

For an arbitrarily encoded **rational feasible solution**, the only use of its numerical values needed to construct the graph is testing whether each rational `s_v` is positive. With positive-denominator rational encoding, this is an integer sign test. No division, numerical tolerance, radical comparison, nonlinear optimization, or separation oracle is required. The matching algorithm then works only on a graph of size linear in the pooling instance. Its output flows and qualities belong to `{0,1}`. Total running time is polynomial in the instance and supplied solution encoding lengths, even if a positive strict flow is extremely small.

The existence argument also holds for arbitrary real feasible solutions. An algorithmic claim for real solutions would need a representation supporting exact sign tests, so the draft correctly states the bit-complexity rounding claim for rational solutions. A standard Turing-model PTAS outputs a finitely encoded feasible solution, and this family has rational integral optima, so this poses no obstacle to the approximation reduction. Approximate numerical feasibility alone is a different contract; the proof does not rely on it.

## Independent-set identity and all degree restrictions

Given the supplied proper three-edge-coloring of a simple cubic graph, each color class is a perfect matching. Shared clean inputs impose exactly the `E1` clean-clean conflicts; shared strict outputs impose exactly the `E2` clean-clean conflicts; shared dirty inputs impose exactly the `E3` dirty-dirty conflicts. The two modes in one pool conflict through unit pool capacity. Private lax outputs introduce no other conflicts.

The resulting conflict graph is precisely the graph obtained by replacing each `E3` edge `uv` by `u-d_u-d_v-v`. Thus an integral pure pooling point is exactly an independent set in this graph, with profit equal to cardinality. For a general continuous pooling point, the preceding matching rounding provides an independent set with at least as much profit.

Any independent set of `G` extends by one internal vertex per subdivided edge. Conversely, when an independent set in the subdivided graph contains both original endpoints of a subdivided edge, neither internal vertex can be present. Replacing one original endpoint by its adjacent internal vertex preserves independence and cardinality. This creates no external conflict because that internal vertex has only its two path neighbors. Since `E3` is a matching, the replacements do not interfere. The remaining original vertices form an independent set in `G`, and at most `n/2` selected vertices are internal. Therefore

```
OPT_profit = n/2 + alpha(G),
recovered independent-set size >= original profit - n/2.
```

Every input has out-degree two; every pool has exactly two inputs and two outputs; strict outputs have in-degree two; private lax outputs have in-degree one. All capacities equal one, and all four costs belong to the stated constant set. There are `n` inputs, `n` pools, and `3n/2` outputs. For source threshold `k`, the target threshold is cost at most `-(n/2+k)`, with the claimed direction. The construction is linear in graph size and has bounded physical data, giving strong NP-hardness.

## Source verification and approximation transfer

This reviewer independently opened the [Chlebík–Chlebíková author manuscript](https://pure.port.ac.uk/ws/portalfiles/portal/1887750/3DM_JOURNAL_revision_old.pdf), Section 5(A), printed pages 25–26. The argument constructs proper three-edge-colorings of the consistency gadgets and states that the resulting graph `f(I)` is cubic and edge-three-colored. It retains the independent-set objective and the NP-hard approximation gap before interpreting the same graph as a three-dimensional matching instance. Therefore the required source is valid **with a supplied coloring**; no algorithm for finding an unknown coloring is presumed. The paper's graph convention is simple graphs. This source check does not rely merely on the more general cubic independent-set theorem in its abstract.

The bound `alpha(G)>=n/4` gives `OPT_profit<=3 alpha(G)`. From profit at least `(1-epsilon)OPT_profit`, recovery therefore gives at least `(1-3epsilon)alpha(G)` independent-set vertices. The fixed source gap rules out a PTAS for the nonnegative profit objective unless `P=NP`. This argument does not apply a multiplicative ratio to a negative cost.

## Weighted integer-capacity extension

For the displayed generalized costs, direct substitution of `a+d=s+b` gives cost `-alpha_v s-beta_v d`. The same purification preserves the two rewarded quantities. Once one mode per pool is chosen, the remaining optimization is a bipartite capacitated flow problem: input and output capacities are vertex bounds, and each pool capacity is an edge bound. With integer capacities its feasible polytope is integral; rational mode rewards do not change that fact. A maximum-weight integral flow is at least as profitable as the given fractional one. Thus existence of an integral pure optimum follows, with no claim that the full pooling feasible set is integral or convex.

With unit capacities, the two mode edges of a pool have distinct endpoints because clean and dirty inputs are distinct quality types and strict and lax outputs are distinct specification types. The rainbow-matching interpretation with one color per pool is therefore exact for this cost and quality subfamily.

## Positive strict-quality tolerance extension

The proposed cleanup inequalities also hold for the original mixed feasible flows. At a pool of quality `p<=eta`, retaining clean-strict flow `min(a,s)` loses profit

```
s+d-min(a,s) = d+max(s-a,0) <= 2d <= 2eta,
```

using `s-a=d-b<=d` and `t<=1`. At a pool of quality `p>eta`, retaining dirty-lax flow `min(d,b)` loses at most

```
s+d-min(d,b) = s+max(d-b,0) <= 2s,
```

using `d-b=s-a<=s`. Both changes decrease all incident arc flows. Summing strict output quality inequalities gives `sum p_v s_v<=delta sum s_v<=delta n`. Thus high-quality pools have total strict flow at most `delta n/eta`, establishing loss at most `2n(eta+delta/eta)`.

With rational `eta>0` and `delta=eta^2`, loss is at most `4eta n`. The draft's choices `eta<gamma/32` and `epsilon<gamma/6` give `3epsilon+16eta<gamma`; the approximation contradiction follows exactly as written. Constants can be fixed independently of the instance. The positive-tolerance result consequently retains approximation hardness with bounded rational data; its proof uses a source gap rather than the zero-tolerance exact integer objective identity. Adding one to every input quality and output bound preserves feasibility by pool and output mass balance, so the strictly positive quality normalization is valid.

## Verification scope

The review supplies independent exact derivations and an explicit polynomial rounding algorithm. Existing numerical and disjunctive-LP checks were read after this analysis; they are consistent with it. No further numerical optimization was needed for this second review. The novelty screen remains a separate task, and no assertion that every feasible or optimal continuous point is integral is warranted or needed.

## Addendum: all four degrees exactly two

The author's later refinement merges the two private lax outputs associated with endpoints `u,v` of every `E3` edge into one shared unit-capacity lax output. This refinement also **passes** independent review. Purification still only decreases arc flows, so it remains valid with the added output-sharing constraint. On pure-mode points, the merged lax output receives exactly the sum of the two corresponding dirty throughputs; their common dirty input already bounds that same sum by one. Thus the merged output creates no additional pure-mode conflict, and the conflict graph and optimum identity remain unchanged. The matching graph may have parallel dirty-mode edges between the same input and output; treating them as distinct pool-labelled edges gives the same integral matching polytope and polynomial algorithm.

All inputs now have out-degree exactly two, all pools have in-degree and out-degree exactly two, and all outputs have in-degree exactly two. The network has `n` inputs, `n` pools, and `n` outputs. This proves the corresponding stronger exact-degree hardness and profit inapproximability corollary. The positive-tolerance cleanup remains valid because it also only decreases arc flows.
