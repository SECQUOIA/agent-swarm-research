# Stage 5 minor corrections

All eight accepted findings in `stage05-r01-assessment.md` are resolved. I read
all five complete review reports before editing. No accepted issue is deferred.
No scientific input, saved objective, bound, selection, timing result, legacy
module or tracked original repository file was changed. `PROCESS.md` and the
other paper were not edited.

## Changes

1. The computational section now expands SCM and DCM as static-cost measurement
   and dynamic-cost measurement, consistent with the source and foundations.
2. A short main-text note explains the intended dropped-zero labels and the
   optimizer's uniform spacing-map shift. Both copies of the source-kinetics
   README give the source lines, the intended sample-index formula, why every
   pairwise difference and feasible schedule is unchanged, and the CSV's original
   and archived filenames. The two README copies are byte-identical. Only this
   entry's hash changed in `archive-manifest.json`.
3. The synthetic-case paragraph specifies independent standard-normal entries
   within each array and the exact same-seed 48-row prefixes of the 96-row arrays.
   It explicitly avoids describing six independent replications.
4. The all-diagonal replay explicitly checks exact cardinality `sum(z) == k`
   before evaluating the point. Its verified-field list names cube and cardinality
   feasibility; the existing exact point routine checks the cube.
5. The fresh model checker now checks nuisance-block symmetry and positive
   definiteness, exact stationarity `C G + B^T = 0`, and equality of the direct
   Schur matrix, quadratic matrix and stored mixture information. Empty anchors
   use the parameter block directly. Only after these identities does it accept
   the inverse weight and mixture lower bound.
6. The computational appendix now distinguishes the grids: reference matrix and
   nuisance witness at `10^8`, bridge regression coefficients at `10^12`, features
   at `10^18`, scores at `10^8`, and final logarithms at `10^12`.
7. The spacing wrapper now calls `noisy_markov_spacing_design.py first-case`.
8. Validation checks both the archive and new-source manifests before any
   scientific validation runs. Hash mismatch raises an explicit error naming the
   manifest and file. Source hashes were refreshed; manifest files are excluded
   from their own lists to avoid self-reference. Documentation distinguishes hash
   integrity from scientific witness verification. The validation report retains
   the archive count and adds the new-source count.

## Focused validation

Evidence is in `verification/stage05-corrections/check.py`, `checks.json`,
`change-audit.json`, and `spacing-reproduced/`. The checks used the coordinator's
base-only Python 3.13.11 environment; Gurobi, CVXPY and Clarabel were confirmed
absent. The complete focused suite passed in 6.64 seconds on this run.

- Both manifests matched: 159 archive entries and 11 new-source entries, both
  in the repository and an independent temporary supplement copy.
- The current four exact fresh mixtures passed the strengthened Schur checks,
  all 224 joint-information identities and all 224 support prices. The associated
  model diagnostics also passed: 864 ODE entries and 16 high-precision rows.
- A perturbation of an actual saved nuisance witness was rejected by stationarity
  even though choosing the inverse of its quadratic matrix satisfies the old
  inverse-weight premise. A changed stored Schur matrix and an indefinite
  nuisance block were independently rejected.
- The actual all-diagonal portion of the replay function was executed in
  isolation, using its parsed statements rather than duplicating its checks.
  The current point has exact cardinality 16. Its full exact dual, PSD factor,
  diagonal domination, trace, lower bound and separation all passed. A changed
  point was rejected by the new cardinality assertion.
- Altering a listed new checker, the fresh result, or a legacy checker in the
  temporary copy made the actual `validate.py` command fail at preflight before
  any scientific stage started. Restoring each file restored all hashes.
- `reproduce.py spacing` completed in that temporary copy, with command
  `noisy_markov_spacing_design.py first-case`. It returned
  `surrogate_hull_optimal_tolerance`, retained its complete log, and exported its
  changed proposal JSON. Wrapper time was 4.42 seconds. No frozen archive bytes
  changed. These are new reproduction observations, not replacements for the
  manuscript's historical timings or certificates.
- A forced clean `latexmk -pdf -gg -interaction=nonstopmode -halt-on-error
  -outdir=build main.tex` completed successfully: 61 pages. The final log has no
  warnings, undefined references, overfull boxes or underfull boxes.

The frozen-file comparison found only the ten intended manuscript/supplement
files changed. All legacy and saved scientific-result bytes remain unchanged.
The separate original source-kinetics README was updated exactly as authorized.
The coordinator's already completed full 46-certificate and full source-ranking
baseline was not redundantly rerun; these checks exercise the changed premises,
preflight behavior and CLI directly.
