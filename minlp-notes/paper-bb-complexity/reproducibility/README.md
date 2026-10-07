# Archived computational evidence

This package contains recorded evidence for the accompanying branch-and-bound complexity manuscript. It was assembled on 2026-10-05 without rerunning solvers, synthetic experiments, or Monte Carlo trials. The outputs are trusted archived observations. New work checked file hashes, schemas, record groups, and arithmetic, and produced a static figure from recorded nodes.

Run the read-only verifier from any directory:

```sh
python3 /path/to/reproducibility/verify_archive.py
```

It needs only Python's standard library. It checks SHA256 digests, copied-file byte counts, required record fields, duplicate run keys, cohort sizes, all 176 archived solver fit groups, figure-record grouping, and eight selected MINLPLib node ratios against the archived rounded tables. It also checks the archived sparse C1 re-decisions, the three sparse rule exceptions, the 330 binary least-squares C1 decisions, and the corrected qflat2a leaves/bound ratio. It never imports or invokes SCIP and writes no files. `VERIFICATION-REPORT.json` records the package check results. Hashes detect changes; they do not certify the original solver's mathematical correctness.

`SOURCE-INVENTORY.json` maps every original repository-relative path to its copy, size, and SHA256 digest. Original files are copied byte for byte beneath `archive/`, preserving their relative paths and local imports. `SHA256SUMS` covers every package file except itself.

## Recorded studies

The three principal source directories lie under `archive/research-20260928b/bb-complexity/`:

| Directory | Evidence and protocol |
|---|---|
| `solver-validation/` | 2,134 SCIP runs on 20 synthetic instances; seed 0; eps from 1e-1 to 1e-7 in half decades; absolute-gap stopping, zero relative gap, feastol 1e-9, 100,000 nodes, 120 seconds. Each sequence stops after its first limit. `default`, `model`, and all ablations remain distinct. |
| `minlplib-branching/` | 57 selected MINLPLib instances; core 5 settings × 3 seeds = 855 runs at 120 CPU seconds; 171 optional seed-0 runs; 228 further tolerance runs on 19 small continuous instances. The retained archive has 1,254 records. With screening (486) and two diagnostic batches (171 and 16), the recorded total is 1,927. Only core runs enter the principal five-setting comparison. |
| `robust-branching-points/` | Separate MINLPLib study: 57 instances × 12 settings × 3 seeds = 2,052 runs at 60 CPU seconds. Parameter-only and external-branching-plugin settings are distinct. Synthetic SCIP evidence: 16 kink instances × 12 settings × 5 seeds × 4 tolerances = 3,840 records. `sim*.jsonl` are model simulation summaries; some summarize randomized trials, rather than exact rational counts. |

`spatial-face-exact/kink_exact_runs.py` and its logs provide exact rational kink counts. The robust directory also contains rational `exact2d.py`/`exact2d.log` and the archived recentring checks in `chain1d_D.log`. These relate idealized branching behavior to the practical studies without asserting that solver counts are certified.

`sparse-regression/{code,data}` and `sparse-regression/stronger-relaxations/{code,data}` retain random-design sparse regression generation, original arithmetic summaries, and raw records, including the 31 later C1 re-decisions. Decisions labelled `capped` in earlier raw files must be replaced by their records in `c1_redecided.jsonl` for the revised tables. `binary-least-squares/{code,data}` similarly retain the random MIMO root, C1, tree, threshold, and SDP archives and original summary scripts. Their recorded software stack is Python 3.13, NumPy 2.5, SciPy 1.18, Clarabel 0.11, and CVXPY 1.9 (1.9.3 for stronger sparse relaxations); larger sparse SDPs used SCS. These finite-size experiments do not measure the theorems' asymptotic constants. Internal review scripts and review logs are excluded; original generation and presentation code is retained.

SCIP 10.0.2, PySCIPOpt 6.2.1, Python 3.13.11, and SoPlex 8.0.2 are recorded in metadata; the MINLPLib studies record Ipopt 3.14.19. The machine was Linux WSL2 x86-64; MINLPLib metadata identify an Intel Xeon w5-2565X. The source exponent note is dated 2026-09-28, and branching studies 2026-09-29. These are documented study dates, not claimed timestamps for each file. Timing is specific to this machine and concurrent workload.

## Aggregation and interpretation

The original exponent analysis excludes `nodelimit`, `timelimit`, and `error`; it retains `optimal` terminations. Tail slope is the least-squares slope of log10 nodes against log10(1/eps) on the last five available eligible records with eps <= 1e-3. Wide slope uses all eligible records with eps <= 1e-2. At least three points and a log10 eps span of 0.99 are required. These are finite-window fits, not asymptotic extrapolations. Plateaus can result from exhausting the tree at the solver's numerical scale.

The `model` setting supplies a known optimum as incumbent, disables heuristics, and sets best-first order; ordinary propagation remains enabled. These changes were made together. The solver uses floating point and global gap stopping, so this setting is a controlled solver comparison rather than a rigorous certificate implementation.

MINLPLib node ratios aggregate with shift 10 over seeds and instances. Time uses shift 1 second, with unsuccessful runs assigned their time limit. Node-limit and time-limit runs retain their observed count. Bootstrap intervals use 5,000 resamples over instances, random seed 1; the Wilcoxon calculation is a two-sided normal approximation with tie correction. The first study averages whatever seed node counts are available after a crash. The separate robust study excludes a paired instance if any required seed lacks nodes. These rules are preserved in the original scripts and in the new arithmetic checks; the studies must not be pooled. The selected benchmark and its observed counts do not establish universal improvements or rigorous bounds.

## Figure and original scripts

`presentation/node-scaling.pdf` is a vector scientific figure; the PNG is a 300 dpi preview. `presentation/figure-metadata.json` records source SHA256, original line numbers, exact instance/setting groups, displayed observations, and archived fit metadata. Panels show optimal-set growth (`model`), flat growth (`model`), isolated minima (`model` and `default` separately), and branching-rule effects on an aligned McCormick instance. The tolerance axis is logarithmic throughout; node axes are logarithmic except panel (c), whose linear node axis shows additive growth per tolerance decade. For legibility, panel (c) omits the default iso4 series, whose counts reach 3,431. Squares mark `optimal` tree exhaustion; triangles mark node limits. Dotted lines show theorem powers with arbitrary vertical normalization. No records are pooled or averaged.

The new presentation can be regenerated from the archive alone:

```sh
python3 /path/to/reproducibility/plot_node_scaling.py
```

This requires NumPy and Matplotlib, produces presentation files, and copies the figure to the manuscript's neighboring `figures/` directory. It never invokes a solver. Regeneration changes presentation-file hashes, so compare or regenerate the manifest afterward if needed.

Original generation and analysis scripts are retained unchanged for provenance. They have different dependencies:

- Solver generation requires SCIP/PySCIPOpt; exponent instance evaluation uses mpmath; exponent analysis uses NumPy; bound integration and relaxation probes use SciPy.
- MINLPLib generation requires external OSiL models at the original cache path `~/.cache/minlplib/minlplib/osil`. Those models and solver binaries are not included. The copied selected list, job lists, metadata CSV, solution-value summaries, feature output, and repository OSiL parser identify the inputs used. The original parser's relative import path is preserved.
- The robust plugin directly loads the bundled PySCIPOpt SCIP shared library through ctypes and expects matching C API symbols. This is version-specific. Its original analysis imports the first study's analysis helpers through the preserved sibling directory.
- Exact rational kink scripts use the Python standard library. Other model scripts use mpmath/NumPy; the large simulation's original C source and driver are included, but no compiled program is included.

The copied `trace.jsonl` files contain small aggregate diagnostic records needed by the original analyses. Large raw solver traces, transformed SCIP models, solver binaries, external benchmark files, and internal review documents are excluded. Original analysis scripts may overwrite their own summary or fit outputs; the new verifier is the supported read-only package check. The archive contains evidence relevant to this manuscript and excludes the central decomposition experiments of the separate decomposition paper.

Targeted commands actually run during packaging: `python3 paper-bb-complexity/reproducibility/plot_node_scaling.py` and `python3 paper-bb-complexity/reproducibility/verify_archive.py`, plus standard-library read-only record counting and byte/hash comparison. All targeted checks passed. No project-wide verification or CI inspection was performed.

## Public export

This public copy contains privacy and redistribution edits. Current package hashes describe the exported files; `original_sha256` records identify the original committed bytes when an exported file changed. Historical experiment and review hashes remain provenance records. Scientific result values were retained, and the experiments were not rerun. Repository-level `THIRD_PARTY_NOTICES.md` records licenses for retained third-party material.
