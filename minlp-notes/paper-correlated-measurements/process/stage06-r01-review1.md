# Stage 6 independent integration review 1

## Assessment

**No major issue found.** The new abstract, introduction, contribution table,
and discussion accurately integrate the accepted technical statements and
computations. I found one small precision issue and one useful missing piece
of directly relevant current literature. Neither changes a proof, certificate,
experiment, or qualified novelty conclusion.

This is the requested integration review. It does not replace the separate
whole-manuscript gate or claim to reverify every earlier proof and numerical
artifact.

## Minor findings

### 1. Reuse of a gated upper bound does not need a conditioning bound

Location: `sections/06-discussion.tex`, lines 10–12.

The discussion attributes reuse of a global gated upper bound to the
“condition-dependent comparison.” The operative fact is instead the
unconditional order `J(S) <= J_gate(S)` for every positive definite covariance.
The certificate-contract paragraph in `sections/01-foundations.tex`, lines
454–458, correctly invokes the gating proposition. The condition-dependent
Kantorovich upper comparison quantifies possible efficiency loss; it is not
needed to reuse a gated global upper bound with a correctly reevaluated lower
bound. The present wording is not a false bound, but obscures that distinction
in a paragraph expressly explaining certificate scope.

Suggested remedy: refer to the information ordering, optionally with the
foundations proposition or certificate-contract cross-reference. If desired,
give the condition-dependent comparison its separate role of controlling loss.
No technical result needs alteration.

### 2. Add the directly relevant new growing-dimension A/E-design boundary

Location: `sections/06-discussion.tex`, lines 69–80, or the approximation
paragraph of `sections/00-introduction.tex`; bibliography and source log.

The current synthesis stresses that fixed information dimension is essential
but omits a recent primary preprint addressing exactly the additive
partition-matroid A/E-design problem:

Nikhil Bansal and Yuze Xu, *Hardness of A/E-Design under Partition Constraints*,
arXiv:2608.05468v1, 5 August 2026.
https://arxiv.org/html/2608.05468v1

I read the primary introduction, Theorem 1.1, and its reduction/inverse proof.
It establishes severe approximation hardness when information dimension grows,
even for partition constraints and invertible information matrices. It directly
follows up Brown–Laddha–Singh's broader-dimensional question. This is fully
consistent with the present fixed-p cover, and does not contradict its
polynomial dependence on accuracy. Adding one carefully scoped sentence and a
preprint citation would make the current complexity discussion more complete.
Do not call it a barrier at fixed p or to the weighted-trace theorem.

This is a literature-context omission, not evidence against the qualified
all-target cover novelty claim. The proposed addition can stay in the new
integration sections without reopening accepted proofs.

## Checks and affirmative findings

- Read the complete Stage 6 author report, both new section files, main file,
  top-level README, contribution/assumption map, and corresponding accepted
  source-reanalysis, approximation, certificate, and computational passages.
- Checked that the abstract's cover quantifier is every attainable matrix,
  with one actual feasible object, two-sided relative PSD order and exact
  singular ranges. Fixed information dimension, explicit DAGs, rational
  represented matroids and additive atoms are retained. The introduction
  explicitly rules out correlated-history matroid generalization and large
  spectral-set benchmarking.
- Checked the weighted-trace roadmap against Theorem `thm:trace-fptas`:
  fixed decay/noise promises, rational input, input-sized dimensions, complete
  packets, exact count, mandatory/forbidden times and minimum spacing agree.
- Checked statistical scope against foundations: known parameter-independent
  covariance, pre-data selection, nominal mean sensitivities, no covariance
  Fisher term silently omitted, no global identifiability or physical-noise
  validation inferred, and the stronger SPD prior hypothesis for practical
  logdet/separator certificates is explicit.
- Checked the public reanalysis attribution and numbers: the integration does
  not claim to reconstruct published stored solutions; all 11 D and A choices
  agree, only the budget-3000 trace choice changes; 2,347 acquisition schedules
  and exact criterion ranking are consistent with the detailed computation.
- Checked all-scalar and all-diagonal claims against the common-input
  inequalities and fixed fractional witnesses. The discussion retains the
  exclusions for branching, unrelated cuts, continuous optimization error,
  and non-universal empirical dominance.
- Checked nested-anchor language against the full-schedule hull theorem and
  fresh disjoint intervals. It does not apply the theorem to nonnested archived
  block partitions. The 192-point target and fully accounted cost limitations
  match the tables.
- Checked the finite-scenario discussion against uncertain-normalizer bounds
  and reported shared-price intervals. Continuous-region robustness is not
  implied.
- Reopened the primary Hainy v1 HTML and inspected its selected-covariance
  definition and Proposition 3. The equivalence credit is accurate:
  https://arxiv.org/html/2504.17651v1 .
- Read the local Liu 2016 primary extraction's Section IV, equations 29–31,
  and warning about full-inverse truncation. The introduction correctly
  credits the established statistical distinction rather than claiming its
  discovery here.
- Read the retained primary Brown–Laddha–Singh 2024 PDF extraction's opening
  theorems and general matroid extension. The new introduction's randomized
  fixed-dimensional predecessor versus deterministic rational-representation
  cover distinction agrees with that source. Primary publisher/NSF location:
  https://par.nsf.gov/servlets/purl/10548928 . The web refetch timed out, but
  the locally retained primary text was available and read.
- Read the actual new source-inspection record and verified that the README
  describes internal review records as development evidence, with anonymous
  author metadata and no invented permanent archive URL.

## Limitations and changes

No manuscript, supplement, saved output or frozen source was changed. This
report is the sole written artifact. I did not rerun the full supplement or
rebuild the PDF, because this review targets the statistical and literature
integration and the accepted scientific files were unchanged. I found no new
counterexample to the precise cover or anchor claims in the primary sources
inspected, which is a scoped literature assessment rather than proof of
universal priority.
