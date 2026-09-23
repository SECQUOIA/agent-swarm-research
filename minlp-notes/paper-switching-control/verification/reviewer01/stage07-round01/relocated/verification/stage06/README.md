# Exact computations and manuscript generation

`results.json` stores exact rational values as strings and descriptive timings
as floating-point seconds. `derived_public.json` stores exact integrated
masses for the 12-, 24-, and 48-cell public grids. The CSV is fetched from:

https://raw.githubusercontent.com/adbuerger/pycombina/6b073fe29984186dccfc7e2108bfba9692a6cc9c/examples/data/mmlotka_nt_12000_400.csv

Required SHA-256:
`1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883`.
No source data are fetched implicitly and no original literature PDF is bundled.

From the manuscript directory:

```sh
python verification/stage06/experiments.py --fetch
python verification/stage06/render_results.py --figures
python verification/stage06/check_results.py
python verification/stage06/render_results.py --check
```

The first script also accepts `--data PATH` (still hash-checked) and `--output
PATH` to retain a separate result run. Its accompanying `derived_public.json`
is written alongside the specified output. The renderer uses the archived
stage06/results.json; copy a deliberate replacement there to render a new run.
Only figure rendering requires Matplotlib. `--check` compares table/macro text
against the exact JSON without overwriting it.

## Mathematical checks and limits

The original decimal rates are normalized per cell and quantized by largest
remainders to denominator one million, with mode index resolving ties. All
row sums and nonnegativity are checked. The script verifies both the rate
bound and the actual cumulative perturbation; the manuscript uses the simpler
conservative bound delta=12/1,000,000. Normalization error relative to the raw
columns is a separate reported quantity. Fractions are parsed from decimal
strings, never from binary floats.

The fine-grid one-switch optimum is checked against all labeled one-switch
schedules by endpoint enumeration. The continuous optimum is computed from
all six exact affine crossings and independently evaluated at every fine
input knot plus the returned switch. Coarse schedules are expanded to the
original grid and their errors checked at every fine endpoint. Each public
M12/M24 optimum is corroborated by a separate labeled-word/boundary enumerator;
M48 uses the proved exact subset solver. All budgets0–3 are compared on each
fixed grid. The stage05 coarsener independently reproduces the M24/s2 general
certificate. Nested coarse boundaries make all intervals valid for both the
continuous and 12,000-cell optima. No dwell or transition restrictions are
imposed in these experiments.

Uniform n3/s2 continuous optimum1/6 is proved directly in the paper and checked
against all tested exact coarse optima. Every convergence point is corroborated
by separate full word/boundary enumeration. Controlled comparisons use the
same instance, objective, grid, and budget for both exact methods. Scaling
inputs are uniform, horizon1, and budget2. The deterministic heterogeneous
inputs for the controlled comparison are specified in both script and paper.

`check_results.py` works offline from the derived grids. It re-solves all
coarse cases, verifies the archived schedules (allowing different optimal
solver ties), checks interval endpoints and strictness, verifies the continuous
crossing routine on independent analytic examples, and reruns controlled and
uniform-convergence enumerations. It also checks stored fine/continuous summary
identities, but it does **not** claim to revalidate source-to-derived integration
or public off-grid crossings without the fine data: run `experiments.py` for
those checks. `render_results.py --check` validates generated table/macro text.

Timing values are medians of three fresh calls in one process. CPU and wall
samples, Python/platform/CPU identification, and timing boundaries are stored.
The solver timer excludes input construction, network retrieval, verification,
and plotting; it includes the solver's input validation. The machine is shared
and no CPU affinity/frequency controls are imposed. Timings are observations,
not reproducible constants or evidence of superiority over other CIA solvers.

The checked-in generated PDF figures can be used directly by LaTeX. They plot
exact data or formulas after conversion for display; no plot establishes a
mathematical claim. `source-record.md` records the primary-source audit.
