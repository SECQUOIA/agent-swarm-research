# Independent audit of the compressed network–simplex implementation

Date: 2026-09-07. Reviewer: independent `literature` subagent.

## Scope and verdict

The core rational assembly in
[model.py](../code/network_simplex_compressed/model.py) and the verified-cut
recovery in [certificate.py](../code/network_simplex_compressed/certificate.py)
pass this audit for bounded rational input with integer graph/state indices.
The proof of the compressed formulation was checked against the implementation,
including signs, multigraph blocks, self-loops, unobserved states, infeasibility,
and reconstruction of global state flows. The later observation-rank elimination
also passes; its additional review is recorded below.

The assembly is exact rational arithmetic. Optimization, membership, and the
phase-I search use floating-point HiGHS. Only returned cuts are verified exactly;
the implementation does not certify feasible membership in exact arithmetic.

## Mathematical and implementation checks

The iterative Tarjan implementation skips only the actual parent edge, so
parallel edges are correctly retained as back edges. Self-loops are independent
rank-one blocks. The DFS subtree reference obeys incoming-minus-outgoing
balances; component imbalance adds an inconsistent row. Negative capacities
also produce explicit infeasibility rather than invalid numerical bounds.

Within each cyclic block, every chord has its own unit row. Tree return paths
produce a fundamental-cycle matrix. Normalizing the first nonzero sign and
grouping equal rows is valid because these arcs carry equal signed circulation
deviations. This may merge more than visibly degree-two paths, which is sound.
The strongest lower and upper bounds in each group retain all arc bounds.

Each observed state's auxiliary vector has scaled group bounds. Residual rows
subtract all explicitly retained states from a representative original arc,
including the reference term with the correct sign. Since equal normalized
rows denote the same circulation expression, representative arcs suffice.
Observed bridge equations reduce to z_ej=v_e*y_j. Bounds and equations force
zero-weight state deviations to zero, including cases where the reference lies
outside the capacity box.

The cut recovery includes all bounds and both signs of equality rows. It
rationalizes numerical nonnegative dual multipliers, checks nonnegativity and
exact cancellation of every auxiliary column, and checks strict violation in
rational arithmetic. Its RREF repair repeats those checks. Multiplier
normalization is not needed for validity; nonnegative combination and exact
annihilation suffice. The final `Cut` convention has positive evaluation at the
separated point, with the constant equal to minus the combined right side.
Failure to recover an exact certificate remains explicit.

## Verification actually run

The canonical check

```sh
PYTHONPATH=code python -m network_simplex_compressed.verify
```

passed 300 full-EF objective comparisons, 379 membership comparisons, and six
degenerate models in the first rerun. The final rerun after observation
elimination and the input-validation repairs passed **600 objective comparisons,
758 membership comparisons, and 476 exactly verified Farkas cuts**, with every
cut also checked by independent full-EF optimization, plus six degenerate models.
Both retained and eliminated formulations are included in these final counts.

I separately ran 40 random rational-witness checks with seeds 1000–1039,
nine vertices, 28 arbitrarily oriented arcs (allowing loops and parallels), five
simplex labels, and independently shuffled sparse observations. For each graph,
six feasible integral state flows were obtained from independent original
network LPs; their rounded values were checked exactly against capacities and
integer balances. Weights were (0,1,2,3,4,5)/15, so a zero state and a nonzero
residual state were both exercised.

- **13,464 assembled rational rows** were checked exactly at their explicitly
  constructed convex-combination witness, including auxiliary chord deviations.
- **40 numerical compressed solutions** were converted back into all six
  complete state-flow vectors. Aggregate x, each state's balances and scaled
  bounds, and every observed z were checked independently within 1e-7.
- **40 returned certificates** were independently recombined from their stored
  row indices and rational multipliers. Nonnegativity, exact annihilation of
  auxiliary columns, and exact positive separation were rechecked outside the
  implementation's certificate validator.

All checks passed. Numerical agreement and sampled witnesses support the code
audit; they do not replace the general mathematical proof.

## Issues raised during review

The author had identified and repaired `y_fixed` accepting negative or
above-one weights by replacing original bounds. The inspected repair rejects
those values; weights whose sum exceeds one remain excluded by the simplex
row.

Two further observations were sent to the author and repaired:

1. Scanning the complete observation list inside every block introduces
   O(number-of-blocks times |O|) work. Pre-indexing observations by edge avoids
   this. The final code uses `observed_by_edge` and each block's own observations.
2. Observation indices had range checks but no integer-type validation. A
   fractional arc/state index should be rejected at the API boundary. The final
   code checks integer or NumPy integer types as well as index ranges.

These did not invalidate the assembled hull on valid inputs. No unresolved
correctness issue was found in the final inspected implementation.

## Additional audit: observation-rank elimination

The optional `_eliminate_observed` method only pivots on auxiliary cycle
coordinates. Original x,y,z columns are never removed. Each pivot is free before
substitution, so deleting its variable bounds loses no constraint. Its defining
observation equation is retained through substitution; dependent observations
continue to impose their original-coordinate consistency equations.

Previously selected pivot expressions are reduced when a new pivot is chosen.
Consequently every final expression contains only retained coordinates, which
justifies the method's single-pass global substitution. States and blocks use
disjoint auxiliary columns, so combining their substitutions introduces no
cross-block dependency. Constant rows expressing infeasibility are retained.

The number of eliminated pivots is the rank of the observed cycle rows. The
remaining auxiliary count was also checked against the independently computed
cycle rank of each unobserved subgraph by the final verification script. That
script checks unit auxiliary coefficients after elimination. The exact-rational
row assembly and certificate checks still apply after substitution.

`Block.offsets` deliberately names the pre-elimination cycle coordinates;
`retained_variable_map` names the final LP columns. The method documents this
distinction. Consumers reconstructing state flows must account for elimination.
The numerical timing field `assembly_seconds` measures conversion and solve
preparation inside `optimize`, not constructor preprocessing; benchmark reports
must include constructor time separately when comparing total assembly cost.
