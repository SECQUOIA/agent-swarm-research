# Reproduction package for the September 29 results

This package links the numbers in `research-20260929/open-instances-summary.md`
and `bound-audit/audit-report.md` to saved programs, model inputs, certificates
and outputs. The integration-review response adds the stored all-leaf EG
evidence; the final manifest rebuild remains pending. The experiments were
not repeated. Short checks are recorded in `logs/smoke-results.json` and
`logs/integration-r1-eg-smoke.json`.

## Start from a checkout

Use Python **3.13.11**. The versions used by the earlier reproduction runs and
these smoke checks are pinned in `requirements.txt`: mpmath 1.3.0, numpy 2.5.1,
scipy 1.18.0, sympy 1.14.0, PySCIPOpt 6.2.1, CVXPY 1.9.3, Clarabel 0.11.1,
and HiGHS/highspy 1.15.1. `environment.json` records the interpreter build.
PySCIPOpt uses **SCIP 10.0.2** in this environment. Numerical optimization can
change with the solver or BLAS build; exact verification of a saved certificate
does not depend on getting the same optimizer multipliers again.

From the repository root:

```bash
R="$(pwd)/research-20260929"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
# In a Python 3.13.11 environment:
python3 -m pip install -r "$R/publication/reproduction/requirements.txt"
python3 "$R/publication/reproduction/tools/prepare_inputs.py" --download
```

The last command restores saved inputs that Git ignored and checks every model
hash. It downloads only missing OSIL files from
`https://www.minlplib.org/osil/<instance>.osil` into
`os.path.expanduser("~/.cache/minlplib/minlplib/osil")`. It rejects a different
upstream file or a different existing input. Without `--download` it only
restores the archive and verifies the existing model cache.

Commands write into the saved `logs/` folders and can replace tracked evidence.
Run them in a disposable copy of the checkout.

The scientific scripts expect the working directory shown below. Their imports
and repository input paths are now relative to the script location. The cache
location follows the current user's home directory. Run commands sequentially,
or use at most four single-threaded processes. Older queue scripts under the
five track directories record historical launches and contain historical
machine paths; they are not the entry points for this package.

## Inputs, outputs and provenance

| record | contents |
|---|---|
| `manifest.json` | SHA-256, size and Git status of scientific scripts and saved evidence, organized by directory; base commit and archive hash |
| `inputs/saved-inputs.tar.gz` | saved ignored `.sol`, `.osil` and `.html` inputs, at their repository paths |
| `inputs/saved-inputs.json` | each archive member's SHA-256, size and original download URL |
| `inputs/osil-models.json` | 95 cache models, with SHA-256, size and download URL |
| `commands.json` | 443 prior measured commands with exit codes/timings, plus 54 EG evidence commands with inputs, output hashes and expected results; expensive historical commands are marked not to repeat |
| `cops/manifest.json`, `small/manifest.json` | earlier detailed run/input comparisons; historical absolute paths are provenance |
| `result-map.json` | every summary table row expanded to its instances and certificate script/input/output paths, with explicit numeric evidence at saved precision |
| `audit-map.json` | all 46 screened audit instances, every classified pair, exact enclosures, and per-point commands/evidence |
| `logs/saved-evidence-counts.json` | audit and scout population counts read from saved JSON |

`$R` in `commands.json` means the checkout's `research-20260929` directory.
`$SCRATCH` means a directory chosen for temporary replay outputs. The catalogue
is a historical record: failed diagnosis runs, interrupted runs and deliberately
timed-out startup audits remain visible. Only a successful run is evidence for
a completed calculation. Times below come from that catalogue or the original
scientific logs, not from new full experiments. They are indicative times on a
shared machine.

The archived MINLPLib pages preserve the September 2026 snapshot. Do not fetch
current pages to reconstruct historical listed bounds. `bound-audit/pages.json`
holds every displayed solver bound and listed point as a string, including its
date. `open-instances-scout/fetched.json`, `open-instances-wave3/logs/`, and
`open-instances-wave3/eg/retry/logs/` preserve the family-specific page extracts.
The scout's `parse_pages.py` reads its saved pages and candidates; its output has
283 candidates, of which 146 have `gap_best > 1e-4`. The candidate input traces
to `treewidth-census/census_merged.json` and `fetch_pages.py:candidates()`.

The first-wave bound scripts and the scout/census tools import
`research-20260922/scouting/minlplib-open-data/osil.py`. Keep that file at
its repository path in a relocated checkout; the final manifest builder
hashes it as an explicit cross-directory input. `open-instances-scout/hvycrash_check.py`
and `open-instances-scout/structure.py`, and `treewidth-census/census.py`, now
resolve imports from their own file locations. The saved census remains the
evidence; running the full census is unnecessary for reproduction.

## Control and camshape

First run in `$R/open-instances` to regenerate ordinary primal files and the
older author certificates. For the tight displayed bounds, use the independent
checks in `$R/reviews/open-instances-verification` as specified in the table.

| instance | command and working directory | expected certificate / saved output | prior runtime |
|---|---|---|---|
| lnts50 | reviewer: `python3 v_lnts.py 50 100 200 400` | summary lower 0.5546687649381; primal 0.5546687649387; `logs/lnts_verify.json` | 1.58 s for all four |
| lnts100 | reviewer batch above | 0.5545954011663 / 0.5545954011669; same file | same batch |
| lnts200 | reviewer batch above | 0.5545770161025 / 0.5545770161031; same file | same batch |
| lnts400 | reviewer batch above | 0.5545724137001 / 0.5545724137007; same file | same batch |
| dtoc5 | author: `python3 dtoc5_primal.py`; `python3 dtoc5_bound.py`; reviewer: `python3 v_dtoc5.py` | 5.38967211918114; reviewer `logs/dtoc5_verify.json` | 1.04 + 5.96 + 18.15 s |
| camshape100 | author: `python3 camshape_bound.py 100`; reviewer: `python3 v_camshape.py 100 200 400 800` | exact optimum rounded down −4.28414712174675; reviewer `logs/camshape_verify.json` | author 0.80 s / reviewer 8.03 s, four-instance batches |
| camshape200 | author: `python3 camshape_bound.py 200`; reviewer batch above | −4.27850023299273; same reviewer file | same batches |
| camshape400 | author: `python3 camshape_bound.py 400`; reviewer batch above | −4.27568847892555; same reviewer file | same batches |
| camshape800 | author: `python3 camshape_bound.py 800`; reviewer batch above | −4.27427414195420; same reviewer file | same batches |
| lukvle10 | reviewer: `python3 v_lukvle10_prep.py`; `python3 v_lukvle10_bnb.py 1` | safe display 352.2380254050784; primal 352.2380254064961; `logs/lukvle10_{prep,bnb}.json` | 0.64 + 300.35 s |
| optcdeg2 | see quadratic-calibration commands below | safe lower display 293.87607509587509; primal upper 293.87607509587509328 | 8.32 s author certificate; 18.84 s reviewer exact certificate |

Run each reviewer batch once to reproduce its four-record `logs/*_verify.json`.
A single-instance call replaces that shared file with just one record.

The lnts author's command `python3 lnts_bound.py lnts50 lnts100 lnts200 lnts400`
uses a looser default relative offset and produces bounds about 5.5e-11 below
the primal. The reviewer tries tighter offsets and supplies the summary's
5.5e-13 gaps. Likewise `lukvle10_bound.py 3` gives 352.238025369202; the
reviewer's `v_lukvle10_bnb.py 1` supplies the tighter displayed result.

For optcdeg2, run these commands in order if generating the final calibration
again is desired:

```bash
cd "$R/theory-bangbang"
python3 optcdeg2_refine_primal.py
python3 optcdeg2_kkt_primal_check.py
python3 optcdeg2_qcal_certify.py 1.0 0.05
python3 optcdeg2_qcal_recheck.py
cd "$R/reviews/bangbang-verification"
python3 v_model.py
python3 v_states.py
python3 v_primal.py
python3 v_qcal_exact.py
```

Inputs include the cached OSIL, `open-instances/minlplib_sol/optcdeg2.p1.sol`,
the saved controls and states, `theory-bangbang/logs/optcdeg2_qcal_data.npz`,
and the reviewer's state enclosures. `theory-bangbang/logs/` and
`reviews/bangbang-verification/logs/` save the certificate and primal checks.
The earlier certificate sequence in `open-instances/` is
`optcdeg2_primal.py`, `optcdeg2_bound.py`, `optcdeg2_head.py 3080`, and
`optcdeg2_verify.py 3080`; it is superseded for the summary. The bound script
now also saves `logs/optcdeg2_mu.npy` and `logs/optcdeg2_lam.npy`; the prior
regeneration comparison found both bit-identical to the saved multipliers.

First-wave inputs in `minlplib_sol/` were ignored by Git and are included in
the archive. `publication/primal/lnts/` and
`publication/primal/dtoc5-lukvle10/` provide additional primal construction
and verification commands, all indexed in `commands.json`. Those later
primal studies do not replace the summary's original primal values.

## COPS: chain and catmix

The completed earlier reproduction is documented in [cops/report.md](cops/report.md).
It matched 52 main runs; its sandbox audit checked 43 complete short runs and
three deliberately stopped long-run startups. These were not repeated here.

In `$R/open-instances-wave2/cops`, for each chain size N:
`python3 chain_model.py N`, then `python3 chain_bound.py 1e-14 N`.
In `$R/reviews/cops-verification`, use `python3 v_chain_bnb.py 1e-14 N`.

| instance | author's saved binary-double bound | author / reviewer runtime | inputs and output |
|---|---|---|---|
| chain50 | 5.072261493982863 | 11.6 / 71.7 s | model OSIL; author `logs/chain50_bound.json`; reviewer `logs/chain50_bnb.log` |
| chain100 | 5.0697846107387505 | 15.7 / 100.8 s | corresponding size's saved KKT arrays and bound files |
| chain200 | 5.068917341793162 | 20.7 / 143.1 s | corresponding size's files |
| chain400 | 5.068621694604009 | 28.8 / 194.8 s | corresponding size's files |

These are binary-double values printed with `repr`, not all valid decimal
lower bounds; see the rounding caveats below. The summary coarsens them to
`5.06862 … 5.07226`. The original closure uses tolerance-feasible KKT points.
Optional exact primal construction is in `publication/primal/chain/`:
`python3 build_points.py N`, then `python3 verify_points.py N`.

For each catmix N = 100, 200, 400, 800, the author's full computation is:

```bash
cd "$R/open-instances-wave2/cops"
python3 catmix_model.py 100 200
python3 catmix_primal.py 100
python3 catmix_primal.py 200
cd explore
python3 catmix_primal_snap.py 400 2e-3
python3 catmix_primal_snap.py 800 2e-3
python3 catmix_primal_snap_eval.py 800
python3 catmix_stage_lb_selftest.py
cd ..
# Substitute one N at a time; these are long runs, not smoke tests.
python3 catmix_bound.py N 1e-5 200 1e-7 0.0685 0.0725 1e-6
```

| instance | author's bound | reviewer's tighter bound / exact primal | author / reviewer runtime |
|---|---|---|---|
| catmix100 | −0.048069432038882705 | −0.048069432031144562 / −0.048069432030979596104 | 17.5 / 46.0 min |
| catmix200 | −0.048059145600671712 | −0.04805914559907277 / author's −0.0480591455801144 | 28.8 / 20.2 min |
| catmix400 | −0.048056547950296354 | −0.04805654782467129 / −0.0480565477559440726 | 50.0 / 45.2 min |
| catmix800 | −0.048055901841076894 | −0.048055901479675652 / −0.0480559013312308003 | 76.7 / 46.1 min |

The catmix100 reviewer is `v_catmix_dp.py 100 16 0.0697 0.0715 20 300 25`
in `reviews/cops-verification/`, after `v_catmix_selftest.py 100`.
For catmix200 it is `v_catmix_dp.py 200 15 0.0695 0.0717 19 200 24`, after
`v_catmix_selftest.py 200`. These read the recorded policies in `logs/`.
The exact catmix100 primal is produced by `v_catmix_newton.py 100`.

For catmix400/800, run in `$R/reviews/catmix-recheck-checks`:

```bash
python3 v_catmix_selftest.py 400
python3 recheck_dp.py 400 13 --sband 0.0703 0.0710 21 40 310 --sband 0.0695 0.0717 19 40 310 --win 200 24 logs/catmix400_theta_traj.npy --win-skip 56 288 --tree logs/tree400_final.json --save-traj logs/catmix400_final_policy_traj.npy --save-u logs/catmix400_final_policy_u.npy
python3 policy_exact.py 400 logs/catmix400_final_policy_u.npy
python3 v_catmix_selftest.py 800
python3 recheck_dp.py 800 13 --sband 0.0703 0.0710 21 95 600 --sband 0.0695 0.0717 19 95 600 --sband 0.060 0.0695 17 570 650 --win 200 24 logs/catmix800_theta_traj.npy --win-skip 112 576 --tree logs/tree800_final.json --save-traj logs/catmix800_final_policy_traj.npy --save-u logs/catmix800_final_policy_u.npy
python3 policy_exact.py 800 logs/catmix800_final_policy_u.npy
```

`cops/manifest.json` gives every command's traced inputs, their hashes and
the corresponding saved outputs. The recovered `catmix_primal_snap_eval.py`
is included in the new script files to commit.

## Small models and eg

The tight ex6, etamac and pricing050 numbers in the summary come from the
independent reviewer, whose bounds can be tighter than the author's defaults.
Work in `$R/reviews/wave2-small-verification` unless the table says otherwise.

| instance | command sequence | expected output / inputs | prior runtime |
|---|---|---|---|
| hvycrash | author in `open-instances-wave2/small`: `python3 hvycrash.py`; reviewer: `python3 v_hvycrash.py` | exact objective −0.2185, explicit feasible point; OSIL and `sol/hvycrash.p*.sol`; saved `logs/hvycrash*` | 0.17 / 0.15 s |
| ex6_2_7 | `python3 gibbs_kkt.py ex6_2_7`; `python3 gibbs_bb.py ex6_2_7 0 6e-15 1`; `python3 gibbs_bound.py ex6_2_7 0=logs/ex6_2_7_bb_type0_tau6e-15.json` | bound −0.16084761546364904344, safe summary −0.16084761546364905; primal −0.16084761546360086; saved BB JSON and `logs/ex6_2_7_bound.json` | original BB about 50 s; saved-bound check 3.20 s |
| ex6_2_5 | `python3 gibbs_kkt.py ex6_2_5`; `python3 gibbs_bb.py ex6_2_5 0 1e-17 1`; `python3 gibbs_bound.py ex6_2_5 0=logs/ex6_2_5_bb_type0_tau1e-17.json` | bound −70.75207783344770759; primal −70.752077833447706; corresponding saved BB and bound files | original BB about 200 s; saved-bound check 3.61 s |
| etamac | `python3 v_etamac.py` | rigorous lower safely displayed −15.294675643368093; own exactly feasible recursion; `logs/etamac.json` | 21.67 s |
| pricing050 (max) | `python3 v_pricing050.py` | upper −1813.8290784519730577; exact primal −1813.8290784519731; `logs/pricing050.json` | 27.72 s |
| pindyck | in `reviews/pindyck-review-checks`: `python3 primal_check.py`; `python3 author_data.py`; `python3 own_ranges.py`; `USE_AUTHOR_G=1 python3 own_ranges.py`; `python3 own_concavity.py`; `python3 verify_own_leaves.py`; `python3 final_bound.py` | safe lower −1170.4862854360886163932; primal −1170.486285436088562; `logs/`, including saved range/concavity leaves | range and concavity checks: seconds and 322 s; final evaluation 0.12 s |

The author's `gibbs.py <instance> 1e-11`, `etamac.py`, `pricing050.py`,
`pindyck.py` and `pindyck_global.py` remain available in
`open-instances-wave2/small/`. All `.sol`, JSON and leaf files used above
are either tracked or restored by `prepare_inputs.py`.

For eg, work in `$R/open-instances-wave3/eg/retry`. The producer is
`egbb.py`; input coefficients come from the OSIL and saved exploration
arrays in `logs/`. Every final partition and checkpoint is saved.

| instance | full producer commands | expected dual / exactly feasible primal | original final-run time |
|---|---|---|---|
| eg_int_s | `python3 egbb.py eg_int_s 1e-9 3600 logs/int9_final.npz` | 6.4531031529331155 / 6.4531031593842275 | 274 s |
| eg_disc_s | `python3 egbb.py eg_disc_s 1e-9 5400 logs/disc9_p0.npz - 0 2` and corresponding part 1 | 5.760539610694994 / 5.7605396164535107 | 726 + 650 s |
| eg_disc2_s | for k = 0,…,7, sequentially: `python3 egbb.py eg_disc2_s 1e-9 3600 logs/disc2_9_p${k}.npz - $k 8` | 5.642100574331458 / 5.6421005799711068 | 12,378 s (sum of part wall times; 38 min elapsed) |

The eg_disc_s display 5.760539610694994 is 2.4e-16 above the certifier's
binary64 bound; it is valid because the independent retry review certified
every leaf against this exact decimal, under the same A1/A2 assumptions.
The eight final disc2_9_p{k}.npz checkpoints are byte-identical by
construction: each records an empty final queue.

Aggregate the recorded parts with `python3 summary.py`, which also checks
`done=True` and includes closed minima from resumed checkpoints. Check the
primal with `python3 verify_primal.py <name> <checkpoint.npz>`: use
`int9_final.npz`, `disc9_p1.npz`, and `disc2_9_p1.npz`, respectively.
The resulting `sol/<name>.retry.sol` and the saved reviewer checks trace the
primal side.

Independent replay and leaf checks are in `reviews/eg-retry-review-checks/`:
`record_run.py` records a tree using the corresponding producer arguments;
`verify_tree.py <record.npz> <name> <displayed_dual> 1.0` checks every leaf.
The earlier eg_disc2_s retry review checked part 1 fully and sampled
**110,676 of 979,044 leaves** outside part 1. That sample is historical.
The current [all-leaf report](../eg-recheck/report.md) and
[review r1](../reviews/eg-recheck-review-r1.md) cover **all 1,114,361 leaves
of run G, with zero failures**, against the exact decimal
θ* = **5.642100574331458**, under **A1** (the certifier's hand-checked
floating-point error analysis) and **A2** (numpy exp relative error at most
1e-14, checked by sampling). **1,152,830 is the processed-box count**.
The review proves coverage exactly with a tree-free guillotine decomposition.
It separately certifies **10,404 leaves of parts 0 and 2–7**, including the
300 tightest per part, with outward-rounded intervals and no libm assumption;
that stronger check remains a sample.

The package manifest scopes now include `publication/eg-recheck/` and
`publication/reviews/eg-recheck-r1/`. Their saved evidence is tracked and
does not require a new input archive. `result-map.json` includes their scripts,
inputs and outputs; `commands.json` indexes the 38 certification chunks,
eight recorded trees, stored-evidence checks and interval samples. The final
manifest was rebuilt by this integration implementation task on 2026-10-04 after all covered edits; the default package check passed.

| stored evidence | inputs | command (in a disposable copy) | expected result |
|---|---|---|---|
| all-leaf summary | `publication/eg-recheck/res/p{k}_c{c}.npz` (38 files), pinned OSIL | in `$R/publication/eg-recheck`: `python3 summarize.py` | `logs/summarize.log`: 1,114,361 leaves, 0 failures; every index in exactly one chunk; all eight parts cover the domain |
| independent bookkeeping | `rec/rec_disc2_p{k}.npz`, 38 chunk NPZs and chunk logs | in `$R/publication/reviews/eg-recheck-r1`: `python3 own_bookkeeping.py` | `logs/own_bookkeeping.log`: `ALL GOOD`; writes `leaves_p{k}.npz`, with boxes identical to the certified boxes |
| exact coverage proof | `leaves_p{k}.npz`, pinned OSIL | same directory: `python3 own_cover.py` | `logs/own_cover.log`: `COVERAGE PROVED` for all eight parts and the OSIL domain |
| model identity | pinned OSIL, `reviews/eg-retry-review-checks/data/eg_disc2_s.gms` | same directory: `python3 cmp_model.py` | `logs/cmp_model.log`: `MODEL DATA IDENTICAL` |
| interval sample | derived leaves, pinned OSIL, `minF_p{k}.npy` for sample C; saved `sample_{A,B,C}_p{k}.npz` | historical `own_sample.py` arguments in `commands.json` | union of A/B/C: 10,404 distinct leaves, zero failures; logs `own_sample_{A,B,C}.log` |

The historical all-leaf command, in `$R/publication/eg-recheck`, is
`python3 recheck_leaves.py rec/rec_disc2_p{k}.npz eg_disc2_s 5.642100574331458 c N res/p{k}_c{c}.npz`.
The chunk counts N for parts 0–7 are **4, 5, 6, 7, 7, 5, 3, 1**;
c ranges from 0 to N−1. Inputs also include the reviewer's GAMS data above;
outputs are `res/p{k}_c{c}.npz` and `logs/cert_p{k}_c{c}.log`, each with
zero failures. The 38 chunk timing fields sum to about **41,162 s of per-chunk wall time** (time.time()); up to 12 chunks ran concurrently, and the scheduler finished after **5,372 s**.
Do not repeat tree generation or the full certification for packaging.
For a small relocated smoke check, run from the repository root:

```bash
python3 research-20260929/publication/reproduction/tools/check_eg_relocated.py
```

This requires Linux **bwrap (bubblewrap)** and **strace** on PATH. It writes
to a fresh disposable output directory by default and removes its temporary
scientific copy on success. It copies the stored evidence, hides the source
trees and original cache,
checks the stored summary, certifies 29 interleaved leaves of part 7 through
`recheck_leaves.py`, and reproduces eight random leaves per part with the
unchanged certifier. It uses one BLAS/OpenMP thread and at most four CPUs.
Historical `run_record.sh` and `run_cert.py` launch eight and twelve processes,
respectively; use the indexed individual commands sequentially if a new
scientific run is separately authorized.

## KAN, powerflow and ANN

For KAN, in `$R/open-instances-wave3/kan`, use
`python3 run_kan.py <name> 1e-10 7200` (1800 suffices for the three r3 cases).
Inputs are the OSIL; listed comparison points are in `../sol/<name>.p*.sol` (p1, p2 or p3 as saved). Results and improved points
are saved in `../logs/` and `../sol/`. `kan_summary.py` aggregates them.

| instance | recorded lower / tolerance-feasible primal | author's prior runtime |
|---|---|---|
| kan_r3_h1_n4 | 0.002781237152581 / 0.0027812372214418 | 22.57 s |
| kan_r3_h1_n5 | −0.01104267952178 / −0.011042679414487 | 23.83 s |
| kan_r3_h1_n9 | 0.01296365996347 / 0.0129636600530393 | 22.34 s |
| kan_r5_h1_n3 | −262.8642259092 / −262.8642258850652 | 1083.76 s |
| kan_r5_h1_n5 | 0.2725832538548 / 0.2725832539566226 | 101.50 s |
| kan_r5_h1_n8 | 0.06932786051053 / 0.0693278606061910 | 87.33 s |

These are certificates of the intended network relaxation **R**. All six
OSIL models have no exactly feasible point. In `reviews/wave3-verification`,
`python3 kan_infeas_cert.py <name>` rechecks that fact in 0.64–1.64 s;
`python3 kan_bnb.py <name> 4e-11 1800 1024` independently bounds R.
`publication/primal/water-ann-kan/code/nn_exact.py <name>` verifies saved
points for the intended network; it does not construct an OSIL-feasible point.

| powerflow instance | certificate command | expected bound / original primal | prior runtime |
|---|---|---|---|
| powerflow0030p | in `reviews/wave3-verification/powerflow`: `python3 run_root.py powerflow0030p` | exact 576.893412298800469849…; safe summary 576.8934122988004 / 576.8934134704 | 4.15 s |
| powerflow0039p | in `open-instances-wave3/powerflow/ext`: `python3 verify_exact.py powerflow0039p bb3t` | 41869.05148485014 / 41869.0515113202 | 77.59 s |
| powerflow0039r | same command with `powerflow0039r` | 41869.05148327243 / 41869.0515113208 | 24.12 s |

The 0030p input is `open-instances-wave3/logs/powerflow0030p.sdpcert.json`
(raw saved multipliers and exact bound); the checker rebuilds the model and
uses an exact rational LDLᵀ proof. **A new `pf_cert.py powerflow0030p` solve
with the pinned current stack returns 576.8905424271796, not the published
bound.** It also overwrites the saved certificate in its output directory.
Use a disposable copy for optimization and keep the published certificate
for the exact replay.

For 0039p/r, `ext/logs/<name>.bb3t.json` saves leaf boxes and multipliers;
`verify_bb3.py <name> bb3t` takes about 1.6 s. Generation is
`python3 pf_bb3.py <name> 2400 <primal> 1/10000 1e-10 bb3t`, with the primal
from the table. The earlier measured regeneration took 316 / 463 s and
used `bb3t_repro` as its output tag. `reviews/powerflow0039-review-checks/`
contains independent leaf verification. The original primal is the listed
`open-instances-wave3/sol/<name>.p1.sol`; `publication/primal/powerflow/`
contains later primal enclosures, which are separate from the summary.

For **ann_cumene_tanh**, the saved extension certificate gives the safe lower
**−3386.5403**, versus the original primal **−3379.9824** and the wave-3
lower **−4024.495**. Inputs: the OSIL, `open-instances-wave3/sol/`,
`ann/ext_logs/open1800_v1.npz`, `open_run2.npz`, and both code snapshots.
The original producer commands in `open-instances-wave3/ann/` are:

```bash
PYTHONPATH=. python3 ext_logs/ann_tm_v1_snapshot.py 1e-6 1800 ext_logs/open1800_v1.npz sep
PYTHONPATH=. python3 ext_logs/ann_tm_run2_snapshot.py 1e-6 5400 ext_logs/open_run2.npz sep-gradsmall ext_logs/open1800_v1.npz
```

The snapshots preserve the code used for those time-limited runs (1800 and
5400 s). Machine load changes the final frontier at a wall-clock limit.
For replay by saved node counts, use `reviews/ann-extension-review-checks/`:
`python3 replay.py run1 "$SCRATCH/replay_run1.npz"` and corresponding
`run2`; `leaves.py extract` extracts the closed regions;
`verify_boxes.py <boxes.npz> <out.npz> -3386.5402291369187 2` independently
checks the open frontier and closed regions. The existing network logs and
`commands.json` give the complete sequence and measured times. The saved
first-run and second-run frontiers are tracked. The original wave-3 proof
and caveats remain in `reviews/wave3-verification/ann/`. Its cheap
`python3 annv.py points` verifies the original primal values in 0.28 s.

## Water

For T = 6, 9, 12, 18, 24, work in `$R/open-instances-wave2/waterno2`.
The cached OSIL, `logs/implied_TT.json`, `logs/mult_TT_w1_impl.json`, and
`logs/cert_TT_w1_impl.json` contain the input bounds, slopes and all period
results. The original period certificate can be regenerated by substituting
T and its two-digit TT:

```bash
WATERNO2_IMPLIED=logs/implied_TT.json python3 certify.py T logs/mult_TT_w1_impl.json 1 logs/repro_cert_TT_w1_impl.json 3 300000 3600
```

This uses three workers and is a long computation. To reproduce the final
sum from the saved rigorous period bounds, use
`python3 vsum.py T` in `reviews/waterno2-verification/`; it reads OSIL
constants and saved binary-double bounds and sums them in exact fractions.

| instance | safe displayed wave-2 bound | original primal | prior author certificate runtime |
|---|---|---|---|
| waterno2_06 | 263.735099; raised twice below | listed 282.888 | 221.25 s |
| waterno2_09 | 824.834692 | 914.012 | 772.61 s |
| waterno2_12 | 2089.754565 | 2233.821 | 994.20 s |
| waterno2_18 | 4790.820715 | 5023.983 | 2385.66 s |
| waterno2_24 | 6576.151388 | 6963.795 | 3210.92 s |

The original primal files are `logs/primal_TT_w2.json`; their producer is
`primal.py` and `reviews/waterno2-verification/veval.py T <file>` checks
their violations (about 0.1–0.3 s). Reviewer's period runs are in
`reviews/waterno2-verification/` (T=6) and `reviews/waterno2-recheck/`
(T=9–24); `vsum2.py T` aggregates the latter. `commands.json` retains all
period-specific commands, targets, runtimes and saved results.

For **waterno2_06 separator branching**, in `waterno2/sepbranch/`:
`python3 verify.py logs/cert3.json`. Inputs are `logs/cert3.pkl`,
`logs/cert3.json` and `../logs/implied_06.json`; output
`logs/cert3_verify.json` gives **272.584700** (safe display).
The producer is `certify_dp.py logs/cert3.json`; original certification cost
25,308 s CPU / 1056 s wall with 24 workers. For a new run on this machine,
make a scratch config with `workers: 4`; do not change the saved config.
`reviews/waterno2-sepbranch-review-checks/ind_verify.py <cert3.pkl> <implied.json>`
recomputes the exact path bound; prior runtime 0.94 s.

For **waterno2_06 cell-dependent slopes**, in `waterno2/cellslopes/`:

```bash
PYTHONPATH=../sepbranch:.. python3 verify_cs.py logs/certB_cert.pkl.gz ../logs/implied_06.json logs/certB_verify_replay.json ../data/waterno2_06.p4.sol
```

Expected bound is the exact fraction
**39157472136693483/140737488355328**, whose decimal starts
**278.230573774**; the summary's safe display is **278.230573**.
`certB_cert.pkl.gz` contains the cells, slopes and all records. The original
producer is `certify_cs.py logs/certB.json`; its config names
`logs/planG_final.pkl`, saved as `planG_final.pkl.gz`. Decompress that input
in a scratch copy before rerunning, set workers to at most four, and allow
hours. For exact replay, use the slim certificate directly.
In `reviews/waterno2-cellslopes-review-checks/`, run
`ind_verify_cs.py <certB_cert.pkl.gz> <output.json> <certB_verify.json>`;
the earlier measured runtime was 10.72 s. This validates the record
corrections, cell coverage and exact shortest path; it does not rerun the
49,315 pair bounds. The original review re-bounded all those pairs.

The water gaps use `(primal − dual)/abs(dual)`; ANN uses
`(primal − dual)/abs(primal)`. Gaps in other summary tables are absolute
unless marked relative. A tolerance-feasible primal is not a proof that an
exactly feasible point exists. The summary explicitly retains this caveat
for lnts, dtoc5, lukvle10, chain and powerflow.

## Systematic bound audit

The historical population, displayed bounds, point dates and solved marks
are in `bound-audit/pages.json` and the archived `bound-audit/pages/*.html`.
In `$R/bound-audit`, the stages are:

```bash
python3 parse_pages.py
python3 audit.py screen
# Saved sol/ inputs are already restored; do not redownload the snapshot.
python3 audit.py evaluate --jobs 1
python3 audit.py verify --jobs 1
python3 cert_linear.py watercontamination0303.p2
python3 cert_ndnetgen.py nd_netgen-2000-3-4-b-a-ns_7.p2
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cert_topopt.py topopt-cantilever_60x40_50.p4
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cert_topopt.py topopt-cantilever_60x40_50.p5
python3 cert_socp.py emfl050_3_3 emfl050_3_3.p2 emfl050_3_3.p4 emfl050_3_3.p5
python3 cert_socp.py emfl050_5_5 emfl050_5_5.p4 emfl050_5_5.p5 emfl050_5_5.p6
python3 cert_socp.py emfl100_3_3 emfl100_3_3.p3 emfl100_3_3.p4
python3 cert_socp.py emfl100_5_5 emfl100_5_5.p2
python3 audit.py classify
python3 summarize.py > logs/summary.txt
python3 make_tables.py > logs/tables.md
python3 check_display.py
```

The evaluate and verify stages reuse existing per-point JSON. A genuine
recomputation requires removing only those output records in a disposable
copy; do not remove saved evidence from the working tree. Exact margins,
ratios, classifications and the histogram trace to `results.json`,
`summary.json`, `summarize.py` and `make_tables.py`. The cheap classification
and tables can be run from the saved proof records without solving models.

Expected counts: **1633** instances, **2816** listed points, **11086**
solver bounds; **158** screened point/solver pairs, **46** instances and
**56** points; **131** distinct instance/solver pairs; **19** proven invalid
pairs on **15** instances, split into **11** gross and **8** tolerance-scale
pairs. Display ties are **3851** pairs on **1133** instances. The per-instance
commands and exact enclosures for every class are in `audit-map.json` and
the [audit instance table](audit-instances.md), including undecided and
model-repair cases, which are not proofs of solver errors.

| proven-invalid family | exact/existence certificate command in `bound-audit/` | saved output | original/prior time |
|---|---|---|---|
| ghg_3veh (ANTIGONE, BARON) | `python3 verify_one.py ghg_3veh.p2` | `logs/verify/ghg_3veh.p2.json` | reviewer Krawczyk 0.60 s |
| glider100 (COUENNE, LINDO) | `python3 verify_one.py glider100.p2` | `logs/verify/glider100.p2.json` | reviewer 3.34 s |
| methanol50 (LINDO) | `python3 verify_one.py methanol50.p4` | `logs/verify/methanol50.p4.json` | reviewer 5.40 s |
| nuclear14 (LINDO) | `python3 verify_one.py nuclear14.p3` | corresponding verify JSON | reviewer 0.97 s |
| sssd20-04persp, sssd22-08persp, sssd25-04persp, sssd25-08persp (LINDO) | `python3 verify_one.py <name>.<point>`: p3, p4, p3, p4 respectively | corresponding verify JSON and repaired center | independent exact construction 0.11 s for all six listed-point checks |
| smallinvDAXr1b150-165, smallinvDAXr1b200-220, smallinvDAXr2b150-165, smallinvDAXr2b200-220 (LINDO) | `python3 verify_one.py <name>.p2` | corresponding verify JSON | reviewer exact r2 batch 0.08 s |
| nd_netgen-2000-3-4-b-a-ns_7 (CPLEX, GUROBI) | `python3 cert_ndnetgen.py nd_netgen-2000-3-4-b-a-ns_7.p2` | `logs/cert_ndnetgen_*.json` | 0.93 s |
| watercontamination0303 (BONMIN, LINDO) | `python3 cert_linear.py watercontamination0303.p2` | `logs/cert_linear_*.json` | 6.18 s |
| topopt-cantilever_60x40_50 (LINDO) | `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cert_topopt.py topopt-cantilever_60x40_50.p5` | `logs/cert_topopt_*.json`, center | 164.44 s |

The four emfl instances have valid listed duals and tolerance effects in
listed primal values. `cert_socp.py` gives two-sided optimum enclosures.
The independent `reviews/bound-audit-recheck/emfl_bounds.py <name>` gives
its own enclosures (2.21, 4.76, 3.00 and 12.79 s in the saved runs).
Read the exact rational/interval output in the saved audit and reviewer
logs; the two codes need not produce the same enclosure endpoints.

Independent invalid-bound checks live in
`reviews/bound-audit-verification/` (`run_kraw.py`, `nd_netgen_exact.py`,
`water_exact.py`, `topopt_exact.py`, `emfl_cert.py`) and
`reviews/bound-audit-recheck/` (`sssd_exact.py`, `smallinv_exact.py`,
`emfl_bounds.py`). Their required `data/` inputs are restored from the
archive, including the recheck's `emfl050_3_3.osil`, which the earlier run
copied manually. `commands.json` lists their exact arguments and outputs.

## Other numbers and limits

- **Rocket and methanol LINDO findings:** in `reviews/wave2-small-verification`,
  `python3 v_lindo.py methanol50`, and `python3 v_lindo.py rocket100`,
  `rocket200`, `rocket400`. Inputs include the tracked polished author points
  and reviewer `.sol` files; `logs/krawczyk_<name>.json` saves the existence
  proof and margins (about 9.8e-5, 1.07e-7, 4.7e-8 and 1.9e-7). Regenerating
  those proofs needs no GAMS license. Their numerical point search used GAMS
  **54.3** / CONOPT; the original CONOPT build is not recorded in the retained
  logs, so that search is not fully pinned. Optional GAMS helpers now use
  `gams` and `gdxdump` from `PATH`; their downloaded `.gms` models are not saved
  in this checkout. This does not remove the saved proof inputs.
- **SCIP period error:** `open-instances-wave2/waterno2/scip_unreliable.py`,
  `logs/scip_repro_mult.json`, saved SCIP comparison logs, and the independent
  exactly feasible constructions in `reviews/waterno2-verification/` trace
  the 1.0–2.4 differences. The producer uses SCIP 10.0.2 via PySCIPOpt 6.2.1;
  its five settings on three periods are solver experiments, not smoke tests.
  The cause in the summary remains an inference. BARON cross-checks used
  GAMS 54.3; the BARON build is not pinned in the retained logs.
- **Separator SCIP inconsistency:** saved `sepbranch/` and reviewer
  `scip_claim.py` inputs and outputs trace the 55.69 / 65.12 claims and the
  tolerance-feasible points about 9.4 below the higher claim. These are not
  exactly feasible points or an established solver cause.
- **Camshape and hvycrash listed-point artifacts:** OSIL, archived listed
  points, `v_camshape.py` and `v_hvycrash.py` trace the checks. The summary's
  separate SCIP camshape100 incumbent observation was explicitly not checked
  independently; retain that qualification.
- **Rounding:** `cops/logs/exact_display_checks.json` records five unsafe
  shortest decimal representations in the detailed notes: chain50,
  chain200, catmix200 author, catmix100 reviewer configuration B and catmix800
  reviewer. Safe displays and exact gap calculations are in that file.
  None of those unsafe strings appears in the summary. The earlier COPS
  review also found some detailed-note gaps microscopically understated.
  `check_display.py` distinguishes audit displays from quotations; do not
  interpret all its printed failures as new invalid certificates. The earlier
  water-audit rerun regenerated the topopt p5 certificate. `cert_topopt.py`
  chooses its basis by pivoted QR, which depends on the BLAS thread count;
  with one thread it found a different exactly feasible point, objective
  10.33547432783171797…. Its four p5 displays then fail, giving
  `ok 80, failed 12, skipped 1`. With the committed certificate (objective
  10.335474327803234…), the report's `ok 84, failed 8, skipped 1` is correct.
  The other eight failures are quotations discussed in the audit report;
  the skip is a histogram row. Class, margins and verdict are unchanged.
  The commands above pin one thread to reproduce the regenerated point with
  the recorded software stack; this does not recreate the committed point
  or guarantee the same QR basis across different BLAS builds.
- **Interpretation and historical attribution:** the pattern discussion and
  statements about earlier publications are prose claims, not measured
  quantities. Saved notes and reviews give their sources. This package does
  not turn them into experimental conclusions.

Every summary result and audit classification has a saved script, input and
output trace. Exact regeneration of all historical optimizer-produced
endpoints is not promised: some routines save the resulting bounds rather
than the raw numerical multipliers (notably the audit SOCP solve), and the
original numerical build is not fully recorded. Those are provenance limits,
not reasons to repeat the experiments during packaging.

## Smoke checks and patch record

`tools/smoke.py` creates a different-path copy from inventoried working-tree
files, restores the archive, and copies only the listed OSIL inputs. The
review-response copy restored all 2,063 archived inputs and checked 95 OSIL
hashes. It hides the main tree, the earlier clean worktree and the original cache with
`bubblewrap`, then records file opens with `strace`. Its 25 checks finished
successfully in the review-response rerun, with **138.65 s** summed wall
time, excluding file copying and input restoration. Every check's numerical output matches its prior saved output
line by line after masking only timing values and rebasing checkout paths.
Single-instance checks use explicit line ranges from historical batch logs;
all lines in each selected record, including warnings, are required. No successful
file open read either source tree. The eg/ANN/catmix checks cover cheap
primal evaluations; they do not rerun their long dual searches. The water
cell-slopes check replays the exact saved-record calculation.

The exact commands, comparisons and traces are in `logs/smoke-results.json`
and `logs/smoke/`. Run the suite only when another smoke check is needed:

```bash
python3 "$R/publication/reproduction/tools/smoke.py"
```

Apply patches only to an older checkout lacking the integrated fixes:
the control 01–03, COPS 01–04, small 01–02, and water-audit 01 patches
were checked and applied in that order within each track. The small
`00-shared-ev-kan_iv-applied-by-another-track.patch` was skipped as marked;
the current checkout still needed those two fixes, now recorded in
`patches/01-remaining-portability.patch` along with the remaining network
and optional GAMS path changes. The review response adds
`patches/02-scout-census-portability.patch` for the three scout/census imports.
Keep all patch files as provenance.

See [report.md](report.md) for the exact packaging checks, untracked files
that must be committed, and the open issues. No commit, push, CI inspection
or project-wide verification was performed.

Before committing the package together with the minor-fixes and integration
changes, finish every edit to those files. If integration changes summary
rows, refresh the maps with `tools/build_result_maps.py` first. Then run
these as the last step:

```bash
python3 "$R/publication/reproduction/tools/rebuild_manifest.py"
python3 "$R/publication/reproduction/tools/check_package.py"
```

The rebuild updates only `manifest.json`; it runs no experiment. The checker
lists each missing file, stale hash or unlisted cross-directory input and
fails until the manifest is current. During ongoing edits, targeted map,
syntax and smoke checks can use `--checks maps syntax smoke`; that does not
replace the final full package check. `numeric_evidence` records literal
numbers in their saved source files. `reported_row` retains the summary's
rounded displays and prose; the checker checks the explicit numeric evidence,
not the scientific validity of rounding or every number embedded in prose.
See `report.md` and `files-to-commit.json` for required commit dependencies.
