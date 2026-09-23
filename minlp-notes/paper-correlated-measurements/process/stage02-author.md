# Stage 2 author handoff: local conditional information

Author completion: 2026-09-13. Five independent reviews are still required;
this record does not mark the stage accepted. `PROCESS.md` remains root-owned.

## Written material

- `sections/02-locality.tex`: exact noiseless Markov prior mapping; genuine
  local conditional definitions; a shared residual-to-information lemma and
  overlapping-history row lemma; scalar and complete-block noisy Markov
  bounds; stationary spacing/innovation-floor/finite-horizon pricing; general
  block covariance decay with all constants and a complete weighted-conjugation
  proof; supplied block metrics; intrinsic and Euclidean partial-observation
  bounds, with a singular-covariance-safe transport proof; calendar graph,
  feasibility masks and scope; explicit prior-art reductions and comparisons.
- `appendices/locality-scope.tex`: regular Markov score orthogonality and full
  Gaussian mean/covariance gap calculation; stationarity and random-intercept
  counterexamples; KL-to-relative-information proof; repeated-pair Kaporin
  scaling; exact thesis pivot supermodularity/marginal-identity counterexample
  and separately qualified fixed-order greedy-bound contradiction.
- `main.tex`: added locality main section and appendix, with an insertion
  comment for later main sections before `\appendix`.
- `references.bib`: added inspected primary sources. `macros.tex` and the
  accepted foundations section were unchanged.
- `process/coverage.md`: appended actual label-to-development map and later
  stage interfaces. `process/literature.md`: appended actual primary-source
  reading, version scope and search record.

## Development beyond the archived notes

The complete-block theorem now uses the stronger far-pair bound, not only
the archived gain-only triangle bound. Root suggested this strengthening and
the author checked it analytically and with exact rational examples:

`Cov(X'_s,Z'_s) = Pi_s^-(H_s)` in full observation. When `s<t-L`, every
update of the fresh t-local filter is after s. The cross covariance propagates
as its ordered product of whitened transitions and symmetric contraction
updates, so its norm is at most `Pbar*rho^(t-s)` without any commutativity
assumption. Lemma `lem:local-row` then gives
`2*Pbar/d_* [T_L(rho) + kappa*N_L(rho)]`, the sharp-far scalar formula.
The archived gain-only bound remains stated as a valid weaker version; old
certificate numbers must not be silently relabeled as using the new constant.
No analogous stationary `1-kappa` near factor is asserted for general blocks.

The partial-observation proof was completed at the main place where the notes
were terse: two residuals have different fresh histories. At the earlier
endpoint `U D_s^-1 U^T <= kappa Pi_s^{-,s} <= kappa P_s`; a proved
range-factorization lemma expresses this covariance through `P_s^(1/2)`
without any inverse of a possibly singular latent covariance. It can then be
transported through the later filter starting at unconditional `P_s`.

Shared lemmas consolidate duplicated proofs. The manuscript proves all finite
geometric identities used in constants and both required prior reductions.
No result was invalidated. The prohibited nonstationary stationary-factor
extension and unproved historical FSAI inheritance route remain explicitly
excluded; the thesis issue is attributed only to the inspected thesis version.

## Author verification

Command from repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  code/research_20260912/.venv/bin/python \
  paper-correlated-measurements/verification/stage02/check.py
```

The independent script uses dense principal covariance calculations and imports
no historical implementation. All checks passed, saved in
`verification/stage02/results.json` and `check.log`:

| Check | Count |
|---|---:|
| Exact rational geometric identities | 27 |
| Exact theta perturbation smallness identities | 2 |
| Exact counterexample constructions | 2 |
| Exact full-block spectral sandwich models | 60 |
| Exact improved full-block far pairs | 40 |
| Exact Markov paths, both innovation directions, including singular transition | 15 |
| General covariance floating subset/window models | 155 |
| Supplied-metric floating subset/window models | 155 |
| Singular partial-state floating subset/window models | 155 |
| Exhaustive floating row-majorant DP checks | 1,500 |
| Exact separated-mask counts | 240 |
| Floating stationary spacing/floor/spectral models | 1,280 |

Exact PSD tests use all principal minors of the symmetric rational congruent
matrices `delta*D +/- (Cov(Z)-D)`; no square roots or floating eigenvalues
are used in those checks. The new full-block far test uses exact PSD of
`Pbar^2*rho^(2h)*I - pair*pair^T`. General/partial/spacing floating tests
are numerical diagnostics, expressly not certificates or proof substitutes.
The partial model has rank-two state covariance moving through four-dimensional
coordinates and varying one/two/three-dimensional observation packets. The
general model has unequal packet sizes and large diagonal eigenvalues; a
nonuniform invertible block metric yields the same measured relative error.

The printed generic-decay windows 49 and 58 for target errors 0.05 and 0.01
were independently recomputed. Root separately produced additional diagnostic
scripts under `verification/stage02-root`; this author did not modify them.

Compile from the paper folder:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The final build passes: `build/main.pdf` is 23 pages for the accepted foundations
plus this locality stage and bibliography. `build/main.log` has no warnings,
undefined references/citations, or over/underfull boxes. Build stdout is saved
at `build/stage02-build.txt`. The foreign plain-TeX choose warning was removed
by using `\binom`.

Final author source SHA-256:

- `sections/02-locality.tex`:
  `3525bcb4d5c76706fe89b9c8e5fe805b23c7b445589d3c841b6ddee5791f3a43`
- `appendices/locality-scope.tex`:
  `ddda642e827483dfec71cb9e1a24dbed66e8c10a361698445f7c7939c0a33989`
- `verification/stage02/check.py`:
  `a1f2fb21c10e74e5342aca72138309b6c4538eb97d2ec1138ec92ef74e7c4795`

## Review focus and later interfaces

The five reviewers should independently check the partial-state endpoint
inequalities and transport through differing histories; the newly strengthened
full-block far bound; the generic weighted-conjugation constant and no-dimension
factor; spacing masks when `L<g-1`; exact Markov prior mapping; and the literature
and counterexample scope. Every positive theorem has a complete written proof.

The supplied interfaces are `eq:precision-sandwich`, `eq:prior-aware-local`,
`eq:calendar-arc`, and the four explicit error bounds. Later approximation
theorems may use the stronger block bound, but their polynomial arguments can
also retain the simpler conservative envelope. Stage3 owns all approximation
schemes, bit complexity, scalar prior reduction and spectral/matroid results.
Stage4 owns rational log certificates, virtual-noise comparisons, robust
normalization and separators. Their absence from this stage is intentional.
