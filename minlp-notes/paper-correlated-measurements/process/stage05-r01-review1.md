# Stage 5 independent review 1

Assessment: **PASS on mathematical and computational substance; no major issues. Two minor presentation/provenance issues should be corrected.**

## Scope and independence

I read the Stage 5 author report, all of `sections/05-computation.tex`, all of
`appendices/computational-models.tex`, the source-kinetics README and both exact
ranking programs, and the relevant definitions and public-source comparison in
Section 1. My primary audit was the public-source kinetics reconstruction. I
inspected the immutable original software checkout at commit
`430090e610446aab88328ce495ffb15b684c56c4`, including its actual covariance,
feature indexing, costs, binary installation/selection constraints, time windows,
regularization and FIM assembly. I read the corresponding local Wang manuscript
passages after reading `literature/AGENTS.md`. I did not inspect another Stage 5
review, edit any frozen file, execute original optimization or deserialize stored
third-party solutions. The Stage 6 synthesis remains outside this stage's scope.

## Findings

1. **MINOR — use the established expansions of SCM and DCM.**
   `sections/05-computation.tex:61–62` introduces “static continuous measurement
   (SCM)” and “dynamic measurement (DCM).” The source and the existing Section 1
   use **static-cost measurement** and **dynamic-cost measurement**. SCM describes
   the cost/selection model; continuous observation is an application motivation,
   not its defining mathematical property. Replace these two expansions with the
   source's established names. The already stated eight-sample all-or-nothing
   interpretation and all results remain correct.

2. **MINOR — make the reported time labels' source convention explicit.**
   `sections/05-computation.tex:60,89–91` and
   `supplement/source_kinetics/README.md` report the intended dropped-zero labels
   `7.5,...,60`. There is a small source-code discrepancy a careful reproducer
   will encounter: `kinetics_MO.py:207` constructs `linspace(0,60,9)` and
   lines 214–215 separately map its final eight entries to `7.5,...,60`, but
   line 275 passes the full nine-entry array to the optimizer.
   `measure_optimize.py:1059–1064` reads its first eight entries, so its internal
   spacing map is instead `0,...,52.5`. The source's supplied sensitivities have
   the initial zero rows dropped. The manuscript's intended labels are reasonable,
   but the statement is presently more seamless than the code provenance.
   Add a short supplement note (with, if desired, a brief main-text pointer):
   sample index `i` is reported as `7.5(i+1)` using the dropped-zero convention;
   the inspected optimizer's spacing map is shifted by `-7.5`, which leaves
   every pairwise difference and every feasible acquisition schedule unchanged.
   **Do not change the objective values, selections or reported intended times.**
   I independently checked equality of every actual 10-minute source window
   under this shift. The same note can identify the source file as
   `kinetics_source_data/Q_drop0.csv`, archived here as
   `kinetics_Q_drop0.csv`; its bytes and hash match exactly.

Neither issue changes the 2,347 schedules, any of the 66 optima, or the regret.

## Exact computational checks

- Re-ran the default independent full-covariance checker with its output directed
  into my own review directory. It passed **all 2,347 schedules and 14,082 exact
  objective equalities**, with record SHA-256
  `27564740f997568ae08d90a2af0508193eb2805d0eb3e022157025b577e444e4`.
  This is the full run, not the winners-only option. My observed time was
  16.06 seconds; it is a validation time, not a solver comparison.
- Wrote a separate source-family audit using the original source's explicit
  10-minute sliding windows, per-species and total sample caps of ten, and
  installation exclusion. Its complete feasible set equals the archived set.
  Counts by number of SCM species are 1,158, 1,023, 165 and 1, totaling 2,347.
  The effective cap of four DCM samples follows from these windows on eight
  times; it is not an unsupported replacement for the source's nominal cap.
- Checked that the comparison index set is exactly all eleven budgets times all
  three stated criteria, that all 66 exact optimum sets are singletons, that
  stored winning descriptions agree with the indexed schedules, that all
  runner-up margins are strictly positive, and that all reported optimizer-
  agreement flags match the actual optimum sets. Exactly one comparison changes:
  budget 3000, trace information.
- The smallest relative runner-up margins over both formulas and all budgets
  are approximately 0.00208984 for trace, 0.00533512 for determinant and
  0.00000137872 for conventional A. Uniqueness is established by exact fractions,
  not these approximate displays.
- Confirmed the copied CSV is byte-identical to the pinned original. Its 24 rows
  are species-major and its four columns are `A1,A2,E1,E2`. The same rows serve
  both modalities, exactly as the original `get_jac_list` arguments specify.
- Read the rational generator's determinant elimination, inverse, principal-
  cofactor inverse-trace evaluation and all ranking directions. The independent
  checker instead uses full selected covariance inverses and explicit information
  inverses. These are meaningfully distinct routes, and the ordering of conventional
  A versus trace information is correct.

Evidence files are under `verification/stage05-review1/`:
`check_source_family.py`, `source-family-audit.json`, and
`independent-rankings.json`. The source-family script refers to the pinned local
checkout solely for this review's provenance check; it is not part of the
standalone submission supplement.

## Mathematical and scientific conclusions

The block covariance is exactly the stated `[[B,B/2],[B/2,B]]` under the declared
rational interpretation of source constants. The original implementation forms
its full pseudoinverse before selection; this covariance is positive definite,
so the corresponding mathematical operator is the inverse. The source then sums
all ordered pair contributions gated by binary selection products. Expanding
static measurements into their eight scalar responses produces the gated
quadratic form used here without an omitted cross-modality factor.

For selected-covariance information, time independence makes the generator's
sum of local selected inverses identical to the independent checker's full
selected covariance inverse. The positive prior gives positive definite
four-parameter information even for small schedules. Exact determinant ranking
therefore suffices for D, and exact inverse-trace ranking suffices for A.
The stated loss of about 3.112800396788 percent and both winning schedules are
supported. The code-level rational instance is appropriately distinguished from
physical derivative generation and uninspected stored published solutions.

The novelty scope is appropriate: the correct selected-covariance formula and
its disagreement with inverse gating are credited as prior knowledge. This
stage adds an exact instance-level reanalysis and specific certified comparisons;
it does not claim to have discovered the basic statistical distinction. The
separate temporal and within-time experiments are clearly distinguished.

The broader computational presentation consistently separates exact certificates,
floating bounds, numerical model checks and historical timings. In particular,
the no-advantage packet results, failed diagonal witness, fixed-grid timeouts,
missed separator target, and empirical nonnested comparisons are retained rather
than concealed. The nested experiment compares common complete schedules and
identifies its mixture lower endpoint correctly. I found no serious broader
Stage 5 issue on reading.

## Limits

I did not independently replay all 46 historical certificates or rerun every
new numerical experiment; those families are outside my primary assignment.
I did not prove the physical sensitivities in the public CSV or inspect the
publisher's final typeset Wang article. Neither is claimed by this stage.
This review does not assert external peer review or formal proof-assistant
verification.
