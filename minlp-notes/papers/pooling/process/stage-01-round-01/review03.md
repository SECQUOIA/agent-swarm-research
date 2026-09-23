# Stage 1, round 1 — reviewer 03

Reviewed the entire `sections/01-foundations.tex`, with particular attention to destination decomposition, single-product projection, capacities, signs, and approximation inequalities. I reconstructed those arguments directly and consulted the source results `pooling-triviality-polynomial.md` and `pooling-facial-quality-integrality.md`. I did not inspect the current round's other reports or edit the manuscript.

## Findings

### 1. Major: the endpoint formulation needs an upper-only quality hypothesis

**Location:** `01-foundations.tex:641–672`, especially the hypothesis at lines 641–642 and the claimed equivalence at lines 647–658.

The general model allows both lower and upper product quality bounds. The endpoint paragraph restricts the upper bounds to `{0,1}` but does not remove or restrict lower quality bounds. Its disjunction consequently does not characterize quality feasibility under its written hypotheses.

**Counterexample:** Use one input of quality zero, one pool, and one product, with feed and outlet capacity one and product quality interval `[1,1]`. Every input quality lies in `[0,1]` and the product upper bound is one, exactly as stated. The disjunction has `D=0` and `S=0`, so it accepts a unit flow. That flow has quality zero and violates the product lower bound. This example even has facial `F=empty`, so treating the paragraph as a special case of the preceding facial setting does not repair the omission. With outlet cost `-1`, the proposed MILP has optimum `-1` while the physical optimum is zero.

**Correction:** State explicitly that the only product quality restrictions in this special case are the indicated upper bounds (equivalently, any lower bounds are redundant, for example at most zero). Keep lower *flow* bounds permissible. Then the disjunction, MILP, and certificate conclusions are justified by the proof already given. This is a short repair, but it supplies an essential hypothesis to an exact-formulation claim.

### 2. Minor clarification: make the standing bounded-flow convention explicit

**Location:** model at `01-foundations.tex:49–50`; start of the single-product subsection; universal-integrality conclusion at lines 529–532; compact-lift discussion for cycles.

The wording that arcs and totals “may have finite rational lower and upper bounds” can mean that some upper bounds are absent. Subsequent statements use a minimum, compactness, network-flow *polytopes*, and an attained optimum for every objective. Those conclusions require bounded feasible arc flows. The source triviality result explicitly assumes finite arc and node capacities. If all relevant upper bounds are absent, the one-bypass network of cost `-1` is already an unbounded counterexample to the attained-optimum statements.

I regard this as a convention clarification rather than an identified flaw in the intended capacitated theory: the subsequent arguments consistently use finite capacities. State globally that every arc flow has a finite rational upper bound, explicit or implied by specified capacities, except in the expressly uncapacitated conic-hull constructions. Alternatively state boundedness precisely where optimization and compactness are invoked. In cyclic networks, finite source/product bounds alone do not bound isolated circulations.

## Checks supporting the principal arguments

- Destination disaggregation uses the **head** probability correctly. At a pool, its incoming total and quality mass acquire the same multiplier, while the recursion gives the same outgoing total. Its served product retains every original incoming arc and therefore its original quality. Summation is exact on every positive arc. Coordinatewise domination preserves every arc, input-withdrawal, pool-throughput, and product-delivery upper capacity. Zero lower bounds and the absence of intermediate specifications are essential and are stated.
- The single-product LP retains all capacities. Summing pool mass-quality equations, including bypass terms at products, gives exactly the aggregate input-quality mass. Topological reconstruction establishes sufficiency for the same **arc flow**, not merely for some alternative routing. At zero delivery, acyclicity eliminates all positive flow. Rational reconstruction has polynomial bit length by the triangular linear system argument.
- Both cost chains have the correct directions for minimization with nonpositive optimum. For an optimal physical flow, the cheapest of the `m` feasible components costs at most `z*/m`. For an optimal destination LP flow, the cheapest component costs at most `z_rel/m`, and it individually respects capacities because the sum does. Neither inequality assumes that every component has negative cost.
- Shortest-path mixtures preserve aggregate source withdrawals and product quality. All retained upper capacities can be satisfied by one positive rational scale. Active coordinate-quality rows have rank at most `K`, yielding support at most `K+1`. This bound is on paths used in the witness, not on path lengths or pool count.
- The uncapacitated conic hull follows from disaggregation, scaling, and finite conic combinations. The stated capacity-reimposition counterexample respects the feed, outlet, input, product, and common-pool bounds and separates the two sets as claimed.
- For cycles, a terminal active pool SCC without a product outlet has no external positive inflow by conservation and is isolated. Remaining components absorb at products; the backward reconstruction matrix is transient whenever its SCC has external inflow. The isolated circulation summand can be merged into one product component without breaking mixing or domination. Negative cycles supply profitable circulations under the explicitly chosen steady-state semantics. Removing nonnegative-cost cycles from an ordinary path/cycle decomposition preserves source withdrawals and product deliveries.
- The facial characterization, nonfacial counterexample, recognition LP, support enumeration, and fixed-dimension face counting are mathematically sound under bounded-flow conventions. Omitted positive-lower-bound arcs are explicitly handled as infeasible branches.

## Verdict and limits

**Verdict: major findings present**, because the endpoint special case lacks an essential quality-bound restriction. No mathematical defect was found in the destination, single-product, sign, approximation, or conic-hull arguments under finite upper capacities.

This was a proof and statement review of the entire first section. It does not verify the later sections, completeness of the entire repository-to-paper coverage, publication priority, all bibliographic metadata, or compilation. Local primary-literature extracts were spot-checked for the one-product approximation attribution, but this was not a comprehensive literature audit. No numerical tests were needed for these symbolic arguments.
