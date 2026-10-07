# Review responses and final integration

The manuscript combines the September iterated-OBBT theory and October
adaptive-OBBT work. Four Opus writing lanes produced the full paper. Separate
Sol audits and reviews checked the local theory, foundations, certificates,
constraints, algorithms, and saved evidence. An Opus reviewer independently
checked foundations and algorithms; a second Opus reviewer checked the full
paper, and a new Opus round reviews the integrated revisions. Luna with maximum reasoning owns the literature review and `$lit`
maintenance. The original reports and scientific source bytes are preserved.

## Resolved mathematical findings

| Finding | Final treatment |
| --- | --- |
| Boundary terminal estimate invalid for a start already below the cutoff floor | Coarse first-round bound; refined estimate begins only after its induction premise holds. Free-coordinate rates concern prescribed enclosing scales. |
| Unsupported exact successive ratios for arbitrary quadratic boxes | Two-sided geometric bounds and kth-root rate; exact multiplicative rates only for proved eigenboxes. |
| Contraction and stall criteria presented as exhaustive | Sufficient tests; a fully proved critical scalar family has sublinear convergence and a cubic-root cutoff floor. |
| Incorrect hull/protected-box inclusion chain | Independent inclusions corrected; greatest fixed-box development supplied by Opus reviewer for the final revision. |
| Fixedness inferred only from nested compact boxes | Separate decreasing-family closedness premise; explicit nonfixed-limit example. |
| Fair directional schedules and selective rounds confused | Complete-block sandwich proves equal fair-schedule intersections; selective updates inherit lower enclosures only. |
| Lifted attainment inferred from projected compactness | Compact lifted sets and continuous objective explicitly assumed. |
| Projected monotonicity confused with literal auxiliary reuse | Projected monotonicity suffices for endpoint and objective ceilings; lifted nesting is needed to reuse the same auxiliary vector. |
| Completed-round counterexample showed only auxiliary failure | Proposition now tests complete lifted pools on the rebuilt box, matching the example and exact driver. |
| Pool cutoff threshold unnecessarily required every witness | Sharp per-face least-cost threshold, and full-relaxation face threshold for the same prescribed box. |
| Upper residual could never be subtracted after the first round | Under the checked supersolution, the after-round bound is `Me <= e-r`; exact state and invariant comparison region are required. |
| Finite residual bound unnecessarily required spectral contraction | Finite supersolution and least-majorant series handled without that premise; fixed-point cutoff comparison retains its separate spectral premise. |
| A current basis treated as a uniform sensitivity certificate | Complete invariant-region cover, exact strict-violation coverage test, and rebuilt-row stationarity correction. |
| Global incumbent treated as a protected point in every node | Incumbent singleton must lie in the current box. |
| Only positive-width boxes treated as finite certificates | Singleton fixed boxes are allowed; exact termination distinguished from a tolerance stop during asymptotic convergence. |
| Strict and non-strict cluster conditions equated | Same numerical threshold; different inequalities stated precisely. |
| Zero initial gauge passed into a logarithm | Zero-round case handled before the logarithmic bound. |
| No finite tail certificate described as a zero-tail certificate | Scalar-history scope and absence of a finite majorant stated correctly. |
| Nonlinear graph repair constant weak | Exact one-sided `L=1/2048`; proved width factors `25/48` and `1/3`, plus a finite constraint-tangent variant. |
| Concurrent optional operations used a serial ledger argument | Serial completion or sufficient outstanding reservations required. |

## Resolved evidence and interpretation findings

- September control/r5 SCIP solve counts are 573/563. Two wrong-answer rows
  are excluded from solved counts. Archived detailed time and node tables
  explicitly retain their original descriptive success convention.
- First-round productive trajectories number 239. The 104 one-entry histories
  split into 97 completed unchanged rounds and seven interrupted rounds
  (three unchanged, four productive). There are 22 completed unchanged second
  rounds following a productive first round, plus one interrupted second round.
  None of these numerical stops is called an exact fixed-box certificate.
- The October comparison retains all 120 runs and the same solved sets. Its
  adaptive arm used 20.9% fewer LPs but more propagator time. Callback and LP
  costs are separated; aggregate shares are not presented as per-run bounds.
- The observed maximum propagator time is 1.00501 seconds; the numerical policy
  has no proved hard overrun limit. Untimed admission checks remain separate.
- Search changes and better incumbents are reported, but no additional solve,
  demonstrated overall speedup, or causal ablation claim is made.
- The experiments measure current-round screening and heuristic policy choices,
  not the computational value of stronger all-future certificates.
- Input provenance distinguishes prospectively frozen October data from
  retained September inputs. Original bytes, missing retained solutions,
  required path relocation, solver versions, and numerical validation scope
  are documented in the companion.

## Review records

The authoritative scope-specific second-pass reports are
`review-local-r2.md`, `review-certificates-r2.md`,
`review-constraints-r2.md`, and `review-evidence-r2.md`. Each closes its
material first-round findings and identifies its reviewed snapshot and limits.
`review-opus-foundations-r1.md` supplies the exact box-relative tangent
counterexample and complete overflow-proof revision. The Opus author revision is recorded in author-revision-r2.md.
The focused final reviews review-foundations-r2.md, review-local-r3.md,
review-certificates-r3.md, review-algorithms-r3.md, and
review-integration-r2.md accept their revised scopes with no unresolved
scientific findings; source attribution remains the literature lead’s separate
review.

## Full-review revisions

- The two cutoff worked cases now distinguish failure to retain the auxiliary
  coordinates from failure to protect their projected hull. The cutoff-zero
  case supplies the latter counterexample explicitly.
- The restart sandwich uses a direct order proof and allows cutoffs below the
  optimum and empty iterates. Closedness and nonempty iterates are used only
  for the additional identification with the greatest fixed box.
- A numerically safe step requires a proved safe bound evaluated with directed
  rounding; outward rounding of an unverified approximate optimum is insufficient.
- The restricted tangent theorem is in the local-rate section. All artificial
  observed-history examples are in the residual section. The basis-cover and
  coverage proofs and elementary scheduling results are in appendices.
  The structural revision preserved all moved mathematical environments and
  proofs byte for byte; its report records the hashes.
- The analytic figure plots the proved eigenbox rates and the scalar sufficient
  bound. It does not show fitted rates from computational experiments.
- The precursor comparison states which detailed aggregates retain the
  archived success convention and which archived comparisons have not been
  reconstructed by the saved analyzer.
- The callback cost allocation is a descriptive quotient over recorded
  callbacks, rather than an estimate of a homogeneous cost for every callback.
- The temporary probing-node interpretation is tied to the actual SCIP
  10.0.2 release source. The inference uses the event records and does not
  claim that the logs recorded node types.

The Opus revision closes the front-matter and numerical-validation findings.
It supplies the greatest-fixed-box lemma and empty-box conventions, the exact
moving-tangent counterexample, the sufficient joint-lsc condition, and a complete
faithful-rounding proof on extended binary64 values. It distinguishes exact
finite closure from finite-budget stopping and explains rational digit growth.
The introduction and discussion now use the theorem domains and upper-order
bounds, distinguish pool expiry from loss of fixedness, identify singleton
certificates, and limit the measured policy’s connection to the theory.

The numerical-validation block is now Appendix B; all six algorithm proof
environments are verbatim before and after that move. The main implementation
section retains the conditional validity result and incumbent-cutoff caveat.
Applegate et al. and Neumaier–Shcherbina are cited for established exact-LP
reconstruction and safe bounds. The completed-round examples require the
rebuilt-row check; the full box threshold is described by its at-most-2n face
optimizations rather than an unsupported runtime comparison.

The final Luna source audit dispositions all 37 bibliography entries and lists
13 unavailable source artifacts or versions. Repeated OBBT, cutoff use,
arithmetic and composition rules, convergence-order analysis, and earlier stall
examples are credited explicitly. Source-specific negative claims are avoided
where full texts remain unavailable. The final Sol source-integration review
accepts the prior-work and contribution wording; its one Taylor/McCormick--Taylor
wording correction is applied. The published Sundar entry identifies the read
preprint version, and the Belotti pair distinguishes the published 2010 chapter
from the read 2012 manuscript. The final literature check returned `KB_CHECK=ok`;
the timed global counts and unrelated shared-KB changes are recorded in the run
account. The base scientific bibliography and approved supplement have the same 37
unique keys, all cited in the paper. The separate software batch adds nine
verified benchmark and software entries, bringing the final bibliography to
46 unique cited keys.

The integrated Opus round-2 review accepts the science and closes all earlier
M1--M3, m1--m15, F1--F8, and A1--A8 findings. Its minor final text requests
are applied: the Belotti pair is also cited in foundations; the restricted
tangent pointer names its correct subsection; the stall summary uses negative
values on every face; singleton exactness is conditional; upper-order bounds
motivate reconsideration without asserting that it pays; the three limits use
consistent wording; the recorded maximum is described as at most 1.00501 s;
and number-zero callbacks retain the literal observed category separately from
the probing inference. All 185 statement/proof environments remain verbatim.
The standard Collatz--Wielandt name is retained with its self-contained
definition and comparison proof; no nonlinear spectral theorem is invoked.
The same Luna lead supplied the nine identified software-citation additions:
the original MINLPLib article and current library overview, the SCIP Suite 10.0
report, the project-recommended HiGHS and PySCIPOpt references, the Gurobi
reference manual, and three SCIP 10.0.2 propagator source files. The homepage
snapshot identifies MINLPLib; it does not certify the historical cohort, whose
retained inputs are in the companion. The software references identify the
recorded stack without inventing an unrecorded HiGHS version. A final focused
Sol round-4 review accepts their integration with no remaining findings. It
verifies the corrected author accent, neutral bibliography notes, and the
release-pinned sources dated 2026. The full mathematical statements and proofs
remain verbatim against the accepted Opus snapshot. The base scientific access
limits and the unavailable immutable historical MINLPLib snapshot are
documented audit limits; the archived cohort inputs retain their disclosed
provenance. Final source and companion checks pass, and all 14 final review
source identities match the released files.

## Verification scope

No archived computational experiment or campaign was rerun for the paper.
Authors did use narrow mathematical checks, including exact rational identities
and small supplementary numerical checks of closed forms; their reports name
those commands. Source consistency, TeX builds, artifact hashes, direct saved-data
reads, analytic proofs, and reviews provide distinct evidence. Local checks are
limited to this topic; no project-wide verification or CI inspection was used.
