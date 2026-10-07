# Independent final review of computational evidence

Date: 2026-10-05. Disposition: **pass for empirical accuracy, provenance,
and interpretation**, for the file versions pinned below. No remaining
empirical blocker was found. This review does not replace the mathematical
reviews of the preceding chapters or the root's standalone LaTeX build.

Only this review file was authored by this reviewer. The experiment author
made the manuscript corrections described below. No solver, instance
generator, Monte Carlo trial, or archived experiment was rerun. No literature
search, project-wide verification, or CI inspection was performed.

## Reviewed versions

Paths in this table are relative to `paper-bb-complexity/`.

| File | SHA256 |
|---|---|
| `sections/experiments.tex` | `455ef17d3c7ec4042e93d2b3d01f8e283813e6db9942c13debbdea17a5c47350` |
| `tables/empirical-protocols.tex` | `48b157ed6fae62f5c6733450341ae995af1b6546c07c5aa51a03665f04fabcd7` |
| `tables/empirical-branching.tex` | `d10dc8b4294c1683a114c00d7b6dd266bdd52b62c22851951d62fe0cff09e4bd` |
| `tables/empirical-finite-c1.tex` | `3eb71cec88973722abf01ece4a5463fa8152250c8f26df858447ef8cc4027fc8` |
| `figures/node-scaling.pdf` | `3eb3c03c8d569768896811073ebe53ab7adc9cefc57ec0e5619b51dece2dd54b` |
| `reproducibility/presentation/figure-metadata.json` | `22daf262fe84145697e4cab0fc7c8e0d01f52efecd5a805f1d14d6913933d8b9` |

The figure metadata's source hash was checked directly against the archived
`solver-validation/results/runs.jsonl`:
`3e79309ca7044082dae22358058f0f872192c53feba6ecfa0c55fff0cbddbaf4`.

## Scope and evidence

Read `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`,
`ISSUES.md`, `EXPERIMENT-MAP.md`, `ARCHIVE-PROVENANCE.md`, the reproducibility
README and verification report, and the figure caption and metadata. Checked
the manuscript and every table against actual retained records, relevant
original aggregation and generation code, and archived fits and summaries.
Actual data took precedence over summary prose where they disagreed.

Source paths below are relative to
`reproducibility/archive/research-20260928b/bb-complexity/`.

### Synthetic tolerance study

`solver-validation/results/runs.jsonl` has 2,134 records on 20 named
instances: 1,655 gap limits, 420 optimal terminations, and 59 node limits.
The stated half-decade tolerance grid, seed, absolute-gap rule, relative-gap
setting, feasibility tolerance, limits, epigraph construction, and combined
`model` changes agree with `run_one.py`, `sweep.py`, `instances.py`, and
recorded metadata. The synthetic expressions agree with the generator.
The source's Ipopt patch version is correctly described as unrecorded.

The recorded minimum incumbent error is
`-5.494292655980564e-9`, supporting the stated `5.5e-9` numerical caveat.
The figure includes 230 observations, 19 separate curves, and 14 distinct
instances. Every displayed source-line locator, tolerance, node count,
status, instance, and setting was checked against the JSONL record. The
preview is legible; the caption correctly explains guide normalization,
status markers, different node axes, and the omitted default iso4 series.

The sphere3 sequence 79, 747, 7,475, 76,699, the expanded ring2 count
37,439, and the aligned McCormick counts 3, 45, 10,469 match their exact
archived settings and tolerances. Default iso4 has 3,431 nodes at `1e-7`.
The default iso2/iso3 plateaus and the qflat1 model-versus-bisection slopes
match the retained records and fits. Reported model slopes and additive
nodes-per-decade values match `results/runs_fits.json`.

The manuscript now distinguishes one- or two-decade fit windows from the
two- or three-decade available sequences for the two-dimensional optimal
sets. Limit records are excluded from fits and exhausted trees retained,
as in the archived analysis. It does not interpret a numerical plateau or
a finite-window slope as an asymptotic certificate result.

Using only retained `thm_bounds.json` and recorded processed/open leaves,
the smallest eligible ratio is `1.5855475634370466` on qflat1. Seven
instances contribute. The model ranges independently recomputed are:

| Instance | Eligible observations | Minimum | Maximum |
|---|---:|---:|---:|
| iso2 | 13 | 6.8380012059 | 9.7758201228 |
| linediag2 | 12 | 15.8820837116 | 23.6543595021 |
| qflat2a | 13 | 6.7620917088 | 9.4054312661 |

These match the final rounded text, including all eligible half-decade
qflat2a observations. The text treats them as numerical consistency checks.
Processed nodes and final leaves remain distinct measurements.

### Selected MINLPLib campaigns and kinks

The first campaign's core is 855 records, `57 × 5 × 3`, at 120 CPU seconds.
Its records have 797 optimal terminations, 57 time limits, and one crash.
The additional accounting is correct: 171 optional plus 228 tolerance-sweep
records give 1,254 retained runs; adding 486 screening and 171 + 16 trace
records gives 1,927. The selected list contains 57 instances, 24 with
integer variables; five default diagnostic records have no continuous
branching. Selected screen times range from 1.02 to 19.29 seconds.

The separate second campaign has 2,052 records, `57 × 12 × 3`, at 60 CPU
seconds: 1,943 optimal, 104 time limits, five crashes. The synthetic kink
cohort has 3,840 records and the stated 2,024/1,816 gap-limit/optimal split.
All displayed per-setting termination counts match the records and have
denominator 171, even where paired ratios use only 56 instances. The two
campaigns are never pooled.

Independent arithmetic on the observed counts reproduced all nine displayed
paired ratios and bootstrap intervals, with the original instance ordering,
5,000 instance resamples, seed 1, and a shift of 10:

| Campaign | Setting/reference | Paired instances | Unrounded ratio | Rounded 95% interval |
|---|---|---:|---:|---|
| first | lp/default | 57 | 1.0334845283 | [0.83, 1.26] |
| first | lp_noclamp/default | 57 | 2.1848857998 | [1.43, 3.39] |
| first | mix_noclamp/default | 57 | 1.3483581917 | [1.03, 1.85] |
| first | mid/default | 57 | 1.1497611982 | [1.03, 1.28] |
| second | rclamp/default | 56 | 0.9629728376 | [0.87, 1.06] |
| second | lp/default | 57 | 1.0103973815 | [0.81, 1.21] |
| second | x_recenter/x_lp | 56 | 0.9389847623 | [0.86, 1.01] |
| second | x_recenter/default | 56 | 0.9226014681 | [0.71, 1.14] |
| second | x_noclamp/x_lp | 56 | 1.9993541449 | [1.43, 2.96] |

The midpoint p-value agrees with the original summary and the described
Wilcoxon approximation. The archive's seed-noise quantile rounds to 1.51
over 56 completed default triples. The complete-only no-clamp ratio is
`1.0843944619` on 41 instances. Missing-node handling, counts observed at
termination, multiple comparisons, selection effects, and the 10.0.3 source
versus 10.0.2 executable distinction are disclosed.

The diagnostic proportion was corrected from the source summary's erroneous
11/16 to **10/16**. Both `results/trace.jsonl` and `trace2.jsonl` support
ten instances with an LP-at-bound proportion between approximately 42%
and 100%. In trace2, the other six comprise one 14.7% proportion, four zero
proportions, and ex4_1_5 with no bounded continuous branchings.

The one-dimensional kink sequences, McCormick means of 7,190 and 21, and
random-clamp mean 766 with range 7–3,443 match the appropriate five-seed
cells. The latter's actual position is `0.010169169457068361`, correctly
reported as near `0.0102`. The exact rational log reports 19,537 at `1e-8`.
`spatial-face-exact/kink_exact_runs.py` increments its count for every popped
node, so the final term **processed model nodes** is correct. The stale
experiment-map word “leaves” must not be propagated. No rational script was
executed.

### Finite random designs

All eight sparse cells were independently checked after keyed replacement
of capped decisions by `c1_redecided.jsonl`. Sample sizes 55/64, 64/74,
72/84, 89/103 and pass counts 8/8, 8/8; 8/8, 8/8; 6/8, 8/8; 7/8, 8/8
match the table. All eight root criteria fail in every displayed cell.
The 31 replacements comprise 30 passes and one failure. The three rule
exceptions and their two rules' node counts match the raw rule files.

The stronger-relaxation comparison is correctly identified as a separate
`k=3` experiment with nested columns and the fixed `log(200)` ridge rule.
At n=20, the gap denominator uses the numerically enumerated global optimum,
which can differ from the planted-support value. After the archived filter
requiring relative perspective gap greater than `1e-4`, the four contributing
denominators are **7, 8, 8, 8**, and median closed fractions are
`0.5107707694`, `0.2537720062`, `0.1154809093`, `0.0327541028`.
These support 51%, 25%, 12%, 3%; omitting the filter would instead give
approximately 50% for the first cell. The n=40, p=3,200 records confirm the
six selected C1-optimal instances and four pairwise-hull inexactness witnesses.
The helper-column convention and selected-cohort limitation are stated.

The binary least-squares archive has 330 decided C1 records. All displayed
square-system fractions and denominators match `data/c1.jsonl`; all dashes
correspond to absent cells. The tall-system finite transition ranges agree
with the archive, with very small sample sizes. The planted box-minimizer,
some-vertex box-minimizer, successful rounding, root inactivity, and C1 events
are not conflated.

The tiny-root grid has 32 cells, each with 20,000 trials, on exactly the
reported N, beta, and rho values. The most-fractional geometric node means
at `rho=4 log N` are `43.69636`, `97.16257`, `508.98019`, `15764.99250`,
with 6, 6, 6, 4 observations; all finish. The four static N=256 records
are unfinished at 100,001 processed nodes after a nominal 100,000 budget,
so the manuscript correctly describes budget hits rather than completed
tree sizes.

The sparse condition `(log p)^6 <= n <= p` is stated with the correct
variable. Finite sparse and binary experiments are explicitly outside a
claim to measure asymptotic constants. Passing C1 is treated as a sufficient
certificate; failing it does not prove every search tree must be large.

## Corrections and final assessment

All reported corrections are incorporated in the pinned sources:
direct rounding of 2.1848858 to 2.18; 10/16 diagnostic instances;
one/two-decade fitted windows; optimal-set dimension terminology; and the
stronger sparse protocol, numerical OPT denominator, and 7/8/8/8 contributors.
The earlier processed-node correction for the rational kink is also present.
S6/S7 decomposition experiments are omitted from the empirical chapter and
portable archive, as required by the assignment.

The section is readable as a sequence of three finite computational
questions, with numerical limitations explained before the comparisons.
No theorem is inferred from fitted slopes, no broad solver recommendation
is made, and node improvements are not described as runtime speedups.
The reproducibility material distinguishes retained evidence from external
model files and solver binaries. No additional empirical integration request
remains for these versions.

## Targeted checks actually performed

Used `rg --files`, `rg -n`, `cat`, and targeted `sed -n` reads of the named
evidence, manuscript, and archived protocol/summary/code files. Viewed the
existing figure PNG with `view_image`; no figure was regenerated.

Ran standard-library `python3 - <<'PY' ... PY` read-only arithmetic blocks
to inspect record schemas, count cohorts and statuses, check selected node
examples, reconstruct revised sparse C1 cells, check BLS cells and tree
means, identify tiny-root grids, recompute filtered stronger-gap medians,
recompute nine paired ratios and their archived bootstrap convention, check
the seed-noise and complete-only cohorts, count diagnostic bound shares,
check leaf/bound ratios, and validate figure source hashes and record
locators. These blocks imported only `json`, `math`, `statistics`,
`collections`, `random`, `csv`, `hashlib`, and `pathlib`; they read existing
files and wrote no experiment output. All final arithmetic matched the
corrected manuscript. Intermediate discrepancies are recorded above.

Ran this exact final hash command:

```sh
sha256sum paper-bb-complexity/sections/experiments.tex paper-bb-complexity/tables/empirical-protocols.tex paper-bb-complexity/tables/empirical-branching.tex paper-bb-complexity/tables/empirical-finite-c1.tex paper-bb-complexity/figures/node-scaling.pdf paper-bb-complexity/reproducibility/presentation/figure-metadata.json
```

The package's existing verification report and documented verifier scope
were read; the verifier was not rerun by this reviewer. That report is
distinguished from this reviewer's direct arithmetic.
No CI result or project-wide check is claimed.
