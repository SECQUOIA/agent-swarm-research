# Stage 6 author/developer report

Status: complete and ready for the five independent reviewers. No stage 7
writing or reviewer delegation was performed. Accepted Sections 1–5 and all
four accepted appendices are unchanged. All substantive changes are in the
paper folder. The compiled manuscript has 73 pages.

## Completed development

`sections/06-computation.tex` contains self-contained proofs and executable
scope for rational convex KKT paths, the exhaustive status oracle, aligned
rank-one convex sweeps (including signed loadings and negative rank-one
coefficients when the total Hessian is SPD), nonconvex fiber allocation,
complete candidates and global comparison, incremental contact preservation,
optimistic/pessimistic upper optimization and attainment. Each selected output
has degree at most two; the entire atlas is explicitly not asserted to share
one quadratic field. It proves value convexification and original contact
reconstruction, the false-feasibility example, and the exact capacity jump
with optimistic maximum and unattained pessimistic supremum 51/160.

The new `code/original_faces.py` independently solves the full continuous-price
and upper task. It imports no compressed code and shares only rational input
mappings. It checks every nonempty principal Hessian minor, rejects singular
minors, enumerates the original-coordinate stationary faces with positive
definite free Hessian, intersects original KKT intervals, and compares original
quadratic values over all crossings. It retains all ties and independently
optimizes the same tariff/affine-row task under both semantics. Completeness
follows from the positive-semidefinite Hessian on any global minimizer's
minimal face and the checked nonzero determinant. The older fixed-price
singular-face value oracle has a different, narrower contract, explained in
both paper and README. No singular/flat support is claimed for the new baseline.

`code/compressed_solver.py` preserves the original solver except for two small,
profiled changes: a rational sign fast path before `cancel`, and a rational
midpoint when both sampling endpoints are rational. The full algebraic fallback,
fiber, candidate, envelope, contact and upper code are unchanged. A direct diff
was inspected. Exact rational midpoint samples need not be dyadic; the docstring
and paper use the correct term. No mathematical source defect was found in the
canonical algorithms. Early baseline fixture choices inadvertently had singular
principal minors and were correctly rejected; the supported fixtures were
changed and explicit rejection remains a separate test. The initial SymPy
Boolean-to-int helper error was corrected before completed checks or timings.

## Sources read and reconciled

Read the full canonical quadratic algorithm, nonconvex scalar algorithm,
nonconvex computation/closeout/source-positioning and reopened screening
computation notes. Read both implementation READMEs; full quadratic solver,
quadratic and tariff benchmark drivers, screening MILP comparison and its
original screening/recovery routines; full nonconvex solver, benchmarks,
review_one/review_two, example checker and contact plotting source. Inspected
the actual archived JSON tables, including the old pairwise compressed baseline,
heterogeneous and grouped timings, numerical discrepancies and follow-ups.
The detailed source-to-label disposition is appended to `process/coverage.md`.

Primary attribution was checked directly:

- Bemporad, Morari, Dua and Pistikopoulos (2002), actual openly hosted paper,
  Theorem 2 (printed p. 8) and Theorem 4 (p. 10), active-region affine optimizer
  and continuous piecewise-affine optimizer. Inspected PDF retrieved from
  `https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf`
  by curl after web extraction failed. The DOI/published metadata were verified
  on the publisher record:
  `https://www.sciencedirect.com/science/article/pii/S0005109801001741`.
  No convexity claim for our original parameter-dependent value is imported.
- Kiwiel's actual 2002 report, printed pp. 1–2, clipped multiplier Eq. (2.1),
  Fact 2.1 and introductory credit for sorting 2N breakpoints. The open report
  is `https://rcin.org.pl/Content/139441/PDF/RB-2002-77.pdf`; root's downloaded
  copy/text were read. Published metadata independently checked at
  `https://link.springer.com/article/10.1007/s10107-006-0050-z`:
  Mathematical Programming 112(2), 473–491 (2008). We credit the allocation
  ingredients, not a new general breakpoint-search algorithm.
- Gardiner–Lucet (2010), publisher abstract and bibliographic record at
  `https://link.springer.com/article/10.1007/s11228-010-0157-5`.
  It expressly describes quadratic and linear-operation envelope algorithms.
  Full subscription text was not used; no rational-bit or original-contact
  claim is attributed to its abstract.
- Moehle, Gindi, Boyd and Kochenderfer (2023), actual published open PDF,
  Section 6.3 and Appendix B (printed pp. 1679–1680, 1684–1687), read directly:
  `https://web.stanford.edu/~boyd/papers/pdf/portf_constr_lcso.pdf`.
  Published record `https://web.stanford.edu/~boyd/papers/portf_constr_lcso.html`.
  Credit is for piecewise-quadratic convex envelopes and incremental construction.
  The printed tangent formulas have apparent typographic problems, independently
  flagged by root (q1 instead of q2 in Eq. 25; endpoint intercept and boundary
  inequality directions). Our self-contained candidate/contact proof imports
  none of these formulas or an implementation-correctness assumption.

The paper has its own four new bibliography entries. `literature/AGENTS.md`
was respected; no generated literature index/bibliography or user-supplied
original was edited or redistributed. Downloaded primary originals remain in
root's verification area or temporary storage; their access is documented.

## Actual checks and experiments

Commands run from the paper folder unless the recorded diagnostic command uses
an absolute repository path:

```
python code/check_full_task.py
python code/run_diagnostics.py
python code/run_experiments.py
python code/run_experiments.py --resume
python code/archive_inputs.py
python code/summarize_experiments.py
python code/plot_contacts.py
python -m py_compile code/original_faces.py code/compressed_solver.py code/run_experiments.py code/run_diagnostics.py code/archive_inputs.py code/summarize_experiments.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

`verification/stage06-author/diagnostics.json` records exact commands, exit
codes and wall times. All five diagnostic groups passed:

- New full-task tests: 18 adversarial/seeded instances, both semantics, complete
  response sets on every independently generated baseline stratum, and direct
  verification of each attained witness at its returned price. Additional
  checks cover singular-minor rejection, full flat responses, singleton
  aggregates and unchanged-versus-paper fast-path boundary outcomes.
- Convex certificates: 33 dense LP comparisons, 24 quadratic dense-face
  comparisons, five hand quadratic cases and five exact aligned boundary cases;
  also corrupted certificate/coverage, forced failed numerical proposals,
  exhaustive recovery, almost singular and beyond-floating-range data.
- `review_one` redirected to the paper solver: 86 exact checks including isolated
  contacts, changing upper rows, flat intervals, negative prices and ties.
- `review_two` redirected to the paper solver: 350 original-face value queries,
  72 atlas-point/cell face comparisons, 30 pairwise-partition envelope comparisons,
  and 11 explicit edge cases. Counts are distinct categories, not a formal proof.
- Exact scalar example checker: phase transition, capacity, nonattainment,
  false convexified choice and rational algebraic-interior sampling.

The cProfile artifact `profile-before.prof/.txt` covers original family(12,17)
atlas construction and one unconstrained upper solve. It records 9.875 profiled
seconds and 5.742 cumulative seconds in symbolic cancellation. This diagnosis
motivated the two exact fast paths. Controlled ordinary paired runs solve the
same constrained task for both copies: N12 original/paper median build
3.1071/2.7076 seconds and totals 4.0547/3.6053 seconds. Profiled times are never
used as benchmark times.

`data/stage06-results.json` contains 60 completed workers: three repetitions
of four compressed/face pairs (including the capacity jump), two old/paper
N12 runs, five larger/grouped compressed cases, three convex sizes and two
screening sizes per repetition. Each worker is a cold fresh subprocess with
cleared SymPy cache; paired order alternates. Environment variables and HiGHS
thread option request one thread, with all warnings retained. Effective native
pool sizes were not separately inspected because threadpoolctl is unavailable.
The machine is shared, without isolation. All 60 retained workers exited zero;
there were no solver timeouts. The new baseline was not attempted above N6,
not presumed timed out. Full exact values and attainment agree across methods
and repetitions. The evidence shows mixed small-instance timing winners.

Prepared scalar instances and full convex/screening inputs are archived with
seeds and hashes. Heterogeneous N48 has 66 fiber pieces and 135 points;
two-type N1000 has only three pieces and seven points. Convex N10000 is a
separate positive-coupling synthetic family. The archived nonconvex and convex
numbers are reported as historical observations under different protocols.
All four archived and both fresh screening sizes favor numerical MILP timing
after preprocessing. Exact rational returned-point verification and the N8
numerical-tolerance discrepancy/follow-up are retained.

## Harness repairs and measured-source provenance

The first driver attempt failed before any timing because optional
`threadpoolctl` was unavailable. Its import was removed; the absence is recorded
in metadata. Its traceback is preserved as a reconstructed transcript excerpt.
The next attempt completed and stored 18 worker records, then failed to parse
the first screening worker's mixed JSON/native HiGHS stdout. This was a transport
failure, not a solver failure; that preliminary screening attempt has no usable
measurement record and is excluded. Its traceback and the 18 successful partial
records are preserved as `experiments-initial-failure.log` and
`experiments-initial-partial.json`.

The transport was changed to a separate worker JSON file, retaining native
stdout/stderr independently. The remaining 42 worker keys were resumed, without
repeating the successful 18. The numerical worker functions, instances,
algorithm implementations and timed regions were unchanged. The final record's
driver hash names this transport-repaired version; its source was preserved as
`measured-run-experiments.py` and verified against that exact recorded SHA-256:
`ee8ff621af8a9a7a03bbfd59007000c84cb8441667ddccfd2f52475459c3705e`.

After measurement, the final driver adds deterministic full convex/screening
input archival outside the worker loop and creates missing output directories.
The test helper/diagnostic runner likewise gained only output-directory creation.
`measured-check-full-task.py` matches the helper's recorded measured hash
`8f9ace9546106d843e73b29c3af64b24dfc2b311b845aa49783505fe30e08ae9`.
The raw measured hashes are preserved, rather than replaced with final wrapper
hashes. `manifest.json` records both measured mappings and all final source and
artifact hashes; solver files match their measured versions. These changes do
not alter algorithms or quoted solver timings. The measured scripts are
provenance snapshots, while README commands use the final portable locations.

The final LaTeX run exits successfully with 73 pages and no warnings, undefined
references/citations or overfull boxes. The contact figure and a rendered table
page were visually inspected; the three tables also match regenerated data.
No significant open mathematical obligation remains within stage 6's declared
scope. The limits are explicit: scalar aligned specializations, exponential
small-instance baseline, generic numerical-proposal failures, synthetic data,
no general QE implementation and no industrial performance claim. Stage 7
integration and the mandated five-reviewer gate remain root-owned next steps.
