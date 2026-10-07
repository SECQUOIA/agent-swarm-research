# Standalone computational supplement

This directory supports the paper **Globally certified measurement selection
with correlated errors**. It can be copied outside the repository. The main
validation requires Python, NumPy, SciPy, SymPy and mpmath; it does not require
Gurobi, CVXPY, a network connection, the original repository, or a literature
folder once dependencies have been installed.

The mathematical paper is the specification. Exact certificates apply to the
saved rational input arrays and the stated finite feasible families. They do
not validate a physical noise model, make rounded exponential derivatives exact,
or prove global identifiability. Numerical solver results and sensitivity checks
are explicitly different evidence from exact certificates.

## Validate

From this directory:

```sh
uv sync --frozen
uv run --frozen python validate.py
```

Alternatively, install the dependencies in `pyproject.toml` and run
`python validate.py`. The locked environment was resolved with Python 3.13.11;
the archived and fresh paper runs used NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0
and mpmath 1.3.0. Validation sets numerical-library thread counts to one.

The command first verifies both `archive-manifest.json` and
`source-manifest.json`, including the new checkers and saved fresh result.
Manifest files are excluded from their own hash lists to avoid self-reference.
This integrity check is separate from the following scientific validation:
the command runs finite proof checks,
checks all 2,347 public-source schedules by independent full-covariance rational
inversion, validates the kinetic derivatives with independent ODE and 70-digit
matrix-exponential formulations, checks the fresh nested-anchor witnesses, and
replays all 46 principal saved certificates. It ends with a separate exact
recomputation of the fresh full-block experiment. Results and logs go to
`results/`; the frozen `legacy/` and `source_kinetics/` files are not overwritten.
The full exact replay alone took about 129 seconds in one observed development
run, largely because the original direct-rational spacing and large separator
certificates are retained. Runtime varies by machine. `--quick` skips three
expensive separator replays but is **not** the full paper validation.

`results/validation.json` records a completed full run of an earlier
`validate.py`, from before the stage-5 correction that added verification of
`source-manifest.json`; it therefore has no `source_manifest_files` entry and
is not a report from the current checker. A full passing run of the current
`validate.py` (same SHA-256) on an extracted copy of this supplement, with 159
archive-manifest and 11 source-manifest files verified, is kept outside the
supplement in the repository record
`paper-correlated-measurements/verification/final-root/validation.json`.
A new run of `validate.py` replaces `results/validation.json`. A successful software
check is finite evidence for the implemented instances; the manuscript contains
the general proofs. None of these checks is external peer review or Lean
verification. The PSD approximation-set fixtures are tiny proof checks, not an
implementation or timing study of the large theoretical polynomial algorithms.

## Reproduce numerical searches separately

The paper's reported historical times remain the original single-run timings.
Replaying exact witnesses does not rerun a numerical optimizer and does not
reproduce a solver's stopping time. New searches may return different witnesses
or statuses; record those outcomes instead of expecting identical wall times.

The supported wrapper runs each old producer in a fresh writable copy of the
archive and exports changed files and the complete log. It never writes the
frozen inputs. Results appear under `results/reproduced/STUDY/`; an existing
output directory is refused rather than overwritten. Some producers explicitly
reuse exactly matching archived precursor runs; that reuse remains recorded.

```sh
uv run --frozen python reproduce.py block4
uv run --frozen python reproduce.py block16
uv run --frozen python reproduce.py partial
uv run --frozen python reproduce.py spacing
uv run --frozen python reproduce.py robust48
uv run --frozen python reproduce.py robust96
uv run --frozen python reproduce.py robustdense48
uv run --frozen python reproduce.py robustdense96
uv run --frozen python reproduce.py separator48
uv run --frozen python reproduce.py separator96
uv run --frozen python reproduce.py separator192
```

The synthetic, scalar-kinetic and fixed-physical-grid pipelines also run the
historical Gurobi outer-approximation comparator. An appropriate Gurobi license
and the optional package are needed for those branches:

```sh
uv run --frozen --extra proposals python reproduce.py synthetic
uv run --frozen --extra proposals python reproduce.py kinetics48
uv run --frozen --extra proposals python reproduce.py kinetics96
uv run --frozen --extra proposals python reproduce.py grid
uv run --frozen --extra proposals python reproduce.py diagonal-kinetics
```

The last command uses CVXPY/Clarabel for a **proposal**; the existing exact dual
is verified without those packages. Historical kinetic SLSQP and SDP failures
remain in the archive and are discussed in the paper. The corrected covariance
oracle is `legacy/covariance_dense_oracle.py`; the precision-space prototype is
preserved only for historical reproducibility and its documented failure mode.
The simple commands above use archived model specifications and source hashes.
They do not fetch third-party optimization software or literature.

Fresh exact experiments and the source ranking generator can be reproduced with
explicit new output files. The source ranking replay needs a locally obtained
input: `source_kinetics/prepare_input.py` retrieves the pinned numerical table
and verifies its SHA-256 before writing it to an ignored local path. Use
`--from-file PATH` to verify a separately obtained copy. The scientific checks
do not download inputs; see [source input provenance](source_kinetics/README.md).

```sh
uv run --frozen python fresh_experiments.py all --output results/fresh-rerun.json
uv run --frozen python source_kinetics/prepare_input.py
uv run --frozen python source_kinetics/exact_rankings.py --output results/source-rankings-rerun.json
uv run --frozen python source_kinetics/check_rankings.py --record results/source-rankings-rerun.json --output results/source-rankings-rerun-check.json
```

For fresh-study timing comparisons, set `OPENBLAS_NUM_THREADS=1`,
`OMP_NUM_THREADS=1`, and `MKL_NUM_THREADS=1` before launching Python. The
fresh producer records those variables. It saves exact mixture weights, matrices,
nuisance/weight witnesses, support prices, model arrays and optimizer status.
Setup, numerical pricing/search, exact certification and total time are separate.
The small dense comparator uses the same incumbent and exact cardinality family.

## File and table map

All names in the middle column are under `legacy/results/`, unless stated
otherwise. JSON fractions, not rounded display fields, carry the certificates.

| Paper material | Main artifacts | Treatment |
|---|---|---|
| Public-source kinetics | `source_kinetics/exact-rankings.json`, CSV, checker, README | All exact objective values, optima and margins; pinned public input; independent full-covariance check |
| Six synthetic scalar rows | `noisy-markov-extended-benchmark.json`, `noisy-markov-extended-certificate-0.json` through `-5.json` | Numerical producers plus exact true-design bounds; seeds 0–2 at each size |
| Four scalar kinetic rows | `noisy-markov-kinetics-probe.json`, `noisy-markov-kinetics-n96-probe.json`, four `noisy-markov-kinetics-certificate-n*-*.json` | Separate per-grid covariance instances; exact decimal-input certificates |
| Dense fixed-split and all-scalar separation | Three `dense-design-*-certificates.json` and three `dense-all-splits*-certificates.json` files | Ten continuous intervals and ten all-split witnesses; exact common-model comparisons |
| All-diagonal separation and negative probe | `diagonal-split-kinetics-certificate.json`, both `diagonal-split*-probe.json` | Positive kinetic rational dual; unsuccessful synthetic fixed-point witness remains numerical |
| Spacing and arithmetic refinement | `noisy-markov-spacing-kinetics-{certificate,integer-certificate,refined-certificate}.json` | Same data/incumbent; separate arithmetic and pair-bound improvements |
| Complete packets | `block-snapshot-d4-probe.json`, `block-snapshot-d16-probe.json` | Numerical negatives retained: identical greedy designs, tighter dense bounds |
| Fresh full-block improvement | `results/fresh-all.json`, key `blocks` | Exact 56-schedule experiment plus fresh theoretical constant comparisons; does not relabel archived outputs |
| Partial observation | `partial-observation-trace-probe.json`, four `partial-observation-trace-certificate-*.json` | Four normalized trace guarantees; old L=6 and weaker bounds retained |
| Robust comparisons | `robust-kinetic-n48.json`, `robust-kinetic-n96.json`, `robust-dense-n48.json`, `robust-dense-n96.json` | All scenarios, nominal/greedy/exchange branches and reference-generation costs |
| Robust exact guarantees | `robust-kinetic-n48-certificate.json`, `robust-kinetic-n96-certificate.json`, `robust-kinetic-n96-polished-certificate.json` | Unknown normalizers enclosed; original and polished incumbents separated |
| Fixed physical grids | `fixed-physical-grid-benchmark.json`, `fixed-physical-grid-refined-transfer.json` | Primary first-price timeouts, diagnostic run, numerical bounds and full cost provenance |
| Five separator certificates | `latent-separator-n48-b8-certificate.json`, `latent-separator-n{96,192}-b{12,16}-certificate.json` | Exact true-design bounds, saved arbitrary nuisance witnesses; b16 certification cost retained |
| Fresh nested-anchor study | `results/fresh-all.json`, key `nested` | 56 identical feasible schedules at every anchor level; exact mathematical hull intervals, same incumbent |
| Independent model validation | `results/model-validation.json` | 864 ODE entries, 16 high-precision rows, 224 exact Schur identities/supports |
| Theory checks | `checks/stage02.py`, `checks/stage03.py`, `checks/stage04.py` | Exact and numerical scope identified separately in their result files |

The archived comparison JSONs retain additional timings, model-equality and
input-hash checks. Early n12/n24/L6 proofs of concept, numerical validation
records, obsolete larger constants, capped runs and smaller-block sweeps are
retained as historical evidence; their role and superseding results are described
in the manuscript appendix. The archive includes no adjacent ODE-relaxation,
validated-tube, storage, MINLP or unrelated paper developments.

## Provenance and portability

`archive-manifest.json` gives original repository paths for attribution and
SHA-256 hashes for every copied code, data and result file. Those original paths
are descriptive strings; no checker resolves them outside this directory.
`legacy/` modules and result files are byte-preserved copies of the repository's
measurement research implementation. Stage checks are adapted to local output
paths, and Stage 3's explicitly identified audit helpers are included locally;
their historical `main` routines are not invoked by validation. The new wrappers,
fresh study and model checker live at this directory's top level.

The public CSV originates from `dowlinglab/measurement-opt` at commit
`430090e610446aab88328ce495ffb15b684c56c4`, file
`kinetics_source_data/Q_drop0.csv`. SHA-256:
`54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca`.
See `source_kinetics/README.md` for its row order, feasible family, redundancy
convention and source URL. No authors' pickled selections or third-party
literature PDFs are included. We make no new licensing assertion about the
public sensitivity data. Its numerical provenance does not establish physical
sensitivity-generation provenance.
