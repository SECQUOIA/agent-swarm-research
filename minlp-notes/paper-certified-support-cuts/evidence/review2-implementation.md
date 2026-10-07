# Review round 2, lens: implementation and protocol fidelity

Manuscript: "Certified support cuts for shared nonlinear expressions and
quadratic blocks" (`main.tex`, typeset text `development/draft-round2/main.txt`).
Date: 2026-10-03. Reviewer scope: Sections 6.3, 7, 8.1, Appendix G (Tables 6
and 7, selection rules) and the code and data availability statement, checked
against the campaign-4 code snapshot
(`experiments/v4/snapshot/research-20261003-convexification/`), the v3 and v3d
snapshots, the run records of every campaign-3, 3D and campaign-4 directory,
`evidence/implementation-facts.md`, the protocols (`campaign-v3-protocol.md`,
`campaign-v4-protocol.md` with Amendment 1, `mechanism-protocol.md`) and the
runner READMEs (`v3/README.md`, `v3d/README-diagnostic.md`, `v4/README.md`).

PDF page numbers refer to `main.pdf` as rendered in `main.txt`. Section
numbers: 6.3 Records and replay (pp. 19-20), 7.1 (pp. 20-21), 7.2 (p. 22),
8.1 Setup (p. 23), Table 1 (p. 24), 8.2-8.7 (pp. 23-31), availability
(p. 32), Appendix G (pp. 49-51).

## 1. Targeted checks actually run

All local, read-only on `experiments/` and `evidence/`, with
`/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python` and
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`. No SCIP or Gurobi
solve was run. No project-wide test suite and no CI status were used.

Pre-existing implementation-lens scripts, re-run (outputs quoted below):

| Script | What it checks |
|---|---|
| `verification/R9_impl_run_inventory.py` | modes, seeds, node and time limits, Config overrides (incl. `max_rounds`), SCIP and Gurobi parameters per run directory |
| `verification/R9_impl_load_concurrency.py` | load averages per part, concurrency per campaign |
| `verification/R9_impl_replay_summary.py` | every `replay.json`: passed flag, cuts replayed, 14 tamper controls per cut mode |
| `verification/R9_impl_allowance.py` | separator allowance overruns, soft-budget overruns |
| `verification/R9_impl_crosscampaign.py` | baseline root bounds, statuses, nodes: campaign 3 versus 3D reruns |
| `verification/R9_impl_root_full_funnel.py` | identical separator counters in full and root runs of the path family |

New scripts written for this review:

| Script | What it checks |
|---|---|
| `verification/R9_implementation_concurrency.py` | simultaneous runs within and across run directories (strict interval overlap) |
| `verification/R9_implementation_cut_methods.py` | support method and block dimension of every recorded cut |
| `verification/R9_implementation_block_cap.py` | how often discovery reached the 32- or 128-block cap |
| `verification/R9_implementation_affine_infeasible.py` | the 8 Part D pool models refused as `affine_infeasible`, with an exact recheck of the final contradiction |
| `verification/R9_implementation_kernel_coverage.py` | which blocks the frozen kernels certify (calls the snapshot `certify_support`) |

Inline read-only probes: 3D versus campaign-3 root bounds of Parts A and B;
per-part load distributions in campaign 4; identity of the frozen `Config`
across campaigns; recorded SCIP and Gurobi versions; total rounding
rejections; fields of `v4/c4-references.json`; `diff` of the v3, v3d and v4
snapshots; file timestamps of the protocol, the snapshot and the C4 code.

Housekeeping disclosure. The first runs of
`R9_implementation_affine_infeasible.py` and
`R9_implementation_kernel_coverage.py` imported snapshot modules without
suppressing bytecode and created three `__pycache__` directories (only `.pyc`
files) under `experiments/v4/snapshot/` (`code/univariate_envelopes/uenv/`,
`research-20261003-convexification/solver/`,
`research-20261002-convexification/solver/`). I deleted these three
directories; no source file, manifest or record was touched (the manifest
covers source files only). Both scripts now set `sys.dont_write_bytecode`.
A directory `experiments/v5/` appeared during the review; it was not created
by this review and was not examined.

## 2. What was verified and found correct

- Frozen `Config` (`integration.py:40-63`) equals Table 6, column
  "Campaigns 2-4": 32 blocks, 6 nonlinear and 16 affine sides, 2,000 subsets,
  3 root callbacks, 12 cuts / 4 per callback, 24 support calls, 3 exchange
  LPs, 128 cells, depth 16, allowance min(1 s, 0.05 T), thresholds 1e-5 and
  5e-4, grids 33 and 7, gap 1e-4. Every `all`/`auto` record of campaigns 3,
  3D and 4 carries exactly this configuration (one distinct value).
- HiGHS LP (`integration.py:329-335`): time limit 0.05 s, one thread, LP
  direction rejected unless the scaled objective is below -1e-5. Samples
  33 / 7x7 / 3^d plus exact vertices and centroid (quadratic blocks only).
- Polytope budget arithmetic of Section 7.2: with m = r + 2d, d = 4 allows
  r <= 7 (1,941 subsets; r = 8 gives 2,517), d = 3 allows r = 16 (1,794).
- `auto` rule (`integration.py:255-269`): quadratic block, a side whose
  Hessian is not proved PSD, and a domain row with two or more nonzero
  coefficients or two distinct source rows; stop after two failures.
- Safe export (`row_certificate.py:213-221`): compensation
  `min(e*lo, e*hi)` with both bounds required whenever the rounding error is
  nonzero, rhs rounded down; the paper's "more conservative" remark is right.
- Stored-row audit (`integration.py:343-367`) compares columns through the
  transformed-variable map, coefficients, constant, lower side, infinite
  upper side and scope; rows are created `local=False, removable=True` and
  added with `forcecut=True` (`integration.py:523-537`); separator `freq=0`
  and a depth check make it root-only.
- Replay (`experiments/replay.py`): verifies the snapshot manifest, the pinned
  OSiL hash and the model digest; re-runs `build_model` through
  `reviews/model_binding_audit.py:74`; replays the bound proof; rebuilds
  signed sides with its own splitter; re-runs `replay_support` and
  `replay_row_certificate`; compares the recorded stored row. The 14 tamper
  mutations (`replay.py:353-386`) are exactly those listed in Section 6.3.
- Replay outputs: all 13 run directories passed; 7,498 + 30,998 + 104,771 =
  143,267 cuts replayed; 14/14 mutations rejected for every cut mode of every
  part; Gurobi runs listed as omitted runs without cuts.
- Modes as recorded: SCIP parameter sets of `baseline-novarlocks`,
  `baseline-extra`, `*-noaggr` equal Table 7; Gurobi records carry
  `Threads 1, NonConvex 2, MIPGap 1e-4, Seed 0`; all SCIP records report
  SCIP 10.0.2, all Gurobi records 13.0.3; Python 3.13.11, SymPy 1.14.0,
  python-flint 0.9.0, SciPy 1.18.1, PySCIPOpt 6.2.1 (driver `sessions.jsonl`).
- Seeds, limits and rotation: Part A full seeds 0-2, Part B full seeds 0-1,
  root runs seed 0; soft limits 300 s (full), 60 s (3A, 3B, 3D-A/B, 4B2
  root), 120 s (3C, 3D-C, 4C2-4C4, 4D root); no process timeouts or worker
  errors in campaigns 3, 3D and 4.
- Code provenance: v3d `integration.py` differs from v3 only by the
  whole-row loop; v4 differs from v3 only by the documented `PATCHES`
  (`row_directions`, `scip_params`); no other snapshot file differs.
- Amendment 1 was in the protocol before campaign 4 started: the snapshot
  copy of `campaign-v4-protocol.md` (17:01:46 UTC) is byte-identical to the
  current file; the first campaign-4 run (Part D screen) started 17:08:56 UTC.
- No row was rejected by safe rounding (sum of `row_rounding_rejections` = 0);
  allowance overruns were at most 0.084 s; full and root runs of the path
  family have identical separator counters (Table 3 caption); every cut-mode
  run of the four path-family cells stopped at its cut cap.
- Host: 36 logical CPUs, 18 cores (Intel Xeon w5-2565X), WSL2.

## 3. Findings

### F1 (major). The diagnostic, mechanism and wide modes raise the number of root callbacks from 3 to 10; Appendix G says they raise only the limits in Table 7

Location: `sections/A-instances.tex:5-8` (p. 49) and Table 7,
`sections/A-instances.tex:50-59` (p. 51); `sections/07-implementation.tex:128-131` (p. 22).

Issue. The text says: "the other modes raise only the limits named in
Table~\ref{tab:modes} and set the allowance to $\min\{s,\,0.5\,T\}$". Table 7
has no column for root callbacks. Every `all-diag`, `all-diag-rowdir`,
`all-diag-mech`, `frozen-wide` and `rowdir-wide` run (and the 3D modes) used
`max_rounds = 10` instead of the frozen 3.

Evidence. `R9_impl_run_inventory.py`: "config max_rounds by mode:
('all-diag', 10) ... ('all-diag-mech', 10) ... ('frozen-wide', 10) ...
('rowdir-wide', 10)", and 3 for all other modes, in every directory. Source:
`v4/v4_worker.py:44-46` (`ALL_DIAG`) and `mechanism_limits` (`max_rounds: 10`);
`campaign-v3-protocol.md:49-51`, `mechanism-protocol.md:38-41`,
`v4/README.md:48-52` all list `max_rounds 10`. The setting is material: the
separator runs `max_rounds` callbacks (`integration.py:437`), so with 3
callbacks `all-diag-mech` (n cuts per callback) could add at most 3n < 4n
cuts and the wide modes 12n < 16n. Section 8.5's argument "every run of the
four cells stopped at its cut cap" depends on the undisclosed 10.

Fix. Add a column "Callbacks" to Table 7 with 3 for `all`, `auto` and 10 for
every other separator mode, and replace the sentence by: "The other modes
raise the limits listed in Table~\ref{tab:modes}, including the number of
root callbacks, from 3 to 10, and set the allowance to
$\min\{s,\,0.5\,T\}$ with the listed $s$."

### F2 (major). Up to ten runs of campaign 3 were active at once, not six

Location: `sections/08a-setup.tex:23-24` (Section 8.1, p. 23): "At most six
runs of a campaign were active at a time".

Issue. The post hoc diagnostic 3D, which Table 1 lists as a part of campaign
3, ran its Part C (4 workers) while campaign-3 Part A full (6 workers) was
still running. The v3d driver used its own slot directory (`v3d/.slots`), so
the six-slot limit of `v3/README.md` ("drivers running at the same time
together never exceed six workers") did not cover both. This also departs from
`campaign-v3-protocol.md` ("At most six jobs run in parallel") and from the
diagnostic's own rule ("Same instances, limits and hardware rules as Part C").

Evidence. `R9_implementation_concurrency.py` (strict overlap
`start <= t < end`): campaign 3 alone max 6; 3D alone max 6; campaign 4
max 6; campaign 3 including 3D max 10, at 2026-10-03 07:29:28 UTC (6 Part A
full, 4 3D Part C). Part A full ran 07:16:54-07:56:45 UTC, 3D Part C
07:28:36-08:00:28 UTC. 155 of the 270 Part A full runs overlapped a moment
with more than six of the project's runs active. `R9_impl_load_concurrency.py`
gives the same maximum (10). Driver code: `v3/driver.py:40` and
`v3d/driver.py:40` both use `SLOT_DIR = HERE / ".slots"`.

Fix. Replace the sentence by: "At most six runs of a part were active at a
time; the 3D diagnostic of the path family ran during the last 28 minutes of
Part~A, so up to ten runs of campaign~3 were then active (155 of the 270
full runs of Part~A were affected)." Keep "Timings are therefore descriptive".
The paired design (modes of one job back to back) still limits the effect on
mode comparisons; say so.

### F3 (major). The model builder refuses models whose affine rows are infeasible in exact arithmetic; eight benchmark models with known MINLPLib solutions were refused, and the paper does not say so

Location: `sections/07-implementation.tex:65-72` (Section 7.1, "Bounds", p. 21);
`sections/A-instances-D.tex:6-7` (Appendix G, p. 50).

Issue. Section 7.1 describes exact affine bound propagation but not what
happens when it proves a contradiction. The builder then refuses the model
(`model.py:298-299`, status `affine_infeasible`). In the Part D pool this
happened for 8 of 322 models, all of which have a finite primal bound in the
MINLPLib metadata, so they are feasible within tolerances. This is a direct
consequence of the paper's semantics (binary64 data read as exact
rationals) and bears on its applicability; a referee will want it stated. The
Appendix sentence "A discovery scan ... admitted 301 of them" also gives no
reasons for the 21 refusals (8 `affine_infeasible`, 7 unsupported input, 4
killed at the 120 s hard limit in `build`, 1 unsupported model, 1 unproved
variable-power domain) and conflates the 60 s discovery deadline with the
120 s hard limit.

Evidence. `v4/scanD/scan-summary.md` (refusal table) and
`R9_implementation_affine_infeasible.py`, which re-derives the final
contradiction of each chain in exact arithmetic:

```
hda                row 204 lower: minimum activity exceeds rhs by 1.67e-16
sepasequ_complex   row 316 lower: minimum activity exceeds rhs by 5.55e-17
sfacloc1_{2,3,4}_{90,95}  (6 models): 3 integer roundings, then a row
                   whose minimum activity 0 exceeds rhs -1 (excess 1)
```

MINLPLib primal bounds: hda -5964.53, sepasequ_complex 368.76,
sfacloc1_2_90 17.89, ... (from the snapshot `instancedata.csv`).
(The check of the last step trusts the earlier steps of the recorded chain;
the builder's own `replay_bounds` also accepted each chain.)

Fix. Add to "Bounds" in Section 7.1: "Propagation is capped at 8 passes and
10{,}000 steps. If it derives a contradiction in exact arithmetic, the model
is refused: under the exact reading of its binary64 data it has no feasible
point. This happened for 8 of the 322 models of the Part~D pool, all with a
known MINLPLib solution: on two, an affine row is violated by about
$10^{-16}$ at every point of the box; on six, a bound of an integer
variable lies just below an integer and its rounding leaves no feasible
value." In Appendix G replace "A discovery scan with a 120-second limit per
model admitted 301 of them" by "A scan of import and discovery (60-second
discovery deadline, 120-second process limit) admitted 301 of them; 8 were
refused as infeasible in exact arithmetic, 9 contained unsupported input or
an unproved domain, and 4 did not finish the import within 120 seconds."

### F4 (minor). "We compare modes only within such paired runs" is not true for Part 4C2 and for Table 8

Location: `sections/08a-setup.tex:24-25` (p. 23); `sections/08g-summary.tex:23-26`
(p. 31); Table 8, `sections/08e-path.tex:43-82` (p. 29).

Issue. Part 4C2 has, by protocol, no baseline of its own; its modes are
compared with the campaign-3 baseline and `all-diag-mech` runs
(`v4/README.md:103-108`, `summarize_v4.py` reference `c3:baseline`). In
Table 8 the "Solved" column of the block "seeds 0-4" mixes campaign 3 (load
14-21, up to ten concurrent runs, F2) with campaign 4 (load 3-8). Solved counts
within 300 s depend on time. Section 8.5 argues the point for the four
additional solves, so the issue is the setup's blanket statement.

Evidence. `R9_impl_crosscampaign.py`: baseline root bounds and statuses
repeat exactly between campaign 3 and the 3D reruns (40/40 path-family runs,
30/30 Part A root, 30/30 Part B root), but node counts differ in 11 of 40
path-family runs. So root bounds are reproducible across campaigns, and
time-limited outcomes are not paired.

Fix. In 8.1: "Within a part, modes run back to back in rotated order and are
compared within these paired runs. Part~4C2 has no baseline of its own and is
compared with the campaign-3 runs of the same instances; root bounds of
identical runs repeated exactly across campaigns (all 100 baseline root
bounds rerun in the 3D diagnostic), whereas solved counts and times are not
paired across campaigns." Add to the caption of Table 8: "In the block seeds
0-4, SCIP default and the remainder/mech. row are from campaign~3, the
post hoc rows from the 3D diagnostic and the other rows from campaign~4."
In 8.7 replace "we compare times only within paired runs of one campaign" by
"we compare times within paired runs of one part, except where stated".

### F5 (minor). Section 7.2 misstates which blocks can be certified and does not define the "required value"

Location: `sections/07-implementation.tex:80-91, 106-115` (Section 7.2, p. 22);
used in `sections/08d-funnel.tex:41-46` (p. 27).

Issue. (a) "A side is admissible if its remainder ... is either univariate or
a polynomial of total degree at most eight": the code rejects univariate
polynomials of degree above 8 (`integration.py:208-214`); the rule is
"polynomial of total degree at most 8, or nonpolynomial in one variable".
(b) "Polynomial remainders of degree three or more in three or four variables
... so such blocks yield no cuts" is both incomplete and partly wrong. The
kernels decide on the whole block: Bernstein needs a block of at most two
variables and ball arithmetic a block of one variable, and a nonpolynomial
feature blocks the polynomial paths even with weight zero
(`certified.py:143-145, 342-348`). So a block of two or more variables that
contains a nonpolynomial side yields no cut in any direction. Conversely, a
block with a degree-4 side can yield cuts from directions that give that side
weight zero. (c) For non-quadratic blocks the separator passes
`target = LP activity + threshold` (`integration.py:482`); the Bernstein and
ball-arithmetic subdivisions are refined only until the target is reached and
otherwise return *incomplete*. Without a target they return the coarse
one-cell bound. Section 8.4's "did not certify the required value" relies on
this undefined notion, and a "failed certification" for these blocks
includes rows that would not have been violated. (d) "only the star oracle of
Theorem~\ref{thm:star} can apply": the separator uses the simpler oracle
described at the end of Section 4.2, not the algorithm of the theorem.

Evidence. `R9_implementation_kernel_coverage.py` (snapshot `certify_support`,
cells 128, depth 16, budget 2,000):

```
A {x,y} with exp(x) side, weight on x*y only     unsupported (ball arithmetic needs one variable)
B {x,y,z} with degree-4 side, weight on x*z only complete, quadratic_polytope
C {x,y,z} weight on degree-4 side                unsupported (Bernstein: 1D/2D only)
D {x} x^4-x^2, target 0 (exact min -1/4)         incomplete
D' same, no target                               complete, rhs = -0.5 (coarse)
```

Fix. Replace lines 80-91 (from "A side is admissible") by: "A side is
admissible if its remainder involves one to four variables with finite proven
bounds and is either a polynomial of total degree at most eight or a
nonpolynomial expression in one variable. [...] The kernels apply to the
whole block: exact enumeration or the star oracle when the combined function
is quadratic, Bernstein bounds when it is a polynomial in a block of one or
two variables (at most 1{,}024 tensor coefficients), and ball arithmetic in a
block of one variable. A block of two or more variables with a nonpolynomial
side, or of three or four variables whose combined function has degree three
or more, therefore yields no cut in that direction." Add after "The binary64
values of $a$ and $\lambda$ are then certified.": "For a non-quadratic block
the subdivision is refined only until the bound reaches the value that makes
the row violated by the threshold at the current point; if it does not, the
call counts as a failed certification." Replace "only the star oracle of
Theorem~\ref{thm:star} can apply" by "only the star oracle
(Section~\ref{sec:star}) can apply".

### F6 (minor). Table 1 does not describe what was run in Parts 3A, 3D and 4D, and the paper never states the root time limits or what a "seed" is

Location: Table 1, `sections/08a-setup.tex:52-76` (p. 24);
`sections/A-instances-D.tex:22-26` (p. 50).

Issue and evidence (`R9_impl_run_inventory.py`):
- 3D: Table 1 says runs "as 3A-3C". The diagnostic ran only root runs for
  Parts A and B (`partA-root-rowdir`, `partB-root-rowdir`, modes baseline,
  `all`, `auto`, `all-diag`, all with whole-row directions) and full and root
  runs for Part C (baseline, whole-row with mechanism limits, whole-row with
  wide limits). The 3D A/B root runs gave the same root bounds as campaign 3
  on all 240 paired runs (probe: no difference above 1e-4), a result the
  paper does not report.
- 4D: "baseline, all, auto, extra; root runs also all-diag, all-diag-rowdir"
  suggests `auto` in root runs; the root runs had baseline, `all`, `all-diag`,
  `all-diag-rowdir`, `baseline-extra` (100 runs), as in the protocol.
- 3A: "seeds 0-2" applies to full runs; root runs used seed 0.
- Root-run time limits (60 s for 3A, 3B, 3D-A/B, 4B2; 120 s for the path
  family and 4D) and the hard process limits (360 s full; 90 s or 180 s root)
  appear nowhere except two table captions in Appendix G.
- "Seed" means SCIP's `randomization/randomseedshift` in Parts A and B but the
  instance generator seed in the path family (where SCIP's seed is 0).
- The path-family generator bounds $t_i\in[-10,10]$ are not stated
  (`v3/mechanism.py:98-99`).

Fix. Caption: "Full runs have a budget of 300\,s (process limit 360\,s); root
runs have a node limit of one and 60\,s (Parts 3A, 3B, 4B2) or 120\,s (path
family, 4D). Seeds are SCIP's random seed shift; path-family instances are
identified by their generator seed and run with SCIP seed 0." Rows: "3A ...
full runs seeds 0-2, root runs seed 0"; "3D & 3A, 3B root runs; 3C & whole-row
variant of all modes; 3C also wide limits & root (A, B); full, root (C)";
"4D & ... & full: baseline, all, auto, extra; root: baseline, all, all-diag,
all-diag-rowdir, extra". Add one sentence to 8.3 reporting the 3D A/B result.
Add "and $t_i\in[-10,10]$" to the path-family description.

### F7 (minor). The load average of campaign 4 is understated

Location: `sections/08a-setup.tex:22-23` (p. 23): "about 3 to 8 during campaign 4".

Evidence. Per-part one-minute load readings (start and end of each run):
C2 2.3-7.4, C3 0.8-8.0, B2 2.4-4.7, D root 2.8-7.3, D full 1.1-8.5, but C4
1.9-14.8 with median 8.2, 95th percentile 13.9 and 90 of 360 readings above 9.

Fix. "about 3 to 8 during campaign 4, and up to 15 during Part~C4".

### F8 (minor). On the larger models the block cap usually binds, so the separator examined only the 4-variable groups with the smallest variable indices

Location: `sections/07-implementation.tex:84-86` (p. 22, "at most 32 blocks
are kept, in a fixed order with the largest first"); Part D paragraph,
`sections/08c-minlplib.tex:112-129` (p. 26).

Issue. Discovery sorts groups by (size descending, variable-index tuple) and
keeps the first `max_blocks` (`integration.py:230, 272-274`). The tie-break is
not stated, and the paper does not say that the cap was reached on most Part D
models. This matters for "where it does its cuts are not stronger than SCIP's
relaxation": the cuts came from an arbitrary, index-determined subset of the
blocks. The Part D qualification ("a block that the auto rule admits") was
also evaluated on this capped list (`scanD/scan-summary.md`: "block cap (32)
reached" for all 85 qualifying models).

Evidence. `R9_implementation_block_cap.py`: Part D root, mode `all`: discovery
completed on 8 models, cap reached on 6; `all-diag` (128 blocks): cap reached
on 10 of 20; Part D full `all`/`auto`: 7 of 9. In Parts A and B the cap was
reached on at most 2 models.

Fix. Section 7.2: "at most 32 blocks are kept: the largest first, ties
broken by the indices of their variables." Part D paragraph: "Discovery found
more blocks than the cap on 6 of the 8 models where it finished in mode
\code{all} and on 10 of the 20 in mode \code{all-diag}; the blocks tried were
then those with the smallest variable indices."

### F9 (minor). The C4 reference values are not known "exactly"

Location: `sections/08e-path.tex:31-38` (Section 8.5, p. 28): "For C4 we know
two reference values exactly ... computed with the exact convex envelopes";
`sections/A-instances-D.tex:25-26` (p. 50): "the exact reference values".

Evidence. `v4/mechanism_c4.py` docstring and `v4/c4-references.json`: the
optimum is an exact rational (e.g. 533/4096) obtained by re-solving Gurobi's
pair assignment exactly, and an exact branch and bound on the Lagrangian bound
certifies it to within `optimum_minus_lower` <= 2.4e-59 (tolerance n*1e-20).
Bound (ii) is computed by 100 bisection steps on the multiplier with
envelopes built in mpmath at 60 digits; its enclosure width
(`bound_ii.upper_minus_lower`) is 1.6e-29 to 1.3e-28.

Fix. "For C4 we know two reference values to high accuracy: the optimum, an
exact rational from a convex mixed-integer quadratic reformulation solved by
Gurobi, re-solved exactly for Gurobi's choice of pairs and certified by an
exact branch and bound to within $10^{-58}$; and the best root bound ...,
enclosed in an interval of width below $2\cdot10^{-28}$ by bisection on the
multiplier of the coupling row." In Appendix G: "the reference values with
their certificates".

### F10 (minor). Not all campaign-4 code was fixed before the campaign's first run

Location: `sections/08a-setup.tex:6-9` (Section 8 introduction, p. 22): "Each
was run with code, limits and protocol fixed before its first run".

Evidence. The separator snapshot (manifest `098bda40...`, 17:01 UTC) and the
protocol with Amendment 1 predate the first campaign-4 run (17:08 UTC). The C4
instance builder and reference computation (`v4/mechanism_c4.py`,
`v4/make_jobs_c4.py`, last modified 18:03 UTC; `c4-references.json` 19:35
UTC) were written while Part C3 was running (17:27-18:13 UTC) and before the
first C4 run (20:59 UTC). The C4 instances and modes are fixed by the
amendment, so the design remains prospective.

Fix. "Each was run with solver code, limits and protocol fixed before its
first run; the job builder and reference computation of Part~C4 were written
during campaign~4, as specified by the protocol amendment, before any C4 run."

### F11 (minor). Part U deviates from the protocol in which cuts it analyses; the paper does not say so

Location: Table 2 and text, `sections/08b-validity.tex:95-123` (Section 8.2, pp. 24-25).

Issue. Amendment 1 specifies "every recorded cut of the MINLPLib parts of
campaigns 3 and 4 (A, B, B2, D)". The analysis (`evidence/ablation-uncertified.md`)
uses 5,116 cuts: it adds the 998 cuts of the 3D A/B root reruns and drops the
151 cuts whose certificate is a Bernstein (9) or ball-arithmetic (142) lower
bound rather than an exact minimum (5,267 - 151 = 5,116;
`R9_implementation_cut_methods.py`: 143,116 polytope, 9 Bernstein, 142 Arb
cuts overall, all non-polytope cuts in Part A). The caption's "each cut with
an exact certificate" hints at the second change only.

Fix. Add to the paragraph: "The MINLPLib set comprises all cuts of Parts A,
B, B2 and D and of the post hoc A and B root reruns whose certified value is
the exact support value; the 151 cuts certified by Bernstein or
ball-arithmetic lower bounds, all in Part~A, are excluded because a larger
uncertified constant would not show an error."

### F12 (minor). The availability statement omits replay dependencies and details a referee needs

Location: `sections/99-availability.tex:4-15` (p. 32).

Issue and evidence.
- "Replay needs Python with SymPy, python-flint and PySCIPOpt": replay imports
  the OSiL reader package `uenv`, whose `envelope.py` imports NumPy and SciPy
  (`code/univariate_envelopes/uenv/envelope.py:14-16`), so both are required.
- Versions missing: NumPy 2.5.3 (sampling), mpmath (C4 envelopes,
  `mechanism_c4.py`), gurobipy 13.0.3 (recorded in `sessions.jsonl`).
- Gurobi needs a licence; the comparator runs and the C4 optimum cannot be
  reproduced without one, while replay and all checks can.
- The CPU model is not stated anywhere (Intel Xeon w5-2565X, 18 cores).
- "the scripts that produce every table and number" should name where the
  recomputation scripts live (`summarize_v3.py`, `summarize_v4.py`,
  `summarize_c4.py`, `verification/ablation_uncertified.py`, the `R*`
  recomputation scripts); the campaign-1 and campaign-2 snapshots live outside
  the paper directory (`research-2026100{2,3}-convexification/experiments/`).

Fix. "Replay needs Python with SymPy, python-flint, PySCIPOpt, NumPy and
SciPy; it constructs, but does not solve, a SCIP model. The Gurobi runs and
the C4 reference optimum require a Gurobi licence. The experiments used ...
NumPy~2.5.3, mpmath~[version] ... on an Intel Xeon w5-2565X (18 cores)."

### F13 (suggestion). Column "LPs" of Table 3 also contains sample construction

Location: Table 3, `sections/08d-funnel.tex:9-20` (p. 27); text line 65.

Evidence. `candidate_seconds` wraps `propose_direction`
(`integration.py:424-432`), whose first call per block builds the sample:
grid, exact polytope vertex enumeration and `lambdify` evaluation
(`integration.py:288-317`). Fix: head the column "direction search" and say
"sampling and direction LPs" in the text.

### F14 (suggestion). Say that replay checks the recorded stored row, not SCIP's row

Location: `sections/06-certification.tex:117-127` (Section 6.3, pp. 19-20).

The stored-row check (C4) is performed once, at generation, through
PySCIPOpt's row accessors; replay compares the recorded row with the
recomputed export (`replay.py:271-290`) and cannot observe SCIP again. The
trusted base lists "its accessors for stored rows", which covers this, but
the replay paragraph reads as if replay re-checked SCIP. Suggested addition:
"and compares the result with the stored row as recorded by the separator;
the stored-row check itself is made only at generation time."

### F15 (suggestion). Section 7.2 omits four implementation details that shape the results

Location: `sections/07-implementation.tex:93-127` (p. 22).

- The separator has priority 100000, so in each root round it runs before
  SCIP's own separators (`integration.py:619-621`); with `forcecut` its rows
  bypass SCIP's cut selection. This is relevant to the root bounds that got
  worse in Section 8.3.
- The remainder (and whole-row) directions of a block are tried once per run:
  a direction already tried for the block is skipped in later callbacks
  (`seen`, `integration.py:475-477`), and a block is skipped when the LP
  point is unchanged.
- Exact vertices and the centroid are added for quadratic blocks only.
- $T$ in the allowance is the soft budget minus the worker's preparation
  time (`v4_worker.py`, `budget = time_limit - preparation_seconds`).

### F16 (suggestion). Some prespecified metrics are not reported

`campaign-v3-protocol.md` (Metrics) prespecifies shifted geometric means per
seed and pooled, bound comparisons at 1e-6 as well as 1e-4, and Part S counts
by stratum. The paper reports pooled means, 1e-4 comparisons and the overall
Part S count (111 of 392) only. Either add them to Appendix G (the 1e-6
comparisons are in `experiments/v4/results-c3/results.md`, the Part S counts
by stratum in `experiments/v3/scan/scan-summary.md`) or state that they are
omitted and where they are archived. Note also that `v3/README.md` step (v)
promises `v3/results.md` and `summary.json`, which do not exist; the
campaign-3 summaries were produced by `summarize_v4.py` into
`experiments/v4/results-c3/`. The availability statement should point there.
