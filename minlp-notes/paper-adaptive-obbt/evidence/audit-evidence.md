# Archived experimental evidence audit

## Corrections that must enter the manuscript

The September report's Section 0 supersedes several unchanged statements in its
body. The stored CSVs also preserve the older counting rule. In
`results/final_outcomes.csv`, `solved=True` does not exclude `wrong=True`.
Reading these flags directly gives the following corrected counts among the
678 instance–seed pairs; this audit did not rerun any analysis or experiments.

| Solver | Default | Control | r1 | r5 | ad0.5 | ad0.8 | fp |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gurobi | 640 | 642 | 637 | 638 | 637 | 637 | 637 |
| SCIP | 575 | **573** | 570 | **563** | 570 | 571 | 561 |

The two excluded SCIP rows are `crudeoil_lee1_05`, `pipe-none`, seed 1
(primal -79.35000041494852), and `crudeoil_lee1_09`, `pipe-r5`, seed 1
(primal -79.35000057866084). Both carry `wrong=True` and `solved=True` in the
archived CSV. `arm_tables.csv`, `analysis_output.txt`, and the report's main
solver table retain 574 and 564. They are archived unchanged for provenance;
the manuscript must use 573 and 563.

Corrected solved counts do not retroactively correct the stored time or node
summaries. The original summary rule still counts these wrong runs as successful
for time and paired-node metrics. A manuscript quoting the archived September
ratios should identify them as originally reported descriptive summaries, or
avoid detailed ratios for the affected arms; no corrected timing analysis was
executed or claimed here.

Other explicit review corrections:

- Round 1 tightens at least one bound on **239**, not 241, of 339 instances.
- Direct saved-history inspection **supersedes the archived review's 23**
  one-productive-round convergence claim. Exactly **22** trajectories have a
  productive first round followed by a **completed** zero-change second round.
  A 23rd (`qspp_0_10_0_1_10_1`) has a capped zero-change second round, which
  does not establish completion. These are numerical no-change events, not exact
  fixed-point certificates. Of 104 one-entry histories, **97** completed their
  first round with no change, **three** were capped with no change, and **four**
  were capped with changes. Thus “100 no-change” and “seven capped” overlap in
  three; they do not form a partition or count productive convergence.
- The corrected one-round stopping fraction for `ad0.8` is **46–54%**; its
  at-least-five-round counts are **32/19/22** for known/Gurobi/SCIP cutoffs,
  rather than 30/18/21.
- The independent review corrects integer-only first-round OBBT time totals to
  **12,981 of 14,115 seconds** (about 92%), not 4,976 of 5,457 seconds (91%).
- The 149-instance contraction histogram is conditioned on at least four moving
  rounds. It excludes fast trajectories and cannot show that stalls or cutoff
  floors are typical across the cohort, or distinguish those mechanisms.
- The statement that hard-instance node ratios against the control lie uniformly
  between 0.96 and 1.1 is false: SCIP `ad0.8` gives 0.87 overall and 0.78 where the
  box changed, according to the archived independent review.
- Some September Gauss–Seidel/Jacobi and filtering box-comparison counts depend
  on a tolerance and on code not saved in `analysis.py`; they are not a fully
  reproducible primary claim. Keep their limited status explicit if retained.

## Scope and interpretation

September is an external preprocessing/restart study: 339 nonconvex MINLPLib
QCQPs in 85 historical families, two seeds, 600-second total budgets, Gurobi and
SCIP, root-incumbent cutoffs, and distinct known-optimum reference trajectories.
The known-optimum arm is an oracle diagnostic, not a realistic policy. September
feasibility/optimality checks are numerical, not exact MINLP proofs.

October is a separate prospective integrated-policy comparison: 12 selected
public problems plus eight synthetic stress problems, two seeds, three arms,
120 attempts, and 10-second inclusive call limits. Public admission uses only
historical September outcomes and a deterministic family-capped ordering. The
public cohort is a selected challenge set, and historical labels still separate
related packing applications. Two seeds do not create independent families.
All arms retain native SCIP LP-based OBBT; fixed/adaptive add a local sidecar.

October empirical policy applies coefficient/width ranking, current-LP witness
screening, a two-direction pilot, and node/incumbent/domain retriggering. It does
not implement all-future protected-box closure or matrix-tail certificates.
The exact rational reference certificates/driver are a separate implementation
for their explicit lifted relaxation family. They do not certify native SCIP
rows, incumbent feasibility, or an entire MINLP solve.

## October transcription checks

Saved `summary.json` agrees with the report's all-run table:

| Policy | Solved | Mean PAR-2 (s) | Process shifted mean (s) | Mean gap score |
|---|---:|---:|---:|---:|
| Native | 14/40 | 13.85512752259965 | 5.956665002193501 | 0.20351221668621844 |
| Fixed | 14/40 | 13.988117750101447 | 6.284634040148177 | 0.1843805157320931 |
| Adaptive | 14/40 | 13.996928299700084 | 6.264773731872334 | 0.18806112462003616 |

The public stratum has 2/24 solves per arm; synthetic has 12/16. No additional
arm has a new or lost solve. Fixed/adaptive directional LP counts are 2,172/1,719
(a 20.9% reduction), sidecar times 19.529969016759424/23.123433156462852 seconds
(an 18.4% increase), callbacks 404/741, accepted bound changes 112/308, and
nonroot callbacks 300/639. The adaptive screen removes only two directions;
574 callbacks stop after an unproductive pilot. More accepted bounds and fewer
LPs do not demonstrate a net solver benefit.

Mean PAR-2 includes all 40 runs: full process time for valid numerical success,
20 seconds otherwise. The shifted mean has shift one second and includes full
uncapped process cost. Capped metrics are diagnostic. The all-run gap score is
capped at one and assigns one without a valid incumbent and a finite consistent
dual bound. Only 39 native/additional pairs have comparable finite gaps;
adaptive improves four and worsens twelve by more than 1e-4. These denominators
must stay explicit. One no-incumbent run occurs per arm, and all 117 returned
incumbents pass the declared numerical checks.

Shared-machine load and short budgets prevent a claim of statistically
established slowdown from these timing differences. The supported conclusion
is fewer LPs, no additional solves, and no demonstrated overall speedup in this
selected short-budget campaign.

## Packaging and verification

The companion preserves byte-identical original source and results under their
repository-relative paths. It includes the complete October campaign and frozen
inputs, original protocol, exact reference source and saved checks, and
September code, review, reports, and the **entire September results directory**.
All 5,962 result files are included, including 4,589 tightened boxes, 377 FBBT
boxes, 640 root vectors, and 339 final vectors. The saved September analyzer's
input set is complete within the archive; its original success-count issue
remains documented and its source is unchanged.

The historical metadata catalog and probe pool are included at their original
repository-relative paths. Every OSiL file for the 377 archived candidate names
exists locally and is included. The relevant retained solution/cache files
comprise 409 solution files and 44 download-completion markers. Thirteen
candidate names lack a retained p1 solution, recorded in `SEPTEMBER-INPUTS.json`.
No missing files were downloaded or synthesized. Cache files are relocated
under `retained-inputs/september/`, with original cache-relative locations in
the manifest. The README explains explicit path redirection for validation
without editing the scientific source, the original setup script's absolute
metadata path, and solver/environment/license dependencies.

September metadata/cache files have no retained pre-campaign hash record.
Their packaged current bytes establish retained-input lineage, not evidence of
prospective source/input locking. The October freeze remains byte-identical;
every previously included source hash was checked before rebuilding.

The completed archive contains 7,128 original files (83,353,542 uncompressed
bytes) in a 10,162,415-byte gzip archive. `companion/MANIFEST.json` and
`evidence/companion-manifest.json` agree. There are no omitted September result
files and no omission inventory in the final package.

Checks performed during this audit are targeted reads of archived reports,
JSON and CSV, direct counting of `solved`/`wrong` flags, filesystem inventories,
byte/hash comparisons, and package inventory checks. No solver, numerical
experiment, saved analyzer, project-wide verification, or CI check was run.

Targeted commands actually run:

- `python` with a read-only CSV/JSON heredoc counted September `solved` and
  `wrong` flags: 573 control and 563 r5; identified the two wrong rows above.
- `python` with a read-only JSON/hash heredoc compared every October original
  artifact, frozen source and model digest against its archived declaration:
  zero mismatches, 120 scheduled tasks, 120 raw records, 120 logs. It read the
  339 known-cutoff September trajectories and counted 239 changed first rounds.
- `python` filesystem-inventory heredocs matched the archived 377 candidate
  names to the local OSiL/solution caches and recorded the exact input coverage.
  All 377 OSiL inputs are present; the retained p1 gaps and download-marker
  counts are recorded without performing downloads.
- `python` packaging heredocs compared previously included source hashes,
  retained every September result file, and created the archive and manifest
  with all relevant local metadata/cache inputs: original scientific sources
  were unchanged and no result file was excluded.
- `python paper-adaptive-obbt/companion/verify_archive.py`: passed; all 7,128
  archive members and four companion files matched their manifest digests and
  sizes. It reads bytes and executes no scientific code.
- `python` with a temporary-extraction/import heredoc imported `certificates`
  and `certified_driver` from the archive's preserved sibling layout: passed;
  no LP or scientific driver routine was called. Their preserved original
  bytes were unchanged in the expanded package.

These are package/evidence checks, not reruns of the archived mathematical
fixtures or numerical experiments. Future commands in the companion README
are documentation only. No CI status or logs were inspected.
