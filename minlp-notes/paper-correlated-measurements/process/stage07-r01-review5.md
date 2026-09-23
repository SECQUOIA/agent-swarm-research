# Stage 7, whole-manuscript review 5

Decision: **No major or minor correction requests.** I found no unresolved mathematical, empirical, integration, or reproducibility issue in the frozen manuscript that requires a change. This is an independent internal review, not external peer review or a guarantee about every possible future criticism.

## Reading scope

I read the complete source manuscript: `main.tex`, `macros.tex`, all seven section files, all four appendix files, and the entire bibliography. I checked the compiled 66-page text, inspected the densely populated page 43 visually (Tables 5 and 6 and the hierarchy discussion), and checked the build log for unresolved references or box warnings. I read both package READMEs and the public-source provenance README, and inspected the validation driver, certificate replay, model validator, numerical-reproduction wrapper, fresh experiment producer, and both source-ranking implementations. I did not consult the other Stage 7 reports.

My deeper review concerns the empirical claims and their connection to the mathematical statements. I also followed the proofs across the entire paper rather than treating earlier stage acceptance as sufficient. In particular, I checked the selected-inverse/gating comparison and efficiency direction; the residual-to-precision congruence; the overlap calculation and the full-block far-pair covariance identity; the normalization floor, exact-range filtering, signed profiles and actual-object recovery; the represented-matroid contraction and noncancelling coefficient test; prior-aware support directions; all-diagonal lower weak duality; uncertain robust normalizers and the second approximation factor; and the changing-anchor Schur identity with its prior cross terms. I found their assumptions and later uses consistent.

## Distinct checks performed

`verification/stage07-review5/check.py` and `results.json` record my independent display and integrity checks. All passed:

- All 30 entries in the scalar table obey their stated outward direction when compared as exact fractions to the saved witnesses. The ten memory, fixed-split and all-scalar cases have exactly identical `problem_data`, not merely matching names or dimensions. The separations are against integer upper bounds and do not assume that the common incumbent is globally optimal.
- All four partial-observation relative percentages are rounded upward. Their denominator is feasible information, consistent with the definition in Section 6.1.
- All robust and separator table endpoints and gaps equal the saved terminating rational values exactly.
- All four fresh nested-anchor intervals contain their saved exact endpoints; the full-block constants, upper/lower values and relative gaps obey the indicated rounding direction. I separately checked that the displayed L=4 upper bound 2.212989488 is larger than the actual stored rational upper bound (approximately 2.2129894871358795).
- The four principal determinant-root percentage claims (the scalar-kinetic uniform guarantee, polished robust absolute efficiency, polished robust efficiency relative to optimum, and 48-point robust efficiency relative to optimum) are valid lower inequalities. I proved the numerical comparisons with a rational alternating-series lower bound for exp(-x), independently of floating exponentials and the supplement logarithm routine.
- Both manifest families validate an intact throwaway copy; modifying or removing the public CSV is rejected. The checks touched no frozen input. The manifests contain 159 archived files and 11 new source/input files.
- The 204 files in `process/stage07-r01-freeze.json` all retained their recorded hashes at the end of this review.

The root is independently running the full clean base-only validation. I deliberately did not duplicate that expensive replay. My code inspection confirms that the full command invokes all 46 principal certificate replays; `--quick` explicitly omits the three costly separator cases and is accurately described as incomplete. Exact-replay modules use local archived inputs and recompute support quantities, SPD conditions and logarithm enclosures. Optional Gurobi/CVXPY dependencies are associated with numerical proposal branches and are not evidence for the mathematical certificates. The reproduction wrapper uses a writable temporary archive and refuses an existing output destination.

## Scientific interpretation and model matching

The public-source reconstruction is correctly separated from the temporal examples. I inspected the pinned source locally, including `kinetics_MO.py` costs, the 10-minute interval and modality restrictions, and `measure_optimize.py`'s time-label map and global DCM-window constraints. The at-most-four DCM condition follows from the eight-point nonadjacent family even though the original explicit manual-count cap is ten. The uniform -7.5 shift changes no feasible pairwise spacing. The reanalysis uses the code's symmetric covariance, fixed regularizer and species-major CSV, and does not claim to regenerate physical sensitivities or the authors' stored solutions. The two enumeration constructions and independent full-covariance ordering are meaningfully different. The paper correctly reports that only one trace choice changes, whereas all tested D and conventional A choices agree.

The manuscript keeps several potentially misleading comparisons separate:

- A tiny continuous support residual is not presented as a tiny discrete gap.
- A feasible mixture supplies the lower side of a mixture-optimum interval, not an integer-design lower bound.
- A common-point all-split witness survives split tuning and the stated affine upper supports, but does not constrain branching or unrelated cuts.
- The all-diagonal proposal's failed numerical status is retained; the rational repaired factor supplies the actual certificate.
- Full-packet examples that favor the dense bound are reported; their larger channel count changes information normalization.
- The fresh noncommuting-block improvement is a new exact tiny study and theoretical-constant comparison, not a retroactive reclassification of archived floating bounds.
- The fixed-per-index kinetic tests are not described as a common physical process under grid refinement. The separate fixed-physical study keeps its budget fixed, preserves exact nested covariance values, identifies first-pricing timeouts, and retains the separately budgeted diagnostic.
- The large separator b=12 and b=16 partitions are nonnested; their empirical ordering is not attributed to the nested-anchor theorem. The fresh hierarchy study uses exactly the same 56 complete schedules at all four levels.
- Historical timing includes the stated common incumbent and individual reference-generation costs where required. Generation and exact certification are separate; the 192-point b=16 accounted total exceeding 30 seconds is visible, and every large separator misses the .01 target. No controlled speedup or universal dominance is claimed.
- The sensitivity checks are numerical consistency evidence. The actual rational design certificates refer to encoded decimals and do not establish physical noise validity, exact real exponential derivatives, or global identifiability.

## Literature and integration

The introduction's contribution table and the later proofs agree on what is inherited and what is claimed. The finite-history factorization, virtual-noise equivalence, inverse-logdet convexity, general subsystem design, maximin efficiency normalization, exact profile interpolation, and guessed-vector normalization are credited. The qualified novelty assertions concern the combined all-target relative PSD guarantee and the particular changing-anchor hierarchy. Neither the scalar predecessor nor general localization is claimed as a first result.

I independently opened the primary August 2026 Bansal–Xu preprint and read its theorem and construction. Its invertible partition-base hardness supports the discussion's weaker no-polynomial-factor statement for growing information dimension; this does not contradict the paper's fixed-dimensional theorem. I checked the official PMLR metadata for Mahabadi–Vuong and the official Dagstuhl record for Bökler–Chimani–Jasper. Their names, dates, titles, volumes and page identifiers agree with the bibliography. Sources used for these checks:

- https://arxiv.org/html/2608.05468v1
- https://proceedings.mlr.press/v300/mahabadi26a.html
- https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.112

I did not independently retrieve every cited article in this final pass or rerun every historical optimizer. The manuscript records inspected-version limits and does not infer absence of prior work from unavailable final texts. Its scope is broad and the paper is long, but that length reflects the requested comprehensive treatment: the introduction supplies contribution boundaries, proofs expose the limiting assumptions, computations separate evidence types, and the discussion connects practical gaps to their causes. I found no dangling claimed result, unproved positive extension, mismatched criterion, or empirical conclusion that requires a correction.
