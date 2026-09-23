# Reproducible network--simplex comparisons

Run the manuscript experiment from the repository root:

```sh
PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06 \
  --output paper-network-simplex/verification/stage06-benchmarks.json
python paper-network-simplex/verification/stage06-tables.py
```

Defaults give five repetitions after one recorded warmup per case, with method
order rotated. `--quick --repetitions 1` is a smoke test. JSON retains versions,
platform/thread settings, warmups, raw min/median/max timings, and audit times.
The host is not isolated. CSR bytes exclude solver and peak process memory.
Component medians need not add to the median total. Decomposition-inclusive
queries are timed independently from membership-only queries; their difference
is not reported as isolated recovery cost.

## Methods and controls

`strong_baselines.py` implements vectorized sparse full/global-label-merged
disaggregation, fixed-y independent network optimization, and positive-state
point membership. Optimization retains all original y coordinates and costs.
Extra original-coordinate rows are mapped into each relevant formulation.

The legacy full membership baseline already treated x,y,z as data. The new
baseline removes only exactly zero states, uses block sparse assembly, and
distinguishes status 2 from solver failures. With two positive states, a
one-flow baseline uses f and x-f with intersected bounds and observations.
One positive state is checked directly. LP membership is numerical; aggregate
balances use tolerance `1e-9`. Zero-weight and bound consistency checks use
exact input arithmetic.

Fixed-y linear optimization without coupling separates into one network LP per
observed label plus the common unobserved cost. This baseline is included.
The aggregate-budget case compares equivalent relaxations H intersected with
a budget, without claiming the convex hull of the constrained product graph.

The all-labels-observed ablation has 16 blocks, three length-two paths per
block, four disjoint labels per block, 64 global labels, 111 arcs, and 192
observations. Global merging cannot help. Initial/eliminated variable counts
are checked as 495/367, versus 7,279 for full or global disaggregation.

Flat cases have lengths 8,32,128,512, weights `(1/2,1/2)` and `(1/3,1/3)`,
and feasible or McCormick-feasible infeasible points. Comparators are the new
and retained unreduced exact oracles and stronger LPs. Initial/eliminated
general models are also measured at lengths 8 and 32. Old larger-length
compressed comparisons remain available in their historical JSON.

The stronger LPs overturn the former 512-gadget boundary-face speedup. Interior
cases differ and some have wide ranges. Global merging explains much of the
old many-label gain; the all-labels-observed ablation isolates local compression.
No persistent callback, industrial data, or production-solver gain is claimed.

## Verification and historical data

```sh
PYTHONPATH=code python -m unittest network_simplex_benchmarks.test_strong_baselines -v
```

Tests compare with the unchanged legacy EF on arbitrary small multigraphs,
nonzero y costs, fixed/free weights, zero states, observation conflicts, and
aggregate budgets. Injected solver failures must raise rather than count as
infeasibility. Exact witnesses/cuts and numerical support audits are labeled
separately and checked outside timed runs.

Earlier `baselines.py`, `run.py`, `repeats.py`, `flat_repeats.py`, and result
JSON files remain unchanged. Pre-upgrade copies and hashes are in
`paper-network-simplex/verification/reference/stage06/`. The new runner loads
the retained flat oracle explicitly. The old flat runner importing current
production code would no longer reproduce the old algorithm; use the snapshot
to reproduce historical comparisons.
