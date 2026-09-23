# Independent review of the graph-to-cut separator

Date: 2026-09-07. Reviewer: independent `review_separator` subagent.

**Verdict: pass for the stated parallel-path block class.** No mathematical or
implementation error was found. This review covers the implementation in
[`separator.py`](../code/network_simplex/separator.py), with SHA-256
`b3233e7196ddc6d8a06c68b2cebe2313ccc6b008a49088832d8d35ff2df34a46`, against the
[cycle/theta theorem](../results/network-simplex-cycle-theta-hull.md) and
[parallel-path theorem](../results/network-simplex-parallel-path-hull.md).
It does not establish novelty, optimized computational performance, or support
for general series-parallel graphs.

**Later input-validation addendum.** The independent flat-chain implementation
review found that observation index range checks alone admitted fractional
indices. The author added integer checks to both separator constructors. The
final `NetworkSimplex` SHA-256 is
`c7f5692d8f37c7681ebd9ba318b6778c25f58b0cf03a9cf666eb646a345bc395`.
The independent multigraph suite below was rerun after that change and passed
with the same results. No hull algorithm changed. See the
[flat-chain implementation review](review-network-simplex-flat-chain-implementation.md)
for the malformed-input regression and correction.

## Mathematical and implementation review

- The iterative edge-stack traversal preserves parallel arc identities. Its
  spanning-forest reference has incoming-minus-outgoing balance equal to the
  input balance, even when the reference violates capacities. Component balance
  sums and forced bridge capacities detect the corresponding infeasibilities.
- Nontrivial blocks are accepted only when they are internally disjoint paths
  between two terminals. Cycles are split into two paths. A loop is separated
  from the undirected traversal and has one independent scalar coordinate.
  Signs and path bound intersections implement the affine circulation map.
- Candidate flow bounds, flow balances, simplex constraints, and bridge products
  are checked before block separation. Once these hold, each aggregate path
  coordinate is well defined and non-scalar block coordinates sum to zero.
- Grouping retains all states observed in a block and one merged state. Every
  unobserved positive-weight state receives the same normalized block vector.
  Zero weights force zero state coordinates and are never divided. Different
  blocks may use different merged state groups without obstructing gluing.
- Active lower endpoint branches are affine lower bounds on the convex lower
  endpoint; active upper branches are affine upper bounds on the concave upper
  endpoint. The resulting state and aggregate cuts are therefore globally valid,
  rather than expressions that agree only at the rejected candidate.
- For two or three paths, tightened coordinate intervals supply the complete
  support family. The suffix construction retains feasible membership in the
  sum of the remaining state polytopes; its greedy column has zero sum and
  belongs to the current state polytope. Scalar loops use the interval case.
- For larger blocks, the nonnegative lower-shifted transportation instance has
  equal total row and column requirements. Exact Edmonds-Karp residual updates
  are correct. On failure, reachable rows determine a violated subset support;
  choosing the smaller state support and its active endpoints yields a globally
  valid original-variable cut. A saturated flow reconstructs the state matrix.
- Compact decomposition reconstructs the original flow, simplex weights, and
  every observed product. Every materialized positive-weight state flow obeys
  the original capacity and balance constraints.

The constructor sorts observations and state labels. Its implementation therefore
uses up to `O(|O| log |O|)` comparisons in addition to linear graph extraction;
the repeated cycle/theta separation call does not sort. This was communicated
to the implementation author and is now explicit in the README. It does not
change the mathematical linear-arithmetic oracle theorem, which need not sort.

## Independent executable checks

The review added
[`verify_separator.py`](../code/network_simplex_review/verify_separator.py).
It does not import the author's tests, benchmark baselines, block coordinates,
or private transportation routines. Run from the repository root:

```sh
python code/network_simplex_review/verify_separator.py
```

With seed `972451`, the checks cover:

1. **120 random multigraphs:** one to five attached or disconnected blocks,
   one to seven paths per block, random path lengths and orientations, rational
   capacities, feasible nonzero balances, bridges, loops, isolated nodes, sparse
   observations, repeated path observations, and zero state weights.
2. **426 candidates on those graphs:** true graph points and perturbed product
   coordinates. Membership agrees with a separately assembled full state-flow
   LP on every candidate. Every returned cut is maximized over the entire base
   flow polytope at every simplex vertex using an independent LP.
3. **240 additional hypersimplex models, 480 candidates:** unit-capacity parallel
   arcs with an integral total flow; graph points are mixed across different
   state flows. Alternative state profiles remain individually feasible, so
   rejection exercises aggregate coupling rather than local state infeasibility.
   Membership again matches the independently assembled LP. For each rejected
   candidate, global cut validity is checked **exactly** at every binary base
   vertex and every simplex vertex. Integrality of this cardinality-constrained
   box makes this a complete exact global-validity test for those models.
4. **550 accepted decompositions:** capacity bounds, balances, aggregate flow,
   and every observed product are verified with exact rational arithmetic.
   Rejected cuts have strictly positive exact evaluation. Their flow/product
   coefficient magnitudes are at most one.
5. **326 random domain violations**, plus a separate flow-balance violation,
   empty graphs, disconnected balance infeasibility, forced bridge infeasibility,
   negative capacities, rejection of K4, and rejection of a nested
   series-parallel block outside the implemented graph class.

There are 27 transportation-subset rejections, including 22 with exhaustive exact
global cut checks. The additional mixed-state family also exercises both lower
and upper aggregate support cuts in the fast two/three-path branch. The random
multigraph branch checks `decompose=False` against the constructive call.

Recorded output:

```text
{'aggregate lower support': 1, 'aggregate row lower bound': 2,
 'bridge observation': 28, 'feasible decomposition': 122, 'flow bound': 120,
 'hypersimplex aggregate lower support': 6,
 'hypersimplex aggregate row lower bound': 21,
 'hypersimplex aggregate upper support': 3,
 'hypersimplex feasible decomposition': 428,
 'hypersimplex transportation subset': 22,
 'simplex nonnegativity': 103, 'simplex total weight': 103,
 'state interval': 258, 'state lower sum': 3, 'state upper sum': 7,
 'transportation subset': 5}
PASS: 120 random multigraphs + 240 hypersimplex models; independent EF,
global cut LPs, exact vertex/decomposition checks; seed=972451
```

The full-EF comparisons and general-flow global maximizations use numerical
SciPy/HiGHS LPs, with a `1e-7` tolerance only for checking their objective values.
They are regression evidence, not exact LP certificates. Decomposition checks,
candidate cut violations, and the exhaustive hypersimplex global checks are exact.
The code review supplies the structural correctness argument beyond finite tests.

## Practical limitations to preserve in a paper

The separator consumes exact rational candidates. Decimal float conversion does
not repair solver residuals; a floating-point solver adapter needs a separate
feasibility and cut-rounding policy. The implementation is suitable for exact
experiments and correctness demonstrations but does not establish a competitive
production solver callback. Any time or memory advantage must be measured
against the full extended hull and the newly investigated compressed formulation.
Unsupported graph blocks are explicitly rejected. Additional linking constraints
can use these cuts, but exactness for their joint hull does not follow merely by
intersection.
