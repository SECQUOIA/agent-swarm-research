# Numerical companion

This archive supports the numerical chapter of *Quadratic hulls on boxes:
valid inequalities and semidefinite representability*. It contains the
archived outcomes used in the paper, a small record inspector, and snapshots
of the implementations. No optimization experiment was rerun when the
manuscript and this archive were prepared.

Run the record inspector from any directory with Python 3:

```bash
python /absolute/path/to/companion/inspect_records.py
```

The inspector uses only the Python standard library. It checks the SHA256
hashes of copied sources, reconstructs all 334 rows of the chain, cactus,
and hard-tree comparison tables from their JSONL records, reconstructs the
109-objective gap-closure table, and recomputes the strict-audit gain
sensitivities. It imports no archived modeling module, generates no
instance, and solves no model. Add `--write` to export the reconstructed
tables to `tables/*.csv`; this writes reporting files only.

`source-manifest.json` records each byte-identical copy's original repository
path, byte count, and SHA256 digest. Its `derived_summaries` entries identify
the inputs and input digests for the compressed small-dense campaign
summary. Those original 30 campaign files are not bundled. The manifest
establishes file provenance and detects altered copies; it is not a proof
that a solver output is correct.

The compact archive includes:

- The core conic models, separator, drivers, and instance generators in
  `code/`, as snapshots of the archived research implementation.
- The 109 hard three-variable objectives and the sparse objective data for
  the constructed comparison instances in `data/`. Constructed-instance
  JSON files store the upper triangle of `H`, the linear vector `g`, and
  construction metadata. Their objective is `x.T @ H @ x + g.T @ x`;
  each stored off-diagonal `H[i,j]` is therefore half its full polynomial
  coefficient. Each line of `pool_hard3.jsonl` instead stores a dense
  `3 x 3` matrix `H`, `g`, and a constant `c0`. Its archived hard-objective
  values include `c0`. The same constant is added to every method and
  cancels in gap and closure comparisons.
- Per-round records for the 16 chains, eight cacti, and eight hard-tree
  instances, the separate chain `XF` runs, and selected SCS comparisons in
  `logs/`. Each `safe` field is the archived floating-point dual-residual
  correction. Each `pobj` field is a primal diagnostic, and `pinf` is the
  solver's reported primal infeasibility.
- The feasible reference-value records, 99 benchmark baseline summaries,
  original benchmark audit summaries, the one completed stricter audit,
  the AP-variant exception, and summaries of additional three-variable
  searches. Full moment arrays, depth arrays, and benchmark instance files
  are not duplicated.
- Existing full and compact Markdown tables, reconstructed CSV tables,
  and a compressed summary of all 30,000 small-dense outcomes. The summary
  reports the two generators separately and retains the single AP-variant
  gap.

For a minimization problem, the reported closure is
`(method_safe - B_safe) / (U - B_safe)`. On constructed instances `U` is
usually the best feasible reference, rather than a proved optimum. A
Gurobi record marked optimal met its requested numerical gap tolerance;
it is not an exact certificate. In the hard three-variable table, the
reference is `X_safe`, because the tetrahedral formulation is exact in
theory. Numerical accuracy still affects that reported value.

A method's `round = 0` record contains its starting solution before its
first strengthening solve. Cumulative solve time therefore sums all its
records after the first; the baseline includes all baseline solve records.
For `KAF`, `KAFc`, and `KAX`, the comparison table adds the preceding `KA`
stage's solve time and rounds. Separation time sums the method's own
recorded separation intervals. It does not include the preceding `KA`
stage for those combined methods. Model size is taken from the last
record. The matrix-entry count is the sum of `k*(k+1)/2` over PSD blocks,
including baseline blocks; it is not their matrix order.

The five tetrahedra in `relax.py` define the exact comparator actually
used. A lifted triple adds five `4 x 4` DNN blocks, thirty off-diagonal
nonnegativity constraints, and ten linking equations. A family orientation
adds one `5 x 5` PSD block and six nonnegative auxiliaries. `F` selects
orientations by the simplex minimum over 15 supports. `XF` uses this same
selection rule for an exact lift; their different iterates can select
different triples. `K`, `A`, `KA`, and `X` instead select triples by the
full cube-hull depth test. `K` identifies shared higher monomials across
triples, so the paper's bound for independent triple-local systems does
not apply to that implementation.

The archived settings are Clarabel 0.11.1, one thread, and gap/feasibility
tolerances `1e-8` in the principal comparisons; full three-variable
comparisons use `1e-10`, and hull-depth subproblems use `1e-9`. Selected
cross-checks use SCS 3.3.1 at `1e-5` or `1e-6`. Reference global solves use
Gurobi 13.0.2, one thread, `NonConvex=2`, a requested relative gap `1e-6`,
and usually an 1800-second limit. The precise per-run outcomes are retained
in the logs. The original NumPy, SciPy, and Python versions were not
recorded. The source snapshots use these packages in addition to the
solvers, so this archive does not claim a fully pinned original software
environment.

Ordinary constructed-instance comparisons can be run from `code/` using
the bundled objective JSON. For example, the original driver interface is:

```bash
python driver.py --json ../data/chain_m300_e0.3_s1.json \
  --methods F,X,KA --max_rounds 25 --log /tmp/new-chain-comparison.jsonl
```

This command solves models; it was **not** run in preparing this archive.
It requires NumPy, SciPy, Clarabel, and, when requested, SCS. Use a fresh
output path because the driver overwrites its log. The larger chain
comparison uses `--cap 1000 --max_rounds 15`. Full reference-value
reproduction also requires an available Gurobi executable and license.
The archived global-solver wrapper with machine-specific installation
and license paths is not bundled.

The full original campaigns require additional inputs and outputs not
included here: published BoxQP instances; the original benchmark moment
and depth arrays; complete small-dense and large sampling records; and
the original workflow's environment and launch settings. The source
manifest gives their repository provenance where they support a compressed
summary. This archive is sufficient to inspect the paper's constructed
tables and core implementation, but does not by itself reproduce every
benchmark audit or sampling campaign. Published source papers and other
external literature files are excluded.

Treat the mathematical and numerical contracts separately. Near-singular
support systems are skipped in the floating-point separator. The words
“exact,” “certify,” and “safe” in some preserved research-code comments
describe the intended mathematical routines, rather than interval
certification of their outputs. In particular, the strict benchmark audit
contains computed depths that are not one-sided bounds. Its 0.045% gain
expression is a diagnostic. The 0.60% sensitivity figure assumes a
`1e-7` upper bound on depth overestimation, and reaches 1.10% after adding
the primal-to-dual margin; neither that depth-error bound nor exact
baseline feasibility is certified. Only one strict all-triple benchmark
audit was completed.

Timing records are wall clock on a shared 36-core machine under varying
load. Chain `XF` and `F` comparisons cross separate runs; cactus comparisons
are within an invocation but remain subject to changing load. Solve-time
ratios also reflect different selection rules and selected sets. The
archive measures root relaxations and supplies no evidence of a global
solver speedup.

## Public export

This public copy contains privacy and redistribution edits. Current package hashes describe the exported files; `original_sha256` records identify the original committed bytes when an exported file changed. Historical experiment and review hashes remain provenance records. Scientific result values were retained, and the experiments were not rerun. Repository-level `THIRD_PARTY_NOTICES.md` records licenses for retained third-party material.
