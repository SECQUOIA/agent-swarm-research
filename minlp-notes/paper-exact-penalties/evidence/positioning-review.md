# Contribution and literature revision review

Baseline: `b63317ab072109d74ba5e27ee74759374ee24be9`.
This combined increment, milestone and final review covered the complete
contribution revision, including the source, compiled PDF, bibliography,
and untracked source and validation records. The target stayed frozen
throughout all reviews; the lead compared SHA-256 fingerprints before
and after the external review and found no change.

Five fresh-context Codex reviewers worked independently and read-only,
without further delegation or access to earlier review conclusions:

| Reviewer | Scope and outcome |
| --- | --- |
| `positioning_review_whole` | Entire revision, relevant primary sources and artifact consistency. No substantive findings; suggested naming the upper bounds' norms explicitly. |
| `positioning_review_encoding` | Encoding claims and the exact-penalty, squaring-chain and few-quadratic precedents. No findings. |
| `positioning_review_calibration` | Calibration restrictions, QUBO hardness, conservative bounds and Gibbs guarantees. No findings. |
| `positioning_review_context` | Convexification and perturbation context, source assumptions and scope. No findings. |
| `positioning_review_clarity` | Reader-facing hierarchy, qualifications, bibliography and PDF consistency. No findings. |

A fresh Claude session using `fable` with high effort explicitly launched
one independent Fable full-target reviewer and three Opus reviewers for
claim consistency, citation accuracy, and novelty/evidence. All four
reported before the parent completed its independent adjudication. The
final report is retained in `reviews/positioning-claude.txt`. It found no
mathematical error or conflicting primary result, and recommended several
localized wording corrections.

## Lead adjudication

The lead checked each material finding against the manuscript and source
statements. Accepted corrections are:

- Name the infinity and one norms and the existence quantifier in the
  upper-bound summaries; name the infinity norm for the explicit grid
  coefficient. Present the two parameterized bounds without implying
  that either dominates the other in every regime.
- Replace empirical-sample wording by the theorem's probability statement.
  State that preservation of the original optimizer is not guaranteed,
  and retain convex objectives and affine residuals in the perturbation
  summaries.
- Describe Bhardwaj's MILP/MIQP theorems as existence results with
  data-dependent parameters, while crediting quantification in their
  proofs and the explicit strongly convex, smooth bound. Identify the
  inspected arXiv version, since the published SIAM text was not available.
- Describe the compact residual-space result as an analogue of classical
  convexification. It is not literally a special case of the cited MILP
  theorem, and nonattainment is not a distinction from that theorem.
- Distinguish Boland–Eberhard's augmentation assumptions from the later
  MILP norm result. The lead read assumption (3) in the primary manuscript:
  its growth requirement excludes a plain norm.
- Clarify native constraints, the affine equality system, the single
  multiplier in the lower-bound family, and the Gaussian tube reference.
  Attach the numerical-size and solution-time limitations to the
  sufficient-coefficient results they qualify.

The lead did not adopt the optional Kleinert et al. citation in the paper.
Their primary abstract concerns two validity proxies for big-M bounds in
bilevel KKT reformulations, a different quantity from the least exact
norm-penalty coefficient. Generic penalty-choice hardness is already
credited to a direct predecessor. Ketkov–Prokopyev's related posterior
bilevel verification result likewise does not establish the restricted
calibration theorem. These screened neighbors do not justify broader
novelty claims or require expanding the paper's focused comparison.

The introduction deliberately uses d for chain length and n for the
upper bounds' continuous dimension. The lead retained that distinction
and requested only a concise chain-length identification, rather than a
parenthetical notation translation. An NP-hardness statement does not
assert strong NP-hardness; Section 6 already explains the binary-box
reduction's bit-complexity limitation. Additional strict-point details
would repeat the lower-bound theorem without changing the comparison.

All accepted fixes are local prose, attribution or bibliography changes.
They change no result, proof, assumption used by a proof, or claimed
novelty scope. Under the build skill, direct inspection and targeted
validation suffice without another full review round, provided they
leave no material uncertainty. The final verification is recorded below.

## Verification limits

These reviews check the stated comparisons and claims, not exhaustive
priority. Primary publisher access was incomplete for several sources;
the evidence record identifies the inspected preprints and failed
retrievals. General algebraic and Gaussian results were not rederived.
No project-wide checks or CI inspection occurred. Unchanged mathematical
scripts did not need another run for this prose revision.

The external web-fetch harness automatically cached four primary PDFs
outside the repository despite the read-only review instructions. The
writer was instructed to move exactly those identified files into the
paper folder's ignored source directory, without touching other cache
files. The writer completed that move and verified that all four files
are ignored. They are not part of the committed deliverable.

## Final direct verification

The lead inspected the completed local corrections and the updated source
and validation records. All accepted findings are resolved. The mathematical
statements and proofs remain unchanged; the writer's post-review comparison
and reference audit again passed, as recorded in `positioning-validation.md`.

After the final freeze, the lead ran `git diff --check -- paper-exact-penalties`
and read-only Python/Poppler checks. The LaTeX log has no warnings, errors,
undefined references or box warnings; the PDF is newer than all TeX and
bibliography inputs; extracted text has no unresolved reference markers.
`pdfinfo` reports 23 pages and 391946 bytes. The lead visually inspected
final pages 1–3 through in-memory Poppler renders, covering the revised
abstract, introduction and convexification attribution; no layout defect
was found. Repository status contains only this paper folder's task changes.
