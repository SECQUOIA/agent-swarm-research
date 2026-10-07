# Paper artifact

This directory indexes the paper's saved evidence and records targeted checks
from a fresh `/tmp` copy. It adds no research results. Paths in `claims.json`
are relative to the repository root, which contains `paper-open-minlplib/` and
`research-20260929/`.

AI agents (Anthropic Claude and OpenAI GPT models), working under the authors'
direction, selected the instances, devised the certificate constructions, wrote
the proofs, implemented the computations and re-implemented them separately,
checked code and proofs, ran the solver experiments and the audit, searched the
literature and drafted the manuscript **[authors to confirm, as in the
declarations of the paper]**. Section 2.6 of the paper states how the
implementations were produced and checked, what "separately written" means, and
the resulting common-mode risk.

"Round 1", "round 2" and "round 3" in these files, as in "the round-1 reruns" or
"the round-3 sources", refer to the authors' internal review rounds before
submission, not to a review by the journal. Folder names such as
`development/reviews/round1/` keep these names.

| File | Purpose |
| --- | --- |
| `claims.json` | 27 reproduction-register rows and 38 distinct reported-value claims, with paper labels, displayed values, input/code/output SHA-256 hashes, check recipes, expected outputs, recorded times, evidence levels, status and verification labels per instance and per named component, and trust tags. |
| `check_claims.py` | Recomputes hashes and checks every file, every LaTeX label, the displayed values and the status labels (per instance and per component) of every register row, the agreement of the register with `RUNS.md`, and claim IDs and reported-value coverage. Uses the Python standard library. |
| `build_claims.py` | Rebuilds the index from the register (`sections/I-reproduction.tex`), `RUNS.md`, `numbers.json` and the earlier reproduction maps. Reads evidence; runs no scientific script. |
| `RUNS.md` | For every register row: full checker paths, arguments, the recorded command, expected output, recorded times and run records; the reruns made during internal review; the guarded KAN replay; run records that the supplement does not print. |
| `HISTORY.md` | Earlier and superseded certificates and displays, including strings in older records that must not be read as bounds, historical checkers, and history that the supplement does not print. |
| `RELEASE.md` | SHA-256 of the two PDF files of the release. |
| `prepare_paper_inputs.py` | Paper-only input preparation: restores and checks the archived inputs, verifies the 69 models of the paper and lists the 26 unused models of the manifest; never downloads. Standard library only. |
| `run_short_checks.py` | Copies the selected scripts and inputs into a new `/tmp/minlp-artifact-*` directory, limits CPU affinity to at most four cores, and runs targeted checks there. |
| `path-edits.json` | Lists the minimal portability edits. |
| `logs/check_claims.log`, `logs/build_claims.log` | Output of the last rebuild and validation of the index. |
| `logs/short-checks.json`, `logs/short-checks-r4/` | The 15 short checks of the final recipe test (`logs/recipe-test.log`): actual commands, elapsed times, result comparisons, and the output of each check. |
| `logs/short-checks-packaging.json` | The earlier packaging run with `--eg-int`: actual commands, elapsed times, result comparisons, the `eg_int_s` array comparisons, and initial setup failures followed by their corrections. |
| `logs/recipe-test.log` | The setup recipe below run as written in a fresh copy, with the short checks and a before/after listing of the real `~/.cache`. |
| `logs/corrected/` | A fresh-copy check of the corrected runner, without repeating the five-minute `eg_int_s` run. |
| `logs/*.log` | Other checker outputs, including the regenerated `eg_int_s` audit (a separate run from a clean copy). |

## Release contents and placeholders

The code, certificate data, exact point definitions, logs, the number file and
the claim register form the archive that accompanies the paper; it will be
deposited at **[archive DOI, to be added before submission]**. Licence:
**[authors to choose]**. The archive contains the repository tree described
below, the archived model files and inputs, and the two built PDFs
(`paper-open-minlplib/build/main.pdf` and `supplement.pdf`).

`check_claims.py` validates the sources and the evidence (hashes of inputs, code
and outputs, paths and labels); it does not identify the PDF files, whose SHA-256
hashes `RELEASE.md` records.

The SCIP reproducer `fm336` with its exact witness and the other SCIP witnesses
(`research-20260929/publication/scip-bug/`, `RUNS.md` row R24), and the exactly
feasible points and existence certificates behind the audit's 22 refutations
(Section S4; `RUNS.md` rows R22 and R23), are in the archive.
As of 2026-10-05, the authors have not yet reported the SCIP defect to the SCIP
developers or sent the refutations to the MINLPLib maintainer.

## The claim index

The 38 reported-value entries use `numbers.json:claims_table[i]`. Three
campaign rows also appear in `tab-claims.tex`; they are indexed once. The 27
register entries retain every label in grouped rows. `checker_recipe` holds the
checker paths and arguments of the row from `RUNS.md`, and
`register_checkers_latex` the file names printed in the register; commands
containing `<...>` require the indicated instance, period or grid arguments.
`$SCRATCH` denotes a disposable output directory. `recorded_commands` are the
runs of the row's checkers recorded by the earlier package, matched by working
folder and script path (a run that names only instances of other rows is left
out); `historical_commands` preserve older run provenance.
Their displays do not override the paper's `numbers.json`, which stores the
generated certified displays (bounds, primal ends, gaps and derived margins)
with their exact values or certificate ends, sources and rounding directions;
run times and fixed metadata come from the run records and the register.

Each register row states its status (Section 2.6 of the paper) in the last
column of the register. `build_claims.py` copies it into `status`, writes one
status word per instance into `status_by_instance` (a parenthesis such as
"(eg_disc2_s: partial second)" applies to the instances it names; a parenthesis
that names a part of the result, such as "(emfl enclosures: weaker second)",
goes into `status_by_component`), and maps each word to
`verification_label_by_instance` or `verification_label_by_component`:
*verified by a separately written implementation* for "verified"; *proved* for
"proved", "weaker second" and "partial second" (proved, with a separately
written implementation that certifies a weaker bound or part of the domain);
*floating-point output* for the solver campaign. A row's `verification_label`
is the weakest of its instances, its components and its status word; for
example, the `eg` row is *proved* because of `eg_disc2_s`, the points row
because the point of `etamac` has one implementation, and row R23 because the
displayed `emfl` enclosures rest on one implementation (the other implementation
proves wider enclosures, which suffice for every verdict on listed values).
The reported-value entries compare the displayed number exactly with a
certified bound. `value_evaluation` says what that number is: as reported
(`none`), the objective at a listed point evaluated exactly (`exact`), or an
ordinary high-precision evaluation without an enclosure (`numerical`). The
listed point of `etamac` is of the last kind, so its entry is *computed*. The
one-hour points are also `numerical`, but their entries are *proved*: the
returned objective value of the trace file (`returned_value`), widened by half
a unit of its last digit, lies beyond the certified bound, which proves that
the returned point is not exactly feasible. The runs used the GAMS files; for
`etamac`, `pricing050`, `pindyck`, `chain50` and the KAN instances, whose GAMS
and OSIL forms `tab:sem-gams` compares only at sample points, this conclusion
assumes that the two forms define the same model, as Section S6.3 states, and
`trust_qualifiers` records the assumption. For campaign rows the violations
are floating-point output (`violation_verification_label`). Evidence levels and
qualifications remain in `evidence_level`, `trust_qualifiers` and the component
fields. Hash validation
establishes packaging consistency; it does not establish a mathematical claim.
Trust tags `read`, `code` and `thm` apply to every row; `int`, `mp`, `fp` and the
recorded exponential/power audit distinguish additional dependencies.

## Environment and input roots

The recorded environment in
`research-20260929/publication/reproduction/environment.json` is Python
**3.13.11**, packaged by Anaconda, GCC 14.3.0, with the following pins from
`requirements.txt`:

| Package | Version |
| --- | --- |
| mpmath | 1.3.0 |
| numpy | 2.5.1 |
| scipy | 1.18.0 |
| sympy | 1.14.0 |
| pyscipopt | 6.2.1 |
| cvxpy | 1.9.3 |
| clarabel | 0.11.1 |
| highspy | 1.15.1 |

PySCIPOpt uses SCIP 10.0.2. The targeted checks used this same Python and
package stack. The `dtoc5` checker also needs the system GMP shared library
(`ctypes.util.find_library('gmp')`); GMP is not a pip requirement. The solver
campaign has a separate environment: GAMS 54.3.1, BARON 26.5.27, Gurobi 13.0.2
and SCIP 10.0.3, plus the relevant solver licences.

Several scripts write into their own `logs/` folders and some replace stored
evidence, so every command runs in a disposable copy `$WORK` of the archive,
with at most four single-threaded processes at a time. A session starts as in
Section S7.1 of the supplement; the unpacked archive `$ARCHIVE` is only read:

```bash
ARCHIVE=/path/to/unpacked/archive          # read only
WORK=$(mktemp -d /tmp/minlp-work-XXXXXX)   # disposable: rm -rf "$WORK"
cp -r "$ARCHIVE"/. "$WORK"/ && cd "$WORK"
export HOME="$WORK/home" XDG_CACHE_HOME="$WORK/home/.cache"
export TMPDIR="$WORK/tmp" PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
R="$WORK/research-20260929"; P="$WORK/paper-open-minlplib"
export MINLP_REPO_ROOT="$WORK" EG_AUDIT_R="$R" MINLPLIB_OSIL_ROOT="$WORK/osil"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
mkdir -p "$TMPDIR" "$MINLPLIB_OSIL_ROOT" "$HOME/.cache/minlplib/minlplib"
cp "$R"/publication/minlplib-status/pages/models/osil/*.osil \
   "$MINLPLIB_OSIL_ROOT"
ln -s "$MINLPLIB_OSIL_ROOT" "$HOME/.cache/minlplib/minlplib/osil"
python3 "$P/artifact/check_claims.py" --repo-root "$WORK"
python3 -m venv "$WORK/venv" && . "$WORK/venv/bin/activate"
python -m pip install -r "$R/publication/reproduction/requirements.txt"
python "$P/artifact/prepare_paper_inputs.py"
cd /tmp && python "$P/data/make_tables.py"
```

- **Input roots.** The archive holds the 69 model files of the paper in the
  folder copied above. `MINLPLIB_OSIL_ROOT` replaces implicit reads in the
  relocated review scripts; the other research scripts read
  `~/.cache/minlplib/minlplib/osil`, which, with `HOME` inside the copy, is a
  link to the same archived input root. `MINLP_REPO_ROOT` selects archived
  dossiers and primal points used by `lnts`, the `dtoc5` display comparison, the
  KAN consistency audit and the Gibbs checker
  `development/dossiers/small-checks/r2/gibbs_cert.py`; it must preserve the
  repository layout. `EG_AUDIT_R` selects reference recordings and research
  logs. The KAN review driver uses its bundled `osil/` directory, and
  `dtoc5/review.py` reads its three bundled inputs. Bundled Python modules are
  script-relative.
- **Isolation.** With `HOME`, `XDG_CACHE_HOME` and `TMPDIR` inside `$WORK` and
  the packages in `$WORK/venv`, the recipe and the checkers of the register
  write nothing outside `$WORK` and the folders `/tmp/minlp-artifact-*` of the
  short-check runner, and nothing into the user's `~/.cache`. Two archived
  drivers use absolute paths outside `$WORK`: the driver of the guarded KAN
  replay, `development/reviews/round1/kan-guard/run_replays.py`, expects its
  tree in `/tmp/kan-guard` and six cores (the section "Guarded KAN replay"
  below reruns the same searches inside `$WORK`, one process at a time), and
  the campaign driver `research-20260929/publication/solver-runs/driver.py`
  names the GAMS installation of the original machine.
- **Order.** The validator runs before anything is written into the copy,
  because `make_tables.py` rewrites `data/numbers.json` and `data/check.log`
  with the date of the run (the index then reports them as changed).
- **Paper-only inputs.** `prepare_paper_inputs.py` runs the archived
  `research-20260929/publication/reproduction/tools/prepare_inputs.py` of the
  copy, which restores the saved ignored inputs from
  `inputs/saved-inputs.tar.gz` and checks every hash; that script exits with a
  nonzero status because 26 further models of its manifest are absent.
  `prepare_paper_inputs.py` exits with status 0 if and only if the saved inputs
  are intact, the 69 models of the paper are present with the SHA-256 of the
  manifest (and of `numbers.json`, where recorded), and every missing model is
  one of the 26 that the paper does not use, which it prints as "not needed by
  the paper"; a changed file or any other missing model makes it fail. It never
  downloads (`prepare_inputs.py --download` would fetch the 26 from
  `https://www.minlplib.org/osil/` and reject any file whose hash differs).
- **Short runner.** The short-check runner sets all roots to its fresh copy and
  copies the hash-checked paper OSIL inputs into its own `osil/` folder.

This recipe and the short checks below were run as written in a fresh copy
(`logs/recipe-test.log`); the long replays of Tiers 2 and 3 were not repeated
under it.

## Tier 1: integrity and short replay

After the setup above, run in the same shell:

```bash
python "$P/artifact/run_short_checks.py" --repo-root "$WORK" --logs "$WORK/short-logs"
```

The integrity check of the setup takes seconds. The runner replays the `lnts`
and `dtoc5` certificates, regenerates the three short KAN r3 searches, runs the
auditor, negative and boundary tests, checks copies, and runs the three `eg`
review scripts against stored evidence. Allow a few minutes. It uses three
concurrent single-threaded checks within at most four CPU cores. Scientific
outputs remain in the printed `/tmp/minlp-artifact-*` tree. It does not rerun
the long certificates.

Expected short-check results:

- `lnts`: `PASS: all four models, exact sign certificates, optimum enclosures, comparisons, and negative tests`; every certificate field matches the saved file.
- `dtoc5`: `PASS; seconds ...`; all result fields match except CPU affinity and elapsed time. The exact primal/dual gap equals the completed-square losses; display and boundary checks also pass.
- KAN r3: all result fields match except `time`; `kan_audit` ends with `ALL AUDIT CHECKS PASSED`.
- `eg`: `ALL AUDITOR TESTS PASSED`, `ALL NEGATIVE TESTS PASSED`, and `ALL COPY CHECKS PASSED`; the numeric, range and stored-artifact checks of the review scripts end in PASS.

The copy check permits exactly the documented cache-location substitution in
`ev.py` and `eg_model.py`; it compares every other byte of these recording
modules with the original research scripts. Undoing the audit wrappers still
recovers the original certifier. No numerical formula was changed.

Add `--eg-int` to regenerate the whole short `eg_int_s` tree and audit its
leaves. The driver uses `--only int --workers 1 --timeout 600` and a new output
directory. The recorded packaging run (`logs/short-checks-packaging.json`, `logs/eg_int*.log`) took **323.818 s**. Its recording arrays
were byte-identical to the saved arrays, and its audited result arrays matched
except `time`. Its final comparison was:

```text
RESULT: PASS (PARTIAL/SAMPLE run; 33385 leaves compared or checked; 1244140388 exp/power results audited, 0 violations)
```

"PARTIAL/SAMPLE" refers to the three-instance suite: this run covers all
`eg_int_s` leaves and does not rerun `eg_disc_s` or `eg_disc2_s`. The complete
stored suite records 1,234,542 leaves and 63,017,129,222 audited results.
The review script checks those stored totals.

The reruns made during internal review (guarded KAN replay, `eg` dyadic primal
check, audit and display checks) are recorded in `RUNS.md`.

## Tiers 2 and 3: longer replay and regeneration

Use the disposable copy above. Follow the checker paths and commands of each
row in `RUNS.md`, and use the grid and chunk arguments in the existing
`research-20260929/publication/reproduction/README.md`. Tiers follow Section 10
of the paper: recorded wall time per instance (summed over its parts), Tier 1
under 10 minutes, Tier 2 under one hour, Tier 3 longer. A result's tier is that
of the replay of its displayed value by the checkers that `RUNS.md` names first;
other implementations can take longer. The recorded times are
from the register and historical logs on a shared machine, not guarantees;
`RUNS.md` gives the times of every code. Run at most four single-threaded
processes; explicitly pass `--workers 4` or less to the existing `eg` driver,
whose historical default remains eight.

| Check or regeneration | Recorded time and tier |
| --- | --- |
| `lukvle10` stage bounds | About 5–6 min; Tier 1. |
| Gibbs bounds, `ex6_2_5` / `ex6_2_7` | 258 / 77 s; Tier 1. |
| `powerflow0039*` exact saved-leaf checks | 78 / 24 s; Tier 1. |
| `catmix` dynamic programs | Replay of the displayed bounds 20–46 min per instance; Tier 2. The first code, which certifies the weaker bounds, took 1,049–4,602 s (Tier 3 for `catmix800`, 4,602 s). |
| Six KAN searches | 22 s to 1 min per `r3` model (Tier 1), 87 s to 20 min per `r5` model (Tier 2); the guarded replay below takes 23–59 s and 12–20 min. |
| `eg` suite under the accuracy auditor | 16,703 s over 44 jobs: `eg_int_s` 465 s (Tier 1), `eg_disc_s` 1,456 s (Tier 2), `eg_disc2_s` 14,782 s (Tier 3). |
| `waterno2_06` saved-record coverage and exact path | 13 / 11 s; the pair bounds (about 60 CPU-h) make the result Tier 3. |
| Remaining `waterno2` stored-target period checks | `waterno2_09` 35 min and `waterno2_12` 49 min (Tier 2), `waterno2_18` 2.5 h and `waterno2_24` 3.5 h (Tier 3). |
| ANN saved-node replay and verification | Replay 33 min and 1.6 h; verification about 1.2 h wall on two processes (2.0 CPU-hours); Tier 3. |
| One-hour solver campaign | 129 one-hour runs; requires the campaign builds and licences; floating-point outputs. |

These long runs were not repeated for packaging. The earlier reproduction
package retains `result-map.json`, `audit-map.json`, `commands.json`, and
`manifest.json`; this paper index computes its own current hashes without
rewriting those historical files.

## Guarded KAN replay (register row R20)

The guarded copy of the second KAN bounding code (path (I) of Section S1.9) is
archived with its logs in `development/reviews/round1/kan-guard/`. Its driver
`run_replays.py` is the record of the original run: it expects the tree in
`/tmp/kan-guard` and starts six processes. The commands below rerun the same
searches inside `$WORK` instead, one process at a time, and compare each result
with the archived one. Run them in the shell of the setup above. The code reads
the OSIL files from `~/.cache/minlplib/minlplib/osil`, which the setup links to
the archived inputs, and writes `<instance>.bnb.json` into the `logs/` folder
next to its own copy.

```bash
A="$P/development/reviews/round1/kan-guard"   # archived guarded code and logs
G="$WORK/kan-guard"; mkdir -p "$G/logs"
cp "$A/kan_bnb_rigexp.py" "$G/"
export PYTHONPATH="$R/reviews/wave3-verification:$R/open-instances-wave3/kan"
for n in kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9; do  # r5: kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8
  python -u "$G/kan_bnb_rigexp.py" "$n" 4e-11 7200 1024 > "$G/logs/$n.guard.log" 2>&1
  python - "$n" "$A/logs/$n.bnb.json" "$G/logs/$n.bnb.json" "$P/data/numbers.json" <<'PY'
import json, sys
from fractions import Fraction
n, old, new, numbers = sys.argv[1], *(json.load(open(f)) for f in sys.argv[2:])
diff = sorted(k for k in old.keys() | new.keys() if k != 'time' and old.get(k) != new.get(k))
ok = (not diff and new['done'] and new['open'] == 0 and new['minquad_stats']['guard_entries'] == 0
      and Fraction(new['lower_bound']) >= Fraction(numbers['kan'][n]['L']['exact']))
print(n, 'PASS: as archived except time; no guard trigger; bound >= reported L' if ok else 'FAIL', diff)
PY
done
```

Each search is single-threaded, and the loop runs them one after another. The
recorded times are 23–59 s per `r3` model and 12–20 min per `r5` model (Tiers 1
and 2), so the three `r5` models, added to the loop, take about 50 minutes.
Expected output: one `PASS` line per instance. The staging and the three `r3`
replays with their comparisons were run as written in a fresh copy, on one core
in 88 s; all three passed (`logs/kan-guard-recipe-test.log`, which also records
a negative control of the comparison). The `r5` replays were not repeated.

## Regeneration limits

- Time-limited ANN runs do not reproduce an identical frontier under different machine load. Replay uses saved node counts. The second implementation's region lists were not kept; replay and leaf extraction reconstruct them.
- `catmix` per-stage chord values were not saved. Verifying the dual calculation reruns the dynamic program (evidence level rerun).
- The audited `eg` suite stores its results; earlier unaudited `eg_int_s` and `eg_disc_s` per-leaf reviewer outputs were not saved. Their comparisons use the original recording and certification logs. `eg_disc2_s` has saved per-leaf results.
- Fresh `optcdeg2` calibration, powerflow SDP, water SCIP target selection, and `emfl` cone-program solves can produce different valid bounds. In particular, the `emfl` rational dual vectors were not saved, only the resulting enclosures, so their check is a rerun.
- The `topopt-cantilever_60x40_50` existence certificate does not store its basis; it is regenerated, not replayed. With one BLAS thread a different exactly feasible point results; the archived certificate gives the displayed value and the same class and margin.
- Some regenerated water incumbents lie below stored period bounds because they are only tolerance-feasible.
- Exact bytes of historical optimiser outputs are not promised across solver or BLAS builds. Historical upstream pages and externally reported claims require the saved snapshot and source documents.
- Replay was run on one machine. Checkers outside the review and audit directories, apart from `gibbs_cert.py`, were not made relocatable; they read the cache folder above, which the setup links to the archived input root inside `$WORK`.

## Rebuilding the index

Any edit to a hashed file makes the index stale, and the validator then fails
on purpose. After the last edit, copy the builder and validator out of the
repository and run them (`REPO` is the repository root):

```bash
cp "$REPO/paper-open-minlplib/artifact/build_claims.py" /tmp/minlp-build-claims.py
cp "$REPO/paper-open-minlplib/artifact/check_claims.py" /tmp/minlp-check-claims.py
python3 /tmp/minlp-build-claims.py --repo-root "$REPO" \
  --output "$REPO/paper-open-minlplib/artifact/claims.json"
python3 /tmp/minlp-check-claims.py --repo-root "$REPO"
```

The index hashes `sections/I-reproduction.tex` and `RUNS.md`, so if the counts
quoted in Section S7.1 change, update them and rebuild once more. The validator
rejected deliberate controls for a wrong SHA-256, a missing file and a missing
label (`logs/validator-controls.log`), and for an empty display of an instance,
a "verified" label on a weaker status, and a register row that `RUNS.md` lacks
or labels differently (`logs/validator-controls-r2.log`). `RELEASE.md` is
written after the final build and is not hashed.


## Public export index

`claims.json` is the historical upstream claim register. It includes 581 input
paths absent from the committed source snapshot. `claims-public.json` records
current digests for the 1,337 retained public files and preserves expected
original hashes for missing inputs in `external_artifacts`. Validate the retained
files from the MINLP root with:

```sh
python paper-open-minlplib/artifact/check_claims.py --repo-root . \
  --claims paper-open-minlplib/artifact/claims-public.json
```

This is package metadata validation, not a new proof or complete scientific
replay. The public transfer does not copy ignored inputs. Original hashes
identify upstream bytes; current hashes identify the retained public files.
