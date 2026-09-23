# Stage 2 corrections and exact-instance development

The correction agent read the primary adjudication and independently derived
the proposed analytic strengthening before editing. Work was confined to the
live paper directory; no snapshot or reviewer report was edited.

## Adjudicated minor findings

1. **Quotient-size scope.** In `sections/04-four-block-certificates.tex`,
   restricted the quoted dimension ranges to `n>=9`, where the symbolic
   topology has stabilized. The symbolic-quotient checker confirms the ten
   dimension triples at nine modes and direct agreement with reconstructed
   symbolic coefficients at 11, 23, and 37 modes.
2. **Heading report.** The primary adjudication did not substantiate the
   alleged margin defect. No correction is claimed for an established
   overrun. Retitled subsection 7.1 to “A three-mode obstruction with an
   exact instance optimum” to describe the strengthened result clearly.

## New exact result

Rewrote the proof of `prop:three-mode-failure` in
`sections/05-small-budget-minimax.tex` around the exact one-sided instance
optimum `18673/18396`, with optimal word `(0,2,1)` and switching times
`8341/4599` and `17639/4599`. The full rational knot table, all six
threshold-one reach conclusions, and the uniform-input comparison remain.
The previous strict lower-bound proof is subsumed by the exact proof rather
than repeated separately.

The proof now includes:

- A capped-inverse sensitivity argument derived from complement slopes at
  least `1/4`. It explicitly treats the possibility that the upper inverse
  endpoint equals the horizon. First reaches increase by at most `4 delta`
  and pair reaches by at most `20 delta`.
- A comparison directly with the final complement at the horizon. Its
  increase from the last original knot is `21 delta_*`, while any distinct
  triple supplies at most `21 delta`. This excludes all thresholds from
  one up to, but excluding, the asserted optimum without assuming an
  uncapped final inverse. The corresponding triple-reach upper bound is
  also stated.
- Exact attainment. The first and second roots lie on the specified
  complement-slope-`1/4` intervals, and the last root lies on the uniform
  suffix. All three block-end negative discrepancies equal the claimed
  optimum.
- Exclusion of repeated modes even at the optimal threshold. Terminal
  support forces active set `{0,1}`. The middle-block upper bound increases
  by at most `16 delta_*`; the required lower bound decreases by
  `delta_*`. The resulting positive gaps are `2923/4599` and `4372/4599`.
  Monotone feasibility handles smaller thresholds, including those below
  one. Shorter schedules are included by zero-length padding.
- The scaling consequence
  `G^-_{3,3}(T) >= (37346/262143) T > (8/57) T`. This is explicitly a
  minimax lower bound. The exact instance optimum is not presented as an
  exact three-mode minimax value.

The proof is analytic and uses the given rational input. No LP solver or
additional certificate bundle is required. Reviewer 02's independent LP
certificate enumeration remains corroboration in its original review files.

## Verification changes and results

Extended the standard-library checker
`verification/stage02/check_new_results.py` to reconstruct cumulative
allocations and their capped inverses directly from the knots. It now checks
all six threshold-one reaches, exact sensitivity coefficients, representative
thresholds (one, the midpoint, and the asserted optimum), final complement
identities, root-interval membership and slopes, the matching schedule, the
scaled coefficient, terminal support, and both repeated-mode gaps.

The matching schedule's one-sided discrepancy is evaluated independently of
the reach formulas on the union of every allocation knot and switching time.
The existing exact polygon audit still independently excludes every one of
27 words on all 972 switching-time cells at threshold one. Aggregate
identities, plateau transitions, asymptotic coefficients, and the prescribed
pair counterexamples also still pass. The finite threshold checks supplement
the analytic inverse-slope argument; they are not a proof over a continuum
of thresholds.

Updated the README to explain the exact-instance checks and their scope.
No bundled reference code, data, dependency, or provenance digest changed.
All 12 reference artifacts still match their recorded hashes, and all 35
files in the frozen stage 2 round 1 snapshot retain their recorded hashes.

Ran:

- `python verification/stage02/check_new_results.py` — passed.
- `python verification/stage02/check_symbolic_quotient.py` — passed.
- `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex` —
  clean rebuild passed; the final LaTeX log has no warnings, undefined
  references, or overfull/underfull boxes. The manuscript has 21 pages.
- `git diff --check -- paper-switching-control` — passed.

Verification logs have prefix `verification/stage02/corrections-`:
`new-results.log`, `symbolic-quotient.log`, `build.log`, and `integrity.log`.
Rendered and visually inspected pages 14 and 18–21. The quotient scope,
subsection title, proposition, complete knot table, sensitivity proof,
matching schedule, repeated-mode argument, and following subsections fit
cleanly. Renders are `corrections-page14.png` and
`corrections-page18.png` through `corrections-page21.png` in the same folder.

All assigned changes are complete. The strengthened mathematical claim is
ready for the planned fresh five-reviewer round; this report does not record
stage acceptance. No snapshot was created by the correction agent.
