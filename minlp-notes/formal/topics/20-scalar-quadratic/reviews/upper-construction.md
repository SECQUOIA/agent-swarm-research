# Independent review: signed-square upper formulations

Date: 2026-09-20. Reviewed `UpperAssembly.lean`, `UpperBounds.lean`, and
`UpperSquares.lean` independently of their author. Verdict: **PASS** for
the actual finite affine assembly, graph and full-epigraph containment,
error bounds, binary counts, auxiliary counts, and row counts.

This review covers the generic normalized signed-square construction.
Obtaining the normalized coordinates and exactly the nonzero spectral
terms from an arbitrary symmetric Hessian is checked separately in
[spectral-upper.md](spectral-upper.md). The scalar square and folding
blocks have their own independent reviews.

## Actual formulation and projection

`UpperAssembly.system` consists of a finite family of real affine maps.
It includes every original-domain row, every component row after an
affine substitution, and two output rows. In graph mode the output rows
impose equality with the affine term plus the weighted component outputs.
In epigraph mode they impose the lower output inequality and one zero
row. No upper output bound remains.

The component substitution uses the same original input in every affine
coordinate. The construction therefore does not assume that the normalized
coordinates are independent or that every point of their enclosing cube
is an attainable original input. `UpperAssembly.relaxation` proves both
directions of the existential projection characterization. Its reverse
direction packs all component witnesses into finite sigma-indexed code
and auxiliary arrays; it does not assume compatible component witnesses.
The component outputs have their own continuous auxiliary coordinates.
Each global binary bound follows from the corresponding component bounds.

The original domain is intersected with all component constraints.
`boxSystem` supplies exactly two inequalities per original coordinate,
including a fixed coordinate. No enclosing box in transformed coordinates
replaces the original input restrictions. An independent client checked
that an input outside a fixed original box cannot enter even when the
component index set is empty.

## Containment and errors

For the graph, choose the exact square output in every component. For
any admitted point, the output equality and the triangle inequality give
error at most `sum_j |c_j| * delta`. Cancellation among signed terms is
not assumed. The proof allows arbitrary real coefficients, including zero.

For the epigraph, negative coefficients use the binary square hypograph;
nonnegative coefficients use the continuous folding square epigraph.
`SignedEpigraph.componentData` packages the actual system together with
its dimensions, so the sign-dependent dimensions do not require an
assumed formulation or an arbitrary cast. `component_relaxation` proves
its exact branch semantics. In the negative branch, multiplication by
the negative coefficient reverses the square upper bound. In the
nonnegative branch, multiplication preserves the square lower bound.
Both give `c_j * (y_j^2-t_j) <= |c_j|*delta`.

Every original epigraph point lifts by taking exact component square
values and leaving the outer output above their weighted sum. Thus the
proof includes arbitrarily large output values, not just graph points.
Summing the signed error inequalities and using the outer lower output
row proves the error for every admitted point. A client checked the
contract with an arbitrary nonnegative output slack.

The assembly uses positive folding depth `L`, whose error is
`4^-L/4`, and negative binary depth `L`, with the same error. This gives
the advertised total bound `A*2^(-2L-2)`. The standalone stronger positive
block in I4 uses depth `L+1`, giving `4^-L/16`; that extra depth is not
needed for this total bound. The assembly does not claim the stronger
individual positive error at depth `L`.

## Exact resources and boundaries

For `m` supplied components, the graph uses `m*L` binaries,
`m*(3+2L)` continuous auxiliaries, and
`D.rowCount + m*(11+10L) + 2` rows. Each component contributes its square
auxiliaries and one additional output coordinate. If supplied a zero
coefficient, this generic graph constructor still allocates that
component; the spectral specialization chooses only nonzero terms.

The epigraph uses exactly `L` binaries for each strictly negative
coefficient and none for a zero or positive coefficient. Negative
components contribute `3+2L` auxiliary coordinates including their
outputs, and nonnegative components contribute `L+1`. Its exact row
count is

```text
D.rowCount + sum_j (if c_j<0 then 11+10L else 3L+3) + 2.
```

The proved uniform auxiliary and row bounds are linear in `m*(L+1)`.
The original box adds `2n` rows. Depth zero and an empty component set
remain valid. An independent client derived the exact affine graph with
zero error and zero binaries from the empty component case, and checked
that a zero coefficient selects zero binary coordinates at every depth.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.UpperSquares
lake env lean /tmp/Topic20UpperReview.lean
```

Both passed. The client checked the four boundary/containment contracts
above and printed axioms for the projection and feasibility equivalences,
both generic error theorems, both signed-square existence theorems, the
negative-bit count, the epigraph row count, and the graph auxiliary count.
Every printed list was `[propext, Classical.choice, Quot.sound]`.
No project-wide verification or CI inspection was performed. No reviewed
proof file was edited.

The source hashes were unchanged between the client-check start and end:

```text
UpperAssembly 3e1aa192b19565fbedbbd89719d68d7184922f4ba1b536b87ad05c8fc2023bf5
UpperBounds   9c74658f71ff1347bde089c9574bed4e0437b5bcc5b9a3d3df83ad861d199bd9
UpperSquares  81e0d06866af75492a670b66977f5e2ad66cb2c8c0797601abf1892d054cbd0f
```
