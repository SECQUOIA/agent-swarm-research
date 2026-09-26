# Repository validity audit, 2026-09-24

Status: **document reassessment complete, 2026-09-25**, against repository
revision `75ef1803`. All 300 numbered findings from the original audit were
rechecked against source, surrounding qualifications, review records and
retained evidence. The previously unnumbered broken-link finding is now m293.
Seven findings remain moderate; M7 is now minor. No reviewed finding establishes
a major failure of a headline result. Local statement errors, scope gaps and
evidence limitations are distinguished in the rows below.

**Fix passes, 2026-09-25.** Two later passes on the same day applied the
remedies to the repository. The first (Section 9) fixed 123 of the 127 rows
that remained open (not refuted or superseded) and partly fixed M19, M27, m35
and m177. The second (Section 10) completed M19, m35 and m177 with a Lean
rerun, a rounding fix with a recheck of all saved cuts, and a corrected
checker rerun. It also added fresh runs or new independent reproductions for
M1, m4, M10, m15, m32, m43, m44, m63, m73, m76, m162, m173, m179 and m261, and
an independent review of CM04 and CM34 (m196). The author waived a fresh
review of the September 24 manuscript rewrite, so M27 stays a documentation
fix. Each open row's State cell records its outcome. The paragraph below
describes the reassessment, not the fix passes.

During the reassessment, only this audit document was changed. No computational experiments, Lean
verification, paper builds, project-wide verification or CI inspection were
performed for this reassessment. Checks used source reading, targeted Git
history and archive comparisons, file hashes, and arithmetic on saved data.
The original September 24 audit's reported proof checks and executions are
preserved separately as historical reports in Sections 4–7; they were not
rerun here. Novelty and publication priority remain outside scope.

Row states describe this reassessment: **confirmed** means the stated defect
is supported; **corrected** means its scope or explanation needed revision;
**refuted** means the alleged defect is not established; **superseded** points
to another row or an existing correction covering it. **Archival limitation**
records a limit on reproducibility or traceability without establishing a
false claim or proof gap. Refuted and duplicate rows remain for traceability and are not additional
open issues. IDs are stable historical identifiers, not current severity
codes; in particular, M7 is retained under minor findings.

## 1. Major issues (validity-threatening)

No major issue was established by this reassessment. This does not certify the
repository as error-free. The original two major candidates were downgraded:
M27 concerns current delivery and review scope, while the formal-record
findings must be judged individually. A dated review or historical hash
mismatch alone is not evidence of a failed proof or false current claim.

## 2. Moderate issues

Seven findings remain moderate after narrowing unsupported inferences:

- **Computational reporting:** M10 reports a solver result inconsistent with
  saved reference bounds; M15 overgeneralizes fast SCIP timings across sizes.
- **Evidence and delivery scope:** M1 falsely says a review links its checker;
  M19 lacks retained post-change build/replay evidence for the displayed PASS
  rows; M27 concerns revised manuscripts distributed with earlier archives
  and insufficiently identified review coverage.
- **Mathematical scope and justification:** M4 lacks a citation or proof for
  finite-box isotonicity of the chosen unclipped relaxation; M25 omits the
  one-pool hypothesis from two README summaries.

The specific evidence, limits and proposed document or repository remedies
are below. The reassessment implemented none of them; the 2026-09-25 fix
pass applied them as recorded in Section 9.

| # | State | File | Issue |
|---|---|---|---|
| M27 | corrected after source, history and archive review · **fixed 2026-09-25 as documentation; re-review waived by the author (§9, §10)** | manuscript sources, delivery archives and review records across the paper folders | Commit `aee2afbf` (2026-09-24) changed 168 LaTeX files across 14 paper folders, including abstracts, introductions and comparison prose. Existing reviews do not establish coverage of that rewrite. For example, the cubic standalone review is dated 2026-09-16, and topic 11 records a six-page visual inspection whereas the current saved paper-build record reports seven pages. Those dated records remain evidence for their original snapshots; their age alone does not make them false. The delivery gap is that some package entry points still present review completion and source archives alongside revised manuscripts without clearly identifying the versions covered. The structured-bilevel README, for example, presents its PDF and source ZIP as submission artifacts and says all manuscript reviews are complete. Its source ZIP now differs in 13 manuscript input files, compared with zero before the rewrite. Pooling has 11 changed manuscript inputs, also zero before; quadratic aggregation has 17 changed directly mapped inputs, previously zero. These counts exclude intentionally substituted archive READMEs: structured bilevel uses `delivery/README-source.md`, and pooling uses `submission-README.md`, both of which still match their archived copies. Certified MINLP has 14 differing archived files, previously six, but its README explicitly states that archives and fingerprints retain their earlier scope. Source differences establish that those archives do not contain the current source snapshot; no archive rebuild was run here, so failure to reproduce the committed PDF is not asserted. Neither review drift nor source drift establishes a theorem error. Earlier claims that scope limitations were deleted were withdrawn after checking paraphrases. Fix: identify the revision covered by each review and archive at the delivery entry points; if the package is intended to distribute the revised manuscript, review the changed claims and update its source archive and delivery manifest together. Preserve dated historical review records as historical evidence. |
| M1 | confirmed by source review; wording corrected · **fixed 2026-09-25 (§9, §10)** | `results/positive-multilinear-frequency-two-optimization.md:65` | The note says the independent audit checked 150 small exhaustive instances of the reduction and that its record links the exact verification script. The review record `notes/review-multilinear-frequency-two-optimization.md` does report the 150-instance check, but links no checker. Searches of `code/` and deleted code filenames found no checker for the prize-collecting edge-cover/hub reduction; the similarly named `code/multilinear_frequency_two_verify.py` checks a different gap bound using distribution LPs. The computational claim is therefore documented but not reproducible from the supplied artifacts, and the assertion that the record links its script is false. The review separately gives a mathematical argument for the reduction, so this finding concerns evidence provenance rather than a demonstrated error in the corollary. Fix: archive and link the original checker, or remove the false link claim and identify the reported check as unarchived. A new checker would provide new evidence, not recover the provenance of the original 150 cases. `formal/topics/19-structural-multilinear/SOURCE-REVIEW.md` lists the algorithmic corollary as an adjacent claim outside the queued nonalgorithmic gap scope; it does not itself verify the 150-instance check. |
| M4 | confirmed by source review; wording corrected · **fixed 2026-09-25 (§9)** | `research-20260922/iterated-obbt/theory.md:40` | The note cites Theorem 4 of Scott, Stuber and Barton, Generalized McCormick relaxations (2011), for finite-box isotonicity (R2). In the local source `literature/papers/scott2011-generalized-mccormick-relaxations/fulltext.md`, that theorem concerns the standard procedure in Definition 9, whose Step 6 clips each factor relaxation to its interval bounds; the theorem proof explicitly uses that clipping. Remark 2 warns that omitting Step 6 can violate Theorem 4. Definition 15 is the later generalized procedure, not the definition supporting this citation. In contrast, `proofs-12-11.md` A.1 defines the product and univariate mid rules without factor-output clipping. Thus the citation does not establish (R2) for the defined rule. This is a proof/citation gap, not a demonstrated counterexample to that particular rule. Fix: adopt the clipped Definition-9 procedure, prove (R2) for the chosen unclipped procedure, or restrict the composite application to relaxation schemes satisfying (R2) by assumption. The clipping repair is supported by `proofs-12-11.md` A.2 property (P_k) and A.4 Remark 2: for the fixed factorization with C² univariate factors, natural intervals and exact univariate envelopes, clipping changes the values by `o(w²)` uniformly on compact shape sets; the locally bounded Lipschitz constants propagate this through the finite factorization, leaving Theorem 12's second-order expansion unchanged. This is a local asymptotic statement, not a bound for arbitrary boxes or other relaxation rules. The finite-box uses of Lemma 1(b), including composite applications of Theorems 4 and 6, Corollary 9 and Proposition 11, need the missing justification. The abstract results assuming (R2), Theorem 12's expansion itself, and the original-variable quadratic example with rate 0.7247 are not refuted by this finding. Historical searches reported elsewhere in this audit are not a proof of (R2). |
| M10 | confirmed by source review; wording corrected · **fixed 2026-09-25 (§9, §10)** | `results/shared-variable-term-links.md:210-215` | The note reports that the positive-exponent reference rule solves `ex8_4_7` in 36 s. The saved `code/shared_variable_terms/results_gurobi_60_linked2.jsonl` entry has status 2 and primal/dual values approximately 26.99421396 after 35.70 s. This conflicts with the listed dual bounds for this minimization instance: the archived `research-20260922/curve-hulls/code/listed_bounds.json` (fetched 2026-09-23) and the [MINLPLib instance page](https://www.minlplib.org/ex8_4_7.html) list 29.04368078 from LINDO and primal 29.04730672. The reported optimum is about 7.1% below that dual bound. The previously quoted 28.71179495 is COUENNE's bound, not the best listed dual. This is strong evidence of an invalid solve claim, although the cited JSONL entry contains no incumbent point from which to certify the precise feasibility error or diagnose its cause. The note discusses a different native-run anomaly and attributes an `8.7e-4` violation to the 28.931 result, but the retained point check is for a different incumbent (m22). It does not discuss this linked2 result. Fix: flag the linked2 result as inconsistent with the reference bounds, exclude it from valid-solve comparisons pending original-model validation, and reassess the claim that the reference choice is merely a conditioning matter. The separate curve-hull study already excludes this instance as numerically unreliable (`research-20260922/curve-hulls/report.md:49`). The note does acknowledge that its rule is a heuristic based on one run per cell. |
| M15 | confirmed by source review; wording corrected · **fixed 2026-09-25 (§9)** | `results/separable-vertex-binarization.md:213-218` | The findings say SCIP solves the reformulated asymmetric Jeroslow family up to `n = 120` in about 2 s, but `code/vertex_binarization/results/jeroslow_w.jsonl` records 35.2 s and 240,326 nodes at `n = 18`, versus 27.1 s for the original model. At `n = 12` the reformulation takes 1.49 s versus 0.71 s for the original. The fast results are at the tested sizes `n = 24, 30, 60, 120`, where the reformulation takes 0.8–2.2 s and the original times out at 120 s. The linked experiment record reports this narrower range and includes the outlier; the results note omits it. Fix: state the tested sizes and times, report the small-size regressions, and scope the large SCIP gains to those larger tested sizes. The summary statement that SCIP solves `n = 120` in about 2 s is compatible with its 1.14 s log entry; the defect is the broader wording in the findings. The theoretical results are unaffected. |
| M19 | corrected after source and history review · **fixed 2026-09-25 (§9, §10)** | `formal/topics/17-grid-switching/VERIFICATION.md:39-47` | The linked 1,541-byte run log contains selected axiom reports and `PASS: audited 1921 GridSwitching declarations`, without the build and replay invocations promised by the surrounding text. The earlier log retained in commit `fa3ed328` records targeted warning-free builds, a combined import, import coverage and replay of all 23 modules. Commit `80f36418` replaced that log with the axiom-audit output while changing six proof modules (Coarsening, Examples, InstanceAlgorithms, Model, Rounding and SubsetDP; +437/-28 lines). The surviving detailed build/replay record therefore covers earlier proofs, while the verification table leaves its warning-free-build and kernel-replay PASS rows unqualified alongside the updated axiom result. This does not prove those checks failed or were not run; it leaves their post-change coverage undocumented. The import-coverage row explicitly labels its counts historical, and the audit script imports all 23 modules together, supporting coexistence of the imported artifacts. Importing artifacts is not itself a fresh source build or kernel replay. The later `90eb77ce` change to Coarsening is comment-only and is explicitly documented as requiring no proof rerun. Fix: preserve or link the historical log and label each result with its checked revision; retain post-change build/replay evidence if available, or state that those checks are only evidenced for the earlier proofs. |
| M25 | confirmed by source review; wording corrected · **fixed 2026-09-25 (§9)** | `README.md:630-640` | Two top-level README entries omit the one-pool hypothesis: Contracted degree-two pooling with common throughput bounds and Pooling feasibility with two source-quality vectors. Both linked theorem statements explicitly begin with one-pool feasibility (`results/pooling-contracted-common-capacity-algorithm.md:13` and `results/pooling-two-source-qualities-convex-feasibility.md:13`), and their proofs do not establish an arbitrary multi-pool extension. The entries list several other structural hypotheses, so omitting the pool count broadens their apparent scope. A nearby one-pool qualification belongs to a different indented entry. The pooling paper correctly states the standing assumption (`papers/pooling/sections/05-contract-algorithms.tex:5`), and each README link exposes the missing hypothesis immediately in its theorem. Fix: add one-pool to both README entries. This is a summary-scope error; it neither refutes the linked theorems nor proves that a multi-pool extension is impossible. |

## 3. Minor findings, provenance limitations and withdrawn allegations

These rows distinguish supported minor defects from optional improvements,
historical evidence limits, refuted allegations and duplicates. Missing raw
output does not by itself show that a reported check did not occur. Likewise,
a correct weaker bound, an explicitly limited regression test, or a selective
index is not a validity defect. Proposed fixes must preserve historical
records and must not silently substitute new hashes for old verification.

| # | State | File | Issue |
|---|---|---|---|
| M7 | corrected after source and provenance review; minor · **fixed 2026-09-25 (§9)** | `notes/lbesh-final-publication-review.md:239` | The final publication review records results-note SHA-256 `7d55fb9e...`, but `notes/lbesh-study-results.md` hashes to `b974bbd3...`. The file has one content version in the inspected Git history, also `b974bbd3...`; its 38,648-byte copy in `paper-lbesh/supplement/publication_bundle_v1.tar.gz` and the publication manifest agree with that version. The review fingerprint therefore does not identify the preserved results note. This could be a transcription error or a digest of an unretained intermediate version; the mismatch alone does not establish that reviewed text was lost or that a different text was reviewed. The theory-note digest matches, but that does not rule out a results-note recording error. No numerical error follows from this mismatch. Fix: establish which version was reviewed and correct or qualify the recorded digest; if that cannot be established, record the uncertainty or review the preserved version afresh. Do not simply replace the digest while asserting the old review covered those bytes. |
| m1 | superseded by m186 | `results/potential-flow-cactus-square-root-sum.md:7` | See m186; the opening theorem sentence still omits the cactus hypothesis that scopes the upper-bound proof. |
| m2 | refuted on document recheck | `results/positive-multilinear-second-order-upper.md:167` | The alleged missing output is archived at `paper-relaxation-limits/verification/repository-checks/verify_multilinear_second_order.txt`; `global.json` records its script digest and status 0. No missing-log issue remains. |
| m3 | confirmed on document recheck · **fixed 2026-09-25 (§9)** | `README.md:813-814` | The statement that equal means always give ratio at most two omits the unit-cube scope made explicit in `results/positive-multilinear-equal-marginals.md:5,91-93`. The surrounding README bullet does not supply that scope. Clarify that the claim concerns equal normalized coordinate values on the unit cube; this is a scope clarification, not a counterexample to the bound. |
| m4 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `results/positive-multilinear-gap.md:279` | The supplementary full binary-vertex LP check at `L=2,3` is documented in `notes/review-positive-multilinear.md:116-132`, including the exact envelope values and the checks performed, but no saved primal/dual vectors or checker for that particular reconstruction were located. The separate `code/multilinear_ratio/dyadic_exact.py` and `.log` check the analytic coupling/certificate, not this LP reconstruction. This is a reproducibility limitation, not evidence that the reported review did not occur or that the values are wrong. If retaining the computational detail, archive the reconstructed vectors and checking code, or identify it as a review-time check whose artifacts were not retained. |
| m5 | refuted on document recheck | `results/potential-flow-capacity-rational-witness-boundary.md:3`; `README.md:368-369` | The result explicitly says the Lipschitz strengthening was proposed during review and checked separately by the investigating agent. The review record requests an additional independent review only before calling it multiply audited; the README calls it reviewed, not multiply audited. The cited texts therefore disclose the review scope and do not make the alleged inflated claim. |
| m6 | refuted on document recheck | `results/positive-box-single-monomial-hardness.md:318`; `results/positive-multilinear-positive-box-sharp.md:272` | The alleged missing outputs exist in `paper-relaxation-limits/verification/repository-checks/`: `audit_single_monomial_hardness.txt` records 120 reduction checks and 12,420 binary vertices; `audit-positive-box-coefficients.txt` records 1,589 coefficient/induction cases. |
| m7 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `results/potential-flow-exact-arc-capacity.md:3` | The two linked review addenda refer to `notes/potential-flow-exact-arc-capacity-investigation.md`, now a redirect; its history reachable from `HEAD` contains only the redirect introduced in `d0052e9e`. The detailed reviews remain available and the redirect leads to the result, so this does not refute the two-review claim. It prevents an exact comparison with the draft bytes reviewed. Preserve a dated draft or identify the promoted result as the reviewed successor if exact snapshot provenance is required. The unlinked bounded novelty note is an optional navigation improvement, not a validity defect. |
| m8 | superseded by m122 | `results/ac-power-flow-existential-reals.md:3-4,160`; `notes/review-power-flow-existential-reals-B.md:183-184,319-323` | See m122 for the unfulfilled review-B requests and the overstated completion claim; it includes the range wording and unused-variable-bus issue identified here. |
| m9 | refuted as a missing-proof allegation | `results/potential-flow-polynomial-law-uncertainty.md:24-26` | The cited bounded-block-rank theorem is quadratic, but Section 2 of the linked `notes/review-potential-flow-affine-law-uncertainty-second.md` supplies the general-law transfer: positive smoothed derivatives, graph structure and a compactness limit suffice. The justification is therefore present. Repeating the general-law lemma in the result would improve self-contained exposition, but no missing argument or false conclusion is established. |
| m10 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `results/potential-flow-joint-resistance.md:128`; `code/potential_flow_mpd/joint_resistance_checks.py:23-37` | The evidence paragraph reports 48 checks of the resistance derivative without naming the objective. The checker uses `delta=0.3`, internal adjoint sources, and the objective `pi_a-pi_c+delta*sum_internal(pi_v-pi_c)`. It therefore checks the perturbed-objective identity, not directly formula (3) for the ordinary unit-source/unit-sink objective. Specify that scope; the paragraph does not explicitly say ordinary unit adjoint, as the earlier audit wording claimed. See also m121. |
| m11 | superseded by M27 | `paper-certified-minlp/PAPER-SHA256SUMS` | Tracked under M27. A targeted comparison finds 14 mismatches among 85 manifest entries, including `main.tex` and nine section files. |
| m12 | confirmed on document recheck · **fixed 2026-09-25 (§9)** | `research-20260922/ridge-envelopes/theory.md:133-160` | For the stated lower-semicontinuous real `sigma`, Step 2 should call the integral functional weakly lower semicontinuous, not weakly continuous; compactness still gives attainment. Step 3 also invokes a continuous-function envelope fact although the hypotheses allow lower semicontinuity, and proves dual attainment only when every `p_k>0`, whereas the theorem assumes only `p_0,p_n>0`. Cite the lower-semicontinuous envelope version and complete the endpoint-positive attainment argument: replace feasible vectors by their concave-hull node values, use the objective and node upper bounds to bound endpoint values below, then use concavity to bound all interior values below. These are repairable proof-text gaps, not established false conclusions. |
| m13 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `results/separable-vertex-binarization.md:181-187` | The assertion that a weighted node bound is at most twice the unweighted one needs a specified comparison relaxation. It is immediate for nonnegative chord objectives (and SDP+RLT), but not for arbitrary weaker separable underestimators, which may be negative. Minimal-parameter alphaBB equals the chord in the cited lower-bound note, so alphaBB itself is not a counterexample to the conclusion. Clarify the proof by bounding every weighted separable relaxation by its weighted chord bound, then bounding that by twice the unweighted chord bound and applying the chord lower-bound theorem. |
| m14 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `code/augmented_lagrangian_bb/albb.py:3,14` | The prototype docstring cites the absent `results/augmented-lagrangian-exact-local-bounds.md` and Lemma 3 of that note. Searches found only two scouting reports discussing it; there is no adjacent README. This leaves its intended mathematical reference unclear. However, the docstring describes its purpose, methods, run command, and floating-point limitations, and all three logs contain results: `run_random_n3.log` is 5,453 bytes and `run_random_n4.log` is 4,124 bytes, not empty. Correct or remove the broken source/Lemma 3 reference; add a short scope/results pointer if this prototype is meant to be discoverable. |
| m15 | corrected on document recheck · **fixed 2026-09-25 (§9, §10)** | `research-20260922/benchmark-observations/nuclear_cw_bounds.json`; `code/nuc_verify.py:199-229` within that folder | The verifier computes rational certificates but serializes the derived certified bounds as ordinary floats; rational `w` and `y` remain available for recomputation. The displayed table in `nuclear-bounds.md` uses conservative six-decimal rounding, but the saved `nuclear_table.txt` and `code/nuc_table.py` use nearest rounding (for example, nuclearva is `-1.184633` there versus the conservative `-1.184634` in the note). Thus the JSON/generated-table numbers should not be described as exact or automatically outward-rounded certificates. Retain the derived rational bounds as fractions and generate outward-rounded display values from them, or label these outputs as decimal approximations. |
| m16 | refuted on document recheck | `results/four-aggregation-strict-pdlc.md:409-417` | The assertion that no second check is recorded overlooks the result paragraph explicitly recording the coordinator re-derivation of the independent positive perturbations. `notes/review-20260922-pdlc-transfer.md:228-251` also records an independently checked dependent-triple perturbation route. The fresh reviewer did propose an extension, but the record does not leave it unchecked as alleged. |
| m17 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `results/infinite-quadratic-aggregation-hhc.md:384-388`; `results/quadratic-aggregation-trivial-hull-certificate.md:3-7` | The broad missing-output claim is false: `paper-quadratic-aggregation/build/stage07/exact-checks.log` records the supplement checker passing 2,601 ray identities and six finite-family witnesses, the same checks with added assertions in `supplement/check_infinite_aggregation.py`. However, `supplement/check_examples.py` is a different exact-arithmetic program from the SCS-based `code/quadratic_aggregation/check_examples.py`; its PASS does not archive the latter's 30-random-instance run. No output for that particular numerical run was located. Link the existing exact evidence and, if the numerical run counts are retained as reproducible evidence, archive their output. The note already correctly calls the SCS work numerical sanity checks. |
| m18 | refuted on document recheck | `README.md:233-236` | The README explicitly limits this sentence to topic 29's formal scope. Hull formulas and SDP lifts are outside that package; topic 30 subsequently formalizes them and is linked elsewhere. The sentence does not call the mathematical formulas open and is not false. Adding topic 30 at this entry would be an optional index improvement. |
| m19 | refuted on document recheck | `results/cluster-free-branch-and-bound-constrained-minima.md:245-248` | The displayed unconstrained bound with `2 tau` is valid: the proof permits the sharper constant `tau`, which implies this weaker bound. The theorem asks for an admissible positive constant, not its minimum. Sharpening the display is optional and is not a validity issue. |
| m20 | confirmed on document recheck · **fixed 2026-09-25 (§9)** | `results/composite-univariate-envelopes.md:75-76` | Unknown intervals need not occur only near inflections or singular endpoints. The algorithm also marks an interval unknown when its finite-width ball enclosure cannot decide the sign of the second derivative; the same section and review discuss this enclosure issue, including the shifted-quartic example. Replace the exclusive claim with that algorithmic condition, giving inflections and singular endpoints as examples. |
| m21 | superseded by M15 | `results/separable-vertex-binarization.md:216-217` | See M15; the body still says SCIP solves up to `n=120` in about two seconds, omitting the `n=18` outlier. |
| m22 | confirmed on document recheck · **fixed 2026-09-25 (§9)** | `results/shared-variable-term-links.md:81-83` | The asserted exact-arithmetic violation of `8.7e-4` for the 28.931 incumbent is not supported by the cited evidence. `review/osil_eval.py` is explicitly a plain-float evaluator, and `review/note_model_point_check.jsonl` records violation `0.0008653346` for a different incumbent, objective `28.92206146`. No retained evaluation of the 28.931 point was located. Attribute the numerical violation to the reproduced incumbent and qualify the inference about the original run, or archive and exactly evaluate the original point. |
| m23 | confirmed on document recheck · **fixed 2026-09-25 (§9)** | `results/shared-variable-term-links.md:43-46,182` | (a) The blanket statement that dual bounds are below best known primal values is wrong for maximization: `results_gurobi_60_moment.jsonl` gives `pricing050` duals about -1283 and -1275, above the listed primal -1813.8. Say they are on the valid side according to the optimization sense. (b) Define the relaxation whose volume is reported as 0.0730: individual term envelopes intersected with the planar hull of `t3=t2^(3/2)` on `t2 in [1,4]`, as specified in `notes/review-shared-variable-term-links.md:243-250`. The equality alone is not that full-dimensional relaxation. |
| m24 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `notes/row-hull-experiments.md:236,344-350`; `results/row-hull-separable-concave.md:82,547`; `README.md:59-60` | Several summaries need consistent scope. The current test source has 217 cases (216 parametrized plus one pricing regression), while the experiment record retains a historical 216-pass command; date that run and mention the later added test rather than rewriting historical output. The results summary places the all-family statistic (45 of 54 easy cases slowed) in the unequal-width clause; saved Gurobi rows give 39 of 45 for unequal widths, and 45 of 54 over all 130 cases. The saved SCIP data give roughly 4.42-6.33 times slower for full-tree versus root-only separation, not 4-5 times. README's statement that BARON confirms the direction should be qualified as three of four water instances; `waterno2_06` falls from 73.7 to 72.8. |
| m25 | corrected on document recheck · **fixed 2026-09-25 (§9)** | `results/smoothed-fixed-treewidth-indicator-dp.md:513-515` | The sentence that a fresh integrated adversarial review remains pending is stale: the header links `notes/review-20260922-fixed-treewidth-result.md`, which reports the completed correctness review. Update that sentence to the completed review and its scope. The separate statement before Section 7 that a dedicated priority review is still required is consistent with the review's explicit exclusion of priority and should remain; there are not two contradictory correctness-review status sentences. |
| m26 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `results/smoothed-spectral-indicator-messages.md:3`; `notes/review-20260922-nearopt-enumeration.md:5`; `notes/review-20260922-spectral-parametric-oracle.md:5` | The reviews identify the former draft path, now an 18-line promotion notice pointing to the full results note. Its only recorded commit, `2cd1bf23`, already contains that notice. Neither review pins the draft by revision or digest, so exact identity between the reviewed draft and promoted text is unrecorded. This does not show that the theorem text was lost: the full proof is preserved at the promoted path and the reviews discuss its arguments in detail. Fix: link the reviews directly to the promoted result and, if the reviewed version can be identified, record that version; otherwise disclose the missing version pin. |
| m27 | refuted on recheck | `code/research_20260922/check_smoothed_block_dp.py:135-159`; `results/smoothed-indicator-block-dp.md:183-185,213-219,661-663` | The checker tests the older derivative bound on stored full quadratics, some of which include the boundary vertex's own terms. Formula (9) applies after those common terms are removed. The results note explicitly limits the checker to deterministic identities and says it does not test the general expected-time theorem. Adding a normalized derivative assertion would strengthen testing, but its absence is not a false verification claim or a theorem defect. |
| m28 | corrected on recheck · **fixed 2026-09-25 (§9)** | `research-20260922/ridge-envelopes/theory.md:135-158,218-260`; `research-20260922/README.md:17` | The status says review corrections are applied, but Step 2 still calls the integral functional weakly continuous rather than weakly lower semicontinuous, and Step 3 proves attainment only when every weight is positive although Theorem 1 also covers interior ties. The endpoint-weight argument is given in `review-theory.md` and should be incorporated (overlap with m12). Corollary 2 itself correctly assumes positive coefficients and explicitly discusses nonnegative/nonpositive coefficients and the failure for mixed signs; it is not missing its hypothesis. The README extension sentence and the mixed-domain sentence omit this limitation for existing order constraints. Fix: complete the attainment argument, use the lower-semicontinuous duality statement, and retain compatible coefficient-sign conditions in those summaries. |
| m29 | corrected on recheck · **fixed 2026-09-25 (§9)** | `research-20260922/ridge-envelopes/nn-experiment/report.md:71-72,84`; `results/bnb/` and `results/root/sigmoid_d2_16_ackley.json` within that experiment | In 23 of 160 saved B&B records, `t_sep` exceeds total reported process CPU time, with maximum ratio 1.42449. This is inconsistent with the nested `time.process_time()` intervals in the committed `bnb.py` and `relax.py`; the saved data alone do not establish which clock or code version caused it. The 91%/98% separation shares cannot be interpreted as fractions of total CPU time without resolving that mismatch. Aggregate total CPU time per processed node is 0.1034 s for R0 and 0.3543 s for R1; any alternative aggregation behind 0.087/0.31 s should be specified. Also, the saved root comparison for `sigmoid_d2_16_ackley` minimization gives R1 = -2.212798522547568 versus R0 = -2.21279706136749, a decrease of 1.46118e-6, for both IBP and OBBT. Fix: qualify the numerical monotonicity claim and document comparable timing fields and their aggregation. These discrepancies do not reverse the recorded overall solve-time conclusion. |
| m30 | corrected on recheck · **fixed 2026-09-25 (§9)** | `research-20260922/ridge-envelopes/numerical-verification.md:14,39,102-109,159-168`; `code/run_verification.py:142,174` within that topic | The report calls tolerance-based concavity constraints and grid/refinement searches exact. The reduction to one dimension is exact, but Gurobi feasibility tolerances and an uncertified global search do not give exact cut-validity certificates; the later no-interval-arithmetic caveat should govern the summary too. The largest saved n=2, N=161 grid gap is 9.29263e-6 (`cube_m3x`), while some cases are at floating-point zero, so 1e-6–1e-9 is not the full range. The per-point-kind statistic at line 174 compares lower endpoints, although the report calls it a midpoint difference; the main aggregate at line 142 really does compare midpoints. Fix these descriptions and distinguish the exploratory S-shape observations from the current theorem, which claims no closed form. Testing that withdrawn candidate structure is not itself an error. |
| m31 | corrected on recheck · **fixed 2026-09-25 (§9)** | `research-20260922/iterated-obbt/theory.md:48,259,429,440,464-488`; `proofs-12-11.md:621` | Corollary 9 invokes Proposition 2's sharp-case limiting-width conclusion without restating its small-width entry and epsilon conditions. The arbitrary-start quadratic proof uses a containing symmetric box that need not lie inside the original `B_0`; extend the quadratic relaxation explicitly to that box and use its global box monotonicity. Define the box hull as closed to support Lemma 1(c)'s compactness argument. Proposition 11's introduction and proof-file remark say the contraction ratio is exactly lambda, but the proof supplies an upper bound by lambda; lambda is an admissible chosen bound, not a proved exact asymptotic rate. Fix this wording, reconcile the remaining sketch with the linked full proof, and call the Castro experiment consistent with the theory rather than an instance proved to satisfy its hypotheses. |
| m32 | corrected on recheck · **fixed 2026-09-25 (§9, §10)** | `research-20260922/benchmark-observations/nuclear_table.txt`, `nuclear_cw_bounds.txt`, `code/nuc_table.py`, `code/nuc_verify.py`, `nuclear-bounds.md`; `research-20260922/nuclear-global/code/review/cert_root_iep.py:145` | The two generated text tables still use nearest rounding for inequalities: e.g. `obj >= -1.184633` exceeds the saved underlying bound about -1.18463307. The Markdown table alone was corrected. Generate displayed upper/lower bounds with outward rounding from exact values. The model description writes ideal peaking fractions (including 1/6, 1/12, 1/24.5 and 1/52), whereas certificates use the model's decimal coefficients; label the fractions as approximations. The nominal 300 s SCIP limit was exceeded in `nuclear104_scip_0.json` (567.949 s), so distinguish requested limit from elapsed time. For nuclear14a the table's reported row violation 5.8e-9 omits the larger integrality violation 2.779e-7 if its heading is intended to mean maximum overall violation. The row-regeneration script exists, but the claimed completed run lacks a linked retained output. Finally, the review says final exact rationals are printed, yet adopted B2 values are output only as nine-decimal floats; the preceding B1 output does print a rational. Fix the output-description mismatch or archive the exact B2 values, without suggesting the displayed six-decimal outward bounds are thereby invalid. |
| m33 | corrected; narrower scope claim · **fixed 2026-09-25 (§9)** | `research-20260922/nuclear-global/assessment.md:70` | The summary says every relaxation that does not solve the coupled equilibrium loses about 13%, although only four relaxations were tested. Restrict this statement to the tested relaxations. The leading correction block already strengthens the domain of the unproved uniqueness assumption U and supersedes the old enumeration/pruning claims; those historical body statements are not separate unresolved errors (see m200). Any future certified enumeration would also need to justify the computed points and exclusion decisions in that domain. No completed enumeration or proof of U is claimed. |
| m34 | corrected on recheck · **fixed 2026-09-25 (§9)** | `research-20260922/benchmark-observations/report.md:48,104-106`; `structural-bounds.md:101`; `research-20260922/scouting/brainstorm2-structural.md:304` | For even polygon N, duplicating one vertex creates m+2 tight distance rows (51 for N=50 and 101 for N=100), rather than the claimed m=N-1. The Gurobi mpbp_06 incumbent was evaluated only in float (`grb_check.py` and its saved JSON), while the report says every incumbent was checked at 50 digits; that higher-precision evidence exists for the four SCIP runs. Saved SCIP metadata labels the PySCIPOpt version 6.2.1 as `scip`; it does not pin the SCIP library version claimed in the report. Fix these counts, scope and version labels. The K=80 LP and BFGS observations lack linked saved outputs, and the scouting ranking calls probe bounds certified despite its own uncertified-method caveat; distinguish reported exploratory runs from archived certificates. Do not count the older elec25 log rounding as an unresolved issue: the very next log entry records its correction. |
| m35 | corrected on recheck · **fixed 2026-09-25 (§9, §10)** | `research-20260922/curve-hulls/report.md:186,263`; `research-20260922/curve-hulls/code/curvehull.py:247-260`; `research-20260922/eigen-cg/investigation.md:18,194,305` | The blanket curve-hull statements that all affected runs were rerun and every reported model check passed exceed the retained evidence: the documented regeneration covers waterno2 cuts, and `modelcheck_rescaled.out` records a JSON decode failure for lnts100. The now-parseable `cuts/lnts100.json` has no linked successful replacement check or run identity in that record. Qualify those statements and identify the source/scaling version of each compared control; file timestamps alone do not establish a version mismatch. In `_piece_lower`, the final subtraction used for the chord bound is not explicitly rounded downward; existing safety margins may absorb its rounding error, but the certification argument should justify that or round this step outward. No invalid saved cut was demonstrated here. In Eigen-CG, the summary still says two BH inequalities suffice without the nonnegativity inequalities needed for rounding slack, and the support sentence should require support at least six, not full support for n>6. The 6,036-cut run uses a finite BH outer approximation with floating-point LP tolerances and lacks linked saved output; describe that scope. An outer approximation is sufficient for a nonnegative lower-bound implication. The README already labels the curve-hull solver runs uncertified, and the report discloses the phase-1 anomaly; those disclosures are not separate defects. |
| m36 | refuted on recheck | `notes/lbesh-study-analysis-method.md:104-109`; `code/minlp_solver_lab/results/lbesh_development/analysis_legacy_v2/` | The listed CSV export exists and is empty because this bundle's `cone_roots` table is empty; the same holds in the primary and repetition bundles. The note does not promise that every export contains observations. Root data and the paper table are retained separately. No incorrect cone-root count or missing claimed data was established. |
| m37 | refuted on recheck | `README.md:230-236,1021-1024` | The exclusion of hull formulas and SDP lifts is explicitly scoped to the linked topic 29 package. The closing paragraph separately identifies topic 30 as proving those claims. These statements are compatible; saying that a small SDP lift remains possible is also true. Consolidating the links could improve navigation but is not a missing formalization or false scope claim. |
| m38 | superseded by m187 | `README.md:44-46`; `results/row-hull-separable-concave.md:17-24` | See m187 for the separate endpoint-rounding correction and its effect on the historical benchmark scope; do not count this duplicate separately. |
| m39 | refuted on recheck | `README.md:799-803` | The README states the analytic family's bound 483/223 and immediately records the certified improvement to 1610000/743033. Both are valid and the stronger value is already present. There is no stale or omitted constant to correct. |
| m40 | refuted on recheck | `README.md:1008-1015` | The short repository-layout list omits the research continuation directory, but does not claim to enumerate every directory. Adding an entry would be a navigation improvement, not an incorrect scientific or verification claim. |
| m41 | refuted on recheck | `README.md` | A direct filename check finds 57 of 207 results notes unlinked from the README. The README does not promise a complete inventory, so this establishes partial indexing rather than a defect in a result, proof, or evidence claim. |
| m42 | refuted on recheck | `results/quadratic-system-noncommutative-rank-complexity.md:3`; `notes/review-quadratic-noncommutative-rank-second.md` | The result links one completed independent review and does not say that only one exists. A separate second review supports the stronger README description. Omitting the additional link is a navigation opportunity, not an incorrect review-status claim. |
| m43 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `notes/review-spatial-bb-lower-bound.md:280`; `results/spatial-bb-relative-gap-exponential-lower-bound.md:226` | Some reviewer-run computations are preserved only as written reports, not as reproducible reviewer programs. For example, the lower-bound review names `/tmp/review/check.py` and `/tmp/review/check2.py`; those locations are not repository artifacts. The relative-gap result separately quotes 2,660 identities per configuration from its review, whose independent program is not linked. Distinguish those reported review checks from the committed author checkers and their saved outputs. Fix: archive and link an independent checker when available, or label the counts as reviewer-reported rather than independently replayable from retained artifacts. This is a provenance limitation, not evidence the checks were not run; the previous aggregate of 15 affected reviews is withdrawn because the row did not identify that set. |
| m44 | confirmed on recheck · **fixed 2026-09-25 (§9, §10)** | `code/spatial_bb_lower_bound/check_sdp_rlt_strengthening.py:60-61,81` | The success message calls the checks exact, but positive semidefiniteness is checked by NumPy floating-point eigenvalues with tolerance -1e-10. Rational identities can be exact while this PSD check is numerical. Fix the success message to distinguish the two; the result note already makes this distinction. |
| m45 | refuted on recheck | `notes/network-simplex-paper-readiness.md:3-13,163`; `code/network_simplex_review/final-validation.json` | Nine of 67 pinned hashes differ from the current tree, but the readiness record opens with an explicit historical-closeout banner, says the manuscript supersedes it, and preserves the old numbers as historical evidence. That is exactly the snapshot qualification the original finding said was absent. Do not regenerate this historical manifest merely to match later source. |
| m46 | corrected on recheck · **fixed 2026-09-25 (§9)** | `formal/topics/00-exact-counts/VERIFICATION.md:14`; `formal/COVERAGE.md:54-59` | The verification table reports an independent specification review without linking a retained review report; its build/audit/replay log does not document that prose review. This is limited review provenance, not evidence that the review never occurred. The coverage narrative says the weighted-box formulation uses fewer auxiliaries than the note, but the current note already uses the same three-weight construction with 3n auxiliaries and 13n inequalities; qualify that comparison as historical or remove it. The table's `constants` entry is a private theorem, but its explicit Scalar file link uniquely identifies it, so the separate claim of an ambiguous declaration is withdrawn. |
| m47 | superseded by m167, m168 and m169 | `notes/lbesh-study-results.md:584`; `notes/lbesh-development-theory.md:3`; `notes/lbesh-publication-readiness.md:33-36` | The root/assignment wording, combined-export label and pending-review status are recorded separately in m167–m169. The additional allegation about accepted witnesses is refuted: the acceptance rule explicitly requires a checked feasible witness, and independent revalidation is separately described. |
| m48 | refuted on recheck | `code/cia_reopened/final-validation.json` | This is an explicitly dated 2026-09-07 integration record, not a claim that its files never change. Six of its 37 hashes now differ (including three results notes), identifying later edits; the original row incorrectly counted 39 hashes and two results notes. Current-tree drift alone does not invalidate the historical checks or justify replacing historical hashes. No assertion that the later versions were covered by that dated run was established. |
| m49 | confirmed on recheck · **fixed 2026-09-25 (§9)** | `paper-correlated-measurements/supplement/validate.py:45-49`; `supplement/results/validation.json`; `supplement/README.md:29-45` | The README describes validation of both archive and source manifests and identifies `results/validation.json` as the completed suite. The committed checker always adds `source_manifest_files`, but the saved report lacks that key, so it is not an unmodified report from the current checker. This does not prove the scientific stages failed; it leaves the current combined wrapper without the described saved passing record. Fix: identify the saved report's checker version and distinguish later integrity changes, or retain a fresh full report after actually rerunning the current wrapper. |
| m50 | refuted on recheck | `code/bilevel_nonconvex/verification_summary.json` | The record is dated 2026-09-07 and scopes itself to the nonconvex-bilevel follow-up. Only its root README digest has changed; all 23 other hashes match. Later edits to the shared README do not contradict that dated verification snapshot, and no claim that it certifies the current README was found. |
| m51 | superseded by m14 | `code/augmented_lagrangian_bb/albb.py:3,15` | See m14 for the missing `results/augmented-lagrangian-exact-local-bounds.md` and unavailable Lemma 3. The prototype does describe its purpose, numerical limitations and run command in its module docstring; the defect is the broken mathematical reference, not absence of all documentation. |
| m52 | refuted after recheck | `notes/cia-reopened-practical-algorithm.md:73-103` | The scripts and pinned benchmark input identify reproducible checks, and `notes/review-cia-reopened-practical-algorithm.md:43-63` records the 530 comparisons, synthetic value `97301/200`, public value `1889/1000`, switching boundary and independently measured runtimes. `code/cia_reopened/final-validation.json` preserves source fingerprints and distinguishes research runs from closeout checks. No claim promises an additional raw log. Its absence alone is not an unsupported-result defect. |
| m53 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `paper-quadratic-aggregation/sections/09-formal-overview.tex:22-24` | The table lists all of Example `ex:closed` as verified, but `formal/topics/28-quadratic-aggregation-consequences/CLAIMS.md` C09–C10 cover strict infeasibility, proper closed hull, trivial convex aggregates and HHC, and explicitly exclude the additional BDS-good-aggregation assertion. The example also proves full-dimensional interior and the absence of good closed-system multipliers; these are not included in C09–C10. Fix: qualify the table as covering the strict-feasibility counterexample properties and explicitly exclude the interior/BDS-good-aggregation argument from the claimed Lean coverage. |
| m54 | refuted after recheck | `README.md:312` | “An SDP decision procedure” summarizes Corollary 3, itself titled “deciding a trivial hull by semidefinite programming,” which says exact SDP feasibility and optimum values decide the question. Neither the README nor the corollary claims an implemented floating-point classifier or a bit-complexity bound. Adding “exact” could clarify the label, but the reported implementation overclaim is not present. |
| m55 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `README.md:308-310` | The phrase “a positive semidefinite quadratic part other than a negative constant” attaches “negative constant” ambiguously to the quadratic part. The theorem says every nonzero nonnegative aggregation with PSD quadratic part must be a negative constant function when the hull is the whole space. Fix: write that formulation, including `A_lambda = 0`, `b_lambda = 0` and `c_lambda < 0`. This is a wording defect; the original exception already prevents reading the sentence simply as excluding every PSD aggregate. |
| m56 | refuted after recheck | `notes/certified-minlp-repair-and-replay.md:52` | The note calls this an “independent arithmetic audit,” not an independent parser or end-to-end checker. Its directly linked JSON states that it reuses the exact row parser and recombines with standard-library `Fraction`. The label matches that limited arithmetic independence; the note also disclaims a second checker implementation. |
| m57 | refuted after recheck | `paper-certified-minlp/experiments/final-source-copy-integrity.json` | All 27 listed files in the distributed core and in `supplement/certified-minlp-core.tar.gz` match the preserved V3 snapshot byte for byte. Later changes in the development tree `code/minlp_solver_lab/` do not falsify an assertion about the distributed core. The original row compared the wrong copy. |
| m58 | superseded by M27 | `paper-certified-minlp/PAPER-SHA256SUMS` | See M27 for source/delivery divergence. A targeted hash comparison finds 14 mismatches among 85 entries. The package README explicitly preserves the earlier scope of these fingerprints; the historical manifest should not be silently overwritten to imply a new verification. |
| m59 | refuted after recheck | `notes/certified-minlp-repair-and-replay.md:56` | The note explicitly says “Reference rounding or numerical feasibility can matter,” excludes all 23 beyond-bound references from the closed-gap count, and says none certifies optimality. It never attributes every discrepancy to reference rounding. Cases larger than a rounding half-width do not contradict the sentence. |
| m60 | refuted after recheck | `paper-multilinear-gap/verification/review.md:3,43-49` | This record is explicitly dated 2026-09-13 and accurately reports its 41-module, 733-declaration run. It links `formal/VERIFICATION.md`, which distinguishes that historical run from the subsequent 48-module, 827-declaration completion and links the completion review. A dated review is not a claim to cover modules added afterward. |
| m61 | refuted after recheck | `paper-cubic-gap/main.tex:233-241` | Repeated supports in the nonnegative expansion can be collected: convex and concave envelopes scale with each nonnegative coefficient, so their total width is unchanged when equal monomials are merged. Moreover, the preceding cube proof sums common-law inequalities term by term and does not use distinctness. Omitting this elementary collection step does not create a mathematical proof gap. |
| m62 | superseded by M27 | `paper-quadratic-aggregation/artifacts.sha256`; `dist/quadratic-aggregation-source.zip` | See M27 for delivery divergence. Two of four artifact fingerprints mismatch (`paper.pdf` and `formal-supplement.pdf`), and 17 archived source files differ from their current counterparts. This establishes stale source delivery; no LaTeX rebuild was performed to test byte-for-byte PDF reproduction. |
| m63 | confirmed after recheck · **fixed 2026-09-25 (§9, §10)** | `paper-certified-minlp/formal/README.md:21-25,52-53` | The README calls `verification/extension-SHA256SUMS` the current source manifest and includes its check in standalone reproduction commands. Two of its 34 entries mismatch: `Verify.lean` and `verification/ExtensionAudit.lean`. Thus this advertised current-source check fails before proof verification. Fix: identify the manifest’s recorded snapshot and provide the matching source revision, or issue a new manifest with appropriately scoped evidence for the changed audit programs. Do not imply that all formal proof sources fail or that a new hash alone renews verification. |
| m64 | refuted after recheck | `formal/VERIFICATION.md:1-5,108-113` | The opening expressly says the counts, commands and fingerprints describe original stages, not the current tree, and the hash command is introduced as checking the “recorded ... snapshot.” Its 25 mismatches among 171 files in today’s tree are expected snapshot drift, not a failed claim of current verification. Historical fingerprints should be retained. |
| m65 | superseded by m58 and m64 | `notes/audit-20260924-repository-issues.md` | The earlier count correction is incorporated into m58 (14/85 paper-package mismatches) and m64 (25/171 historical root-formal mismatches, including seven paper sections). It is not a separate repository defect; the original line reference no longer identifies these counts. |
| m66 | superseded by M27 | `paper-cubic-gap/formal/VERIFICATION.md`; `paper-cubic-gap/verification/SHA256SUMS` | See M27 for delivery/source drift: eight of 88 delivery fingerprints mismatch. The claim review is explicitly dated 2026-09-16, and its reviewed source remains preserved in Git; later edits do not make that historical review false. Withdraw the original assertion that the reviewed text “no longer exists.” |
| m67 | refuted after recheck | `formal/scripts/check_imports.py`; `formal/CheckBasis.lean` | The library and coverage check intentionally target `Formal/**/*.lean`. `CheckBasis.lean` is a scratch file importing Mathlib and issuing eleven `#check` commands; it declares no theorem, definition or axiom on which any claimed result depends. Its exclusion is not evidence of an unchecked proof. A hypothetical future proof outside the library is not a present validity defect. |
| m68 | refuted after recheck | `results/shared-variable-term-links.md:129-133` | Recomputing the shifted geometric mean over all 48 instances gives 8.21868 s native and 8.40256 s linked, matching 8.2/8.4 in the note. As in `compare_rules.py`, each unsolved record receives the 60 s limit. The original audit’s 7.5/7.6 figures do not use that convention. |
| m69 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `notes/separable-vertex-binarization-experiments.md:109-113` | The sigmoid discussion says the BARON `m = 5` run is missing and the SCIP/BARON runs at `n >= 50` were not completed, although the table immediately above contains those results. The BARON reformulated gaps across the full table span 3.3–3.8%, not 3.3–3.5%. Fix: remove the missing-run claims and state the size range used for each numerical summary. |
| m70 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `notes/composite-univariate-envelopes-experiments.md:126-128` | “Every run” and “324 runs” overstate the reference comparison’s coverage. `code/univariate_envelopes/consistency.py` skips error records and instances without parseable reference bounds. Of 324 saved records, the `t1000` split error and all six runs for `ex8_6_1` and `uselinear` are excluded, leaving 317 eligible comparisons. Fix: report 317 compared records and list these exclusions; a lack of violations is a consistency check against reference data, not a proof of every run’s soundness. |
| m71 | refuted after recheck | `notes/row-hull-experiments.md:408-411`; `code/row_hull/results/code_version.sha256` | The hash file is described as the code of the final experimental reruns. Its `rowhull/rows.py` digest exactly matches that file before commit `6903d2ec` (2026-09-22), which later corrected endpoint handling. That is valid historical provenance, not an assertion that the current code still matches. Replacing the hash without rerunning would misidentify the experiment source. |
| m72 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `results/row-hull-separable-concave.md:543-550`; `notes/row-hull-experiments.md:234-238` | Recomputing the repository’s family-summary convention from `code/row_hull/results/scip_sepa_sweep.jsonl` gives full-depth/root-only node-reduction factors 1.50–3.37, depth-8 node reductions 2.08%–20.98%, and full-depth/root-only time factors 4.42–6.33. Fix the quoted 1.3–3.4, 5–20% and 4–5 ranges in both summaries. These are shifted-geometric family summaries, not per-instance bounds; the random-log full-depth set has four seeds while root-only has five, as the experiment note discloses. |
| m73 | confirmed after recheck · **fixed 2026-09-25 (§9, §10)** | `notes/row-hull-experiments.md:188-218`; `code/row_hull/README.md:33` | The minimal branch-and-bound table explicitly retains pre-pricing-fix `uniform` and `uncap` results while asserting the fix did not change them. Mode `L` calls the affected `RowSeparator.separate` on child boxes, where equal root widths need not remain equal; the saved `random` rerun alone does not establish unchanged results for these families. The code README also says superseded-pricing-bug runs are “not used,” contrary to this table. Fix: label retained rows and the combined 5–29 node ratio as historical, remove the unsupported unchanged-result assertion, and qualify any current-code comparison to the actually rerun cases. Rerun only if fresh performance claims are wanted. |
| m74 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `notes/separable-vertex-binarization-experiments.md:140-146`; `results/separable-vertex-binarization.md:229` | The claim that the five other box-QP instances change by at most 20% is contradicted by `spar080-025-1`: 0.557087 s originally, 0.707591 s in `bin` (+27.02%), and 0.742157 s in `bin2` (+33.22%). `spar060-020-1` takes 0.076047 s originally and 2.108871 s in `bin`, a factor 27.73 rather than 20. Fix: report these measured figures or round the multiplicative slowdown to about 28; the one-run comparison still supports no demonstrated benefit. |
| m75 | confirmed after recheck · **fixed 2026-09-25 (§9)** | `research-20260922/curve-hulls/report.md:160-167` | The per-piece lower bound `min(g(a),g(b)) - M*(b-a)^2/8` requires `M >= 0` as well as `M >= sup g''`. With `g(t) = -t^2` on `[0,1]` and `M = -2`, it returns `-3/4`, above the true minimum `-1`. Fix: use `max(0,M)` or define `M` to be a nonnegative upper bound. `code/curvehull.py::_piece_lower` already applies this clamp, so this is a report formula error and does not show an invalid computed cut. |
| m76 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `research-20260922/eigen-cg/investigation.md:306` | Section 6.1 reports 6,036 F3 cuts and a minimum of at least -2.3e-13, but the retained driver `code/t6.py` prints its results to stdout and no corresponding run output is identified in the investigation or retained in its code directory. Fix: archive and link the output, or label the count and minimum as an unarchived numerical observation. The driver uses bounded separation without `exact=True`, but this does not itself undermine a nonnegative minimum: omitting valid BH inequalities enlarges the LP relaxation, so a nonnegative minimum over that relaxation still supports implication, subject to the floating-point caveat already stated immediately before Section 6.1. The earlier audit incorrectly treated the known separation false positives as evidence against these no-violation results. |
| m77 | confirmed by source review · **fixed 2026-09-25 (§9)** | `research-20260922/eigen-cg/investigation.md:20,194` | Two summary statements conflict with the correct argument and the independent review. The rational-direction case needs two BH inequalities plus nonnegativity BH inequalities to absorb coefficient-rounding residuals; two alone suffice in the no-rounding F2 case. Section 4(a) establishes support at least six, not necessarily “full support 6” in larger dimensions. Fix: make these two wording changes, matching Section 4(c) and `review.md:100-102,189`. |
| m78 | confirmed with corrected scope · **fixed 2026-09-25 (§9)** | `research-20260922/README.md:121` | The README compares the safe bound -93325.22 for `pooling_sppc0pq` with -95124.69 from `pooling_sppc0tp` without naming the variants or carrying the equivalence assumption disclosed in `pooling-multiattribute/verification.txt:10-12,32-34`. Fix: use the like-for-like archived pq comparison, -93325.22 versus -95824.43, and date it to the 2026-09-23 library snapshot; alternatively state the cross-variant assumption. The improvement survives. The bound comes from a 46-point, piecewise McCormick Balas outer relaxation, but the README merely says “multi-attribute pooling cuts,” not “exact hull cuts”; that wording alone is not a demonstrated method error. |
| m79 | confirmed by source review · **fixed 2026-09-25 (§9)** | `paper-multilinear-gap/README.md:80-87` | The advertised command for checking the delivered snapshot, `sha256sum -c verification/SHA256SUMS`, fails on seven files: `formal/Verify.lean`, `main.tex`, `main.pdf`, and four paper build/text records. All 48 bundled proof-module entries pass. The recipient-rebuild metadata caveat does not cover these mismatches in the committed delivery. Fix: issue a reviewed, internally consistent delivery with matching fingerprints, or clearly identify and provide the earlier snapshot to which this manifest applies; do not reinterpret historical verification as a new run. |
| m80 | refuted by source review | `formal/topics/07-multilinear-disproof/VERIFICATION.md:1,33-38` | This is a dated 2026-09-12 verification record. `formal/VERIFICATION.md:1-5` and `formal/README.md:68-71` explicitly say earlier topic commands, counts and fingerprints describe their original snapshots. A checksum mismatch in a later tree does not refute that historical check; the audit’s claim that drift is undisclosed is incorrect. No current-tree build or replay failure was established. |
| m81 | refuted by source review | `formal/topics/07-multilinear-disproof/README.md:52-55` | The linked `REVIEW.md:1-5` explicitly defines the reviews as independent of the root integrator and discloses that the second reviewer authored two modules and reviewed the others. “Two independent agent reviews” does not claim two nonauthor reviews of every module. No undisclosed authorship or missing review is established. |
| m82 | refuted by source review | `paper-multilinear-gap/formal/COVERAGE.md:98` | The claim that no hit count or identity exists is false. `Formal/MultilinearGap/Construction.lean:163-196` defines the local count `D = sum_b (1 - P b)`, equal to the number of hit blocks on Boolean vertices, and proves the identity `anchor * (blockCount - D) = sum_b monomial` inside `level_lower_bound`. Summing it and using the prescribed means, common maximum and endpoint attainment yields the paper’s failure representation. The coverage guide explicitly permits composed identities rather than a named endpoint for every proof line. |
| m83 | superseded by M27; historical-count allegation refuted | `paper-multilinear-gap/verification/review.md:3,43-56` | The 41-module/733-declaration preparation review is explicitly dated 2026-09-13. `formal/VERIFICATION.md` begins with the 48-module/827-declaration completion and links `verification/completion-review.md`, so the earlier counts and then-unformalized calculations are historical, not false current counts. Any concern about manuscript prose changed after these reviews is already covered by M27 and should not be counted again here. |
| m184 | corrected after source review · **fixed 2026-09-25 (§9)** | `formal/Formal/MultilinearGap/BalancedRefinement.lean:655-681`; `results/positive-multilinear-positive-box-sharp.md`, Verification and scope | The results note states its refinement using N nonfixed coordinates, then unqualifiedly says the Lean package formalizes that refinement. `PositiveBoxAspectBoundOfDim` and `positiveBoxAspectBound_add_orientationBeta` use ambient dimension, allowing fixed coordinates; they do not themselves perform the dimension-reducing step. Fix: say the Lean theorem proves the ambient-dimensional bound and identify discarding fixed coordinates as the additional mathematical reduction used for the nonfixed-coordinate formulation. The paper explicitly gives that reduction; no mathematical bound is refuted. |
| m84 | superseded by m53 | `paper-quadratic-aggregation/sections/09-formal-overview.tex:24` | Duplicate of m53’s compact Example ex:closed coverage-table overstatement. Detailed claim maps disclose the boundary; the recommendation is to qualify that compact entry, not to allege an undisclosed omission. |
| m85 | refuted by source review | `results/separable-vertex-binarization.md:7` | “Incorporates every finding” does not say every suggested extension was implemented. The note incorporates the rank-risk and untested-side-variable findings explicitly in its Limitations section (`:270-273`), and the linked experiment record item 9 says the implementation/testing work was not done. Those disclosures are consistent; the audit establishes no hidden limitation or false completion claim. |
| m86 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `results/composite-univariate-envelopes.md:62-63` | The note gives a specific before/after kriging comparison—1,973 versus 231 undecided slivers and 46 s versus 1 s model-build time—without naming the tested expression/domain or linking an output record. The retained univariate experiment record and implementation documents do not identify this comparison, so these four figures cannot be traced to a retained benchmark measurement. Fix: supply the exact case, settings and before/after output, or identify the figures as an unarchived development observation. This is a provenance gap, not evidence that the figures are false. |
| m87 | superseded by m20 | `results/composite-univariate-envelopes.md:67` | See m20 for the overly restrictive unknown-interval description. Sign-indefinite derivative enclosures can persist away from inflections or singular endpoints. Exceeding the interval budget is a separate disclosed rejection path. |
| m88 | refuted by source review | `results/composite-univariate-envelopes.md:127-133` | The example already restricts the exact optimum to even `n`; “exact here” naturally retains that restriction. The linked review labels this “no error” and suggests only repeating the qualifier. The audit’s added formula for odd `n` is false: at `n = 5`, the feasible vector `(1/2,1/2,1/2,-3/4,-3/4)` has objective `-135/128 < -(n-1)/4 = -1`. Withdraw the claimed universal odd-`n` optimum and gap of 1/4. |
| m89 | refuted by source review | `results/monomial-wedge-envelopes-real-exponents.md:452-460` | The 26 exponent cases do use a single geometry, `(p,q,l,u) = (0.4,2.5,0.7,3.1)`, but the note claims exponent-regime coverage and explicitly says these floating-point checks do not prove validity or exactness. It does not claim a geometry sweep. The reviewer separately records 18 parameter sets. Additional retained tests at extreme geometries would strengthen reproducibility but are an optional extension, not a contradiction of the stated verification scope. |
| m90 | superseded by m74; instance count corrected | `notes/separable-vertex-binarization-experiments.md:143` | See m74 for the unsupported “at most 20%” statement. Only one of the five other instances exceeds 20%: `spar080-025-1`, by 27.016% in `bin` and 33.221% in `bin2`, relative to `orig`. These are two modes of one instance, not two instances; the `spar100-025-1` change of about -16% is within the stated interval. Fix the range using unrounded stored times; do not count this duplicate separately. |
| m91 | refuted by source review | `results/cluster-free-branch-and-bound-constrained-minima.md:247` | The displayed formula specializes to `c_2 = tau` without active constraints or equalities, but it also implies the weaker stated bound using `2 tau`, since `tau` is nonnegative. The remark does not claim that `2 tau` is the smallest possible constant. This is a valid conservative estimate, not a mathematical or specification defect; sharpening it is optional. |
| m92 | refuted by source review | `paper-lbesh/sections/abstract.tex:2` | The four saved cut-count reductions are 6.602%, 5.851%, 10.666% and 18.213%; their range rounds to 6–18% at the whole-percent precision used in the abstract. The detailed evidence preserves the unrounded values. This is ordinary reporting precision, not an incorrect numerical claim; adding “about” would be optional editorial clarification. |
| m93 | refuted by source review | `paper-lbesh/sections/abstract.tex:2` | The six displayed schedule ratios imply advantages from about 4.3% to 6.2%, which round to the abstract’s 4–6% at whole-percent precision. The repetitions table exposes the ratios and the discussion also uses “about.” No data discrepancy or changed computational conclusion is established. |
| m94 | confirmed by source review · **fixed 2026-09-25 (§9)** | `paper-certified-minlp/README.md:8-11` | The README ties the “current PDF” rebuild to the September 20 documentation follow-up, but commit `aee2afbf` on 2026-09-24 changes both `main.pdf` and manuscript sources, including Section 6. The sentence therefore describes an earlier PDF revision. Fix: state the current rebuild revision/date and keep the September 20 review and fingerprint scope explicitly historical; changing that sentence must not imply that an additional review was performed. |
| m95 | refuted by source review | `paper-certified-minlp/sections/06-experiments.tex:166-173` | The paragraph reports 18 flagged historical bound/solver pairs and then two returned-point audits, but does not say that both audits were selected from those pairs. The preceding paragraph explicitly states that historical `risk2bpb` was rejected and distinguishes its repaired generation. The alleged cohort contradiction is therefore not established; both original-variable checks remain independently justified. |
| m96 | refuted by source review | `paper-certified-minlp/sections/06-experiments.tex:58-66` | The paper accurately reports 25 negative uniform-reference differences and explicitly calls the references unverified, with every exact comparison retained in the supplement. Recomputing from `tables/uniform-cases.csv` gives maximum magnitude `5.833656876857371e-10` (`syn30m`), consistent with rounding. Stating this bound in the main text would be useful additional detail, but its omission is not a false claim or evidence of unsoundness. |
| m97 | refuted by source review | `paper-certified-minlp/sections/06-experiments.tex:46,72,162` | The unnumbered paragraph labels inherit their enclosing subsection numbers, so the references identify Sections 6.1 and 6.2, which do contain the promised comparison definition and solver audits. These are valid subsection references, not unresolved or wrong destinations. Named paragraph references could be more precise, but that is an optional navigation improvement. |
| m98 | confirmed by source review · **fixed 2026-09-25 (§9)** | `results/positive-multilinear-degree-upper-bound.md:3` | The two review filenames in the header point to reviews of the separate dyadic counterexample, `results/positive-multilinear-gap.md`. Reviews of this logarithmic-degree upper bound do exist: `notes/review-positive-multilinear-upper.md` and `notes/review-positive-multilinear-upper-second.md`, both explicitly naming this result. Fix: replace the two header filenames with these records. The problem is incorrect review pointers, not missing independent review. |
| m99 | superseded by m3 | `README.md:813-814` | Duplicate of m3: the README’s “Equal means always give ratio at most two” omits the unit-cube scope explicitly stated in `results/positive-multilinear-equal-marginals.md:91-93`. Fix the existing m3 wording by adding “on the unit cube”; do not count this as a second issue. |
| m100 | refuted by source review | `paper-relaxation-limits/sections/07-positive-boxes.tex:166-181` | The paper explicitly discards fixed coordinates before applying the `N`-dimensional orientation law, and scopes its Lean claim to the coefficient inequality, original-box transfer and balanced refinement. Lean’s `PositiveBoxAspectBoundOfDim` uses ambient dimension, as its definition and docstring state. Applying that ingredient after the written dimension reduction is sound; the paper does not claim a separate Lean endpoint for the reduction. The results note’s broader coverage wording is the distinct issue m184. |
| m101 | refuted after document review | `paper-relaxation-limits/main.tex:241` | The paragraph explicitly lists the results verified by each linked package and then lists some exclusions; it does not assert that every other paper result is formalized. An exhaustive exclusion inventory would be optional clarification, not an established scope defect. |
| m102 | refuted after document review | `formal/topics/01-switching-control/VERIFICATION.md:26` | The documented checksum command compares a historical snapshot with the current tree: one of 27 entries differs, `paper-switching-control/sections/09-three-mode-floor-chambers.tex`. `formal/VERIFICATION.md:1-5` already explains that historical fingerprints are not current-tree checks. An optional documentation improvement is to link that explanation beside the topic command and identify the snapshot revision; do not regenerate old fingerprints as if the historical verification covered later text. No Lean-source mismatch was found in this manifest. |
| m103 | confirmed after document review · **fixed 2026-09-25 (§9)** | `formal/Formal/GridSwitching/UniformTransfer.lean:28` | Two source comments say grid uniformity is used only once (the overview and the cell-selection comment). In `exists_blockMap_uniform` it is used in both `hcellsum` and `hVnode`; topic 17 COVERAGE.md already describes both uses. Fix both comments to name row normalization and conversion of selected-cell counts to node values. The proof itself is unaffected. |
| m104 | refuted after document review | `results/potential-flow-fixed-support-global-rank.md:24` | The degree-sum argument is correct. In the connected pruned graph with at least two vertices there are no isolated vertices, so splitting the displayed identity gives `sum_(deg>=3)(deg-2)=2r'-2+l`, and each summand is at least one. The claimed count follows immediately. Writing that intermediate line is optional exposition. |
| m105 | corrected after document review · **fixed 2026-09-25 (§9)** | `results/potential-flow-exact-arc-capacity.md:61` | The checker runs 40 trials, alternating 20 subdivided theta blocks (rank two) and 20 subdivided K4 blocks (rank three), so it checks 100 scalar cycle identities across 40 physical states. The note and checker output call these “Forty exact rational cycle identities.” Fix the wording to “40 exact rational physical states, checking every cycle identity” (or “100 cycle identities”). The `3.24e-12` figure is a reported observed recovery error; the `2e-7` assertion threshold is not a conflicting observation. |
| m106 | refuted after document review | `formal/topics/02-fbbt/VERIFICATION.md:38` | Historical manifest comparisons find two differing source-document entries out of 13 in topic 02 and one out of 16 in topic 03: `results/fbbt-doubly-exponential-convergence.md`, `paper-relaxation-limits/sections/appendix-fbbt.tex`, and `results/potential-flow-envelope-rational-certificates.md`. Proof, dependency-pin and saved-certificate entries still match. The project-level snapshot disclaimer already explains this behavior. If clarified locally, link the historical revision and disclaimer beside the commands; retain the original fingerprints. The differences do not establish proof drift or an untraceable reviewed proposition. |
| m107 | refuted after document review | `formal/topics/02-fbbt/COVERAGE.md:6` | The model defines one equation per `CircuitVar n` through `circuitRhs` and `equations`. Counting the equation index type therefore correctly gives the same `4n+4` count as the variables. The short proof using the variable-count theorem is legitimate reuse of a definition-level correspondence, not a false coverage claim. |
| m108 | refuted after document review | `results/potential-flow-envelope-rational-certificates.md:82` | The linked independent review retains the six-case rerun summary: maximum radius `0.000178`, pressure width `0.000477`, endpoint loss `0.0173`, and observed flow error `3.84e-7`, corroborating all four rounded figures. One exact example certificate and the producer source are also retained. Archiving every generated certificate would strengthen reproduction, but the claim that these figures have no retained run record is incorrect. |
| m109 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `results/potential-flow-bounded-block-rank.md:3` | This note and `results/potential-flow-cactus-additive-optimization.md:3` name a root proof review without linking a separate record for that review. The two independent mathematical reviews are linked and substantive. This is only a traceability limitation: no evidence shows the root review did not occur. If a separate record exists, link it; otherwise distinguish the recorded independent reviews from the reported internal root check. |
| m110 | refuted after document review | `results/potential-flow-cactus-additive-optimization.md:162` | The note explicitly states that its 20-instance run retained 32 feasible faces, including only two nondegenerate one-dimensional faces, and calls the checks small numerical evidence rather than a certified global solver. “Searches each one-dimensional face” describes what the routine does to each enumerated face; it does not claim many such faces occurred. Broader numerical coverage is optional. |
| m111 | confirmed after document review · **fixed 2026-09-25 (§9)** | `results/positive-multilinear-incidence-sharp-growth.md:30` | “The exact fixed-k values are not determined” needs qualification: `results/positive-multilinear-treewidth-two-exact.md` establishes `W(2)=2` on the same unit-cube class. Fix the sentence to exempt and link that result; do not imply that the other fixed-parameter suprema have been determined. |
| m112 | refuted as an unresolved-theorem allegation | `results/positive-multilinear-incidence-sparsity-gap.md:21` | The wording explicitly says the sharp value is unresolved “here”, delimiting this note’s weaker orientation argument. The separate `positive-multilinear-treewidth-two-exact.md` proves the value two. Adding a forward link would improve navigation, but the qualified local statement is not a claim that the repository has no solution. Contrast the unqualified statement in m111. |
| m113 | refuted after document review | `results/positive-multilinear-frequency-two-gap.md:163` | The outputs are archived in `paper-relaxation-limits/verification/repository-checks/`: `multilinear_frequency_two_verify.txt` records 94 bipartite cases; `multilinear_convex_cardinality_verify.txt` records 175 curvature checks and 181 bipartite equality samples; `audit-multilinear-feedback-law.txt` is also present. The original absence claim is false. |
| m114 | refuted after document review | `results/binary-factor-width-two-counterexample.md:172` | The note explicitly defines `T/H` as a maximum-payoff ratio, proves the general graph-family ratio in those terms, and separately computes both envelope endpoints for its width-two triangle. It never asserts that the general `k+1` ratio has been established as an envelope-width ratio. An extra reminder would be optional clarification. |
| m115 | refuted after document review | `README.md:827` | The three listed result notes are absent as direct README links, but the README does not promise an exhaustive file index. The frequency-two optimization note is linked from the indexed frequency-two result, and the binary-factor counterexample is linked from the indexed treewidth-two theorem. The claim that a reader following README cannot reach the counterexample is therefore false. |
| m116 | refuted after document review | `formal/topics/06-network-simplex/VERIFICATION.md:28` | Topics 06 and 07 contain dated historical fingerprint commands without a local snapshot explanation. Topic 06 differs in its two manuscript entries; topic 07 differs in five proof/root-import entries after later integration. `formal/VERIFICATION.md:1-5` and `formal/README.md:68-71` explicitly explain that earlier manifests describe original snapshots, including the changed source layout. This is a local discoverability issue only: link that explanation and the historical revision beside each command, rather than replacing old hashes or treating historical PASS results as false. |
| m117 | confirmed after document review · **fixed 2026-09-25 (§9)** | `README.md:977` | The “41 precomputed circuit tests” entry describes the earlier unreduced formulation without its superseded qualifier. The linked note now identifies the residual-eliminated five-test result for two observed labels, with original-domain and zero-row checks. Update the README to that sharper result, or explicitly label 41 as the valid historical unreduced count. |
| m118 | corrected after document review · **fixed 2026-09-25 (§9)** | `formal/topics/21-dag-spectral/VERIFICATION.md:75` | The historical build record reports 66 pages and fingerprints four artifacts; all four current artifacts differ, and the linked build log now reports 67 pages. The historical build evidence remains valid for its recorded snapshot, but the live link caption “66-page manuscript” is stale. Fix the caption and identify the checked revision or link an immutable artifact; do not present old build output as a verification of the replacement PDF. |
| m119 | refuted after document review | `formal/topics/21-dag-spectral/COVERAGE.md:46` | The package proves an explicit work bound in the original input sizes, and COVERAGE.md states that fixed dimension makes this expression polynomial. A separate Lean theorem using an abstract polynomial-growth predicate is not necessary to support that concrete bound. The audit identified no nonpolynomial dependence or missing cost term; absence of such an additional declaration alone is not a formalization defect. |
| m120 | refuted after document review | `notes/research-20260912-dag-psd-approximation-set.md:3` | The saved September 12 checker JSON pins an earlier note (`a5b0cee6…`), while the current note hashes to `1fb9ecdb…`. The later changes add Lean implementation details and Section 9, with separate topic-21 review links; they do not show that the underlying theorem lost its independent review. The linked topic-21 source inventory already calls the first review historical and distinguishes its scope from the later formalization reviews; a local date label would be optional clarification. Do not characterize all current text as unreviewed from a hash difference alone. |
| m121 | superseded by m10 after document review | `results/potential-flow-joint-resistance.md:128` | See m10. The checker uses a perturbed objective and internally sourced adjoint. The evidence paragraph leaves the objective unspecified; it does not explicitly claim an ordinary-unit-adjoint check. |
| m122 | confirmed after document review · **fixed 2026-09-25 (§9)** | `results/ac-power-flow-existential-reals.md:4` | “All requested corrections applied” overstates audit B. Its Part II findings 4–5 request replacement of the “promised” range wording, an explanation of unused/isolated variable buses, and source verification or softening of the Lavaei–Low criticism. The result still contains the old wording and unqualified criticism. Apply the remaining editorial changes or qualify the status. This finding concerns the recorded review requests, not an independent judgment that the cited published proof is wrong. |
| m123 | confirmed after document review · **fixed 2026-09-25 (§9)** | `results/ac-power-flow-existential-reals.md:210` | For `x=y`, the inversion gadget requires three distinct complement path buses: one at `C_I` and two at `D` (conductances one and two). The earlier construction says three correctly, but the converse paragraph says “the two”. Replace that count with three and identify their incidence. This is a prose contradiction, not a defect in the correctly stated construction. |
| m124 | refuted after document review | `results/extended-rpd-supporting-flow.md:153` | Proposition 4 explicitly introduces its own invariant matrices in `Az+Bp=b`; Theorems 2–3 explicitly define their time-dependent support matrices. Reusing locally defined letters in a separate proposition does not create a false statement or ambiguous assumption. Renaming them would be an optional style change. |
| m125 | corrected after document review · **fixed 2026-09-25 (§9)** | `formal/topics/20-scalar-quadratic/VERIFICATION.md:52` | The three paper entries in `verification/paper-sources.json` differ from the current manuscript/PDF, while its three result-note entries still match. The dated 2026-09-20 evidence is a historical record, but the wording “The current paper PDF” points to a later replacement. Label the paper checks as applying to the recorded revision and link that snapshot, or separately record a later paper review. These paper-artifact differences do not invalidate the frozen Lean verification. |
| m126 | confirmed by source review · **fixed 2026-09-25 (§9)** | `formal/topics/20-scalar-quadratic/README.md:28` | The README says topics 21–26 remain queued, but `formal/topics/README.md:30–40` lists topics 21 and 22 as complete and independently reviewed, with only topics 23–26 queued. Fix: update the topic-20 status sentence to match the index. |
| m127 | confirmed with corrected scope · **fixed 2026-09-25 (§9)** | `results/quadratic-inertia-one-sided-integer-complexity.md:279–285` | The numerical-verification paragraph does not distinguish the LP in `code/quadratic_rank/check_one_sided.py` from the folding construction used in the proof. The script uses every level-0-through-L epigraph inequality and the endpoint tangents `t >= 0`, `t >= 2x-1`; the proof uses a single final-level epigraph inequality with L+1 folds. The note already explains in its Lean section that the single-level L-fold system has error `4^(-L)/4` and L+1 folds give the stronger displayed error. This is a construction-identification gap, not an inconsistency in the theorem or a newly reproduced numerical failure. Fix: identify the script as testing the strengthened multi-level LP, or add a separate check of the actual proof construction. |
| m128 | refuted | `formal/topics/22-represented-matroid-spectral/REVIEW.md:58–61` | The review says the targeted build passed; it does not say the reviewer ran it. The immediately linked `REVIEW-FINAL-SOURCES.json:84–88` explicitly attributes the initial build to the implementation authors and also cites the final topic runner. No false independent-execution claim is established. |
| m129 | refuted | `formal/topics/22-represented-matroid-spectral/VERIFICATION.md:35–42` | The three one-element execution examples have deliberately limited coverage, which the record describes accurately and separates from the universal proofs. Additional nontrivial matroid cases would be useful optional regression tests, but the existing text makes no claim of comprehensive branch coverage. |
| m130 | confirmed by source review · **fixed 2026-09-25 (§9)** | `paper-certified-minlp/formal/VERIFICATION.md:13` | The record counts 18 kernel-evaluated acceptance/rejection examples, but `CertifiedMinlp/DiscreteExamples.lean` has 17 `decide +kernel` proofs. Its eighteenth theorem, `integer_half_bound`, applies the general soundness theorem. Fix: report 17 evaluated checker examples and one soundness-application example. |
| m131 | confirmed with corrected scope · **fixed 2026-09-25 (§9)** | `paper-certified-minlp/formal/VERIFICATION.md:14,40–41` | The three rational PSD boundary examples in `CertifiedMinlp/QuadraticElimination.lean:215–224` use `norm_num`, so the blanket statement that the examples use `decide` is inaccurate. Their proofs are still kernel-checked; anonymous `example` declarations are valid proofs and do not require separately named coverage entries. Fix: distinguish the `decide +kernel` structured-checker examples from the `norm_num` PSD examples and describe both as kernel-checked. |
| m132 | refuted | `formal/topics/04-cubic-gaps/VERIFICATION.md:34–35` | Four historical fingerprint entries differ from the current tree, but every entry matches its source at commit `03bfee77e8491158f9d060faf6825098d6d4cacb`, which introduced the manifest. `formal/README.md:68–71` explicitly says earlier manifests identify their original verification snapshots. The exact historical sources are preserved; current hash drift does not invalidate the dated replay record. |
| m133 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `formal/topics/04-cubic-gaps/VERIFICATION.md:12` | The September 11 table asserts an independent specification review, but the topic has no separate review report and the retained run log does not document that review. This leaves the particular historical review without an inspectable narrative or reviewer attribution. Later `formal/topics/11-cubic-completion/REVIEW.md` does independently review existing `CubicGap` statements, so it is incorrect to imply cubic statements have never received a documented review. Fix: link any retained September 11 review evidence, or state that its detailed report was not retained and distinguish the later review. |
| m134 | confirmed; attribution only · **fixed 2026-09-25 (§9)** | `README.md:798-804` | The README says the analytic family proves the two-sided sandwich `483/223 <= R(3) <= 31/12`. That family supplies the lower bound; the separately linked rounding-mixture theorem supplies the upper bound. Attribute the two sides separately. The same bullet already displays the improved lower bound `1610000/743033`; promoting that value into the sandwich is optional, not a missing-result defect (see m158). |
| m135 | refuted | `paper-cubic-gap/main.tex:232–240` | Collecting repeated supports after expansion is a routine exact polynomial operation: the width of a fixed monomial scales linearly with its nonnegative coefficient. The proof applies the common-law inequalities to the expanded sum, so duplicate supports do not create a mathematical gap. An explicit sentence about collecting like terms would be optional exposition. |
| m136 | refuted | `results/positive-multilinear-marginal-floor-gap.md:221–225` | The two cited reviews collectively cover the listed topics, including the two-sided strip in the first review. The sentence does not explicitly assert that each review independently checked every listed item. The audit’s distributive reading does not establish an unsupported verification claim. |
| m137 | confirmed with corrected scope · **fixed 2026-09-25 (§9)** | `results/positive-multilinear-positive-box-lower.md:5–14`; `results/positive-multilinear-positive-box-sharp.md:15–19` | The two notes use `C_box(rho)` for differently defined suprema: the lower note uses common boxes `[1,rho]^n`, while the upper note allows unequal positive boxes with coordinate aspect ratios at most rho. The combined bounds remain valid: the lower construction is in the broader class and the upper theorem covers the narrower class. Fix: use one common definition in both notes or state the class inclusion when combining them. |
| m138 | confirmed by source review · **fixed 2026-09-25 (§9)** | `notes/review-positive-box-sharp-aspect-upper.md:5–8`; `notes/review-positive-box-sharp-second.md:5–8` | Both historical reviews link to the canonical result now proving `rho+2`, but they audit the superseded asymmetric estimate for `rho >= 64`, preserved in `notes/positive-box-asymmetric-upper-predecessor.md`. The current canonical result already links its two fresh reviews. Fix: point these older reviews to the predecessor and identify their historical scope; no new review of the current theorem is missing. |
| m139 | refuted | `paper-integer-dimension/sections/02-quadratic-finite.tex:227–237` | The volume bound `omega_n 8^(n/2)` is valid but loose for diameter `sqrt(8)`; the sharper bound is `omega_n 2^(n/2)`. The displayed `log2(16 pi e)` conclusion follows from the looser bound and still proves the asserted asymptotic separation. Sharpening the constant is optional, not a correction. |
| m140 | refuted | `paper-integer-dimension/sections/02-quadratic-finite.tex:43–44,91–93` | The claimed `O(n p_grid + n^2 + m n^2)` count is a valid upper bound, although output rows and variables can be counted more sharply as O(m), with O(m n^2) output coefficients. The theorem does not claim this size bound is tight. Distinguishing coefficient count would be optional exposition. |
| m141 | refuted | `paper-network-simplex/sections/08-computation.tex:298–303` | The paragraph reports circuit-library construction and explicitly adds inverse-basis time only for the reduced library; it does not present these as equal-component totals or derive a speedup ratio. The saved benchmark also records 1.879 ms for the unreduced inverse bases. Giving both totals (32.93 ms and 19.93 ms) would improve comparability, but the reported component timings are accurate. |
| m142 | superseded | `papers/pooling/source-index.md:3–5` | Duplicate of m146. The defect is the present-tense “retained unchanged” statement, not the explicitly historical September 9 hashes. |
| m143 | confirmed by source review · **fixed 2026-09-25 (§9)** | `papers/pooling/sections/00-introduction.tex:118–122` | The trailing “also when” grammatically extends both strong NP-completeness and absence of a PTAS to the positive-tolerance family, but Proposition `s3:tolerance` in `03-restricted-hardness.tex:338–343` states only strong NP-hardness of exact optimization and absence of a PTAS. Fix: state the positive-tolerance conclusions separately and do not transfer NP membership without a separate argument. |
| m144 | confirmed by source review · **fixed 2026-09-25 (§9)** | `paper-structured-bilevel/README.md:21` | The README says the final paper has 54 references. Current `references.bib` contains 55 entries, and the saved build has 55 `bibitem` entries in `build/main.bbl` and 55 `bibcite` entries in `build/main.aux`. Fix: update the count to 55 or omit the fragile total. |
| m145 | confirmed by source review · **fixed 2026-09-25 (§9)** | `paper-power-flow/appendices/verification.tex:43–46`; `paper-power-flow/process/coverage.md:91` | The subdivision fixture is described as a weighted triangle, but `checks/check_developments_exact.py:228–237` uses a triangle plus pendant edge `(2,3)` on four buses. Fix: describe the fixture as a weighted triangle with a pendant bus; this corrects only the test description. |
| m146 | confirmed with corrected scope · **fixed 2026-09-25 (§9)** | `papers/pooling/source-index.md:3–5` | The statement that companion sources are “retained unchanged” is stale: `results/common-factor-reciprocal-anchor-hulls.md` and `results/common-factor-reciprocal-anchor-full-hull.md` now hash to `8df878b9...` and `2a97bb3f...`, respectively, after commit `367fcbc8` on September 20. The index explicitly says its hashes identify the September 9 author-pass bytes, so those historical hashes should not simply be replaced. Both notes concern removed comparisons, not retained proof dependencies. Fix: qualify the unchanged-source sentence and preserve the historical hashes with their review date, optionally linking the reviewed revision. |
| m147 | refuted | `paper-correlated-measurements/sections/02-locality.tex:354–357,392` | The current proof says a fresh local history has at most `floor(L/g)` observations. Selected times, including the target time, are required to be g-separated, so the preceding observations lie at distances at least g, 2g, and so on, up to L. This is correct. The audit’s raw-window counterexample omits the target spacing requirement and does not contradict the paper. |
| m148 | refuted | `paper-integer-dimension/sections/04-vector.tex:1006–1014` | The interval `[(1-a)/2,(1+a)/2]` correctly describes the average of the two outer-segment inputs, one in `[0,a]` and one in `[1-a,1]`, which have equal weights t. Mixing that average with the middle-segment input also remains in `[a,1-a]`. The audit confused the average of the outer inputs with the full weighted section input. |
| m149 | superseded | `paper-potential-flow/README.md:7`; `paper-potential-flow/process/completion-s7-adjudication.md:21,29` | Post-review manuscript edits are covered by M27 and should not be counted again here. The README already distinguishes the current PDF from historical completion PDF/archive and discloses a September 20 follow-up, while the S7 adjudication describes its accepted stage. Commit `aee2afbf` subsequently changed the manuscript on September 24. Any retained finding should concern traceability of review coverage for that later text, not treat dated S7 assertions as false at their original stage. |
| m150 | refuted | `paper-potential-flow/verification/build-report.json`; `paper-potential-flow/reproducibility/README.md:15` | This is the legacy two-paper build report, not the documented current Paper A build record. The reproduction README explicitly directs readers to the A-only wrapper and `complexity/build/build-check.json`, and says not to use the legacy two-paper CLI. The complexity hashes are historical and one source was deleted, but all 13 uncertainty hashes still match. Historical drift does not establish a false current build claim. |
| m151 | confirmed after source review · **fixed 2026-09-25 (§9)** | `paper-potential-flow/complexity/narrative/06-certificates.tex:24-37` | One theorem uses `u_e` both for nonnegative conjugate-root bounds and for possibly negative upper interval endpoints. This makes the negative-interval branch confusing; the appendix explicitly distinguishes the meanings but the main theorem does not. Fix: use different symbols for the root bounds and interval endpoints. |
| m152 | refuted after source review | `paper-structured-bilevel/appendices/b-inverse-approximation.tex:209-245` | The proof already states `0 <= g'(z) <= P` on the response interval. The mean value theorem directly converts a response bracket of width `tau/(64P^2)` to target error at most `tau/(64P)`. No missing argument or erroneous constant was found. |
| m153 | refuted after source review | `paper-switching-control/README.md:9-12,53-58` | The README explicitly calls the staged review records and Lean checks historical, and does not contain the alleged fingerprint command. Later manuscript drift does not contradict that disclosed scope. Any missing local caveat in topic fingerprint instructions belongs to m189. |
| m154 | refuted after source review | `results/pooling-quality-scaled-path-flow.md:235-242` | Using Hoffman cuts in the equivalent form `ell(delta+(S)) <= u(delta-(S))`, root-excluding cuts give the second inequality of (9); cuts containing the root give the first on the complementary original vertex set. This is exactly the stated order. The audit implicitly chose the reverse cut convention. |
| m155 | refuted after source review | `results/fixed-core-block-polyhedral-optimization.md:280-286` | Adler–Beling Section 5, Remark 1 expressly states polynomial running time in dimension, common-extension degree and input bit size for the rational-number model, and outlines the algorithm. The note cites precisely that remark. Its full details are deferred, but this alone does not establish an incorrect citation or complexity claim. |
| m156 | superseded after source review | `results/pooling-contracted-common-capacity-algorithm.md:86-90` | The claimed absence of checker outputs is refuted: the pooling paper archives the named author and support-checker outputs. The narrower reviewer-script reproducibility question is consolidated in corrected m173. |
| m157 | superseded after source review | `results/fixed-parameter-linear-fibers-np-membership.md:134-135` | Duplicate of m172, which records both the repeated “therefore” and the incorrect attribution of NP-completeness to a construction. |
| m158 | refuted after source review | `README.md:798-805` | The README explicitly gives both the weaker cubic lower bound `483/223` and its certified improvement `1610000/743033`. Both are true and the stronger value is visible in the same sentence. Promoting the stronger value into the displayed sandwich is an editorial preference, not an incorrect theorem or missing result. |
| m159 | superseded by m3 | `README.md:812-814` | Duplicate of the README’s omitted unit-cube qualification; see m3. |
| m160 | refuted after source review | `README.md:1009-1016` | The layout list is selective and does not promise to enumerate every directory. Adding the research directory or paper directories would improve navigation, but their omission establishes no claim, evidence, or validity defect. |
| m161 | refuted after source review | `results/quadratic-system-noncommutative-rank-complexity.md:3-4,405-412` | The note accurately says it was independently reviewed and links one review. The second review exists at `notes/review-quadratic-noncommutative-rank-second.md` and supports the README’s two-audit statement. Omitting that additional link does not make either status statement false. |
| m162 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `results/spatial-bb-relative-gap-exponential-lower-bound.md:224-230`; `notes/review-spatial-bb-relative-gap.md:81-96` | The result accurately attributes 2,660 exact identities per configuration to the independent review, but that review supplies no archived checker or raw output for its separate run. This limits independent reproduction of the reviewer-specific count; it is not evidence that the run failed or that the proof is unsupported. Fix: distinguish reviewer-reported supplementary checks from archived reproducible runs, or link the reviewer artifact if retained. Remove the unverified blanket total of 15 affected reviews. |
| m163 | superseded after source review | `formal/topics/00-exact-counts/VERIFICATION.md:34-39` | Consolidated in m189: historical fingerprints are disclosed at project level, but this topic’s local checksum instructions omit that caveat. Read-only digest comparison found only the cited manuscript section and result note differ in topic 00; no Lean verification was run. Fix the local scope wording, not the historical hashes. |
| m164 | refuted after source review | `notes/network-simplex-paper-readiness.md:3-17,163-166` | The note prominently labels itself “Historical closeout, superseded by the manuscript”, dates the closeout 2026-09-07, and says the original evidence is preserved rather than describing current manuscript claims. Its linked timestamped manifest therefore pins a historical checked source. Subsequent hash differences do not establish stale current-source certification. |
| m165 | superseded by m44 | `code/spatial_bb_lower_bound/check_sdp_rlt_strengthening.py:62-63,81` | See m44 for the printed exact-check label despite a floating-point PSD eigenvalue check. The module docstring and result note correctly disclose that distinction. |
| m166 | refuted after source review | `README.md` | The README is a selective overview and does not claim to index every results file. Unlinked result notes retain their own status and verification sections. A complete index would be a navigation enhancement, not evidence that those results lack verification or that the README makes a false claim. |
| m167 | corrected after source review · **fixed 2026-09-25 (§9)** | `notes/lbesh-publication-readiness.md:33-35`; `code/minlp_solver_lab/LBESH_RESEARCH.md:114-115` | The wording “42 continuous roots and 27 assignments for each of 14 small instances” has ambiguous modifier scope. Saved root records contain 14 small, 14 medium and 14 large instances; only the assignment enumeration is restricted to the 14 small instances. The total 420 calls is correct. Fix: explicitly state 42 roots across all three sizes, plus 27 assignments for each of the 14 small instances. |
| m168 | confirmed after source review · **fixed 2026-09-25 (§9)** | `notes/lbesh-study-results.md:584-585` | `analysis_repeats_v1` is called a “repetition-only export”, but its saved `analysis.json` command includes the primary batch, and its 927 records comprise 663 primary plus 132 in each of two repetitions. Fix: call it the primary-plus-repetitions export, without the later conic batch. |
| m169 | confirmed after source review · **fixed 2026-09-25 (§9)** | `notes/lbesh-development-theory.md:3` | The status still says “independent review pending”, while `notes/lbesh-review-theory.md` records completed review and a final revision check whose SHA-256 matches the current theory note (`7f1a0d0e…`). Fix: mark the qualified theoretical claims independently reviewed and link that record. |
| m170 | confirmed after source review · **fixed 2026-09-25 (§9)** | `formal/COVERAGE.md:54-58` | The coverage text says the weighted-box formulation uses fewer continuous variables than the note. The current result note already uses the same three weights per coordinate, giving `3n` auxiliaries and `13n` inequalities. Fix: say that Lean verifies the same formulation and counts. |
| m171 | refuted after source review | `formal/COVERAGE.md:9`; `formal/Formal/Scalar.lean:14` | The table links `constants` directly to `Scalar.lean`, so the private declaration is unambiguous and inspectable. A separate private helper in `StrictError.lean` does not create ambiguity in that file-specific mapping. Coverage does not promise every helper is an exported name usable with an external `#check`. |
| m172 | confirmed after source review · **fixed 2026-09-25 (§9)** | `results/fixed-parameter-linear-fibers-np-membership.md:134-135` | The sentence says “construction therefore is therefore NP-complete”. Fix: “The two-pool/two-output pooling decision problem is therefore NP-complete”, citing the hardness note and the output-fraction NP-membership argument (`r=pJ=4`). This also resolves m157. |
| m173 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `results/pooling-two-source-qualities-convex-feasibility.md:338-375` | The missing-log claim is false for all seven named committed checkers: `papers/pooling/verification/logs/` contains `stage05-two-quality-physical.txt`, `stage05-path-clamps.txt`, `stage05-divergence-support.txt`, `stage05-rational-support.txt`, `boundary-projection-exact.txt`, `bypass-structure-mapping.txt`, and `fixed-core-support.txt`. The remaining reproducibility limitation is the separately reported 240-network reviewer check, documented in `notes/review-pooling-two-source-qualities-source-intervals-independent.md:153-164` without a linked standalone checker. Fix: link any retained reviewer script or identify these as reviewer-reported checks; do not call the seven archived runs unsupported. |
| m174 | confirmed after source review · **fixed 2026-09-25 (§9)** | `results/pooling-one-quality-degree-two-hardness.md:15-17` | The summary says all numerical data belong to `{-2,-1,0,1,2}`, but the decision threshold is `K=-sum_e w_e` and grows with the instance. The theorem statements correctly restrict the finite-set claim to costs, capacities and quality data. Fix the summary to say “all numerical data except the objective threshold”. |
| m175 | confirmed after source review · **fixed 2026-09-25 (§9)** | `results/pooling-existential-theory-of-reals.md:161-163` | The consequence of Lemma 4 says profit at least `zeta` is equivalent to feasibility plus saturation. The lemma assumes capacity and conservation only; profit does not impose blending-quality feasibility. Fix: “Among feasible pooling flows, profit is at least `zeta` exactly when every forced node is saturated”, or state the capacity/conservation equivalence and impose quality feasibility separately. |
| m176 | refuted after source review | `results/pooling-existential-theory-of-reals.md`, Section 6 item 3 | The remark explicitly allows ε violations of every polynomial constraint and distinguishes approximate from exact rational feasibility. Rounding bounded flow/quality variables gives the asserted polynomial encoding bound for these quadratic rational models; an explicit Lipschitz calculation would be an optional exposition improvement. |
| m177 | corrected after source review · **fixed 2026-09-25 (§9, §10)** | `code/pooling_existential_reals/one_pool_build_and_check.py:109-170`; `results/pooling-one-pool-bypass-existential-reals.md`, Section 5 | The numerical sanity checker classifies every run without an incumbent at the threshold as a negative case, even if the solver stops at its 120-second limit without a separating upper bound. `run_case` can therefore pass an expected no-instance on an inconclusive run. It prints `ObjBound` but never uses it or the termination status. Fix: distinguish threshold witness, numerical upper bound strictly below the threshold, and inconclusive; retain the status/bounds with reported runs. An OPTIMAL status is sufficient for a numerical optimum claim but is not necessary if a valid separating upper bound is available. The note already says these floating-point checks are not part of the proof. |
| m178 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9)** | `results/cia-exact-three-switch-worst-case.md:3`; `notes/review-cia-exact-three-switch-transfer.md` | The status line adds a “full proof review by root” without identifying a retained record for that additional review. The linked transfer review and the separate reach/heavy-mode reviews do provide documented review evidence. Fix: identify the extra review record, or qualify/remove only the unlinked root-review claim. The absence of a separate artifact does not establish that the review never occurred, and the status line does not call it an additional independent review. |
| m179 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `results/cia-arbitrary-block-one-sided-bound.md`, Verification; `notes/review-cia-arbitrary-block-one-sided.md:119` | The 360-input, 928-recursive-contract and 241-full-error counts are recorded in the independent reviewer’s narrative, but its implementation and raw output are not linked or retained with the author’s checker. Thus these supplementary checks cannot be independently reproduced from the supplied reviewer artifacts. Fix: label them as reviewer-reported checks whose implementation/output were not archived, or link the artifacts if available. This is a reproducibility limitation of supplementary tests, not evidence against the analytic proof or evidence that the review did not occur. |
| m180 | refuted after source review | `results/cia-general-four-block-reach.md`, Symmetry reduction; `notes/review-cia-general-four-block.md`, Why the symbolic program is exact | The all-dimension link is proved by stable orbit topology and known affine multiplicities, with an independent source review explaining row-order stability. The checker reconstructs those known coefficients at n=9,10 and checks polynomial identities. Additional direct comparisons at larger n would be useful regression tests, but finite comparisons cannot prove the universal claim and are not required to replace the existing structural proof. |
| m181 | corrected after source review · **fixed 2026-09-25 (§9)** | `results/cia-general-four-block-reach.md`, table of ten symmetry types | The sentence “The last case exists only for n>=6” can ambiguously refer to the entire final table row. Only the final pair/index type P={3,4}, z=5 needs six indices; the z=0 and z=3 types exist at n=5. Fix: name that final pair/index type explicitly. The checker’s `z < n` filtering and the review’s 179-case count already use the correct enumeration. |
| m182 | refuted after source review | `results/cia-three-switch-heavy-mode.md`, Case 3 | The proven strict bound τ<3 implies the displayed 2≤τ≤3, which is true and sufficient for the schedule argument. Replacing ≤3 by <3 would sharpen wording but corrects no mathematical or verification defect. |
| m183 | refuted after source review | `results/cia-arbitrary-block-one-sided-bound.md`, Theorem | The indefinite phrase “a schedule using at most k distinct activation blocks satisfies” is naturally existential, consistently with the immediately following construction and proof. It does not universally quantify over schedules. “There exists a schedule” would remove any editorial ambiguity, but the audit should not claim the theorem is literally a false universal statement. |
| m273 | superseded after source review | `results/pooling-existential-theory-of-reals.md:161` | Duplicate of m175. Lemma 4 correctly characterizes saturation under capacity and conservation; its following sentence incorrectly adds full pooling feasibility to that equivalence. Quality feasibility must remain a separate assumption. See m175 for the finding and remedy. |
| m274 | refuted after source review | `results/pooling-one-quality-degree-two-hardness.md:341` | The source note says the full text "was not available" and explicitly identifies the secondary sources used for its theorem numbering. The current local Haugland full text does contain Proposition 3 at line 159, but present availability does not refute that historical account. Direct-source checking could now strengthen the citation; no false theorem attribution or necessary correction is established. |
| m275 | superseded after source review | `code/pooling_existential_reals/one_pool_build_and_check.py:170` | Duplicate of m177. The checker classifies a case from the incumbent alone and ignores the returned objective bound, so failure to reach the threshold can pass as the expected negative result without establishing exclusion. Use a suitable solver upper bound to establish a negative verdict, and report unresolved cases separately; do not infer that any historical run actually timed out. See m177 for the finding and remedy. |
| m276 | refuted after source review | `results/pooling-all-degrees-two.md:168` | The merged-lax corollary explicitly proves that its new output capacity is identical to the already shared dirty-input capacity, so the feasible pure throughputs and integral replacement are unchanged. Parallel mode edges can also be treated as labeled edges in a bipartite multigraph, whose matching polytope is integral. No missing condition or proof repair is required. |
| m277 | refuted after source review | `results/cia-sharp-grid-transfer.md:13` | The linked full derivation, `notes/cia-reopened-grid-transfer.md:55`, proves attainment using finitely many mode words and compact ordered switch-time simplices, with an objective continuous in switch times. The linked independent review repeats the argument at `notes/review-cia-reopened-grid-transfer.md:57-63`. Applying strict transfer to an attained optimum establishes the displayed strict inequality. No missing hypothesis remains. |
| m278 | superseded after source review | `results/cia-exact-three-switch-worst-case.md:3` | Duplicate of m178. The additional root-review claim has no corresponding located review artifact; this concerns retained provenance, not proof invalidity or proof that the review never occurred. See m178 for the finding and remedy. |
| m279 | superseded after source review | `results/cia-arbitrary-block-one-sided-bound.md:125` | Duplicate of m179. The independent 360/928/241 test counts are recorded in `notes/review-cia-arbitrary-block-one-sided.md:119`, but their separate implementation and raw output were not located. Describe this as unarchived computational evidence, rather than asserting the implementation never existed or the recorded checks did not occur. See m179 for the finding and remedy. |
| m280 | refuted after source review | `results/cia-arbitrary-block-one-sided-bound.md:13` | The theorem says "a schedule ... satisfies", which has the ordinary existential reading supported by its constructive proof. It does not say every schedule satisfies the bound. The proposed bad-schedule example therefore does not contradict the stated result. Adding "there exists" would be optional clarification, not correction of a false theorem; this also resolves duplicate m183. |
| m281 | refuted after source review | `results/cia-three-switch-heavy-mode.md:35` | For a mode served on `[1,5]`, the omitted term satisfies `m_q-4<=A_q(1)` because `A_q(5)-A_q(1)<=4`. Thus `max{A_q(1),m_q-4}=A_q(1)`, exactly the bound printed in Case 1. The independent review gives the same elementary justification. The sentence is correct; adding that justification is optional. |
| m282 | refuted after source review | `results/cia-general-four-block-reach.md:144` | The result explicitly proves fixed orbit topology and affine multiplicities for all `n>=9`, then reconstructs those known affine coefficients at 9 and 10. `notes/review-cia-general-four-block.md:35-43` independently checks that structural argument and reports further finite comparisons. The exact polynomial certificate checks rely on this analytic reduction, as the note explains; absence of a machine proof of the reduction is not a validity or evidence defect. |
| m283 | refuted after source review | `results/bilevel-convex-aggregate-accuracy-bit-algorithm.md:19` | Both `R` (line 19) and `A` (line 54) are explicitly defined by the same expression and are used consistently for the box radius and aggregate error bound. Their equality causes no ambiguity about their values or invalid inference. Combining the names is an optional notation simplification, outside a validity defect. |
| m284 | refuted as missing computational evidence | `README.md:479` | The separate exact-arithmetic audit is the retained analytic review `notes/review-bilevel-fixed-aggregate-response-degree-complexity.md`, which checks growing degree, bit length and exact-output recovery. Neither the README nor that review claims a numerical experiment. “Degree, bit-complexity, and exact-output audit” would be more specific, but no nonexistent computation or missing review is established. |
| m285 | refuted after source review | `results/bilevel-fixed-block-response-algorithm.md:17` | The fixed maximum block dimension is the scalar `d`; the leader-dependent right-hand side is the explicitly defined vector-valued function `d(x)`. Their roles are distinguished by their definitions and arguments throughout the proof. Renaming the right-hand side could improve notation, but no ambiguous mathematical claim or incorrect bound is demonstrated. |
| m286 | refuted after source review | `results/bilevel-response-constraint-accuracy-bit-algorithm.md:56` | The paragraph explicitly refers to "Sections 3–6 of the existing theorem", "its tau", "its inverse tolerance", and "the original proof". Equations (8) and (9) are therefore inherited references to the linked fixed-resource theorem, whose numbering this extension continues with (15)–(18). Qualifying every equation reference would be optional navigation help, not a wrong cross-reference. |
| m287 | refuted as an undefined-function gap | `results/bilevel-response-constraint-accuracy-bit-algorithm.md:202` | The same sentence as `min(1,g_i^(-1)(ell_i(x)))` explicitly extends the inverse by the constant one above its endpoint, supplying the intended domain and valid concavity argument. Using the previously defined clipped inverse, or writing `g_i^(-1)(min{ell_i(x),G_i})` for nonnegative `ell_i`, would make the formula self-contained. The existing explicit extension prevents the alleged gap in the subclass conclusion. |
| m288 | superseded after source review | `results/quadratic-nonlinear-input-rank-precision.md:177` | Duplicate of m207. Equation (6) uses the full-output map `q` with the later effective-output ellipsoid `E_0`; its subsequent application explicitly uses `q_bar`. State the covariance inequality for `q_bar` after defining the effective output space, or make its temporary generic ellipsoid notation distinct. See m207 for the finding and remedy. |
| m185 | corrected after source review · **fixed 2026-09-25 (§9)** | `research-20260922/curve-hulls/report.md`, Excluded as numerically unreliable and Section 5; `code/modelcheck.out:73-75` | The report says the gams02 substituted model rejects MINLPLib’s best point, but the saved `modelcheck.out` reports status 2 and objective 89466860.66118145 for orig, sub and sub+cuts. `modelcheck_rescaled.out` supplies no contrary gams02 result. Fix: remove gams02 from this particular fixed-point infeasibility claim, or identify a different run and its model/version. Its exclusion remains supported by inconsistent optimization output; cut validation at the known point does not by itself identify whether the fault lies in solver numerics, modeling or a version mismatch. |
| m186 | confirmed after source review · **fixed 2026-09-25 (§9)** | `results/potential-flow-cactus-square-root-sum.md:7,93-124` | The opening theorem sentence claims Square-Root Sum equivalence for unrestricted single-source single-sink passive quadratic networks, although its upper reduction is proved only for connected cacti. The title and concluding statement have the correct cactus scope. Fix: insert “on cactus graphs” in the first theorem sentence; retain the additional lower-bound restrictions on simple degree-three triangular cacti. |
| m187 | refuted after source review | `README.md:44-49,338`; `results/row-hull-separable-concave.md:17-24` | The README accurately summarizes the earlier pricing bug and the rerun of its affected experiments. The separate later endpoint-rounding repair and its verification scope are disclosed in the linked results note. No benchmark invalidity or false rerun claim follows from the README omitting that separate fix; adding it would be an optional summary update. |
| m188 | refuted after source review | Five pooling hardness results notes; `papers/pooling/sections/03-restricted-hardness.tex`, corrected Matsui gap and scope remark | The notes rely on the valid large-parameter positive-product hardness theorem. The paper already repairs the intermediate general-p estimate and gives the counterexample to its broader printed form. A cross-reference from the notes would be useful, but no cited hardness statement or reduction is shown false and no requirement makes that additional cross-reference a validity defect. |
| m189 | refuted after source review | `formal/topics/00-exact-counts/README.md`; `formal/topics/08-exact-multilinear/VERIFICATION.md`; `formal/README.md:68-71` | These manifests identify historical verification snapshots, as the project README and verification record explicitly explain; topic 08 dates its checks to 2026-09-12, and topic 00 calls the hashes “recorded fingerprints.” A later mismatch detects source change and does not invalidate the original check. A local reminder could improve discoverability, but no current pass is asserted by these historical records. |
| m190 | confirmed after source review · **fixed 2026-09-25 (§9)** | `.github/workflows/lean.yml`; `paper-certified-minlp/formal/README.md:12-15`; `paper-certified-minlp/formal/VERIFICATION.md:19` | The standalone certified-MINLP documentation says project-wide verification is handled by CI, but the committed workflow selects and builds only `formal/`, not `paper-certified-minlp/formal/`. Fix the documentation to say standalone project-wide verification is assigned but not configured in the committed workflow, or separately arrange that coverage. This concerns configuration only: no CI result was inspected, and the documentation explicitly makes no current full-project replay claim. |
| m191 | refuted after source review | `formal/README.md`; `formal/VERIFICATION.md` | The absence of a committed whole-project replay for the latest tree is explicitly disclosed: local work uses targeted checks, project-wide verification belongs to CI, and historical logs describe earlier stages. No current whole-tree pass is claimed. Uninspected CI evidence cannot establish either success or failure. |
| m192 | corrected after source review · **fixed 2026-09-25 (§9)** | `formal/topics/14-certified-minlp/VERIFICATION.md:13-15`; `verification/delivery.json`; `paper-certified-minlp/certified-minlp-paper-source.tar.gz` | The linked delivery record pins an archive of 549496 bytes with digest 58ac0855…, while the currently linked archive is 549487 bytes with digest b17513c6…; 14 of its 86 archived files differ from their current source counterparts. Thus the page’s unqualified statement that this record confirms the archive matches current sources is stale. Fix: identify the check as historical and name the snapshot it verifies, or refresh the archive and delivery record together after a new package comparison. Do not rewrite historical check results as if they were rerun. |
| m193 | refuted after source review | `formal/topics/{29-infinite-aggregation,30-infinite-aggregation-hull,31-aggregation-accuracy}/verification/paper-sources.json` | Each source/PDF manifest belongs to a dated completed supplement build. The shared macros and each supplement section have since changed, while the recorded PDFs still match their hashes. This establishes later source drift, not a false historical build result. Topic 30’s “current files” sentence describes its final inputs on the record’s 2026-09-22 date; an “at that time” clarification is optional. No fresh build or review is implied by subsequent edits. |
| m194 | refuted after source review | `formal/topics/18-positive-box/README.md`; `VERIFICATION.md:58-59`; `Formal/MultilinearGap/BilinearGraph.lean` | The verification record explicitly says the retained axiom sweep and separate kernel replay precede the odd-dimensional additions. A later warning-free Lean build still checks those proof terms during elaboration; the README’s general verified/completed status does not promise that every earlier auxiliary audit was repeated. No unsupported theorem or incorrect proof is identified. |
| m195 | confirmed after source review · **fixed 2026-09-25 (§9)** | `formal/topics/17-grid-switching/README.md:14`; `CLAIMS.md:105`; `COVERAGE.md:81` | The README says all 37 frozen obligations are discharged by Lean theorems, but SC29 is intentionally a scope statement with no theorem. Fix: say the package accounts for all 37 obligations, with SC29 recorded as scope and the mathematical obligations proved. No proof is missing. |
| m196 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `paper-certified-minlp/formal/VERIFICATION.md:15`; `REVIEW.md:3`; `REVIEW-ANALYSIS.md`, `REVIEW-DISCRETE.md`, `REVIEW-INTEGRATION.md` | The headline says independent reviews cover all 49 obligations, but the detailed review scopes do not name CM04 or CM34. Both are exact-arithmetic/example claims covered by named Lean theorems in `COVERAGE.md`; `Examples.lean` is also listed as a supporting reviewed source, so lack of these identifiers does not prove the claims were never examined. Fix: record explicitly whether the two obligations were reviewed and the result, or narrow the 49-obligation review claim. |
| m197 | refuted after source review | `notes/review-certified-minlp-exact-semantics.md:28-42`; `notes/review-certified-minlp-driver.md:5` | The exact-semantics review explicitly says its hashes identify reviewed bytes, “not a promise that later edits have been reviewed,” and gives a command to compare current files with that historical snapshot. The driver review is dated and pins the same historical bytes. Later driver changes are not a defect in these records. |
| m198 | corrected after source review · **fixed 2026-09-25 (§9)** | `README.md`, certified-MINLP repair-and-replay paragraph; `notes/certified-minlp-repair-and-replay.md`; `paper-certified-minlp/tables/uniform-summary.json` | The README says the linked September 13 repair record links “the current experiments,” although the record expressly preserves the historical 188/92/9 replay and the paper now distinguishes its primary uniform 203/19/67 campaign. Fix the README’s description to say historical repair/replay, and link the paper’s current campaign separately if the overview is intended to cover it. The two counts describe different saved campaigns, not inconsistent recounts of one run; the historical record need not be rewritten. |
| m289 | superseded after source review | `results/quadratic-system-noncommutative-rank-complexity.md:3` | Duplicate of m42. The second PASS review is preserved at `notes/review-quadratic-noncommutative-rank-second.md`; the result note mentions only the first. The two-review claim is supported, and adding the second link is a navigation improvement. Also duplicates m161. See m42 for the finding and remedy. |
| m290 | superseded after source review | `results/quadratic-inertia-one-sided-integer-complexity.md:281` | Duplicate of m127. The numerical checker uses a depth-L LP with lower epigraph rows at every level plus endpoint tangents, while the proof and topic-20 I4 construction use depth-L+1 single-level folding for the same error target. Both are valid; identify the numerical variant precisely rather than imply it tests the exact proof implementation. See m127 for the finding and remedy. |
| m291 | refuted after source review | `results/quadratic-inertia-one-sided-integer-complexity.md:281` | The note accurately says the script checks "the signed error allocation for 3u²-5v²". `code/quadratic_rank/check_one_sided.py:60-63` computes exactly the weighted component bound `3*lower_error+5*upper_error` and checks its allocation budget. The section is titled Numerical verification and makes no exact-arithmetic or full two-variable-solver claim. No correction is needed. |
| m292 | superseded after source review | `results/quadratic-inertia-one-sided-integer-complexity.md:126` | Duplicate of m127. The proof uses depth-L+1 single-level folding, while the cited Beach-style LP and numerical implementation use the stronger all-level system at depth L. These are two construction variants, not three distinct independently specified LPs. Distinguish their descriptions and the scope of the numerical check; also duplicates m290. See m127 for the finding and remedy. |
| m205 | confirmed after document recheck; narrower comparison · **fixed 2026-09-25 (§9)** | `README.md:574` | The statement that the noncommutative-rank result 'unifies and strengthens' the graph and scalar laws should specify their common-accuracy, two-sided leading asymptotics. It does not replace the graph theorem's finite unequal-tolerance LP bounds, scalar finite constants, or one-sided inertia theorem. Fix: say it generalizes the common-accuracy two-sided asymptotic rank laws. The missing standalone derivation of `ncrank(span{H_e})=2 tau*(G)` is not a proof gap: the identity also follows by applying the two proved leading-coefficient formulas to the same graph system. |
| m206 | refuted after document recheck | `README.md:890-895` | 'Every grid size' describes the number of cells for the linked three-mode unit-grid formula; it does not assert a formula for every placement of knots. The immediately following entry separately advertises arbitrary nonuniform grids. The result defines `F_3(N)` on unit intervals and explicitly explains uniform rescaling. Adding 'uniform' would improve specificity, but the alleged arbitrary-grid claim is not present. |
| m207 | confirmed after document recheck; notation/type mismatch · **fixed 2026-09-25 (§9)** | `results/quadratic-nonlinear-input-rank-precision.md:177` | Equation (6) applies `tE_0` to the full transformed `m`-output map `q`, but the subsequently defined `E_0` lies in the reduced output space `R^d`, and `Phi` is formed from `q_bar`. The proof of (7) expressly uses (6) for `q_bar`. Fix: define the output reduction, `E_0`, and its benchmark before (6), and write `p_conv(q_bar,Omega,tE_0)` there (or state the covariance inequality first with generic compatible map and ellipsoid). The later argument already has the intended reading. |
| m208 | confirmed after document recheck; scope and rationale corrected · **fixed 2026-09-25 (§9)** | `results/quadratic-nonlinear-input-rank-precision.md:254` | The closing `5r+1` refinement omits an error-body restriction in a note otherwise allowing arbitrary symmetric convex bodies. Its linked diagonal theorem proves componentwise tolerances; `positive-separable-unconditional-error-precision.md:146-168` extends it to unconditional bodies with the stated oracle assumptions, not arbitrary correlated ellipsoids. Fix: qualify the refinement by componentwise tolerances, or by unconditional bodies and the correct link. The original audit blamed the covariance lower bound incorrectly: for diagonal quadratics, `EJ=(1/4)C diag(Sigma)` is exact. Unconditionality is needed for the displayed coordinatewise upper-error bound to imply membership in the output error body. |
| m209 | refuted after document recheck | `results/quadratic-ellipsoidal-output-precision.md:179-186` | The result claims one linked independent proof audit and separately says the root agent reviewed the proof outline. It does not call the latter a second independent full audit or promise a second review file. Failure to find a separate record cannot disprove that limited root-review statement. No correction is required by this finding. |
| m210 | refuted after document recheck | `results/bilevel-fixed-resource-accuracy-bit-algorithm.md:8`; `results/bilevel-one-resource-accuracy-bit-algorithm.md:60` | Both links go through existing promotion stubs to the reviewed result notes. This is a functioning two-hop reference, not a wrong theorem citation or broken evidence chain. Direct links would be convenient but are an optional cleanup. |
| m211 | confirmed after document recheck; index typo · **fixed 2026-09-25 (§9)** | `results/mip-relaxation-binary-lower-bounds.md:81` | With `g_0=x`, the displayed sum over `k<=j` includes zero and incorrectly cancels the leading `x`; in particular it gives `f_0=0` instead of `x`. The same note's formula at line 69 starts at one. Fix: write `f_j(x,g)=x-sum_{k=1}^j 2^(-2k)g_k`, with an empty sum for `j=0`. This is a localized transcription error, not a defect in the cited sawtooth construction. |
| m212 | refuted after document recheck | `README.md:779`; `results/spatial-bb-exponential-lower-bound.md:267-270` | The README says that one independent review passed with applied corrections; such a review exists. It does not say there was only one review, and an index need not enumerate every later review or proof correction. The result note records the second review and its infimum and discarded-slab corrections. Updating the index would be optional completeness work, not a demonstrated validity repair. |
| m213 | refuted after document recheck | `results/spatial-bb-exponential-lower-bound.md:225-232,325-331` | The relevance remark restricts the claim to termwise relaxations and explicitly identifies coupling relaxations and methods outside the model as escape routes. The note also states that a known global clique cut closes the root and that the result concerns the specified spatial certificate system. It does not prove a bound for unrestricted production solvers, but the cited passage does not claim one. Replacing 'off-the-shelf' with 'in this model' could sharpen style; no mathematical issue is established. |
| m214 | refuted after document recheck | `results/convex-vector-curvature-rank-precision.md:156`; `results/convex-separable-vector-curvature-rank-precision.md:173` | Both cited first-review records explicitly report the exact checks and counts. Their scripts are not archived under `code/quadratic_rank`, so those particular checks cannot be reproduced from retained code alone; neither result claims otherwise. The separable result also links a retained second-review checker. Missing raw code/output for supplementary recorded checks is an archival limitation, not evidence that the reported runs or proofs are invalid. |
| m215 | refuted after document recheck | `results/convex-vector-compiled-integer-precision.md:167`; the two linked overlay reviews | Calling the shared checker independent does not by itself assert a separately authored implementation. The first review records passing checks and the second records inspecting and rerunning the same checker; using one checker across related results is consistent with that evidence. No disagreement in scope or counts is identified. Unrecorded authorship alone does not establish an overclaim. |
| m216 | refuted after document recheck | `results/convex-polynomial-compiled-integer-precision.md:63`; `results/compiled-curvature-quantile-precision.md:97` | The scalar error proof does not require monotone approximate knots; its 'need not be monotone' wording records that weaker requirement. The overlay explicitly specifies canonical, target-independent node evaluations and proves that this available implementation returns ordered knots (`convex-vector-compiled-integer-precision.md`, Section 1). Thus it supplies the extra property it needs rather than importing it without proof. The scalar notes could cross-link this refinement, but no missing algorithm or theorem hypothesis is established. |
| m217 | confirmed after document recheck; review-record mismatch · **fixed 2026-09-25 (§9)** | `results/network-simplex-parallel-path-hull.md:213` | The result says an independent reviewer reran the 300-case check, but `notes/review-common-factor-network-parallel-paths.md` says the verifier was inspected and the author reports 300 passes; `notes/review-network-parallel-paths.md` likewise records inspection, not execution. The retained evidence therefore supports an author-reported run plus independent script/proof review, not the particular rerun attribution. Fix: use that supported description or link a reviewer execution record if one exists. This does not show that no rerun occurred or invalidate the numerical comparisons. |
| m199 | refuted after source review | Results-note checker citations and archived verification directories | The original finding’s broad directory-based counts are not a sound test of missing evidence: many saved outputs live in paper verification directories, and a cited reproducible supplementary checker need not have a committed transcript unless a document promises one. Keep only specific false evidence-link or unsupported-result claims, such as the separately identified cases; no general repository validity defect follows from roughly 27 scripts lacking an adjacent or discovered output. |
| m200 | refuted after source review | `research-20260922/nuclear-global/assessment.md`, Corrections after independent review; `research-20260922/log.md:43-46` | The first section explicitly supersedes the earlier author-status line and each listed numerical or logical statement, explaining the strengthened uniqueness premise, infeasibility pruning, corrected sample maximum and stored-point precision. The old body is a historical pre-review record with prominent errata. Updating it or labeling it “original assessment” would improve navigation, but the corrected document does not endorse the superseded statements. |
| m201 | confirmed after document recheck; narrowed · **fixed 2026-09-25 (§9)** | `research-20260922/README.md:51` | The exact contraction-rate bullet omits the Jacobi-round restriction. `iterated-obbt/theory.md:53-61` explicitly limits exact rates to Jacobi rounds and gives different sequential and Jacobi rates even for `a=1`. Fix: say that the displayed exact rate is for Jacobi OBBT rounds. The experiment report's Section 0 already corrects the historical body figures and interpretations; those explicitly superseded figures and the optional all-hard summary table are not additional unresolved validity issues. |
| m202 | confirmed after document recheck; minor attribution limitation · **fixed 2026-09-25 (§9)** | `notes/composite-univariate-envelopes-experiments.md:18,143-144` | The claim that the split arm isolates reformulation, and that `arki0003`'s gain therefore comes from reformulation alone, is too specific. `code/univariate_envelopes/run_minlplib.py:11` gives only split/hybrid a separate presolve-bound pass, and `uenv/osil.py:298-302` imposes its bounds when accepting a univariate expression. The native arm performs its own presolve, and total reported time includes construction and the extra pass, so this is not outside information or an uncharged timing claim. Fix: attribute the observed gain to the split pipeline, which combines reformulation with precomputed implied bounds; isolating reformulation alone would require a matched-bound comparison. |
| m203 | refuted after document recheck | `results/pooling-existential-theory-of-reals.md:459-469`; `notes/log.md:996-1006` | The two original reviews describe an earlier checker, but the development log explicitly records alignment with the text and a subsequent pass. The note calls the seven cases a sanity check, not proof, and does not claim an archived raw solver transcript or a new independent rerun of the aligned version. Absence of a raw output file is an archival limitation, not evidence that the stated run or theorem is defective. No correction is required by this finding. |
| m204 | superseded by the report's existing correction block | `research-20260922/pooling-multiattribute/assessment.md:3-24` | The leading correction block explicitly supersedes the body baselines and bounds, refutes the sppb0 improvement claim, and reports the safe sppc0 bound and corrected margin. `verification.txt` supplies the dated comparison and distinguishes the original-bound margin (about 1682 across variants) from the safe-bound margin (about 1799). The old body is a superseded scouting record, not an uncorrected final claim. Synchronizing it would be an editorial improvement, not a new validity repair. |
| m218 | confirmed after document recheck; nonexistent section reference · **fixed 2026-09-25 (§9)** | `results/common-factor-fixed-linking-optimization.md:5` | The audit citation says 'sections 1 and 5', but `notes/review-common-factor.md` has only sections 1–3. Its follow-up paragraph within Section 1 covers the integer and signed common-factor corollaries. Fix: cite Section 1, including its follow-up audit paragraph. The review itself exists and covers the claimed extension. |
| m219 | refuted after document recheck | `results/common-factor-reciprocal-anchor-full-hull.md:197`; `code/common-factor-anchor-verify.py:50` | The continuous LP check indeed uses a finite grid enriched with the constructed atoms and cannot exclude a better off-grid law. The result explicitly discloses that support choice, floating-point LP arithmetic, and the fact that these are implementation cross-checks rather than the continuous-support proof. 'Independently formulated' describes the different shared-measure LP constraints, not independence of its support grid from the candidate. The audit identifies an already stated limitation, not an unsupported claim. |
| m220 | refuted after document recheck | `results/network-simplex-series-parallel-coefficient-growth.md:34-40` | The passage specifies the sense in which the new obstruction strengthens the earlier one: treewidth two, planarity, and a linear observation count. Its very next sentence says simplex dimension grows and the fixed-dimension series-parallel case is not established. The earlier theorem fixes simplex dimension two, so the results are incomparable across all parameters, but the source does not claim otherwise when read with its explicit qualification. 'Complements' would be an optional wording improvement. |
| m221 | refuted after document recheck | rank-one, point-packing, McCormick and FBBT verification records cited in the original candidate | Missing standalone stdout/JSON files does not mean only scripts exist: `notes/review-rank-one-stability.md` records exact pass counts; `notes/audit-mccormick.md` records executed commands and outcomes; `notes/audit-packing.md` records the dated solver rerun, environment, tolerances and limitations; other notes record author-reported runs. The point-packing result explicitly labels its table floating-point corroboration. No claimed raw-log archive or exact numerical certificate is contradicted. Additional machine-readable logs would improve reproducibility, but this broad candidate does not establish a validity defect. |
| m222 | refuted after document recheck | `results/scaling-disjunctions-hull.md:128` | The displayed system contains a redundant inequality `n>=0`, already implied by `nl<=X<=nu` and `l<u`, but still correctly describes the hull. The passage does not claim an irredundant inequality list or ten facets. A preceding mention of facet computation does not make every displayed modeling bound a claimed facet. No correction is needed for mathematical validity. |
| m223 | confirmed after document recheck; missing scope restriction · **fixed 2026-09-25 (§9)** | `notes/bilevel-response-complexity-map.md:47` | The conditioned SPD-box additive-algorithm row omits the exclusion of upper constraints involving the follower response. The linked theorem states that exclusion in Section 1 and explains in Section 5 why an approximate response cover need not preserve such constraints. Fix: add 'no response-dependent upper constraints' to this row, consistent with the nearby additive-algorithm entries. |
| m224 | confirmed after document recheck; nonuniform comparison · **fixed 2026-09-25 (§9)** | `README.md:407` | The degree-independent `12r` overhead (`9r` for independent outputs) is called an improvement immediately after the sparse mixture bound `4.5r+sum_i S_i+1`. It improves degree dependence, but not uniformly the numerical binary-count bound: the sparse bound is smaller for low degrees, while the degree-independent guarantee can be better for sufficiently large degrees. Fix: say the dense positive-polynomial theorem removes degree dependence, with these constants, rather than calling it an unconditional bound improvement. The original audit's universal 'practical degree' claim and approximate crossover thresholds are unnecessary and should be removed. |
| m225 | confirmed after document recheck; prose typo · **fixed 2026-09-25 (§9)** | `results/rational-power-compiled-integer-precision.md:286` | The sentence reads 'Thus (6), removes the dense-degree restriction'. Fix: delete the comma after `(6)`. This finding concerns grammar only and supplies no evidence of an error in (6). |
| m226 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `results/accuracy-dependent-curvature-precision.md:220` | The concluding discussion retains an unqualified claim that a multivariate separable analogue remains open (lines 230–234), while lines 263–267 link the completed scalar-sum and independent-output extension. Lines 220–228 also describe the dense-polynomial computational step as conditional, although lines 256–260 link its later solution. Replace the open-status wording with dated local-scope statements and forward links to `compiled-curvature-quantile-precision.md` and `separable-convex-graph-linear-dimension-precision.md`. Preserve the distinction between those later results and the present one-dimensional proof; they do not settle arbitrary coupled multivariate outputs. |
| m227 | refuted by source review | `results/rational-power-compiled-integer-precision.md:215` | Section 3 explicitly defines its local `alpha=2/D`; Section 6 separately defines forward `alpha` and inverse `beta=2/alpha`. The local chord bound is correct under its stated definition. Using `beta` consistently would be an optional notation improvement, not a mathematical issue. |
| m228 | refuted by source review | `results/convex-vector-curvature-rank-precision.md:156` | The linked reviews record the finite-check scopes, counts, and outcomes and explicitly distinguish them from the proofs. They do not promise saved executable reproductions. No standalone reproducer is cited for the listed curvature-rank, unconditional-allocation, or separable-box reviewer checks. Archiving such scripts would improve reproducibility, but their absence does not establish a false claim or proof defect. |
| m229 | refuted by source review | `results/convex-vector-facet-curvature-rank-precision.md:3` | The dependency link resolves to an intentional promotion pointer that directly links the reviewed result and says it preserves existing investigation and review links. The dependency is accessible; linking directly to `results/convex-vector-curvature-rank-precision.md` would only shorten navigation. |
| m230 | confirmed (document correction) · **fixed 2026-09-25 (§9)** | `results/smooth-map-local-rank-integer-complexity.md:321` | The product example computes Hessian eigenvalues only on the diagonal, which need not meet the interior of the arbitrary positive box used in the theorem. The stated coefficient `k/2` is still correct. Complete the justification at any positive point with `H=f(x) diag(1/x)(11^T-I)diag(1/x)`: both diagonal factors are invertible and `11^T-I` has eigenvalues `k-1,-1,...,-1` for `k>=2`. This proves nonsingularity throughout the positive orthant without a diagonal-intersection assumption. |
| m231 | refuted by source review | `results/rank-one-correlation-face-conic-lower-bounds.md:207` | The repository accurately quotes the log-free bound explicitly stated in LRS Theorems 1.1 and 5.4 ([author manuscript](https://www.dsteurer.org/paper/sdpsize.pdf), PDF pp. 5 and 34). The displayed proof of Theorem 5.4 contains an unresolved quantitative discrepancy: its choice `n >= (2/alpha') m^(13/2) log n` directly yields an exponent of order `(n/log n)^(2/13)`. This observation does not establish that the source theorem or its repository citation is false. Remove the claimed citation error; retain the source-level caveat if discussing what follows directly from that displayed derivation. |
| m232 | refuted by source review | `results/rank-one-correlation-face-conic-lower-bounds.md:244` | The linked review records the exact enumeration scope, counts `2,4,8,16,32,64`, and outcome, and says that the proof establishes the unrestricted result. It does not claim a saved executable enumeration script. Preserving one would improve reproducibility but is not an established correctness issue. |
| m233 | refuted by source review | `results/point-packing-relaxations-anstreicher-conjecture-4.md:149` | The note explicitly labels the table as floating-point rerun output and the Fraction audit as supplementary finite evidence. `code/point_packing/pp_relaxations.py` is a saved reproducer for the numerical models, including cases outside the conjectured formulas. A separate raw run log and the inline Fraction audit would improve archival reproducibility, but their absence does not make the table or its qualified status an established defect. |
| m234 | refuted by source review | `results/scaling-disjunctions-hull.md:123` | The displayed system is a correct hull description and does not claim to be an irredundant facet list. The bound `n>=0` is redundant because `nl<=X<=nu` and `l<u` already imply it. Mentioning a direct facet computation does not require removing ordinary redundant variable bounds from the subsequently displayed description. |
| m235 | superseded by m211 | `results/mip-relaxation-binary-lower-bounds.md:81` | Duplicate of the omitted lower summation limit in the displayed definition of f_j; see m211. |
| m236 | corrected; stale literature-status summary · **fixed 2026-09-25 (§9)** | `README.md:774` | The entry reports a search that found no prior spatial tree-size lower bound, while the result’s later source assessment identifies Coniglio’s spatial lower bound and Jarre’s binary-SDP lower bound. Qualify the earlier search as historical and summarize the contribution under its stated certificate model. The existing one-review statement is true and need not enumerate every later review (m212). If discussing objective-based tightening, retain the augmented-cover qualification `nodes >= 1/((q+1)rho)` for at most `q` certified reductions per processed node. This finding concerns consistency with the repository’s later literature assessment, not a fresh novelty judgment. |
| m237 | superseded by m213 (refuted) | `results/spatial-bb-exponential-lower-bound.md:227` | The surrounding text explicitly restricts the claim to the stated certificate model and names coupling and symmetry as escapes. Read in that context, the off-the-shelf wording is not an unrestricted solver lower bound. Replacing it with “schemes satisfying the theorem’s assumptions” is optional clarification; see m213. |
| m238 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260922-constant-data-messages.md:134` | If “maximum degree four” is intended as an exact value for every `n>=2`, the endpoint case is wrong: the maximum is three at `n=2` and four for `n>=3`. State “maximum degree at most four (three for n=2)” or give the two exact cases. The first state `s_1` has three neighbors; degree four occurs at states `s_2,...,s_(n-1)`. The treewidth/pathwidth statement and Gershgorin upper bound are unaffected. |
| m239 | refuted by source review | `notes/research-20260922-planar-message-algorithm.md:334` | The current opening already reports the completed independent review and explicitly says that later work resolved the listed limitations with a different enumeration algorithm, while preserving this note’s original scope. The closing obstacle list is historical context under that current-status pointer, not an unsupported claim that the later results remain open. Labeling it “obstacles at the original drafting stage” would be optional editorial clarification. |
| m240 | refuted by source review | `notes/review-20260922-message-complexity.md:93` | The review does save the two programs’ PASS summaries and describes their test domains at lines 88–109; the assertion that neither code nor output is saved is therefore inaccurate. The inline scripts themselves are not supplied, and the saved author checkers do not reproduce the state-indicator lift audit. Archiving that code would be an optional reproducibility improvement, not evidence that the reported finite checks or analytic proof are wrong. |
| m241 | refuted by source review | `notes/research-20260922-message-complexity.md:307` | The research note says the reviewer “established” the short approximation, while the review calls the approximation correct and refers to its presence in the original note. These statements do not establish conflicting authorship: “established” can describe independent derivation or verification, and the documents do not record the edit chronology needed to allocate authorship. No attribution correction is justified by this evidence. |
| m242 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260912-represented-matroid-psd-approximation-set.md:339` | Specify an oriented (signed) vertex-edge incidence matrix for the rational graphic-matroid representation, and make the same qualification in `research-20260912-represented-matroid-psd-independent-review.md:195`. “Incidence matrix” is ambiguous: an unsigned triangle matrix has determinant of magnitude two over Q, so its three edge columns are independent although the graphic matroid has a circuit. This is a convention clarification; it is not true that every unsigned incidence matrix fails (bipartite graphs are an exception). |
| m243 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260912-dag-psd-approximation-set.md:454` | The unqualified “absence of implementation” is obsolete: Section 9 and Topic 21’s implementation documentation describe an executable Lean reference producer and proved execution bounds. Update the practical-limit sentence to distinguish that reference implementation from practical performance evidence or an optimized solver. Preserve the large worst-case exponent and the note’s explicit distinction between a bit-work theorem and a wall-clock guarantee. |
| m244 | confirmed (document correction) · **fixed 2026-09-25 (§9)** | `notes/research-20260912-block-snapshot-probe.md:222` | The closing statement that a fresh implementation review has not been incorporated contradicts lines 19–22, which link and summarize the passed review. The review and current source both identify SHA-256 `85c328d8cab52989a308c90e54008ecc211ecb0ad1bd5b3db39b90f6ea6193ba`. Remove the obsolete pending-review sentence or replace it with the passed-review link; retain the limits on novelty and empirical process-model validity. |
| m245 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260912-covariance-dense-oracle.md:118` | The displayed maximum errors do not exactly match the cited saved reports. `code/research_20260912/results/covariance-dense-oracle-validation.json` has scaled gradient `5.1736392947532295e-14` and directional error `6.541478470012407e-11`, which round to `5.17e-14` and `6.54e-11`, not `5.19e-14` and `6.55e-11`. Likewise `research-20260912-structured-dense-oracle.md:137` gives `2.80e-8`, while `code/research_20260912/structured_dense_oracle.json` gives `2.794044440257437e-8` (`2.79e-8`). Align the rounded maxima with their reports or explicitly label them upper bounds. The existing values are conservative and do not change validation outcomes. |
| m246 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260922-aggregation-frontier.md:3` | This investigation still presents review as pending and has no current-status pointer to `results/infinite-quadratic-aggregation-hhc.md`, whose reviews and formal packages cover the stated later scope. Add a prominent promotion pointer and identify the `r>=6` construction and “awaiting independent review” section as historical. Explain that the reviewed result proves HHC already for `r>=2`; do not simply replace `r>=6` inside the older proof, which uses a different sufficient-dimension argument. |
| m247 | refuted by source review | `notes/research-20260922-pdlc-frontier.md:9` | The note begins with a clear current-result link and explicitly labels the projective argument below a superseded proof route. Its dated draft status and original review checklist therefore describe retained research history. The first-review account at lines 363–369 records the later check without making the old draft the current result. Updating historical tense would be optional; no current-result status defect is established. |
| m248 | refuted by source review | `results/cluster-free-branch-and-bound-constrained-minima.md:433` | The limitations paragraph says the weaker extension is not proved “here,” while the opening explicitly links the separate projection proof that removes LICQ and strict complementarity under feasible quadratic growth and a linear error bound. The transfer note obtains these from actual-critical-cone SOSC with a fixed KKT multiplier and MFCQ in its stated setting. This is a boundary of the proof retained in this note, not a claim that the extension is globally unproved. A local cross-reference would be optional clarification. |
| m249 | refuted by source review | `notes/research-20260922-aggregation-accuracy.md:362` | The cited reviews record the scopes, counts, and outcomes of their inline exact-arithmetic checks. Both notes explicitly distinguish that finite evidence from their general proofs, and the accuracy note identifies later Lean coverage separately. The inline scripts are not supplied, so exact replay would require reconstructing them, but saving supplementary reviewer programs is a reproducibility enhancement rather than an established error in these qualified historical records. |
| m250 | corrected (qualified document issue) · **fixed 2026-09-25 (§9)** | `notes/research-20260912-noisy-markov-spacing.md:3` | The header still says the constrained solver and certificate integration are under review, although the producer, exact-certificate, integer-integration, and refined-spacing-integration reviews record acceptance. Update that status and link the later reviews. The initially cited helper review covers SHA `6e2fa178...`; the current helper is SHA `a8bdac20548764c11bdd29b476c4a37722af088aa63af0b0e29b46d5d0b08371` and its optional `refined_pairs` mode is covered by `research-20260912-refined-spacing-integration-review.md`. Preserve the scope split: the numerical producer alone supplies no true-likelihood certificate, while the separate exact certifier does. |
| m251 | refuted by source review | `notes/research-20260912-noisy-markov-kinetics-probe.md:101` | The numerical table and exact certificates use different valid memory-error bounds. The note expressly says the exact certifier uses a stronger innovation floor and produces smaller gaps (lines 128–132); the floating value is the reviewed finite-series bound implemented by `spectral_delta` in `code/research_20260912/noisy_markov_design.py:107–116`. The difference between constants is disclosed, not a contradictory certificate. No change is required on this basis. |
| m252 | refuted by source review | `notes/research-20260912-noisy-markov-kinetics-probe.md:143` | The note explicitly adds `0.01 I` in its model (lines 55–57), defines the displayed efficiency as the determinant ratio for that `J`, and limits the guarantee to the stated local-design models. This is a prior-augmented criterion, but it is not presented as an unregularized-information guarantee. Calling it regularized D-efficiency would be optional clarification, not correction of an established error. |
| m253 | confirmed by source review · **fixed 2026-09-25 (§9)** | `notes/research-20260922-approximation-exact-smoothing.md:422` | The limits section still says the proofs need independent adversarial review, especially the partition certificate and finite-grid cutoff. The header links `notes/review-20260922-approximation-exact-oracle.md`, which reviews those arguments and reports no substantive gap. Fix: replace the pending-review sentence with the completed review status while retaining the separate statement that no Lean proof has been produced. |
| m254 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `notes/research-20260922-envelope-higher-moments.md:17,54,307` | The compact parameter domain is not required to be nonempty, yet the `L=0` sentence asserts `K=1` almost surely; an empty domain gives `K=0`. The linked VC review explicitly requests nonemptiness. Also, the verification footer says an explicit continuous-versus-atomic `L=0` distinction was added, but that special case is absent. Section 4 does already count atomic ties and states its bound at zero tolerance, so the original allegation that atomic ties were wholly omitted was too broad. Fix: require nonempty `T` (or separate the empty case), and either add the atomic `L=0` explanation or correct the footer. |
| m255 | refuted by source review | `notes/research-20260922-finite-grid-smoothing.md:287` | The note attributes the 52,266 interval checks and 5,150 budget checks to a reviewer; the linked review identifies its script as a temporary `/tmp/check_grid_smoothing_review.py` aid and says the general results rest on proofs. `results/smoothed-indicator-block-dp.md:664–667` makes the same limited attribution. These passages do not claim the script is archived or independently reproducible from the repository. The other temporary partition checker is a separate review, not the source of these counts. Archiving these aids would improve reproducibility but is not a correction to a false claim. |
| m256 | refuted by source review | `notes/research-20260922-smoothed-dp-checks.md:80` | The checker does test only the disclosed derivative bound `8/3`; adding the tighter message bound `1/3` would extend test coverage. Neither the check record nor the result claims that these finite checks prove the expected-work theorem. The result expressly says they test deterministic identities, and explicitly identifies the four-cycle wording as historical text predating the biconnected-block formulation (`results/smoothed-indicator-block-dp.md:657–667`). Neither point establishes a current mathematical or verification-claim defect. |
| m257 | confirmed by source review · **fixed 2026-09-25 (§9)** | `notes/research-20260912-general-covariance-memory-bound.md:3–8` | The header still requests a fresh proof review and primary-literature audit. `notes/research-20260912-general-covariance-memory-independent-review.md` supplies a passing mathematical review, with a saved JSON record; `notes/research-20260912-covariance-decay-priority-audit.md` supplies a bounded literature audit. The closeout links the completed review. Fix: link those records and describe their completed, limited scope; do not convert the bounded audit into a claim that priority has been established. |
| m258 | refuted by source review | `notes/research-20260912-fixed-parameter-doptimal-fptas.md:5` | The header explicitly says the theorem is also derived from the Lean spectral-cover construction. Section 7 explains the determinant consequence, tolerance `epsilon/p`, and why this route does not require implementation of the predecessor normalization algorithm. It does not claim that the Section 2 algorithm was itself implemented or verified in Lean. The alternate verified route proves the stated existence guarantee, and the distinction is already disclosed. |
| m259 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `notes/research-20260912-gated-information-bounds.md:126` | The sentence about no dimension-free improvement for trace-inverse error is imprecise because its existing multiplicative factor `alpha` is already dimension independent. The independent review (`notes/research-20260912-gated-bound-independent-review.md:274–276`) gives the precise point: rank one can still approach the full multiplicative factor `alpha` for trace-inverse cost. Fix: use that formulation. This is wording precision, not a counterexample to the bound. |
| m260 | refuted by source review | `notes/research-20260912-robust-design-certificates.md:209–211` | The text says “about 99.617800%”, not “at least 99.617800%”. The underlying exact log gap is displayed, and the closeout and paper separately give conservative guaranteed displays. The original audit incorrectly converted an approximate decimal into a strict lower-bound claim. The displayed approximation is slightly different from rounding to six decimal places, but no exact guarantee is overstated by this wording. |
| m261 | archival limitation; not a demonstrated validity defect · **fixed 2026-09-25 (§9, §10)** | `notes/research-20260912-ode-prototype.md:94–97` | The rate-one diagnostic widths `0.188603` and `0.0943015` are not linked to a saved run, and targeted searches did not trace them to the saved ODE artifacts or driver text. The saved singleton-tube example uses rate `9/10`, so it cannot directly substantiate this rate-one display. The qualitative fixed-box obstruction is independently established by the analytic example in `notes/research-20260912-validated-polynomial-tubes.md:5–13`. Fix: label these widths as an unarchived diagnostic, link their actual source if available, or replace the numerical illustration with the analytic example. This review does not establish that the numbers are false. |
| m262 | confirmed by source review · **fixed 2026-09-25 (§9)** | `notes/pooling-bounded-contract-exceptions-algorithm.md:3; notes/pooling-fixed-rank-contract-exceptions-algorithm.md:3` | Both headers still request fresh independent audits, although the respective `review-pooling-*-contract-exceptions-benders.md` and `-second.md` records report PASS for their stated scalar and fixed-rank models. The manuscript coverage map also records incorporation. Fix: replace the pending-audit status with links and scope for the completed reviews, or explicitly identify the old status as historical. No claim of established novelty should be added. |
| m263 | refuted by source review | `notes/pooling-bypass-vertex-cover-algorithm.md:3–8` | The opening explicitly says the note was promoted after two independent audits and that it preserves earlier candidate language. The later “awaiting independent review” line is therefore historical, with the current promoted result linked immediately above it. This is not an unexplained contradiction in current review status. |
| m264 | refuted by source review | `notes/pooling-bypass-degree-four-hardness.md:3,189–201` | The header labels this a retained milestone and records two passing reviews; the end links both PASS records. Saying a first reviewer approved the argument does not say only one reviewer approved it and is logically compatible with those records. The older candidate phrasing does not establish the claimed review-status contradiction. |
| m265 | refuted by source review | `notes/pooling-bypass-linear-universality.md:6–13,64–68` | The note explicitly preserves an earlier, incomplete investigation and links its fully reviewed successor. Its negative-capacity sentence can be simplified: a negative shifted capacity makes the nonnegative port-flow sum infeasible. The extra lower-bound qualification does not produce a false conclusion or undermine the successor theorem. This is optional editing of a superseded investigation, not a current validity defect. |
| m266 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `README.md:945–949` | The summary says an exact extended formulation “needs” one auxiliary per independent unobserved cycle. The linked note explicitly proves an upper bound for its construction and disclaims necessity or a lower bound on extension complexity (`notes/network-simplex-observed-rank-elimination.md:50–53`). Fix: replace “needs” with “uses” or “can be built using” so the README states the proved construction bound. This is an ambiguous summary, not evidence that the hull theorem is false. |
| m267 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `notes/hens-20260912-singularity-and-lift.md:90–114` | The note calls polished numerical points exactly feasible and calls `inf(original) <= 108,999.78` rigorous. Its own checks report nonzero residuals (`1.7e-12`, and `4.5e-10` for the independent reconstruction in Section 8), with recomputed values rounded to doubles. No exact feasible witness or validated correction argument is supplied. Also the independent objective `108999.783324` is rounded downward to `108,999.78`. Fix: describe numerical feasibility and an approximate upper estimate, or provide an exact/validated feasible construction and conservatively rounded bound before retaining “rigorously”. This does not refute the guard singularity itself. |
| m268 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `notes/hens-20260912-singularity-and-lift.md:10–20,132–139,212–220` | The summary and conclusion extend “infimum not attained and far below the recorded primal bound” to gen2/gen3, while Section 6 says those instances were checked structurally only. Finding the same guarded LMTD expression supports a structural warning, but does not by itself establish a jointly feasible limiting construction, nonattainment, or the quantitative comparison with each recorded bound. Fix: confine numerical comparisons to gen1, with the certification caveat in m267, and state the gen2/gen3 conclusion at the actually established structural scope. Stronger claims need instance-specific justification, which may be analytic rather than computational. |
| m269 | refuted by source review | `notes/common-factor-p-split-correction.md:92–120` | The section begins “Consider any lifted convex relaxation”, so inclusion of the true feasible set and hence its hull is already part of the stated model. Its proof then constructs a relaxation point outside a hull-supporting inequality, establishing strict inclusion under that premise. The paper makes the relaxation premise explicit in symbols. Adding the same sentence to the note would improve self-containment, but the original audit overlooked the existing “convex relaxation” assumption. |
| m270 | confirmed by source review · **fixed 2026-09-25 (§9)** | `papers/pooling/sections/06-synthesis.tex:108` | The open-problem discussion says “The general parameter bound is quasipolynomial”, but its cited theorem `s5:quasipoly-path` explicitly has one scalar parameter. Generality there refers to planar transition relations, not parameter dimension; the source note says univariate partition overlay is essential. Fix: say that the one-scalar-parameter case with general planar relations has the quasipolynomial bound, and leave the multiple-parameter boundary open. |
| m271 | refuted by source review | `notes/parametric-affine-strip-path-projection.md:7,45–47` | The model explicitly specifies rational polynomial coefficient functions. These have rational coefficient denominators, and gain normalization subsequently creates rational functions, so mentioning denominators in the proof does not broaden the input model. The linked review expressly says a rational-function-input extension is optional and “not silently needed for the formal polynomial-input statement audited here”. No unaudited extension is asserted. |
| m272 | confirmed in narrower form by source review · **fixed 2026-09-25 (§9)** | `notes/pooling-bypass-degree-three-hardness.md:3,164–177` | The historical header says two fresh independent reviews PASS, but the second review (`notes/review-pooling-bypass-degree-three-second.md:5–10`) discloses that its author proposed the half-port refinement. The first review explicitly is independent of that contributor. Fix: describe the two records as one independent proof review plus a contributor review with a separate implementation, or cite any later independent reviews that justify an updated label. Later manuscript coverage records further reviews, so this is provenance precision for the two named records, not evidence that the final theorem lacks independent review. |
| m293 | confirmed by source review · **fixed 2026-09-25 (§9)** | `notes/research-20260912b-closeout.md:73` | The relative link to `gdp-instance-catalog-20260912.md` points to an absent file in `notes/`. Fix: link the retained catalog, or remove the unavailable link and identify the archived instance set in prose. This is a broken reference, not evidence that the reported instances are invalid. |

## 4. Original audit coverage

Sections 4–7 preserve the original September 24 audit's coverage and reports.
Descriptions of executed checks in these sections are historical, not a record
of new executions. The revised issue tables take precedence over conflicting
earlier conclusions. The original audit reports 108 auditor tasks plus its
skeptic pass; those counts do not describe the reassessment team.

Auditor agents were assigned coherent clusters; results clusters received two
independent lenses. The table records the original audit’s completed assignment list.

| Cluster group | Scope | Auditor reports received |
|---|---|---|
| R1-R25 | all 207 results files, in 25 clusters, two independent lenses each | all 50 done |
| N1-N11 | notes-based results (research-20260912 and -20260922, misc theory) | all 11 done |
| S1-S5 | September 22 research folder, two lenses each | all 10 done |
| L0-L13 | Lean infrastructure and 31 topics | all 14 done |
| P1-P13 | 14 paper folders | all 17 done |
| V1-V6 | verification-process and status-consistency records | all 6 done |
| adversarial pass | findings retained as major/moderate after initial review, with the exceptions in Section 7 | 20 skeptic reports (Section 7) |

Coordinator hand-checks of individual proofs, sources, Lean statements and
saved data are listed in Section 4a; they were chosen to cover clusters that
the agents had not yet reached and to adjudicate every major and moderate
finding independently.

Mechanical checks reported by the original coordinator (no Lean run):

- No `sorry`, `axiom`, `native_decide`, `admit` in any proof module under
  `formal/Formal` or the paper formal exports; the only `native_decide`
  uses are in review example files under `formal/topics/21-dag-spectral/verification/`,
  which are outside the built library.
- `formal/scripts/check_imports.py` passes: all 813 modules under
  `formal/Formal` are imported by `Formal.lean`, so the axiom audit covers them.
- Review-note existence: every `results/*.md` file that claims independent
  reviews links to review notes that exist (a slug-based count produced 45
  false alarms because review notes are named after investigation slugs;
  all linked files resolve). Two results cite audits by file name rather
  than link (`notes/audit-packing.md`, `notes/audit-rank-one.md`); both exist.
  A keyword scan of review notes for negative verdicts found only PASS
  verdicts with incidental wording.
- Broken local link: `notes/research-20260912b-closeout.md:73` points to an
  absent instance catalog (m293). This does not establish that every other
  repository link resolves.
- Historical SHA256 manifests do not identify the later source tree.
  `formal/VERIFICATION.md` and `formal/README.md` explicitly disclose their
  snapshot scope. Such drift alone does not invalidate the original checks.
  See M27 and the individual provenance rows for misleading current-delivery
  claims; do not infer PDF reproduction failure from source differences alone.
- Lean claims in results files: 33 results files mention Lean; the 26
  that link a formal topic link existing topic folders whose own README
  status is complete, and the 7 without a link mention Lean only to state
  that they are not Lean-verified.
- Lean coverage-table names: every backticked declaration name in the 28
  `COVERAGE.md` files (formal root plus 27 topics; roughly 2,500 names)
  resolves to a declaration in `formal/Formal` or the certified-MINLP
  project; the 20 unmatched tokens are module file names (all present)
  or prose fragments. Coverage maps are not stale at the name level.
- Review-count integrity (V6): every `results/*.md` whose header claims two,
  three or four independent reviews or audits links that many distinct review
  notes somewhere in the file, and every such link resolves (0 exceptions over
  the 204 results files that cite a review). Only two results claim a review
  without linking a `notes/review-*.md`: `results/extended-rpd-supporting-flow.md`
  links `notes/research-20260912-ode-theory-independent-review.md` instead, and
  `results/rank-one-zero-lower-hardness.md` names `notes/audit-rank-one.md`;
  both files exist.
- Status-line consistency: several notes have stale review/completion
  wording, including the LB-ESH theory note (m169), aggregation frontier
  (m246) and covariance-memory note (m257). Explicitly historical entries
  and drafts require separate treatment; see the revised rows. The earlier
  assertion that only one live contradiction existed is withdrawn.
- Axiom-audit design (`formal/Verify.lean`): the audit enumerates every
  constant whose owning module name begins with `Formal`, including private and
  auxiliary declarations, collects its axiom dependencies, and fails on
  anything outside `propext`, `Classical.choice`, `Quot.sound`; it also aborts
  if the enumeration is empty, so a misconfigured run cannot pass vacuously.
  The original review found this design sound. The retained logs must be
  interpreted according to their explicitly recorded scope; see m191 and m194.
- Lean claim coverage (L0): every frozen claim identifier in each topic's
  `CLAIMS.md` appears in that topic's `COVERAGE.md`, with four deliberate
  exceptions that the maps themselves explain: MS01-MS03 in topic 13 and FS02
  in topic 15 are script-behavior, historical-measurement and review-history
  obligations that the coverage maps explicitly place outside mathematical
  completion (topic 13's map counts 46 mathematical obligations out of 49
  listed, and topic 15's says FS01-FS03 are outside it). No mathematical
  obligation is silently unmapped.
- Lean module counts: the per-directory module counts (QuadraticAggregation
  21, InfiniteAggregation 43, MatroidSpectral 65, DAGSpectral 124,
  QuadraticPrecision 57, 66 structural multilinear modules, and the
  original 106-module breakdown) agree with the numbers quoted in
  README.md and the topic index.

### 4a. Historical coordinator hand-checks of proofs and sources

- Coordinator exact check of `notes/parametric-path-lp-obstructions.md`
  (N11): for `epsilon = 1/4`, objective `c_j = epsilon^(3(n-j))` (`c_n = 0`)
  and the stated witness `lambda(u)`, every one of the `2^n` Klee-Minty vertices
  is the unique maximizer of `c^T x + lambda(u) x_n` among all vertices, and
  every `lambda(u)` lies in `(-1/15, 1/15)`; verified in exact rational
  arithmetic for `n = 3, 4, 5, 6` (8, 16, 32 and 64 vertices). The note
  credits the construction to Gärtner, Helbling, Ota and Takahashi. Correct.

- Coordinator hand-check of `notes/research-20260922-constant-data-messages.md`
  Proposition 1 and Theorem 2 (N5): iterating `s_i = theta s_{i-1} + theta x_i + r_i`
  from `s_0 = 0` gives identity (3); Cauchy-Schwarz under that single linear
  constraint gives `q_z = (t - c_z)^2/D_z` with
  `D_z = W_n + sum_i theta^{2(n-i+1)} z_i`, and the first summand equals
  `e_i^2` on both supports; denominators lie in `[1, (1+theta^2)/(1-theta^2)]`;
  base-`theta` digit strings first differing at power `k < n` are separated by
  at least `theta^k (1-2theta)/(1-theta) >= theta^n`, which needs
  `theta^2 - 3 theta + 1 >= 0` and holds for `theta <= 1/10`; near each center
  `q_z <= theta^{2n}/9` while every other `q` is at least
  `4 theta^{2n}/(9 C_theta)`, larger because `C_theta < 4`. The `2^n`
  formula lower bound then follows by the finitely-many-roots argument.
  Correct.

- Coordinator hand-check of `notes/research-20260912-noisy-markov-certificates.md`
  (N3): the certificate inequality is right, since concavity of `logdet`
  gives `logdet J <= logdet N - p + tr(N^-1 J)` for any SPD reference `N`,
  and `J_true(S) <= J0 + A_L(S)/(1 - delta)` with trace against `N^-1` being
  monotone in the PSD order yields the stated arc-additive bound; rounding
  scores upward and using the upper logarithm endpoint for the tangent
  constant and the lower one for the incumbent keep the bound valid. The saved
  window-8 certificate (`code/research_20260912/results/noisy-markov-exact-certificate-n48-l8.json`)
  records a gap of 0.0027007, matching the note's table entry 0.00270073.

- Coordinator hand-check of `notes/research-20260912-fixed-parameter-doptimal-fptas.md`
  Section 3 (N2): `J(P*) >= B B^T` because `J` is the sum of all rank-one
  factors `u_j u_j^T`, which include the basis columns, so
  `A* = T J(P*) T^T >= T B B^T T^T >= I` from `1 <= tau_i^2 w_i < 4`; the
  floor residuals give entrywise differences below `N h`, the row-sum bound
  gives `||A_hat - A*||_2 <= p N h = eta/p`, and with `A* >= I` this yields
  `A_hat >= (1 - eta/p) A*`; determinant monotonicity on positive definite
  matrices, invariance of the determinant ratio under the congruence, and
  Bernoulli's inequality `(1 - eta/p)^p >= 1 - eta` give (7). The singular
  fallback is handled correctly. Correct.

- Coordinator hand-check of `notes/generalized-monomial-gap-obstruction.md`
  (N8): convexity of `f_eps = x^(1-eps) + x^(1+eps)` on `[1,3]` holds because
  `(1+eps) x^(2 eps) >= 1 + eps > 1 - eps` for `x >= 1`. The closed forms
  `T_eps = 3 sinh(eps ln 3) - 4 sinh(eps ln 2)` and
  `H_eps = 1 + 3 cosh(eps ln 3) - 4 cosh(eps ln 2)` were checked against direct
  evaluation of the term and sum envelope widths at `x = 2` in 40-digit
  arithmetic (differences below 1e-40 at `eps = 0.3` and `0.01`), and
  `eps T_eps / H_eps` at `eps = 1e-3` is 0.61594, matching the stated leading
  constant `2(3 ln 3 - 4 ln 2)/(3 (ln 3)^2 - 4 (ln 2)^2) = 0.61594`, so the
  ratio is unbounded as claimed. Correct.

- Coordinator hand-check of `results/cia-fixed-switch-budget-algorithm.md`
  (R12): the complexity arithmetic is right. Subset pairs `U subset S` over
  `S subset [k]` number `3^k`, computing every `c_i(U)` costs `O(k 2^k)` per
  mode, and the boundary sets are `binomial(N-1, k-1)`, giving the stated
  `O(nN + binomial(N-1,k-1) n (k 2^k + 3^k))` with `O(nN + n 2^k)` storage;
  for two switches `k = 3` and `binomial(N-1,2)` gives `O(nN^2)` as claimed,
  and `binomial(N-1,k-1) ~ N^{k-1}` is why the result is not fixed-parameter
  tractable in the budget alone. The one-switch error formula
  `max{max_{i not in {p,q}} m_i, t - A_p(t), T - t - m_q}` is complete, which
  the note does not spell out: the two omitted terms are always dominated,
  because `sum_i A_i(t) = t` gives `A_q(t) <= t - A_p(t)` and
  `sum_i m_i = T` gives `m_p - t <= (T - t) - m_q`. Correct.

- Coordinator structural check of
  `notes/pooling-all-product-contracts-quasipolynomial.md` Section 5 (N10):
  the composition step is sound, and the step that matters is stated
  correctly. All components share only the single parameter `q`, so their
  partitions are overlaid by taking the union of breakpoints rather than a
  product of cells, which is what keeps the intersection quasipolynomial
  instead of exponential; the cycle handling (open the cyclic sequence at one
  arc variable, then append the diagonal equation `x = z` and its opposite)
  adds only constantly many rows. The quasipolynomial factor itself comes from
  the cited one-parameter path theorem, which was not re-derived here. The
  note also records that this result is superseded for its physical class by
  a polynomial proof.

- Coordinator hand-check of the ETR-INV to resistive-power-flow gadgets in
  `results/ac-power-flow-existential-reals.md` Section 3 (R5): every pinned-bus
  equation was recomputed. The complement bus gives `V_a + V_b = 5/2`; the
  addition bus gives `z = x + y` from
  `(1-x) + (1-y) + (1-(5/2-z)) = 1/2`; the inversion chain gives `V_I = x` at
  `C_I`, then `x[(x - V_W) + (x - 1)] = -1` so `V_W = 2x - 1 + 1/x`, and the
  `D` equation `(1 - V_W) + 2(1 - (5/2-x)) + (1 - (5/2-y)) = -5/2` reduces to
  `y = V_W - 2x + 1 = 1/x`, hence `xy = 1`. The auxiliary range is right:
  `2x - 1 + 1/x` on `[1/2, 2]` has minimum `2 sqrt 2 - 1` at `x = 1/sqrt 2` and
  maximum `7/2` at `x = 2`, both inside `[1, 4]`. The free-injection bound
  `4 * 3 * 2 * (7/2) = 84` follows from the stated voltage, degree and
  conductance caps. Correct.

- Coordinator hand-check of the suppression counting in
  `results/potential-flow-bounded-block-rank.md` (R4, the theorem whose
  general-law reuse is questioned in m9): in a biconnected block every degree
  is at least two, so `sum_v (deg v - 2) = 2m - 2n = 2 r_H - 2` bounds the
  number of degree-three-or-more vertices by `2 r_H - 2`, giving `|K| <= 2 r_H`
  after adding the two terminals; suppressing degree-two interiors preserves
  cycle rank, so the suppressed multigraph satisfies `r_H = p - |K| + 1` and
  `p = r_H + |K| - 1 <= 3 r_H - 1`. The rank-one specialization gives
  `K = {a, c}` and `p = 2`, the two terminal branches, as stated. Correct.

- Coordinator hand-check of `results/positive-multilinear-gap.md`, the
  hull-gap reduction and the dyadic construction (R6): the block identity
  `sum_{B in P_j} A_j prod_{i in B} Z_i = A_j (2^j - N_j)` is right because the
  product indicates a block with no failed leaf, and disjointness of the
  blocks gives `N_j <= min(2^j, R)`. The rearrangement step is the standard
  one: for nondecreasing `g` and binary `A` with `P(A=1) = u`, the maximum of
  `E[A g(R)]` is the upper `u`-tail, and taking `A_j = 1[U <= u_j]` with a
  single uniform `U` and a nonincreasing quantile `r` makes all anchors
  simultaneously feasible, giving (2). The bit-reversal construction is
  correct: the first `j` bits of the reversal of `k` are the reversal of
  `k mod 2^j`, so the first `R` strings in bit-reversal order hit exactly
  `min(2^j, R)` blocks at every level at once, and a uniform bitwise XOR shift
  permutes blocks within each level, preserving those counts while giving each
  leaf failure probability `R/m`. Correct.

- Coordinator hand-check of `results/network-simplex-series-parallel-coefficient-growth.md`
  Section 3 (R21): the Fibonacci incidence construction was verified entry by
  entry. With `alpha_{P_i} = F_i`, `alpha_{H_0} = gamma - 1`,
  `alpha_{H_i} = gamma - F_i` and `gamma = F_{q+1}`, every column has weight
  exactly `gamma`: `(gamma - 1) + F_1 = gamma` and `(gamma - 1) + F_2 = gamma`
  since `F_1 = F_2 = 1`; `(gamma - F_i) + F_i = gamma`;
  `(gamma - F_i) + F_{i-1} + F_{i-2} = gamma` by the recurrence; and
  `F_q + F_{q-1} = F_{q+1} = gamma`. The matrix is square (`2q - 1` rows and
  `2 + 2(q-2) + 1 = 2q - 1` columns) and invertible: the first two columns force
  `eta_{P_1} = eta_{P_2}`, the paired columns of (7) give the Fibonacci
  recurrence so `eta_{P_i} = F_i c`, and the last column forces
  `F_{q+1} c = 0`. The complement satisfies `C^T alpha = (sigma - gamma) 1 > 0`.
  Correct, and it gives coefficient growth like `phi^{N/2}`.

- Coordinator hand-check of `notes/research-20260912-dag-psd-approximation-set.md`
  Section 4 (N1, the theorem behind the 124-module Lean topic 21): the span
  claim follows because the kernel of a sum of positive semidefinite matrices
  is the intersection of the summands' kernels; the maximum-volume basis gives
  `|x_i| <= 1` by the column-replacement argument; with `1 <= tau_i^2 w_i < 4`
  the transformed coordinates satisfy `|(TB x)_i| = tau_i sqrt(w_i) |x_i| < 2`,
  so a matrix with at most `p` factors has transformed diagonal below `4p`;
  the floor-rounding residual bound `0 <= sum A - h sum floor(A/h) < N h` is
  right, so two paths with equal integer sums differ entrywise by less than
  `N h`, and for a symmetric `r x r` matrix that gives
  `||Delta||_2 <= r N h = eta` with `h = eta/(rN)`; finally `A(P) >= I_r`
  turns `-eta I <= Delta <= eta I` into the two-sided relative sandwich (10).
  The singular-range remark is also correct: `aa^T` and `bb^T` with
  `a = (1,0)`, `b = (1,t)` have different kernels, so neither dominates a
  positive multiple of the other however small `t` is. Correct.

- Coordinator hand-check of `results/cia-exact-two-switch-worst-case.md` (R12):
  the first-block inequality `x + (n-2) y >= nE` follows from the mode
  allocations summing to `y` together with `A_i(y) <= y - E` for every mode
  whose first-block reach is at most `y` and `A_max(y) <= x - E` by
  monotonicity. The displayed identity that upgrades it to (2) was verified
  term by term: `(n/(n-1))[x + (n-2)y] + ((n^2-3n+1)/(n-1))(x-y)` collects to
  `x (n-1)^2/(n-1) + y = (n-1)x + y`, and its last coefficient is nonnegative
  exactly when `n^2 - 3n + 1 >= 0`, that is `n >= 3` as stated, so
  `(n-1)x + y >= n^2 E/(n-1)`. Correct.

- Coordinator hand-check of the two arithmetic gadgets in
  `results/pooling-existential-theory-of-reals.md` (R9, Sections 4.4-4.7),
  closer than the earlier pass: the inverse pools give `w_{R_v} = 1/(vB)` and
  emissions of value `v`, and `w_{R̄_v} = 1/((5/2 - v)B)` with emissions
  `5/2 - v`, so the emission cap of 2 enforces exactly `1/2 <= v <= 2`. In the
  inversion gadget the terminal is saturated at `5/2`, forcing
  `x_{P_x t} = y`, and its quality row `w_{P_x} y + w_{p_c}(5/2 - y) = 1/B`
  collapses to `(x/B) y = 1/B` because `p_c` carries only quality-zero inflow,
  giving `xy = 1`. In the addition gadget `w_{p_+} = 0` gives
  `x_{p_+ t} = x + y`, saturation gives `x_{R̄_z t} = 5/2 - x - y`, and the
  quality row with `w_{R̄_z} = 1/((5/2 - z)B)` forces `x_{R̄_z t} = 5/2 - z`,
  hence `x + y = z`. Capacities are consistent (`x + y <= 4` on `p_+`,
  `5/2 - z in [1/2, 2]`, terminal inflow exactly `5/2`, slack `B - 2M = 3 > 0`,
  diluent `B - 1/v >= 0` for `B >= 5`). Correct.

- Coordinator hand-check of `results/fbbt-doubly-exponential-convergence.md`
  (R20): the circuit identities were re-derived (`c_i = c_{i-1}(1 + b_{i-1}) =
  1 - b_{i-1}^2 = 1 - b_i` from `c_0 = b_0 = 1/2`, so `b = 2^{-2^n}`), the
  variable count `2 + 4n + 2 = 4n + 4` checks, and `z = b + cz` with `b > 0`
  forces the unique point `z = 1`, `w = c`. The invariant `0 <= l_w <= c l_z`
  survives every primitive update: the reverse affine bound needs
  `l_z - b - c l_z = b(l_z - 1) <= 0`, and the forward affine update gives
  `l_z <- b + c l_z` because `b + c l_z >= l_z` exactly when `l_z <= 1`. The
  induction then yields `l_z <= b(1 - c^K)/(1 - c) = 1 - (1-b)^K <= K b`, so
  `l_z >= 1/2` needs `K >= 1/(2b) = 2^{2^n - 1}`, the stated bound. The
  monotonicity transfer from the exactly-initialized run to the unit-box run
  is in the right direction. Correct.

- Coordinator hand-check of `results/spatial-bb-relative-gap-exponential-lower-bound.md`
  (R19, full proof this time): the pruning inequality was re-derived,
  `G K + sum|R_b|/(2 q0) + G eta >= (1-theta) G (K + 1/4)` rearranges to
  `sum |R_b| >= 2 q0 G tau` with `tau = 1/4 - theta(K + 1/4) - eta` exactly as
  stated; the witness-fraction bound uses
  `min((2/3)^{|A_b|}, (2/3)^{|D_b|}) <= (2/3)^{|R_b|/2}` because
  `max(|A_b|,|D_b|) >= |R_b|/2`, and multiplying over independent blocks gives
  `(2/3)^{q0 G tau}`, so the cover needs `(3/2)^{q0 G tau}` leaves; the tensor
  step is valid (a principal submatrix of a tensor product of PSD localizing
  matrices, restricted to index tuples of total degree at most `d`, has
  quadratic form `L[g p^2]`, and `deg(g) + 2d <= 2r` keeps every entry inside
  the functional's domain). The worked example checks out:
  `q0 = t - 2r + 2 = 2`, `tau = 1/4 - (1/32)(11/4) - 1/32 = 17/128`, and with
  `n = 3tG = 6G` the exponent is `17n/384`. The symmetry-breaking coefficients
  `d_{b,i} = eta[(b-1)3t + i]^2/(3t n^2)` are positive, distinct, and sum to at
  most `eta` per block (largest is `eta/(3t)`). Correct.

- Coordinator hand-check of `results/positive-cubic-rounding-upper-bound.md`
  (the 31/12 headline of the rewritten `paper-cubic-gap`): the maximal-deficiency
  identity `T = u - max(0, u+v+w-2) = min(u, (1-v)+(1-w))` was verified in both
  branches, and the inclusion-exclusion floor `E[prod X] >= max(0, u+v+w-2)`
  that makes `T` the largest achievable deficiency was re-derived. Case "at
  least two low coordinates": `u, v <= 1/2` forces `u + v + w <= 2` so `T = u`;
  in the endpoint-orientation law the two low coordinates take disjoint
  intervals whenever their orientations differ, which happens with probability
  1/2 and contributes zero to the product, giving `D_O >= u/2`; independent
  rounding gives `D_I = u(1 - vw) >= u/2`; the mixture weights then give
  `(18 + 6) u / (2 * 31) = 12T/31`. The bilinear cases were checked the same
  way: both low gives `T = u` and `D_I = u(1-v) >= T/2`; exactly one low gives
  `D_B = min(u, 2(1-v))/2 >= T/2` because `2(1-v) >= 1-v`; both high gives
  `T = 1-v`, `D_I = u(1-v) = uT >= T/2`, and each case clears `12T/31`. The
  optimality weights `3/31 + 4/31 + 24/31 = 1` are consistent. Correct.

- Coordinator evidence check of the row-hull solver counts quoted in
  `README.md:36-37` and `results/row-hull-separable-concave.md:78-79`
  ("96 to 124 of 130 for Gurobi 13, 18 to 41 of 44 for SCIP 10, 15 to 44 of 50
  for BARON"), recomputed from `code/row_hull/results/main_gurobi.jsonl` and
  `main_others.jsonl`: Gurobi gives exactly 96 and 124 of 130; SCIP gives 18
  and 41 once the 6 instances where a run errored are dropped (44 remain) and
  a within-tolerance `gaplimit` finish counts as solved; BARON gives 15 and 44
  of 50 only because the note excludes `netflow-random-log-40n3d-s4`, where
  BARON returns status optimal at 72.9288 although the best known value is
  66.864. That exclusion is justified and disclosed: the experiment record
  (`notes/row-hull-experiments.md:153-154`) flags it as a VIOLATION and the
  per-family table sums to 15 and 44. Counting naively without the exclusion
  would give 16. The quoted figures are correct as published.

- Coordinator hand-check of `notes/common-factor-p-split-rotation-gap.md`
  (N8): the witness lift was verified (`p = (2D/3, D/3)`, `a_i = p_i^2`,
  `b_i = (p_i - D)^2`, and `(a,b) = 1/2 (0, 2b) + 1/2 (2a, 0)` with
  `2a_i, 2b_i <= 8D^2/9 <= (D+1)^2`, so both mixture points satisfy their
  disjunct and the global bounds); `dist(p, C) = D/(3 sqrt 2) - 1` because the
  projection `(D/2, D/2)` lies on the center segment. For the rotated model,
  `a + c <= 1` and `b + c <= 1` each force `c <= 1`, an inequality valid on
  the convex hull, so `w^2 <= c <= 1`; for `t <= 0` the diamond gives
  `-t + |w| <= sqrt 2`, hence `t^2 + w^2 <= (sqrt2 - rho)^2 + rho^2 <= 2` with
  the maximum 2 at `rho = 0` and `4 - 2 sqrt 2` at `rho = 1`, so the distance
  to the capsule is at most `sqrt 2 - 1`; the `t >= d` case is symmetric. The
  rational version was checked too: `p = (2D, 4D/3)` satisfies
  `p_i, v_i - p_i <= 2 v_i/3` with equality in one coordinate each,
  `t(p) = 34D/15 in [0, 5D]`, `w(p) = 4D/5`, and the inverse-map bounds
  `x_1 <= 4/5`, `x_2 <= 3/5` (resp. `h_1 >= -4/5`, `h_2 >= -3/5`) give
  `t^2 + w^2 <= 2`. Correct.

- Coordinator hand-check of `results/cia-arbitrary-switch-global-bound.md`
  (R12 headline): the plateau factorization was verified by expanding both
  sides, `C_{n,k} - 1/(k+1) = [2n^2 - n(k+1)(k+2) + k(k+1)^2] / [n k (k+1)(2n-k-1)]`
  and `2(n-k-1)(n - k(k+1)/2) = 2n^2 - n(k+1)(k+2) + k(k+1)^2`, so the stated
  numerator is exact; it is nonpositive precisely on `k+1 <= n <= k(k+1)/2`,
  giving `F = T/(k+1)` there, and the matching lower witness (k+1 pure blocks,
  at most k distinct modes usable) is valid. The quoted instances
  (T/6 for n = 6..15, T/7 for n = 7..21, T/11 for n = 11..55) follow. The
  asymptotic expansion of the uniform-control coefficient was re-derived to
  second order: with `x = 1/(n-1)`, `n((1+x)^k - 1) = k(1+x)[1 + (k-1)x/2 +
  (k-1)(k-2)x^2/6 + ...]`, whose reciprocal gives
  `1/k - (k+1)/(2kn) + (k^2-1)/(12kn^2) + O(n^-3)` exactly as stated
  (the `n^-2` coefficient reduces to `(k+1)(k-1)/12`). Correct. The bound (1)
  itself rests on the universal heavy-mode and arbitrary-block one-sided
  theorems, which are separately reviewed and were not re-derived here.

- Coordinator hand-check of `results/cia-uniform-switching-obstruction.md`
  (R11, the uniform-control lower bound left unchecked earlier): with
  `r = n/(n-1)`, the recursion `t_j <= r t_{j-1} + rE` follows from
  `(t_j - t_{j-1}) - t_j/n <= E`, and iterating gives
  `T <= rE (r^m - 1)/(r - 1) = nE(r^m - 1)` because `r/(r-1) = n`; with
  `m <= s+1` this is the stated bound. The attainment construction was
  verified exactly: for `t_j = T(r^j - 1)/(r^m - 1)` the selected mode's
  discrepancy at its block end is `t_j/n - (t_j - t_{j-1}) = -T/(n(r^m-1)) = -E_0`
  (using `r^{j-1}(r-1) = r^{j-1}/(n-1) = r^j/n`), positive discrepancies never
  exceed `T/n`, and post-block discrepancies rise from `-E_0` by at most
  `(T-t_j)/n`. The specialization `E_{n,1} = T max{1/n, (n-1)^2/(n(2n-1))}`
  follows from `r^2 - 1 = (2n-1)/(n-1)^2`, the `n = 5` value is `16T/45 > T/3`,
  and `n(r^{s+1}-1) -> s+1` gives the stated limit `T/(s+1)`. Correct.

- Coordinator Lean-fidelity check of topic 20 (L8) against
  `results/quadratic-rank-integer-complexity.md`: `HasPrecisionRate feasible r`
  unfolds to "there are `C >= 0` and `eps0 > 0` such that for every
  `0 < eps <= eps0` the minimum feasible count `p` satisfies
  `|p - (r/2) log2(1/eps)| <= C`", which is exactly the note's
  `p(eps) = (r/2) log2(1/eps) + O_(H,B)(1)`, with the constant allowed to
  depend on the fixed `H`, `a`, `l`, `u`, `b`. `IsMinimumCount` is a genuine
  minimum. `ConvexIntegerLift` is an arbitrary convex carrier with `p` integer
  and `q` continuous auxiliary coordinates, with no closedness, polyhedrality
  or boundedness assumption, matching the note's scope; `HasBinaryGraphLift`
  uses the polyhedral binary lift and `toInteger` shows it refines the general
  one, so the two-sided law is stated for both minima as in the note. One
  wording difference is immaterial: `IsGraphRelaxation` requires every point
  of the relaxation to have its input in the box, while the note requires the
  error bound only at points with `x in B`; intersecting any note-admissible
  lift with the convex slab `{x in B}` preserves convexity, graph containment,
  the error bound and the integer count, so the two minima coincide.

- Coordinator evidence check of V1 (certified-MINLP replay campaign,
  `notes/certified-minlp-repair-and-replay.md`) against
  `code/minlp_solver_lab/results/cert_replay_20260913_complete_summary.json`:
  every headline figure reproduces exactly. The saved statuses are 188
  verified, 92 rejected, 9 missing artifacts over 289 records, with 269
  historical acceptances and 81 unrevalidated, matching the note and its
  internal arithmetic. Checker seconds (7,987.954 total, 463.845 maximum)
  and proof bytes (38,826,726,525) match. Recomputing the reference
  comparisons gives 23 records whose recorded primal lies strictly beyond
  the checked bound, the largest by 5.83e-10 in normalized magnitude, which
  matches the note's "all by less than 6e-10" and supports its reading that
  these are reference-rounding effects rather than invalid bounds. The
  discrepancy audit artifacts for `clay0204m` and `risk2bpb` exist and carry
  the exact residuals the note describes.

- Coordinator hand-check of the certified-MINLP soundness contract (V1,
  `notes/certified-minlp-soundness.md` and `notes/certified-minlp-vipr-replay.md`):
  the bound-propagation step (`c_k x_k <= u - Rlo`, integer rounding, `F ⊆ B`
  by induction), the safe-cut derivation (`r(x) - a x >= phi(z) + d (x-z)`
  with `d = p + ell - a`, recomputed; `d_j(x_j - z_j) >= -W_j`; hence
  `a x + b <= r(x)` under (2)), every row of both `W_j` tables (finiteness
  conditions `d_j >= 0` on `[L, inf)`, `d_j <= 0` on `(-inf, U]`, `d_j = 0`
  on the line; the conservative rational `What_j` using the signs
  `z_j - L_j >= 0` and `z_j - U_j <= 0`), the two nonsmoothness
  counterexamples (`-sqrt(x)` at 0; `-sqrt(xy)` with zero axis derivatives at
  the origin failing support at `(1,1)`), the master-to-original transfer
  (`E(x)` feasible with objective `h(x)`, so (3) gives `L <= inf_F h`), and
  the VIPR replay soundness induction (assumption/linear/rounding/unsplit/
  solution rules with `S = {feasible master points with objective <= b}`;
  points outside `S` have objective `> b >= L`) were re-derived: correct.
  The notes state their trust boundary explicitly (Python execution, exact
  arithmetic library, file integrity, and the separate master-equivalence
  and nonlinear-cut checks).

- Coordinator evidence check of V2 (LB-ESH claim register,
  `notes/lbesh-claim-evidence.md`) against the saved runs: every headline
  numerical claim reproduces exactly from the archived records. Held-out
  solves recomputed from `analysis_legacy_v2/records.csv` give ESH hull
  single 33/33, ECP hull single 32/33, ESH big-M single 33/33, ECP big-M
  single 31/33, matching the results table; the conic baseline is 9 of 9
  solved with shifted wall mean 0.455 s against 2.280 s for ESH hull single
  on the same nine instances; the NLP-disabled ablation is 1 of 72 solved
  against 69 of 72 for the matched primary runs (recomputed by pairing each
  `-nonlp` record with its base method); the frozen conic roots are 40
  `Solved` and 2 `AlmostSolved`, matching "40 optimal and two optimal
  inaccurate"; the 14 enumerations hold 27 assignments each, 378 solves
  splitting 174 optimal and 204 infeasible with a witness on every optimal
  one. The register's hedges (no novelty, no causal decomposition, numerical
  not certified) are consistent with what the artifacts support. Only m36
  was found.

- Coordinator hand-check of `results/fixed-parameter-linear-fibers-np-membership.md`
  (R10): the vertex/independent-active-rows certificate, the squared
  determinant system (V), the degree and monomial-count bounds
  (`O(nd)`, `O((nd+1)^r)`), and the appeal to fixed-dimension existential
  theory of the reals were checked: correct.

- Coordinator hand-check of `results/pooling-two-source-qualities-convex-feasibility.md`
  Sections 1-5 (R10): the signed scaling (2), identity (3) from the output
  mass and quality rows, identity (4) (`W_0j = q b_j (B_j - 1) + q(1-q) v_j`,
  re-derived by eliminating `W_1j`), the outlet bounds (5)/(5a), the
  automatic pool quality balance `Y_1 = q (Y_0 + Y_1)` obtained by summing
  (3) and using (1), the `r >= q^2` replacement (6)-(7) with `U_j >= 0`,
  and the exact endpoint procedure (unique `q*` when `m = 0` by the strict
  midpoint argument; `lambda = rho/(2(rho+1))` gives `F <= -rho/2` and an
  interior `q`) were re-derived: correct. Section 6 (supply intervals): the
  class constants (8), rows (10)-(11), and the recovered pool quality
  balance `sum_i h_i = 0` were also re-derived: correct.

- Coordinator hand-check of `results/bilevel-well-conditioned-box-exact-hardness.md`
  (R14): the ReLU network (piecewise maps of `[0,1/3]`, `[1/3,2/3]`,
  `[2/3,1]` into `[0,1]`, `y_i - p_i = min(y_i, 1-y_i)`, residual
  `0 <= rstar <= 2`, coefficient bound `C = 2*3^n`), the scaling
  (`|B_ij| <= C theta^(i-j)`, `||B||_1, ||B||_inf <= 1/50`, hence (4); `Q`
  entries `< 2`, `c, d` entries `< 1`), the projected-gradient fixed point
  `u = clip(Bu + S(b_0 + x b_1) + B^T r)`, the componentwise error system
  (5) with `U = S^(-2) P^T S^2`, the bounds `||T||_inf <= M`,
  `||U||_inf <= 2C theta^2`, the contraction `2MC(1+NC) theta^2 < 1/2`,
  the error (6) `8MC theta^2 = 1/(1250 N^2 C M)`, the objective coefficient
  bound `delta/s_i <= 1`, the gap (7) `delta * 2N/(16N) = delta/8`, and
  `log(1/delta) = O(N^2 log(NC))` were re-derived: correct.

- Coordinator Lean-fidelity check of topic 31 (`formal/Formal/InfiniteAggregation/Accuracy.lean`)
  against `notes/research-20260922-aggregation-accuracy.md` Theorem (1):
  `optimalError_bounds` states `sqrt 2 (log 2)^2/(1600 N^2) <= e_N <= 5 sqrt 2 pi^2/(16 (N-1)^2)`
  for `r >= 2`, `N >= 2` with exactly the note's constants; `optimalError` is
  the infimum of the extended Euclidean Hausdorff distance (in `R^(2r)`)
  over `admissibleFamily` finsets of card at most `N`; `closedRegion` is the
  note's set `C`; `good_iff_goodCone` shows the admissible multipliers are
  exactly the note's `K \ {0}`; `optimalError_theta` is `Θ(1/N^2)`. The
  formal statement matches the informal theorem. (The witness Gram matrix
  of the lower bound, values (3) and determinant `>= 12/25`, also checked.)

- Coordinator hand-check of `notes/certified-positive-polynomial-inverse-approximation.md`
  (N9): the elementary bounds and (2), the zero-branch threshold
  (`z <= t^(1/P) <= 2^(-m)`), the derivative perturbation (3)
  (`(1+1/(4P))^(P-1) - 1 < e^(1/4) - 1 < 1/3`), the Rouché margin
  (`1/3 + 1/2 = 5/6 < 1`, using `t_0 <= z_0 g'(z_0)`), the panel geometry
  (6)-(7) (`|t - t_0| <= tau/(32P)`, ratio `16/63 < 1/2`), the recursion (8),
  the denominator law (9), the Cauchy bound (10), the truncation error (11)
  (`2^(1-q) = 2^(-m-2) <= eta/4` with `q = m+3`), the branch count
  `32 P^2 m`, and the follower-cost transfer (derivative `g(z) - ell`) were
  re-derived: correct.

- Coordinator hand-check of `results/bilevel-fixed-block-response-algorithm.md`
  (R13): the block KKT reduction (the full-problem gradient in `z_b` equals
  the gradient of the strictly convex local QP (1), so each block is the
  unique local minimizer for its compressed `v`), nonsingularity of (2),
  the squared-determinant denominator, completeness of the independent
  active-subset enumeration (Carathéodory reduction in the quotient by the
  equality rows; `O(m_b^d)` subsets), the first-valid-branch rule, the
  fixed-dimensional sign-condition enumeration and quantified comparison
  (KKT is necessary over a polyhedral follower set, so the minimum-value KKT
  point is the global follower minimizer), and the Hoffman-bound closedness
  argument were checked: correct, given the fixed-dimension quantifier
  elimination complexity results it cites through the scalar theorem.

- Coordinator hand-check of `results/pooling-triviality-polynomial.md` (R10):
  Lemma 1 (head-evaluated destination probabilities `h_j`, conservation
  `h_j(v) F_v` on both sides, quality mass `p_vk h_j(v) F_v`, capacities by
  `0 <= y^j <= y`, and `y = sum_j y^j`), Lemma 2 (mass cancellation and the
  topological quality assignment; `t_j = 0` forces the zero flow in a DAG),
  the chains `z* <= z_best <= z*/m` and `z_rel <= z* <= z_best <= z_rel/m`,
  Theorem 2 (path decomposition gives cost per unit `>= sum delta_ij gamma_i`;
  converse by shortest paths plus scaling on the positive-capacity graph;
  vertex support `<= K+1`), Theorem 3 (`conv(S) = cone(S) = sum_j C_j`,
  `cone(P) = conv(S)`), and the two-output strict example were re-derived:
  correct.

- Coordinator hand-check of `results/polynomial-graph-binary-integer-degree-gap.md`
  (R17): the Bernstein bound (1) (`2M sqrt(x(1-x)/N) <= M/sqrt N = 1/32`),
  the exact projection of the two-branch period encoding onto the graph of
  `T_M` (including `t = 1/2` and period boundaries), the admitted error
  `1/16 < 1/4`, the convex-slice chord obstruction at troughs (error
  `>= 30/32`), hence `p_bin >= ceil(log2 M)`, the degree bounds (`>= 2M`
  by sign changes, `<= 1024 M^2`), the piece counts `s <= max(1, D-1)` and
  `b <= 2D`, the chord error `2 M_1 h <= ε/16`, and the final count
  arithmetic in (4)-(6) were re-derived: correct. The cross-referenced
  `3 * 2^p` cell bound and the hybrid theorem's `p + 11` local count were
  taken from their own reviewed notes and not re-derived here.

- Coordinator hand-check of `results/positive-polynomial-loglog-degree-precision.md`
  (R17): the supporting scalarization (KKT with a nonnegative normal
  `lambda`, the zero-row adjustment via `h_K(lambda) = h_K(|lambda|)`, and
  the concavity argument that (4) has the same optimum), the convexity of
  `g_i = sqrt(phi_i)`, inequality (5), the Jensen-error bound
  `(1/4) sum A_i (t_i - s_i)^2 <= h_K(lambda)`, the covariance-volume step
  (ball-minimal determinant `(V/omega_r)^2/(r+2)^r`, Hadamard, caps
  `Sigma_ii/2 <= 1/8`), the constant `A_r < 7r/2` (checked for `r = 1, 2`
  and asymptotically), the layer curvature bound (6) (`(v+1)^2 e^(-v) <= 4/e`
  at `v = 1`; final layer `k(k-1)/D^2 < 1`), the implied-binary selector
  logic, the Taylor rectangle `0 <= f_j - T_j <= (Cp)_j` with
  `h_i^2 <= p_i`, and the counts (1)-(2) (`1/(2 ln 2) < 1`) were
  re-derived: correct.

- Coordinator hand-check of `results/quadratic-integer-precision-approximation-hardness.md`
  (R16): the zero-dimension lemma (`p = 0` iff `M(G) <= ε`, via the LP
  `0 <= w <= ε` and the midpoint `((1/2)1, M(G))`), the `2^t`-point parity
  packing giving `p >= t`, the exponent arithmetic
  `C (tn)^(1-δ)/t = C n^(1-δ-qδ) < 1` for `q > 1/δ`, the tolerance-one
  normalization, and the positive-minimum gadget `8z^2` (one-binary
  formulation `w = 2(β + 2βr + s)` with `max(0, 2r-1) <= s <= r`, residual
  `|s - r^2| <= 1/4`, output error `<= 1/2`; midpoint obstruction error 2)
  were re-derived: correct.

- Coordinator hand-check of `results/bilevel-scalar-leader-spd-box-np-completeness.md`
  (R14): the whole reduction was re-derived: the identity `r_i(x_b,b) = b_i - 3t_i + 1`
  and the residual ranges `[1/(2*3^(n-i)), 1]` and `[-1, -1/(2*3^(n-i))]`;
  the cross-term bound `6 rho/(1-3 rho) < 1/(10*3^n)` and the strict sign
  margin (1) (`1.4 w_i/3^n > w_i/3^n`); the conditional minimizers (3) for
  `p`, `v` and the identity `y_i - p_i = min(y_i, 1-y_i)`; the feedback bound
  `2 eta + 2 m xi < 4 eta = w_n/(25*3^n)`; the value identity (4); the
  unsatisfiable-case rounding argument (`ell_a(y) <= D(y)` for a false
  clause with distinct variables, hence `F >= 2`); `x_b in (0,1)`; the
  polynomial bit lengths (`rho^(n-1)` has `O(n^2)` bits); and NP membership
  via a guessed active set with affine-in-`x` stationarity. Correct.

- Coordinator hand-check of `results/quadratic-rank-integer-complexity.md`
  (R15 headline, Lean topic 20): the geometric lemma (maximal simplex gives
  `S ⊆ s_0 + A[-1,1]^d`; Gram entries `|G_ii| <= 2δ`, `|G_ij| <= 3δ`, row
  norm `<= 3 sqrt(d) δ`, Hadamard with `det G = (det A)^2 det M`), the
  parity-class midpoint step (lifts of exact graph points, so the midpoint
  deviation is exactly `q(s-t)/4`, giving `|q(s-t)| <= 4ε`), the constant
  `c_I = |det H_I|^(1/r) V_I^(2/r) / (48 sqrt r)` (12 times 4), the
  restriction to a nonsingular principal `r x r` submatrix (exists since the
  sum of principal `r`-minors is the product of the nonzero eigenvalues), and
  the sawtooth upper bound (`A 2^(-2L-2) <= ε` iff `L >= (1/2) log2(A/(4ε))`,
  `rL` binaries) were re-derived: correct. The one-sided (epigraph) variant's
  slicing argument along the negative eigenspace was checked in outline only.

- Coordinator hand-check of M4 (`research-20260922/iterated-obbt/theory.md:40`)
  against `literature/papers/scott2011-generalized-mccormick-relaxations/fulltext.md`:
  Remark 2 states verbatim that Step 6 (clipping each factor relaxation to
  its interval bounds) "is necessary for Lemma 1 below, which is in turn
  required for many results in later sections (Sect. I of Online Resource 1
  contains examples where omitting this step results in violations of Lemma 1
  and Theorem 4)"; the proof of Theorem 4 uses `mid(v^L, v^U, vbar) = max(v^L, vbar)`.
  The note's composite rule (`proofs-12-11.md` lines 62-86) is the unclipped
  MCB 2009 rule. The finding stands at the citation level.

These are line-by-line re-derivations by the coordinating agent during the
account-limit pause. "Correct" means no error was found in the listed
steps; it is not a claim about steps not listed.

- Coordinator hand-check of the flagship aggregation theorem
  (`results/quadratic-aggregation-trivial-hull-certificate.md`, Theorem 1,
  Sections 3.1-3.3): the easy direction, Lemmas 1-3, the hyperplane
  separation in Step 1, the simplex-limit argument in Step 2, and the
  uniform-separation contradiction in Step 3 were re-derived and hold.
- Coordinator hand-check of `research-20260922/iterated-obbt/theory.md`
  Sections 1-4: Lemma 1, Propositions 2-3, Theorem 4, Theorem 6, the exact
  two-variable rate `(sqrt(2a^2+4a)-a)/2` (McCormick estimators, the
  minimizing `s`, the branch comparison, and the `a<2` condition), and the
  row-condition stall (Proposition 8 and the strongly convex example) were
  re-derived and hold.
- Coordinator hand-check of `research-20260922/ridge-envelopes/theory.md`
  Theorem 1 (Steps 1-4) and Corollary 2, including the order-polytope
  down-set argument and the mixed-sign counterexample: correct. Two
  expository imprecisions (minor, tracked as m12).
- Coordinator hand-check of `research-20260922/benchmark-observations/nuclear-bounds.md`:
  the (K) burnup monotonicity and beginning-of-cycle bound for F1/F2/F3,
  the Collatz–Wielandt bound (CW) with `phi_T != 0` from the normalization,
  the peaking-aware bound (P) including the division step, and the
  validity of the four solver cuts (per-period CW cap and total-burn
  equality) were re-derived and hold. Certified values were not recomputed,
  but all 18 "proven bound" table entries equal the smaller of the saved
  `bound_lamT` and `bound_peak` values in `nuclear_cw_bounds.json` rounded
  up at six decimals, and `code/nuc_verify.py` computes the bounds with
  `fractions.Fraction` (minor nit m15: the JSON stores those certified
  rationals as floats, so the archived certificate values are not exact).
- Coordinator hand-check of `research-20260922/benchmark-observations/structural-bounds.md`:
  the Yudin bound derivation, the `g(s) >= 0` reformulation and the
  `delta`-shift cost, the 0/1-to-±1 determinant reduction, and the
  numerical values of the Hadamard, Barba, Ehlich (`Dpm(7)^2 <= 344064`)
  and Ehlich–Wojtas bounds (32, 65, 9, 144) were recomputed and agree.
- Coordinator hand-check of `results/four-aggregation-strict-pdlc.md`:
  Lemma A (countable exceptional levels), Lemma B (no points at infinity,
  boundedness, persistence of PDLC, generic independence, `C_eps = cl(S_eps)`),
  Lemma C (strictification via the local-maximum argument and finite
  interior intersections), Lemma D (closedness of the one-negative-eigenvalue
  set, eigenvector orientation and the strict limit, the converse by
  convergence), the dependent-triple remark, and the sharpness table (all
  four witness rows recomputed, including the radical roots `alpha`, `beta`)
  hold. The literal-set form of the statement matches the
  Blekherman–Dey–Sun convention (`S_lambda = {x : f_lambda(x) < 0}`, checked
  in the local full text). The external input (Blekherman–Dunbar Theorem
  1.4) is used with the hypotheses the repository transcribes: the arXiv
  text (2405.18282v1, fetched 2026-09-24) states Theorem 1.4 for PDLC
  triples with `S = cl(int S)`, `int S` nonempty and no points at infinity,
  concluding `cl conv(S)` equals an intersection of at most four literal
  sets `{f_lambda <= 0}` over good aggregations, with no dimension
  restriction. The note additionally assumes linear independence, which
  it arranges by a generic perturbation, so the input is used within its
  hypotheses either way.
- Coordinator hand-check of `results/separable-vertex-binarization.md`
  (Theorem 1 vertex/rank argument without continuity, Corollary 2, the
  `2n+1`-node branch-and-cut of Theorem 3 with both rounding cuts) and of
  `results/composite-univariate-envelopes.md` (Proposition 1 piecewise
  bounds, Proposition 2 biconjugate form, Example 4 values `-n`, `-n/4`,
  `3n/4`, `1/4`): correct. Proposition 3 is quoted as "the sum of the
  `min(m,n)` largest defects"; Udell–Boyd Theorem 1 (arXiv 1410.4158,
  text extracted 2026-09-24) gives the sum of the `min(m~,n)` largest with
  `m~` the maximal number of active linear constraints, which is at most
  `m`, so the quoted form is valid.
- Coordinator hand-check of `results/indicator-quadratic-treewidth-two-hardness.md`:
  Theorem 1 (Hessian entries and Gershgorin bounds, the telescoped identity
  (6), the Cauchy–Schwarz constant `D_{n,theta}`, the bound `1/D > delta_theta`,
  NP membership via rational support QPs) and Theorem 3 (rows of the
  `(e,d)` quadratic form for (13), state activation (14) with `D = 4`, the
  exact threshold `n`, the linear-coefficient bounds `|c_j| <= 9`, and the
  gap identity (16)) were re-derived and hold.
- Coordinator hand-check of `results/infinite-quadratic-aggregation-hhc.md`
  Sections 1-3: the Gram-matrix range argument and nuclear-norm formula (1),
  convexity of (2) via concavity of `sqrt(det G)`, the block structure (4)
  and the good cone `K`, the witness Gram matrices (5) (diagonals and
  determinant bounds), the AM-GM equality case identifying the ray
  `(tau, 1/tau, 2)`, and the closed-hull perturbation (`2 eta > 0`) hold.
- Coordinator hand-check of `results/cluster-free-branch-and-bound-constrained-minima.md`:
  Theorem 1 (Steps 1-6, including the Lagrangian identity, the LICQ
  normal-component bound, the cross-term constant `M'`, and the choice of
  `rho`), the Theorem 2 packing count `(4 sqrt(c_2/c_1) + 4 sqrt(n))^n`,
  Theorem 3, the corrected αBB neighborhood counterexample (`g = q + t^2 +
  s(5b+t-s)`, `mu* = 1`, `gamma = 4 - sqrt 5`, relaxed point at
  `t = -kw/2`, gap `2bkw - k^2 w^2/2`), and the strict-complementarity
  failure example were re-derived and hold. The companion
  `notes/research-20260922-error-bound-transfer.md` Theorem 1 (`d_y^2 >=
  d^2 - 3 rho e`, constant `L_f + 3 a rho`), Corollary 1, and the SOSC-implies-
  quadratic-growth argument were also checked and hold.
- Coordinator check of the Lean statement behind the "Lean-verified" label
  of the aggregation theorem (`formal/Formal/QuadraticAggregation/Model.lean`,
  `Headline.lean`): `System` carries real symmetric matrices, `eval` is
  `x^T A x + 2 b.x + c`, `feasible` is the strict set, `Certificate` is a
  nonzero nonnegative `w` with `PosSemidef` aggregate and nonzero `(A, b)`,
  `HHC` quantifies over all nonzero linear functionals, and
  `proper_hull_iff_certificate_of_hhc` states `convexHull ℝ feasible ≠ univ
  ↔ ∃ w, Certificate w` under nonemptiness and HHC. This is Conjecture 3.3
  as stated in the note; the `m = 0` edge case is consistent on both sides.
- Coordinator check of the Lean statement behind the positive-box label
  (`formal/Formal/MultilinearGap/PositiveBox.lean`, `PositiveBoxHeadline.lean`):
  `boxAspectRatios rho` ranges over all finite index types, nonnegative
  coefficient supports, boxes with `0 < l <= u <= rho l`, and points with
  positive hull gap; `positiveBox_headline` proves `max 2 rho <=
  sSup(...) <= rho + 2` for `rho > 1`, and the lower bound is derived
  without a `BddAbove` hypothesis, so the `sSup ∅ = 0` convention cannot
  make the statement vacuous. Faithful to `max{2,rho} <= C_box(rho) <= rho+2`.
- Coordinator check of the marginal-floor Lean headline
  (`formal/Formal/MultilinearGap/FloorDomain.lean`, `FloorResults.lean`):
  `floorRatios δ` ranges over all finite index types, positive coefficient
  supports, cube points with every `x_i >= δ` and positive hull gap;
  `sharp_marginal_floor_growth` states
  `floorSupremum δ / (log(1/δ)/log log(1/δ)) → 1` as `δ → 0+` (and the
  strip version), which is the informal claim and cannot be satisfied
  vacuously under the `sSup` convention.
- Coordinator hand-check of `results/monomial-wedge-envelopes-real-exponents.md`
  Sections 1-2 and the regime table: Lemmas 1-4 (ray parametrization,
  parallel chords, the Hessian determinant `a_1 a_2 (1-beta) f^2/(x_1^2 x_2^2)`,
  the quasi-convexity classification by `kappa`), the ray function `H`
  (monotonicity of `h`, the concavity/convexity table), Lemma 5, and the
  minorant/majorant and convexity properties of each table entry (including
  the boundary behaviour of `L` outside `[s_l, s_u]`) hold. The Section 3
  exactness proofs (chord, ray and corner decompositions in all six
  regimes, the identification `Y_A ∩ {s >= s_l} = conv(T)` in I.2, the
  "beyond `s_u`" argument in II/III.B1) and the degree-zero interior
  representation of Remark 2 (weights `1-lambda, lambda`) were also
  re-derived and hold.
- Coordinator hand-check of `results/row-hull-separable-concave.md`
  Proposition 1 (vertex generation with one common convex combination),
  Theorem 2 (vertex structure `(S, j, r)`, concavity of the (RH)
  left-hand side, the `(y, zeta)` bipartite total-unimodularity argument
  and the reconstruction `z = w y + r zeta`), and Theorem 2(b) (added
  generators, elimination of `y`): correct. Proposition 3 (endpoint
  minimum of the concave gap, degenerate-case invalidity, lattice
  corollary), Proposition 5 (dual pricing identity, validity of
  `sum omega_i tau_i >= sum pi_i z_i + L` for any lower bound `L`
  independent of LP accuracy, endpoint evaluation with `gamma_j = 0`), and
  the Proposition 6 example (`(3/4, 3/4, 1/2)`, optimum `1/2`, aggregated
  rows) were also re-derived and hold.
- Coordinator hand-check of `results/smoothed-spectral-indicator-messages.md`
  Sections 1-3: Lemma 1 (Pajor sandwich inequality, the conditional
  interval argument for shattered coordinates, the `(1+2 phi a+tau)^m`
  bound), Lemma 2 (first-difference enumeration with certified lower
  bounds, inclusion (3), call count), and Theorem 3 (net transfer
  `F_z(t_j) <= F_w(t_j) + epsilon`, `E_j ⊆ A_{3 epsilon}`, the constant
  `e` from `epsilon = 1/(12 n phi)` and `N >= 2n`) hold. Sections 4-6
  (support quadratic (10) and minimizer (11), the bounds `M`, `L` in (12),
  the grid-rounding oracle guarantee (13) via stationarity, the
  polynomial dependence of `B` and `J`, and the always-valid certificate
  (14)) also hold. Section 7 onward was left to the auditors.
- Coordinator hand-check of `results/shared-variable-term-links.md`
  mathematics: the two rotated cones are exactly the degree-3 truncated
  moment (localizing Hankel) conditions on `[l,u]`, so they describe the
  hull of `(x, x^2, x^3)`; the `x^2, sqrt(x)` joint-hull example
  (`t_2 >= sqrt(1/2)` by Jensen equality) is correct; the exact residual
  `32325/2^49 ≈ 5.74e-11` is stated as tolerance feasibility only.
- Coordinator cross-check of README.md headline numbers for the
  September 21-23 work (composite envelopes 48/48, 35 of 81, 51 vs 54;
  vertex binarization `2n+1`, `n = 24`, `n = 400`; row hulls 96→124 of 130,
  18→41 of 44, 15→44 of 50, 4.8%; shared variables 5178.16 vs 5269.64,
  `5.8e-11`, 21%-130%; curve hulls 226/656/1573/3144/4442; nuclear gaps
  3-20%; elec 0.013-0.07%; hadamard_8 bound 65) against the result notes
  and research logs: consistent.
- Coordinator hand-check of `results/spatial-bb-exponential-lower-bound.md`:
  Theorem 1 (witness membership, the chord values forced by `w in B`, the
  bound `|M ∩ R| > h`, the random-partition fraction `rho`, the leaf
  count `1/rho`), Proposition 2 (middle-child constant chord, leaf bound
  via `|sum x - b| <= sum_low x + sum_high (1-x)`), the RLT+SDP root
  example of Remark 3 (row sums, eigenvalues `c-d` and `0`), and Remark 7
  hold.
- Coordinator hand-check of `results/pooling-existential-theory-of-reals.md`
  Sections 1-4.4: membership in ∃R, the forcing Lemma 4 (profit equals the
  sum of forced-group totals), the variable gadget qualities `v/B` and
  `(5/2-v)/B`, the emission Lemma 5 (`a x_{Qt} = 1`, relay flows, converse),
  the quality flip, and the inverse pools with the range enforcement
  `1/2 <= v <= 2` hold. The inversion gadget (`x y = 1` from
  `(x/B) y = 1/B`), the addition gadget (`5/2 - x - y = 5/2 - z`), the
  slack and capacity bookkeeping (`B - 2M = 3`), and the stated degree
  restrictions were also verified. Corollary 3 rests on the cited
  Abrahamsen–Miltzow rational-equivalence theorem, which was not re-read.
- Coordinator hand-check of `results/mccormick-gap-degeneracy-bound.md`:
  Step 1 (`f(s)-f(s') = 2 v^T A u`, the `∞→1` norm identity), Step 2
  (Khintchine with constant `1/sqrt 2`), Step 3b (locally maximal
  squared-weight cut), Step 3c (fractional orientation with load `rho`
  and weighted Cauchy–Schwarz), and the transfer through Boland et al.
  Corollary 1 hold; constants `4 sqrt rho`, `4 sqrt d`, `2 sqrt Delta`
  follow as stated.
- Coordinator hand-check of `results/geoffrion-property-p-conjecture.md`
  Theorem 1: membership of `x_u` in `X`, the bound `r + u/2 - u r^2`, the
  maximizer `q_u`, the value function `L*`, failure of (B) via
  `(a+b)t >= 1`, the Slater point and the subproblem value `1/sqrt 2`;
  and Proposition 2: correct.
- Coordinator hand-check of `results/fbbt-monotone-system-hardness.md`:
  the least-fixed-point lemma, the layered normalization identities
  (`r_g = r_j + p_j r_k`, `c = 1/2 + (U-V)/(2M)`), the detector roots
  (`1` and `d/c`, discriminant `(1-2c)^2`), the gap `1 - a* = 2 Delta/(M+Delta)
  >= 1/M`, the amplifier (`b <= 1/(8M)`, `z* <= bM <= 1/8`), and the
  arity, coefficient and SCC-size restrictions: correct.
- Coordinator hand-check of `results/rank-one-zero-lower-hardness.md`: the
  repair lemma (both cases, including `W_00 >= r_0 + c_0 - S` and the
  entrywise-norm identity for rank-one differences), the exact penalty
  theorem with `L > 2B`, and the reduction's threshold equivalence and
  coefficient bound `5B+2`: correct.
- Coordinator source check of the claim in
  `results/cia-five-interval-two-switch-minimax.md` that Sager–Zeile's
  published Corollary 5 is contradicted (a high-stakes claim about a
  published paper). The open final PDF (econstor copy, text extracted
  2026-09-24) defines `TV` with a factor `1/2` (Definition 1), so one mode
  switch counts one and `sigma_max` is "a maximum number of switches"
  (Definition 3); the (CIA) objective (Definition 7) is the same grid
  prefix error; `theta_max` in Section 7 is for a given grid; Corollary 5
  states `theta_max >= (N+sigma_max+1)/(3+2 sigma_max) Delta` for
  `1 <= sigma_max <= N-2`, `n_omega > 2`, and its proof cites Theorem 4 and
  Corollary 4, but Theorem 4 gives only `Delta` at `(N, sigma_max) = (5, 2)`
  (its first case, `sigma_max + 2 <= N < 3 + 2 sigma_max`), and `8/7` is
  Corollary 4's upper bound, tight only when `N = k(3+2 sigma_max) + sigma_max + 2`.
  The repository's reading of the source and its counterexample are
  therefore well-founded; the exact value `Delta` is also Lean-verified
  (topic 01).
- Coordinator hand-check of `results/pooling-all-degrees-two.md`: the cost
  identity `a_v - 2 s_v - b_v = -s_v - d_v`, the forced `d_v = 0` when
  `s_v > 0`, the two normalizations of Lemma 1, the bipartite fractional
  matching argument of Lemma 2, the conflict graph and `alpha(H) = |E3| +
  alpha(G)` of Lemma 3, the approximation transfer (`P* <= 3 alpha(G)`),
  and the merged-lax corollary: correct.
- Coordinator source check of `notes/common-factor-p-split-correction.md`
  (claimed counterexample to a published theorem): the local full text of
  Kronqvist–Misener–Tsay states Theorem 6 exactly as quoted ("fully
  disjoint, with additive bounds and constraint functions that are strictly
  convex, a P-split formulation cannot form the true convex hull"), with
  Definition 4 as pairwise-disjoint disjuncts; the two-disk example
  satisfies these hypotheses, every box vertex lies in a disjunct so the
  hull is the box and every convex relaxation inside the box is exact, and
  the explicit lifted witness `(3t, 9-3t, 1)` is valid. The counterexample
  stands, and the diagnosis of the proof gap (no Jensen slack in fixed
  coordinates; no outward neighbourhood on a facet of `X`) is right. The
  companion `notes/common-factor-p-split-rotation-gap.md` Section 2 witness
  (`p = (2D/3, D/3)`, its half-weight auxiliary lift, distance
  `D/(3 sqrt 2) - 1`) was also checked.
- Coordinator hand-check of `notes/certified-minlp-soundness.md` and
  `notes/certified-minlp-vipr-replay.md`: the bound-propagation induction,
  the supporting-plane cut proof (`r(x) - a x >= phi(z) + d (x - z) >=
  phi(z) - sum W_j >= b`, with the finite-`W_j` sign table), the
  master-to-original transfer via the extension `E(x)`, the
  solution-cutoff recovery of (3) with `L <= Umin`, and the VIPR induction
  invariant over the cutoff set `S`: correct as mathematical arguments; the
  notes state the software trust boundary explicitly.
- Coordinator hand-check of `notes/lbesh-development-theory.md` Sections
  1-2: validity of the lifted tangent (1), the perspective-gradient
  identity (`∇_nu G = a_z`, `∂_lambda G = b_z`), the ESH radial inequality
  `a_z^T(p - xbar) >= delta/s`, and the uniform separation bound
  `ell_z(p) >= delta v/(L D)`: correct.
- Coordinator hand-check of `notes/research-20260922-constant-data-messages.md`
  Proposition 1 (identity (3), least-norm value `(t - c_z)^2/D_z`), the
  center separation `theta^n` (needs `theta <= (3 - sqrt 5)/2`, satisfied),
  the unique-minimality window `|t - c_z| <= theta^n/3` (uses `C_theta < 4`),
  and Theorem 2: correct.
- Coordinator hand-check of `notes/research-20260922-smoothing-magnitude-obstruction.md`:
  the scaling identity `F_s(sx, z) = s^2 F(x, z)`, the threshold separation
  `a < b` (equivalent to the first condition on `s`), penalty positivity
  (second condition), and the ZPP conclusion: correct.
- Coordinator consistency check of `research-20260922/curve-hulls/report.md`
  against `research-20260922/log.md` and README: the regenerated seed-0
  bounds (225.68/656.03/1572.66/3144.48/4441.52), the earlier values, the
  overwritten-cut disclosure, and the exact-rational cut checks (0 of 5,928
  violated) are reported consistently; the certification's stated trust
  assumption (float64 library functions accurate to `1e-14` relative) is
  disclosed in the report.
- Coordinator consistency check of the quadratic-aggregation paper's
  checkable-hypotheses proposition (`paper-quadratic-aggregation/sections/04-hypotheses-examples.tex`)
  against the results note's corrected Corollary 5: both state `m = 2`,
  any `n >= 1`, or `m = 3`, `n >= 3` with a positive definite combination of
  the quadratic parts; the proof via the perturbed forms
  `M_i(s) = A_i + s^{-1}(alpha b_i^T + b_i alpha^T) + s^{-2} c_i alpha alpha^T`
  is correct.
- Coordinator hand-check of `notes/research-20260912-fixed-parameter-doptimal-fptas.md`
  Sections 2-4: the maximum-volume basis coordinates `|x_i| <= 1`, the
  dyadic normalization (3) with `I <= TBB^T T^T < 4I`, the `4p` diagonal
  filter, the floor residual (5), the perturbation bound
  `||A_hat - A*||_2 <= pNh = eta/p`, the determinant bound (7) via
  Bernoulli, and the polynomial state count (8): correct.
- Coordinator hand-check of `notes/research-20260912-latent-separator-certificates.md`:
  the global upper-bound inequality (variational Schur quadratic evaluated
  at an arbitrary `G`, then the log-determinant tangent with weight `W =
  N^{-1}`) is valid for any positive definite `W`; the five certificate
  artifacts referenced by the table are present in
  `code/research_20260912/results/`, and their exact rational lower and
  upper bounds reproduce all ten table entries to the printed digits.
- Coordinator hand-check of `results/bilevel-well-conditioned-box-exact-hardness.md`:
  the ReLU ternary network and score identity (2), the diagonal scaling
  giving `||B||_2 <= 1/50` and (4), the residual decomposition
  `|S^{-1} r| <= (I+P)e + 2`, the recursion (5) with `T = (I-P)^{-1}`,
  the contraction `2MC(1+NC)theta^2 < 1/2`, the bound (6)
  `||e||_inf <= 8MC theta^2 <= 1/(16N)`, and the gap (7) `delta/8` versus
  `15 delta/8`: correct.
- Coordinator hand-check of `results/quadratic-system-noncommutative-rank-complexity.md`:
  the second-moment identity behind (4), the AM-GM capacity step (5) and
  volume bound (6), the elementary permanent/Hall substitute for the
  energy constant, the parity covering with the midpoint identity
  `(1/8)(x-y)^T G (x-y)` giving (7), the real shrunk space by
  supermodularity, Lemma 2 and the block form (9) with exponent sum
  `r/2`, and the binary construction's error `C 2^{-T}/4 <= eps` and
  count (11): correct.
- Coordinator hand-check of `results/quadratic-integer-precision-approximation-hardness.md`:
  the zero-dimension lemma (`p = 0` iff `M(G) <= eps`, via the midpoint
  `((1/2)1, M(G))`), the finite-multiplicative impossibility, the
  `2^t`-point parity packing giving `p >= t`, the exponent arithmetic
  `C n^{1 - delta - q delta} < 1` for `q > 1/delta`, and the
  positive-minimum augmentation (`8 z^2` needs one integer; the one-binary
  lift has error `1/2`; `t+1` in the high case): correct.
- Coordinator hand-check of `results/bilinear-graph-binary-complexity.md`:
  the parity-midpoint deviation `(a_i - c_i)(a_j - c_j)/4`, the planar
  width lemma `d_1 d_2 <= 5 delta`, feasibility of `s_i = -log2 d_i` for
  `L_20`, the volume count `p >= L_20`, the shared-bit construction with
  McCormick residual error `h_i h_j/4`, and `L_4 <= L_20 + tau* log2 5`:
  correct.
- Coordinator hand-check of `results/fixed-core-block-polyhedral-optimization.md`
  Sections 2-6: vertex candidates and feasibility signs (2), the
  sign-condition selection of support-maximizing vertices, the squared-
  denominator inequality (4)/(5), Lemma 2 (membership in the Minkowski
  sum via support functions), the fixed-variable formula (8) with
  polynomially many polynomials of degree `O(N)`, and the pooling
  Corollary 3 reformulation (core `q_{i l}`, output blocks of dimension
  `p + m`, quality rows (9), aggregate rows (10)): correct in every step
  checked; the cited Basu–Pollack–Roy and Adler–Beling complexity bounds
  were not re-read.
- Coordinator hand-check of `results/bilevel-fixed-aggregate-response-algorithm.md`
  Sections 2-4: the KKT compression `z_i = clip(-B_i/a_i)` (valid because
  `a_i > 0`), the regime polynomials `L_i, R_i` in the fixed-dimensional
  `v`, polynomially many realizable sign conditions, the cleared
  numerators `Z^sigma`, `K_sigma`, `R_sigma` of polynomial degree and size,
  and the quantified comparison imposing global follower optimality
  (every global minimizer is a KKT point): correct. Section 5's
  attainment argument (Hoffman error bound for fixed constraint normals,
  closed optimistic graph) and the Section 6 boundary examples (cubic
  costs with `sqrt(p_i)` responses, the `a_i = c_i = 0` 3SAT encoding,
  the `x^{2^t} = 2` degree example, the non-attainment example with
  leader-dependent normals) were also checked and hold.
- Coordinator hand-check of `results/pooling-bypass-structure-algorithm.md`
  Sections 2-4: exact affine compression of qualities, the core/block
  partition after deleting at most `c` bypass endpoints (block dimension
  at most `ph + ch + h^2`), placement of quality rows in blocks, and the
  fixed number of aggregate rows (pool balances `p(1+t)`, covered nodes
  `c(1+t)`): consistent with the fixed-core theorem's hypotheses.
- Coordinator hand-check of `results/potential-flow-cactus-square-root-sum.md`:
  the parallel-branch flows `q/(1+sqrt a)`, `q sqrt a/(1+sqrt a)`, the gadget
  drop `q^2 (sqrt a - 1)^2`, formula (2)-(3), the rationalization (4) with
  `r_j = 4 A^3 B^3/(A-B)^4`, the integer scaling by `L = 2 prod a_i`, and the
  reduction (6): correct (the statement's missing "cactus" qualifier is
  m1).
- Coordinator hand-check of `results/potential-flow-fractional-power-arc-barrier.md`:
  the cycle equation with one circulation `z`, `h(0) = sum sqrt(a_i) - K`,
  strict monotonicity giving `x_{N+1} >= -1 iff sum sqrt(a_i) <= K`, the
  integer scaling by `A = prod a_i`, and the general even-denominator data
  (`beta_i phi(c_i) = sqrt(a_i)`): correct.
- Coordinator hand-check of `results/potential-flow-exact-arc-capacity.md`:
  single-block aggregation of the objective edge, the monotone transfer
  `x_e = sign(D) sqrt(|D|/beta_e)` at fixed resistances, the use of the
  quadratic-law nomination-face family, and the fixed-core instance
  (cycle equations linear in the resistance leaves with quadratic core
  coefficients, core-only objective, `r` aggregate rows): consistent with
  the theorems it composes.
- Coordinator hand-check of `results/potential-flow-weighted-tree-np-completeness.md`:
  the identity `F = sum y_i^2/w_i <= K` with equality on subset vertices,
  vertex integrality of (1), the deficit `r(w_i - r)/w_i >= 1/2`, the
  rounding recovery (`K - F >= (1/2) sum m_i`), and NP membership: correct.
- Coordinator hand-check of `results/potential-flow-weighted-potential-cycle-hardness.md`
  Sections 1-4: conservation of the flow parametrization, the circulation
  root `q = -6/(6 + sqrt(36+12 theta))`, the identity
  `F = -12(q+1/4)^2 - 105/4`, the endpoint values `-423/16`, the Subset-Sum
  encoding `theta = 24 iff sum a_i sigma_i = K`, the gap
  `|q+1/4| >= 1/(20K+12S)` and `Delta = 3/[4(5K+3S)^2]`, the integer
  scalings, and NP/coNP membership via the one-circulation quadratic:
  correct.
- Coordinator hand-check of `results/potential-flow-series-parallel-arc-validation.md`:
  the electrical sign lemma's use (two-terminal decomposition with the
  target edge's endpoints as terminals), the adjoint sensitivities
  `partial x_a/partial theta = j_e f_e/g'_a` and `-(1-j_a) f_a/g'_a` with
  `0 <= j_a <= 1`, the zero-basis sign invariance, the smoothing limit,
  endpoint hull equality, and the rank-two/rank-three boundary: correct.
- Coordinator hand-check of `results/potential-flow-discrete-arc-capacity-hardness.md`:
  the weak objective edge with `M = H D^2`, strict monotonicity of `F` via
  the Tellegen identity (2), the bounds (3) `t <= 2/D`, the Lipschitz
  margin (4) `528/D < Delta/8`, the threshold `M c^2 = H` separating yes
  (`t > c`) from no (`t < c`), and the gap (5) `3 Delta/(32 D)`: correct.
- Coordinator check of the Lean statement `sharp_positive_growth`
  (`formal/Formal/MultilinearGap/SharpAsymptotics.lean`, `BoxSuprema.lean`,
  `Suprema.lean`): `boxDegreeSupremum d / (log d / log (log d)) → 1` and the
  dimension analogue, with ratio sets over all finite index types,
  nonnegative coefficients, supports of size at most `d`, and positive
  hull gap: faithful to the informal sharp-growth claim.
- Coordinator hand-check of `results/potential-flow-discrete-resistance-hardness.md`:
  conservation of the displayed theta flows, the cross-cycle equation
  `(12 tau + 1) q^2 + 10 q - 23 = 0`, the span `pi_0 - pi_1 = 2 + (q-1)^2/6`,
  the leaf shift giving `F = 1 - (q-1)^2/6`, `q = 1 iff tau = 1 iff sum
  a_i sigma_i = K`, and the gap `|q - 1| >= 6/(31K + 18S)`,
  `Delta = 6/(31K+18S)^2`: correct.
- Coordinator check of the scalar-quadratic Lean headline
  (`formal/Formal/QuadraticPrecision/ScalarHeadline.lean`,
  `PrecisionArithmetic.lean`, `Model.lean`): `HasPrecisionRate P r` states
  that for all sufficiently small `ε` the minimum count `p` with `P ε p`
  satisfies `|p - (r/2) log2(1/ε)| <= C`; `scalar_quadratic_graph_rank_law`
  instantiates it with `r = H.rank` for arbitrary convex integer lifts
  (`ConvexIntegerLift`) and binary lifts over a nondegenerate box, and the
  inertia laws use `negativeInertia`/`positiveInertia`. Faithful to the
  informal "half the rank / half the inertia" laws.
- Coordinator hand-check of `results/polynomial-graph-binary-integer-degree-gap.md`
  Section 1: the Bernstein error bound `2M sqrt(x(1-x)/N) <= 1/32`, the
  two-integer formulation with admitted error `1/16 < 1/4`, the
  peak/trough chord argument giving `p_bin >= ceil(log2 M)`, and the
  `+1` upper bound (3a): correct. Sections 2-3 rely on the cited chord
  partition and hybrid theorems and were not re-derived.
- Coordinator hand-check of `results/small-exponent-milp-soc-encoding-separation.md`:
  the conic representation (1)-(2) of `t = theta v` including the `theta = 0`
  recession argument (`c^T z = s0^T z >= 0`, `b^T u = -z0^T s <= 0`), the
  squaring chain optimum `a^{2^B}` with the strictly feasible point, the
  dual-cone membership of the certificate vectors, and the four-binary
  segment construction (4) with error `1/16`: correct.
- Coordinator hand-check of `results/spatial-bb-sdp-rlt-exponential-lower-bound.md`:
  the pseudomoment point (`x_i = c`, `X_ij = d` on `U`, exact products
  touching `R`), its equality-product row sums `cK`, PSD covariance
  (eigenvalues `0` and `t(s-t)/(s(s-1))`), all box RLT expressions
  (`d`, `c-d`, `(s-t)(s-t-1)/(s(s-1))`, and the diagonal cases), the
  objective `|M ∩ R| p(1-p) < 1/4 - epsilon` for `|R| < q`, and the
  covering count: correct.
- Coordinator hand-check of `results/spatial-bb-higher-sos-exponential-lower-bound.md`
  Lemmas A-B: the cardinality identity
  `a (t)_a/(s)_a + (s-a)(t)_{a+1}/(s)_{a+1} = t (t)_a/(s)_a`, the
  falling-factorial Vandermonde decomposition of the moment matrix `N`
  into nonnegative multiples of the PSD incidence Gram matrices `P_j`,
  and the conditioning identity for box products: correct.
- Coordinator hand-check of `results/common-factor-fixed-linking-optimization.md`:
  the reciprocal bounds `L_j(x) = max(l_j, p_j/x)`, `U_j(x) = min(u_j, q_j/x)`
  for `x > 0`, the slack-augmented system (2), the lexicographic
  perturbation that orients nonbasic bounds, the rational-function
  candidate (3) with denominator `x D_J(x)`, and the degenerate-cost
  example showing the perturbation is needed: correct in outline; the
  bit-complexity accounting was not re-derived.
- Coordinator hand-check of `notes/hens-20260912-singularity-and-lift.md`
  Sections 1-4: the expansion `f ~ eps (d2+eps)/delta -> +inf` as
  `d1 -> (d2+eps)+`, the sign analysis of the other branches, and the
  inference that process areas `2q/(0.01+f)` can be driven to zero when
  the `dt` variables are tied to temperatures only through big-M
  inequalities: correct given the parsed model structure; the infimum
  bracket `[100,500, 108,846.94]` follows from the relaxation `c1` and the
  50-digit-checked points as stated.
- Coordinator hand-check of `results/quadratic-general-norm-output-precision.md`
  (first half): the image restriction (2) `p(f,K) = p(g,K_eff)` in both
  directions, the exact oracle pullback and radii (3), and the symmetric
  averaging that turns the GLS rounding output into `E_0 ⊆ K_eff ⊆ beta E_0`
  with `W = d(d+1)^2 A`: correct.
- Coordinator hand-check of `results/quadratic-ellipsoidal-output-precision.md`:
  nonnegativity (3) of the group energies, the midpoint bound
  `E_l(Sigma) <= 16 eps_l^2`, and the shared-grid error bound (4)
  (`||Z||_F <= 1/4`, `e^T W_l e <= E_l(P)/64 <= eps_l^2/64`): correct.
- Coordinator hand-check of `results/quadratic-weighted-covariance-precision.md`:
  the parity-support covariance bound (3), `Sigma <= (n/4) I`, feasibility
  of `P = Sigma/c_n` (needs `c_n >= 4` and `c_n >= n/4`), the volume bound
  `2^{A_n} sqrt(D)`, the lower bound `p >= Phi - A_n`, and the rotated
  dyadic grid count `sum L_i <= Phi + n log2 n + n = Phi + B_n`: correct.
- Coordinator hand-check of `results/rank-one-correlation-face-conic-lower-bounds.md`:
  Lemma 1 (trace face `r = c = 1_A`), Theorem 1 (pair and total-sum
  equations select `a = (x, e-x)`, block inverse affine in `X`), Lemma 1b
  (`S <= m + S B + 2 S D` via `|a-b| <= a(1-b) + b(1-a)` and
  `||r-c||_1 <= 2SD`), and Lemma 2 (faces inherit conic lifts): correct.
- Coordinator hand-check of `results/rank-one-correlation-face-stability.md`
  Theorem 1: the rounding estimates `u <= 6SD`, `v <= 8SD`, `h <= SB + 8SD`,
  `||a-b||_1 <= 2SB + 22SD + |m-S|`, the outer-product comparison with the
  rescaled `b~`, and the final constant `C_m = 136m + 10`: correct.
- Coordinator read of `results/rank-one-approximate-sdp-lower-bound.md`:
  Lemma 1 (facial reduction and conic duality give a PSD factorization of
  order `q+1` for valid affine slacks) and the reduction of Lemma 2
  (`L_S(yy^T) = f_k(x_S)`, shift by `theta = eta/(4k^2)`) are consistent;
  the imported Lee–Raghavendra–Steurer quantitative bound and its
  constants were not re-derived.
- Coordinator hand-check of `results/potential-flow-global-energy-maximization.md`:
  the scalar conjugate `(2/3)|d|^{3/2}/sqrt(beta)`, the perspective
  convexity of the dual term, `D = 3V`, the two-cone elimination
  `z^3 <= beta t^2`, and the exact triangle certificate (`U = L = 1/4`,
  maximum dissipation `3/4`): correct.
- Coordinator hand-check of `results/potential-flow-global-correlation-energy-design-hardness.md`:
  the triangle drop `e(s) = 2s/(1+sqrt s)^2` with `e' = 2/(1+sqrt s)^3`,
  `e'' < 0`, the values `A_E = 24 - 16 sqrt 2`, `B_E = 13/2 - 3 sqrt 3`, the
  strict bound `kappa_E > 1/20`, the bridge-bias cancellation
  `r_i + s_i = 3`, and the Max-Cut identity: correct.
- Coordinator hand-check of `results/potential-flow-global-correlation-total-flow-hardness.md`:
  the path flow `f(r) = 1/(1+sqrt r)`, its second derivative
  `(1+3 sqrt r)/(4 r^{3/2}(1+sqrt r)^3) > 0`, the values `A = 2 sqrt 2 - 2`,
  `B = sqrt 3 / 2`, the strict bound `kappa > 7/200`, the graph counts, and
  the Max-Cut identity with the threshold gap `7/512`: correct.
- Coordinator hand-check of `results/bilevel-surrogate-screening-exact-optimization.md`
  Sections 1-2: the difference of the two variational inequalities giving
  `e^T Q e + p^T e <= 0`, the completed square (2), the support bounds
  (3), the vertex maximization (4) of the convex quadratic, the coordinate
  enclosures (5)-(6), and the status tests including the weak-closure
  refinement (10): correct.
- Coordinator hand-check of `results/bilevel-conditioned-box-additive-algorithm.md`
  Sections 2-3: the saturation thresholds (derivative at least `Q_ii z_i`
  when `c_i + D_i x >= -m_i^-`), the slab width `R_i = sum_j |Q_ij|`, the
  cell closure argument, the response bound (2) from the two variational
  inequalities with `mu <= lambda_min`, and the maximum-minor row basis:
  correct.
- Coordinator hand-check of `results/network-simplex-series-parallel-coefficient-growth.md`
  Section 3: column weights `F_{q+1}` under (9), invertibility of `D` and
  `C = 11^T - D`, positivity of the row weights for `q >= 3`, the observed
  count `5q-4`, and inequality (10): correct. The section lemma of Section
  2 was read but not independently re-derived.
- Coordinator arithmetic check of the switching-control closed forms
  quoted in README.md: `(n-1)^3/[n(3n^2-3n+1)]` exceeds `1/4` exactly from
  `n = 8` (so "four through seven modes give `T/4`" is right), and the
  three-switch second term exceeds `1/5` from `n = 12`.
- Coordinator hand-check of `results/cia-exact-two-switch-worst-case.md`:
  the distinct-mode reach theorem (identities behind (2) and (3), the
  bound (4) `M >= B_2`, inequality (5), the aggregate (6), which holds with
  equality in its last step, and the contradiction `(n-1)L > (n-1)B_3`),
  the threshold condition `nE(r^3-1) >= T`, and the sign of
  `n^3 - 9n^2 + 11n - 4`: correct. The heavy-mode lemma in
  `results/cia-two-switch-global-upper.md` was also checked case by case
  (`m_q >= T-2E`; two heavy modes with `A_q(2E) <= E`; unique heavy mode
  with `A_h(2E) <= E` or `> E`), including the sign bookkeeping
  `m < 2E` and `T - 3E <= E`: correct. The uniform-control lower bound was
  not re-derived. Theorem 2(c)'s total-unimodularity
  signing was not re-derived (it is the classical constant-capacity
  flow-cover polyhedron and was checked numerically on 385 sets).

## 5. Historical reports of checks that found no error

This section preserves the original auditors' reports of checks that found
no error in the listed claims. These are historical agent reports, not
certificates. Some excerpts were truncated in the retained record; omitted
text cannot be reconstructed here. Current issue-table adjudications
supersede conflicting historical conclusions.

- R1 (lens B): all nine cactus/region notes, their 17 review notes, and
  cited code checks were read; the flow-region monotonicity and product-hull
  arguments, the deletion identity, the SRS gadget identity, the additive
  algorithm's face lemma (also probed numerically), and the bounded
  block-rank counts were verified by hand. No major or moderate issue.
- R2 (both lenses), R3 (B), R4 (B), R5 (A): no mathematical error found in
  the assigned potential-flow and AC power-flow theorems; issues are limited
  to labelling and provenance listed above.
- R6 (B): the exact dyadic gap values and the second-order certificate were
  recomputed independently and agree with the notes.
- R7 (A): the frequency-two reduction was verified by hand.
- R8 (A): the 1,589-check count was reproduced by arithmetic from the script.
- R22 (both lenses): the BDS Conjecture 3.3 proof (easy direction, Lemmas
  1-3, the three-step separation/compactness argument, Section 3.4), the
  infinite-aggregation hull formulas and the strict PDLC notes were stepped
  through and found correct; the Lean headlines of topics 27 and 30 were
  compared with the note statements.
- R23 (A): cluster-free Theorem 1 (six steps, choice of `rho`, constant
  `c_2 = c' + tau`), Theorem 2 packing count, Theorem 3 width-tight reduction,
  composite-envelope and vertex-binarization theorems re-derived; only wording
  and evidence issues (m19-m21).
- R24 (both lenses): row-hull Proposition 1, Corollary 1', Theorem 2(a)-(c)
  (RH/EF equivalence, TU arguments, flow-cover selection, tilted-cover
  strictness witness), the shared-variable link theorems and the indicator
  hardness reduction re-derived independently by both auditors; numbers in
  the tables reproduced from the saved JSONL files.
- R25 (both lenses): spectral-messages Lemmas 1-2, Theorem 3 (net transfer,
  exponent bound, midpoint net), Section 4 conditional message and rounding
  error, the block-DP and fixed-treewidth results checked step by step; all
  constants recomputed.
- S1 (both lenses): ridge-envelope Theorem 1 (normalization, staircase data,
  Steps 1-4 including Strassen coupling, Lovász-extension concavity,
  duality and the review's `K+` attainment argument) correct under the lsc
  hypothesis; the corollaries hold with the sign condition noted in m28.
- S2 (both lenses): Lemma 1, Propositions 2-3, tangent-map properties,
  Theorem 4, Corollary 5, Theorem 6, Proposition 7 algebra (root 0.72474
  confirmed by a grid computation) correct; the open point is the citation
  behind (R2) for unclipped McCormick relaxations (M4).
- S3 (both lenses): the F1-F3, Collatz-Wielandt and knapsack-dual proofs
  are correct; `nuc_verify.py` computes in exact fractions; the exact CW and
  P values for `nuclearva`, `nuclearvd`, `nuclear10a` were recomputed with
  the reviewer's parser and match the JSON to all digits; all 18 solver rows
  match the logs.
- S4 (both lenses): polygon OSiL structure re-parsed, the odd `m`-gon
  construction and the isodiametric dual argument verified, regular-polygon
  values recomputed to 30 digits; kissing-number and elec certificates
  reproduced.
- S5 (E): every number in the curve-hull report (duals, root bounds, cut
  counts, slacks, ratios) reproduced from the saved `.out` files; the
  chord/second-derivative certificate bound is valid and the interval
  widenings adequate apart from m35(c).

- V5: Checked and found correct (do not re-audit): (1) All 225 local .md links from README.md resolve. (2) README audit-count claims: I cross-checked every README phrase of the form \"two/three audits passed\", \"two independent reviews\", \"doubly/twice reviewed\" against the linked result note's status section and the review notes on disk (~70 results files); every count is backed by that many existing review notes. Specifically verified in full text: ac-power-flow-existential-reals (3 audits A/B/C, blocking finding fixed), pooling-existential-theory-of-reals (2), pooling-one-pool-bypass (2), bilevel-surrogate-screening (2), quadratic-weighted-covariance (2), cia-exact-two-switch (3), potential-
- V6: Mechanical sweep over all 207 files in results/ (status/verification/review sections extracted by script) plus targeted deep reads. Checked and found correct: (1) every markdown link in every results/*.md resolves — 0 broken local links out of the full link set; (2) every result whose status claims independent review links or names review notes that exist (my first slug-based matcher produced 95 false alarms because review notes are named after investigation slugs, e.g. review-pooling-triviality.md for results/pooling-triviality-polynomial.md; after resolving by actual link/backtick target, 0 missing); (3) claimed review counts versus notes found: the only two results whose claimed count exc
- V2: Extensive independent recomputation from the saved JSON reproduced essentially every quantitative claim in the LB-ESH chain exactly; I found no false numerical or mathematical statement.

Numerics verified by recomputing from code/minlp_solver_lab/results/lbesh_development/analysis_v1/analysis.json (and raw JSONL) rather than trusting the notes:
- Record counts: 663 primary (550 numerical_solve / 106 feasible_open_gap / 6 invalid_witness / 1 wall_timeout), 1,464 total across 8 batches, 351 legacy (239/38/4/61/7/2 exactly as stated), 9 trig-sensitivity, 24 legacy-initialization, 72 nonlp ablation, 144 ablation. raw_status 'optimal' = 603 vs 550 accepted, as stated.
- The six invalid witnesses
- L1: Mathematics of the exact-count topic checks out; I found no mathematical error, proof gap, or statement/scope mismatch in the Lean development or the two informal sources.

Model fidelity (Formal/Model.lean): `Admissible` = (every graph point over [0,1]^n has a lifted witness with an admitted code) AND (every lifted point with an admitted code is Valid: x in [0,1] and both |w_j - F_j(x)| <= 1). This matches the paper's def:dimension (01-foundations.tex:18-38) with R taken to be the projection, and matches the note's model. Auxiliary dimension q is existentially quantified and unbounded; `IntegerCodes p` places no bound on integer magnitudes; the convex set is arbitrary and need not be closed
- V4: No mathematical or major verification defects found in cluster V4; every stated number I could cross-check matched its saved artifact. Checked in detail:

NETWORK SIMPLEX (notes/network-simplex-reopened-computation.md vs code/network_simplex_benchmarks/{results,repeated-results,flat-repeated-results}.json and code/network_simplex_compressed): every entry of all five tables matches the JSON exactly — six optimization cases (objectives, cut counts 3/16/1/18/5/42 summing to the stated 85 with 23 transportation-subset cuts, sizes 5675/9160/34689 and 255/48/225/1004, timings 2-5 ms vs 9-319 ms, 319 vs 189 ms), the three membership rows (30.28/218.13/2876.21, 6.44/7.85/11.49, separator = preproces
- L11: Checked and found correct (Lean-fidelity lens, cluster L11).

SUPPLEMENT IDENTITY: `diff -r formal/Formal/QuadraticAggregation paper-quadratic-aggregation/supplement/lean/Formal/QuadraticAggregation` is empty (identical). The five support modules (DAGSpectral/{ProfileCount,Rounding,UpperTriangle}, QuadraticPrecision/{Spectral,SpectralSlice}) and Formal/InfiniteAggregation are byte-identical too. Supplement manifest counts (64 owned modules / 909 declarations / 5 support) match `find Formal -name '*.lean' | wc -l` = 69 and 178+158+248+93+232 = 909; all 86 recorded input SHA-256 fingerprints match the current files; supplement/lean/verification contains fresh build/axioms/kernel logs and a man
- V1: No major error found in cluster V1; the certified-MINLP verification claims are unusually well supported. Checked and found correct: (1) All headline counts reproduce from the saved records - recounting code/minlp_solver_lab/results/cert_replay_20260913_complete.jsonl gives exactly 188 verified / 92 rejected / 9 missing over 289, and re-classifying the 92 rejection messages gives 67 domain-or-curvature, 13 cut-check, 12 proof-inference, matching the note's table and cert_replay_20260913_complete_audit.json; checker seconds 7987.954 / max 463.845, proof bytes 38,826,726,525, campaign wall 1465.381 s, 52/81 near-reference counts, 23 negative differences with max 5.8337e-10, and 18 solver flags
- P11: No mathematical error found in either paper; the theorems and their proofs check out, including all printed numbers. Verified independently (sympy/numpy/scipy, exact where possible):

CUBIC PAPER (paper-cubic-gap/main.tex).
- Lemma 2 (rational scalar certificate): both completed-square identities F-L-p(c) and F-L-q(c) are exact polynomial identities (sympy simplify -> 0); g(c) = -49/6+30c-15c^2 <= 0 on [0,3/10] (max -31/60 at c=3/10) so the constrained branch is valid for a<=1; all five Bernstein rows are exact identities under t=(c-l)/(u-l), and min v_i/D per row is 4133/60000, 901/120000, 6947/240000, 1991/47616, 15869/190464, all >= delta=901/120000. Grid check of F-L on [0,1]^3 gives min
- L12: Read in full and checked: formal/Formal/InfiniteAggregation/{Model, Good, GoodMatrix, GoodBlock, GoodSpectral, GoodConvex, Inertia, GramFrame, GramSupport, GramConcavity, GramBound, Hyperplane, HyperplaneConvexity, Rays, Witness, Cardinality, ClosedObstruction, Consequences, HullModel, HullCoreRoots, HullCore, HullCone, Hull, HullClosure, HullClosedConsequences, HullRepresentations, LiftSmall, Lift, AccuracyModel, AccuracyConstants, AccuracyAngular, AccuracyUpperGeometry, AccuracyMesh, AccuracyUpper, AccuracyLowerPigeonhole, AccuracyLowerGap, AccuracyLowerLipschitz, AccuracyLower, AccuracyRate, Accuracy, AccuracyRational, AccuracyRationalMesh, AccuracyRationalBound}.lean plus QuadraticPrecis
- L0: Checked and found correct (no need to re-verify): (1) Axiom-audit machinery. formal/Verify.lean, paper-multilinear-gap/formal/Verify.lean, paper-cubic-gap/formal/Verify.lean, paper-certified-minlp/formal/Verify.lean and every topic Audit*.lean use the same sound ownership predicate — fold over env.constants, keep names whose owning module matches a `Formal`/`CertifiedMinlp` prefix or an explicit module list, then Lean.collectAxioms transitively with allowlist {propext, Classical.choice, Quot.sound}, erroring on an empty audit. This does cover private, generated and instance declarations, and it catches sorryAx / Lean.ofReduceBool through dependencies. (2) Coverage partition: the 813 modules 
- V3: Verified and found CORRECT (do not redo):\n\nComposite univariate envelopes. Re-ran the repository's own analysis scripts on the saved JSONL: `analyze_minlplib.py results/minlplib_v3.jsonl` reproduces the experiment record exactly (54/53/51 solved of 107; sgm 15.9/16.6/21.3 s; hybrid-vs-native 2 only-hybrid, 5 only-native, 2 faster, 16 slower, 11 gap-better, 10 gap-worse, 61 similar). `root_bounds.py` reproduces the 35/4/42/27 split and the whole better/worse instance list character for character. `consistency.py` prints 0 violations. `tables_separable.py results/separable.jsonl ../vertex_binarization/results/composite_baselines.jsonl` reproduces the 48-row separable table and the solved cou
- S5: Checked and found correct (no need to repeat):\n\nCURVE-HULLS (report.md, review.txt, code/).\n- Separator math in code/curvehull.py: the semi-infinite LP supplies only the direction; the constant is set to minus certified_min(c), which returns the min over a partition of [l,u] of per-piece rigorous lower bounds, so it is a valid global lower bound. The interval arithmetic (outward widening 4e-16 arithmetic / 1e-14 transcendental, ipow/rpow/exp/log/cos monotonicity and extremum handling, _lin_lower summation error term) is sound. The chord/second-derivative piece bound is correctly implemented with max(0, sup g'') (the report's prose omits the max — reported separately).\n- moment3_in_hull i
- L6: I read in full: results/positive-multilinear-gap.md, -sharp-degree-growth.md, -joint-gap-growth.md, -degree-upper-bound.md; formal/topics/07,08,09,10 README/COVERAGE/VERIFICATION/REVIEW + run logs + SHA256SUMS; paper-multilinear-gap/README.md, main.tex (all 775 lines), references.bib, formal/{README,COVERAGE,VERIFICATION}.md, Verify.lean, scripts/{check_bundle,verify.sh}, verification/{bundle-check.json,paper-build.json,review.md,completion-review.md,export.json}; and every Lean module in the cluster: CubicGap/{Laws,Expectation,Hull,Envelope,Polynomial,Termwise,TermwiseUpper}, MultilinearGap/{Construction,Monomial,Termwise,EnvelopeBounds,Deficiency,Lower,Upper,Growth,Results, ResidueSums,Exa
- L7: TOPIC 12 (marginal floor) — checked and correct. Read the source note results/positive-multilinear-marginal-floor-gap.md in full plus README/CLAIMS/COVERAGE/VERIFICATION/REVIEW and all eleven Floor* modules and their dependencies (EasyTerms, GeneralGaps, LowerAsymptotics, Termwise, Results). All 146 backticked names in COVERAGE.md resolve to real declarations. Re-derived by hand: the chord inequality min(1,y)(1-e^{-a}) <= 1-e^{-ay}; floor_gain_pointwise (reduces exactly to tau <= e*u, the stated hypothesis tau/u <= e); density normalization with L = log((1+tau)/tau); the exact marginal repair, proved for 0 <= p < 1 (more general than the note's p < 1/2); the clipping branch of floorUnion_exp
- P4: Read in full: main.tex; sections 00-introduction, 01-setting, 02-certificate, 03-consequences, 04-hypotheses-examples, 05-gram-hyperplanes, 06-infinite-aggregation, 07-approximation, 08-four-aggregation, 09-formal-overview, 10-discussion; appendices/application.tex; appendices/three-dimensional-span.tex; README.md. Also read FORMAL-VERIFICATION.md, supplement/README.md, supplement/lean/README.md, audits 27-31 CLAIMS/COVERAGE, verification/manifest.json, verification logs, results/four-aggregation-strict-pdlc.md, notes/review-20260922-final-aggregation.md, notes/review-20260922-aggregation-accuracy.md, process/stage08-root-audit.md and stage08 assessment, root README entries, and the local BD
- R23: Checked and found correct — no major issue in this cluster.\n\ncluster-free-branch-and-bound-constrained-minima.md: re-derived Theorem 1 Steps 1-6 line by line (constraint values on R(Z), the Lagrangian identity with the (-g_j)_+ slack, the Taylor/modulus-of-continuity form, the LICQ injectivity bound |d_V| <= kappa_0 G + kappa_1(tau w^2 + (M/2)|d|^2), the quadratic-form estimate with M' = gamma/2 + 3M/2, and the assembly with the two smallness conditions on rho). The constants c' and c_2 are consistent (except the Remark-3 specialization reported above). Verified the infimum passage needs no attainment, that (SC) makes the note's subspace C equal to the standard critical cone (so its SOSC i
- P13: I read paper-lbesh/main.tex, all 14 section files, README.md, evidence/coverage.md and notes/lbesh-claim-evidence.md in full, plus supporting material (notes/lbesh-review-theory.md, process/stage0*-disposition.md, data/*.json, all 17 table fragments, lbesh/solver.py::_validate_primal, lbesh_research/validation.py). MATHEMATICS — I reworked every proof step by step and found them correct: Prop. 3.1 (perspective identity: convexity, continuity at the unique zero-weight point via |G| <= lambda*max|g|, tangent coefficients (grad g(z), g(z)-grad g(z).z), completeness g(p)=sup_z l_z(p)); Prop. 3.2 (separate-disjunction hull, both inclusions, empty-term and zero-weight conventions, nu=0 forced at l
- P12: Read in full: paper-certified-minlp/main.tex, all nine sections/*.tex, README.md, experiments/PROTOCOL.md, experiments/REPLAY-SELECTION.md. Also read notes/certified-minlp-soundness.md, notes/certified-minlp-repair-and-replay.md, notes/certified-minlp-vipr-replay.md, notes/certified-minlp-literature-audit.md, notes/review-certified-minlp-exact-semantics.md, formal/COVERAGE.md, formal/VERIFICATION.md, and code/minlp_solver_lab/certify/vipr.py and driver.py.

Mathematics checked and found correct:
- Lemma 3.1 (propagation): implied-bound formulas and sign/direction handling are right for both row senses; integer rounding preserves feasible integral points; F subset of B is the right inclusion 
- R6: Lens A (proof stepper) over all seven assigned files plus their review notes, cited code and logs. No mathematical error, false statement, or unclosed proof gap was found in this cluster; the two findings above are provenance/scope wording only.

positive-multilinear-gap.md: re-derived the whole construction. Monomial count sum_j 2^j = 2m-2, occurrences Lm+2m-2 = O(n log n), termwise envelopes (cav = u_j since u_j <= 1/2 <= 1-1/m; vex = max{0, u_j - k_j/m} = 0), tbtgap = sum_j 2^j u_j = L. Verified cav f = L is actually attained (comonotone U-coupling puts all anchors at 0 whenever any leaf fails, since 2^-j <= 1/2 <= 1-1/m), so chgap = max E sum_j A_j N_j is correct including the E R = 1 bo
- P3a: I read all nine assigned files in full and worked through every theorem/proof step in sections 01-08. Verified correct (with independent exact-arithmetic checks where noted):

FOUNDATIONS (01): vertex-law representation; monomial envelope formulas (circle-covering argument); Prop deficiency (common upper, termwise, hull-deficiency identities); Lemma easy-terms (both cases, constants); Prop box-transfer. Bilinear: density comparisons d/2<=rho<=d, rho<=Delta/2, rho<=arboricity<=d<=2rho; Lemma induced-cut (cell-vertex argument in {0,1/2,1}^V, convexity of T-cH on cells); Lemma cut-row (polarization, Szarek-Khinchin row sums, R >= (1/4)sum||a_i||_2); fractional orientation via max-flow/min-cut; 
- P3b: I read all assigned files in full (sections 09-17 and all eleven appendix-*.tex of paper-relaxation-limits) and worked the proofs step by step; I found no major, moderate, or minor validity defect worth reporting. Details of what was verified:

SEC 09 (cardinality-spatial). Vertex/concavity argument for min F = 1/4 on F_{n,k}; chord identity x(1-x)-l_i(x)=(x-a)(b-x) and both McCormick lower planes collapsing to the chord; alpha-BB second derivative 2(alpha-1). Lemma endpoint-count: the hypergeometric avoidance bound binom(n-s,z)/binom(n,z) <= ((n-z)/n)^s, the max(|A|,|D|) >= |R|/2 step, and 1/N(q) = max of the two reciprocals — all correct, including the degenerate base-one case. Theorem cho
- L2: Checked and found correct (no finding needed):

TOPIC 17 (formal/Formal/GridSwitching, 23 modules).
- Declaration existence: I extracted every backticked identifier from the 37 coverage rows of COVERAGE.md and matched it against all 1036 declarations parsed from the 23 modules. Every named declaration exists (the only unmatched tokens are math variables and Mathlib lemma names). Spot-checked the ones spelled only loosely in prose: `cutoff_a_upper` (LinearPrograms.lean:240, an LPCommon field), the eight `*_mono_budget` theorems (Compactness.lean), the 16 `endpointWitness*` declarations (InstanceAlgorithms.lean). Same check run on topic 01's COVERAGE.md: all names exist.
- Unusual constructs: 
- R3: I read all nine assigned result notes in full, plus their review notes, the cited code, the README entry, and the key external dependencies (results/fixed-core-block-polyhedral-optimization.md, notes/monotone-polynomial-root-polytope-optimization.md, results/potential-flow-bounded-block-rank.md, results/potential-flow-polynomial-law-uncertainty.md §dense-degree). I found no major or moderate validity problem.\n\nVERIFIED CORRECT (proof steps re-derived by hand, with symbolic/numeric spot checks in sympy/numpy):\n\n1. exact-arc-capacity: single-block reduction and interval aggregation (Minkowski-sum projection is exact); monotone transfer x_e = sign(D)sqrt(|D|/beta_e) at FIXED beta*, so nomin
- L3: Checked and found correct (Lean-fidelity lens, cluster L3):

TOPIC 02 (FBBT). Read all 8 modules in full (Boxes, Circuit, Contractors, Dynamics, Lift, Limits, OriginalRun, Results) plus README/COVERAGE/VERIFICATION/run.log. Every declaration named in the coverage table exists. No sorry/axiom/native_decide/unsafe/partial/opaque; only `set_option maxRecDepth` appears anywhere in FBBT+PotentialFlow. Verified: `Box.IsHull` is the genuine minimal-box hull (and forces an empty carrier on an empty intersection, so no vacuity); `Step`/`Run` quantify over *all* exact-hull trajectories from the unit box, not just the canonical `iterate`, and `originalRun_isRun`/`canonical_slow_run`/`roundRobin_fair` m
- R1: Read all nine assigned result notes in full, plus their 17 review notes, the novelty/dependency notes they cite, the cited code checks, README.md, paper-potential-flow/coverage.md, and the relevant paper sections (02-cactus.tex, 06-weighted.tex, 08-design.tex). Verified the following and found them correct.

FLOW REGION (potential-flow-cactus-flow-region-and-optimization.md). H_min/H_max are continuous, strictly increasing, with opposite limit signs; q_max is the zero of H_min and q_min the zero of H_max (H_min<=H_beta<=H_max plus monotonicity); endpoint realization at each root by selecting the attaining endpoint per edge is exact and lands in the finite sets as well as the intervals; all r
- R7: No mathematical error, proof gap or false theorem was found in cluster R7. Checked and found correct (re-derived by hand step by step, plus independent numeric/LP checks where noted):\n\nFEEDBACK GAP (results/positive-multilinear-feedback-gap.md). Universal-law dominations (2) and (3): the single aligned-orientation event has length exactly m(s,b;i) and weight 2^-f, and every prescribed-mean law satisfies P(s,b) ≤ m(s,b;i); residual repair (h_s ≥ 0, Σ_b r_{i,s,b} = h_s, total residual mass 1−1/C, P'_e ≥ P_e/C entrywise with the required (F,i)-marginals); conditional forest gluing (single shared variable per newly reached factor, no loss multiplication along paths); the deficiency identity ma
- L5: Checked and found correct — no mathematical errors located in cluster L5.

TOPIC 05 / results/common-factor-reciprocal-anchor-hulls.md. Read Model/Hull/Representation/Moments/Allocation/PSD/Degenerate/Joint/Separator.lean in full. `graph`/`hull` are the actual convexHull of {(X,1/X,Y,XY)}; `mem_hull_iff_conicBounds` and `mem_hull_iff_psd` match (A)/(B) with 0<a<b, no vacuity; `arrowMatrix` uses real `Matrix.PosSemidef`; zero-denominator cases are proved, not hidden by Lean total division. Verified numerically/symbolically: the tangent-deficit identities 1/x-g_1 and 1/x-g_2 are exact (sympy -> 0); g_1=g_2=3/5 at the incompatible point; the four radical bounds are (sqrt122-11)/3, (sqrt898-27)/
- L9: Deep check of topic 21 (DAG spectral). Nothing major or moderate found; the package is unusually solid. Checked and found correct:

LENS (a) declaration existence: I extracted every backticked identifier from COVERAGE.md and matched it against all `theorem/lemma/def/abbrev/structure/inductive` names in formal/Formal/DAGSpectral/ — every named declaration exists (only `p`, `r`, `N`, `Nh` are non-identifiers).

LENS (d) unusual constructs: `grep -rn 'sorry|axiom |native_decide|unsafe|implemented_by|partial def|opaque |set_option'` over Formal/DAGSpectral returns nothing. `native_decide` appears only inside `example`s in verification review clients (BitFoundationReview, NormalizationReview), ma
- R4: I read all nine assigned result files in full, plus all 18 associated review notes (review-potential-flow-{joint-resistance,joint-resistance-second,reopened-joint-weighted,reopened-joint-weighted-second,affine-law-uncertainty,affine-law-uncertainty-second,secant-envelope-comparison,secant-envelope-comparison-second,series-parallel-arc-characterization-independent,series-parallel-arc-characterization-second,series-parallel-arc-hulls,series-parallel-arc-hulls-second,series-parallel-envelope,series-parallel-envelope-second,series-parallel-exact-arc-barrier,series-parallel-exact-arc-barrier-second,unbounded-rank-arc-obstruction,unbounded-rank-arc-obstruction-second}), the cited code checks, and 
- R5: I re-derived the main theorems of all nine assigned files and found no mathematical error, no unclosed proof gap, and no false verification label beyond the minor items reported.

VERIFIED CORRECT - potential-flow-weighted-arc-cactus-characterization.md: (1) cactus direction: bridge flows fixed, cycle offsets x_e=q+d_e, H_beta(-d_e) independent of beta_e so the physical sign of q+d_e is constant along a one-coordinate section, root comparison gives monotonicity, coordinatewise endpoint movement gives hull equality (2=>3). The "direction may depend on the other resistances" qualification is genuinely needed (both audits give explicit examples). (2) theta gadget re-derived symbolically: a=q+9-
- L8: Read in full: formal/topics/20-scalar-quadratic/{README,CLAIMS,COVERAGE,VERIFICATION,REVIEW,SOURCE-REVIEW}.md, all 18 reviews/*.md, verification/{run_checks.py,AuditQuadratic.lean,modules.json,manifest.json,build.log,axioms.log,paper-checks.json,paper-sources.json}, all 57 Formal/QuadraticPrecision/*.lean modules, the three result notes, paper-integer-dimension/sections/01-foundations.tex (the actual scalar source; 02-quadratic-finite.tex is topic-26 material per SOURCE-REVIEW) and 02-quadratic-finite.tex head, code/quadratic_rank/{check_simplex.py,check_one_sided.py}.

Checked and found correct:
(a) Declaration existence: every declaration named in COVERAGE.md exists in Formal/QuadraticPrec
- L10: Audited topic 22 (represented-matroid spectral) under the Lean-fidelity lens. Everything below was checked and found correct; do not repeat.

DECLARATION EXISTENCE: extracted every backticked identifier from COVERAGE.md (all 37 claim rows) and matched it against a parse of all declarations under formal/Formal. Every named declaration exists; the only non-matches were prose tokens (m, p, I, qh, ENNReal.top, MatroidSpectral).

UNUSUAL CONSTRUCTS: grep over Formal/MatroidSpectral finds no `sorry`, no `axiom`, no `native_decide`, no `unsafe`, no `implemented_by`, no `partial def`, no `opaque`, no `set_option`. No `sSup`/`iSup`/`IsLeast`/`Real.sqrt`/`Real.log`/`Inhabited` tricks. Only 4 `Nonempty
- L13: Checked and found correct (no finding needed).

DECLARATION EXISTENCE: extracted all 244 backticked names from the CM01-CM49 rows of paper-certified-minlp/formal/COVERAGE.md and matched them against CertifiedMinlp/*.lean — every one exists as theorem/lemma/def/structure/inductive. The only four "misses" (Coordinate.bounded/lowerBounded/upperBounded, unsplit) are inductive constructors, correctly referenced.

UNUSUAL CONSTRUCTS: no sorry, axiom, native_decide, unsafe, implemented_by, partial def, opaque, or check-weakening set_option anywhere in CertifiedMinlp/, CertifiedMinlp.lean, Verify.lean, or verification/ExtensionAudit.lean. The five noncomputable defs (realMonomial, extendedOptimum, q
- L4: Repository root: /home/sgusev/repo/minlp-notes. No mathematical error, false statement, or unproven theorem was found in cluster L4; the cubic development is unusually careful and the Lean statements are faithful to the informal claims. Checked and found correct:

UPPER BOUND (31/12). Worked through every case of paper-cubic-gap/main.tex Sections 3-4 by hand and re-derived all deficiency formulas from the law definitions: D_O = (1/2)min(u,a)+(1/4)min(u,b) and D_B = (1/2)min(u,2a)+(1/4)min(u,2b) for one low coordinate; D_O = D_B = a/2+b/4 all-high; D_I = u(a+b-ab); the bilinear cases; the four-case split for 18D_O+7D_B >= 12min(u,a+b) (brute-forced over a rational grid in Python: no violation
- R8: I worked through all nine assigned notes line by line, re-derived the main proofs, and ran independent exact-arithmetic checks. I found no major or moderate defect; only the three minor documentation/attribution items above.\n\nVERIFIED CORRECT (proof steps re-derived by hand):\n1. positive-multilinear-marginal-floor-gap.md. Confirmed the variational setup: cav of a positive multilinear polynomial on the cube is the sum of monomial cavs (comonotone threshold law), monomial gap T_e = min(u, S) equals cav-vex exactly (u - max(0,u-S)), and chgap = max over laws of the weighted anchor deficiency (sign and direction correct). Checked: density h integrates to 1; clipping/completion q'_p in [q_p,1]
- P2a: Read in full: paper-integer-dimension/main.tex, sections/00-introduction.tex, sections/01-foundations.tex, sections/02-quadratic-finite.tex, coverage.md, plus abstract.tex, formal/COVERAGE.md, formal/topics/20-scalar-quadratic/COVERAGE.md, verification/stage1-corrections.md, verification/stage2-corrections.md, reviews/whole-round1/summary.json, revision-20260907/PROCESS.md, and the cached primary sources ggow2020.txt and iqs2018.txt.

Verified correct by re-derivation (section 01): lem:parity (parity classes, closure argument, finite-mixture case); lem:disjunction (integral convex combination of distinct binary codes has single-index support; bounded/common-recession cases); eq:strong-midpoi
- P5: Read in full: paper-network-simplex/main.tex, all ten sections/*.tex, README.md (appendices/ is empty — no files exist), plus tables/*.tex, verification/*.json and *.txt, revision-20260909/{FINAL_REPORT,final-adjudication,final-corrections,final-validation.json,literature-audit}, formal/topics/{06-network-simplex,15-flat-chain-threshold}/{COVERAGE,VERIFICATION}.md, and the local De Loera–Onn primary text.

Mathematics checked step by step and found CORRECT (do not redo):
- prop:disaggregation and cor:integral-flows (including the empty-P and zero-weight cases and the multigraph vertex-integrality argument).
- lem:block-factorization, thm:block-state-reduction (proportional refinement eq:prop
- P1a: Read in full: papers/pooling/main.tex, sections/00-introduction.tex, 01-foundations.tex, 02-algebraic-complexity.tex, 03-restricted-hardness.tex, source-index.md; plus papers/pooling/README.md, process/coverage.md, process/root-stage-03-check.md, notes/pooling-positive-tolerance-extension.md, and the local literature copies of abrahamsen2022 (ETR-INV), abrahamsen2019 (dynamic toolbox), haugland2016.

Checked and found correct (step-by-step re-derivation):
- Sec. 1: destination decomposition (s1:destination), single-product projection (s1:single), sign test inequalities z*<=z_best<=z*/m<=0 and the destination-flow relaxation chain; shortest-path criterion (s1:paths) including the K+1 support 
- P7a: Read in full: paper-structured-bilevel/main.tex, sections/01-foundations.tex, 02-exact-responses.tex, 03-robustness-screening.tex, 04-accuracy.tex, README.md; plus supporting material (process/coverage.md mapping, process/assessments/stage08-round01.md, results/bilevel-fixed-block-response-algorithm.md, results/bilevel-convex-aggregate-accuracy-bit-algorithm.md, results/bilevel-response-constraint-accuracy-bit-algorithm.md sections 10-12, appendices/c-quantitative-bounds.tex lem:polynomial-bregman and prop:accuracy-response-modulus, data/table-screening.tex, data/table-full-task.tex, data/stage06-results.json, delivery/final-artifacts.json).

Checked and found correct (no finding needed):
- 
- P6: Read in full: paper-power-flow/main.tex, sections/00-07, appendices/arithmetic.tex and verification.tex, README.md, all four checks/*.py, process/coverage.md, revision-20260907/STATUS.md, COMPLETION.md, final-adjudication.md, final-review1-5 headlines, the source note results/ac-power-flow-existential-reals.md, and the README.md repo entry. Verified by hand (all correct): pinned-bus equation and the a+b=5/2 complement involution; addition gadget algebra; inversion gadget chain C_I -> v_I=x, I -> v_W=2x-1+1/x, D -> y=v_W-2x+1=1/x; the W range [2sqrt2-1, 7/2] subset (1,4); the free-injection bound 4*3*2*(7/2)=84<85; degree-3, simplicity, and the size bounds n+16m / 18m (at most two path extens
- P1b: Read in full: papers/pooling/sections/04-structural-algorithms.tex, 05-contract-algorithms.tex, 06-synthesis.tex, appendices/A-response-geometry.tex, B-rank-one-costs.tex, C-rank-one-convexification.tex, source-index.md. Cross-read: papers/pooling/README.md, results/rank-one-{row-column-hardness, zero-lower-hardness, correlation-face-conic-lower-bounds, correlation-face-stability, approximate-sdp-lower-bound, low-rank-costs}.md, results/pooling-{bypass-structure-algorithm, fixed-product-contracts-algorithm, two-source-qualities-convex-feasibility, contracted-common-capacity-algorithm}.md, and sections/03 (s3:hoffman, s3:constant-thm) for the two cross-section dependencies.

Verified correct 
- P9: Read in full: main.tex, all seven sections/*.tex, all four appendices/*.tex, macros.tex, README.md; plus process/coverage.md, process/stage07-r01-assessment.md and reviews 1-2, formal/topics/21-dag-spectral/{COVERAGE,VERIFICATION}.md, formal/topics/22-represented-matroid-spectral/VERIFICATION.md, supplement/README.md, supplement/source_kinetics/README.md, and many saved JSON artifacts.\n\nMATHEMATICS VERIFIED CORRECT (step by step, with independent sympy/fractions checks where numeric):\n- Prop 2.2 (gating Schur identity, equality iff B^T A^{-1}F_S=0), Prop 2.5 (Kantorovich sandwich; the compression step K ⪯ ((M+m)I-A)/(Mm) ⪯ αA^{-1} and the rank refinement min(p,r_S)log α), Cor 2.6 (D-, wei
- P2b: I read 03-scalar-nonlinear.tex, 04-vector.tex, 05-conclusion.tex and coverage.md in full and re-derived the main proofs. Verified correct (no findings): (1) lem:scalar-chords — three-piece refinement N_eta<=3N_{2eta}, the factor-two max-vs-midpoint concave-gap bound, N_{2eta}<=2^pconv, and the resulting pbin<=pconv+2. (2) thm:curvature-mass — I re-derived eq:mass-local-remainder (E<=m^2+3m/2) including both branches of rho_eta, the left-end Taylor-remainder chord bound, the tent-kernel bounds J>=g(c)l^2/16, E<=8, the potential inequality eq:mass-potential in both cases l<=d and l>d, the telescoping M_eta<=24N_eta, rho_eta<=2rho_{2eta}, and the constants 49 and +2 in eq:mass-dimension-law. (3
- P8: Read in full: complexity/main.tex, abstract.tex, all 14 sections/*.tex, all 6 narrative/*.tex (needed because the main theorems thm:main-* live there), README.md, coverage.md, process/completion-coverage.md, process/completion-s7-adjudication.md, formal/topics/16-potential-flow-certificates/COVERAGE.md. Re-derived and confirmed correct (by hand and with numeric/exact checks): (1) Appendix K in full — the asymmetric cubic conjugate E_e*(d)=(2/3)sqrt(|d|^3/c), the Fenchel lower bound L<=E(x*), the scalar modulus (u|u|-v|v|)(u-v)>=|u-v|^3/2 and the resulting D_e>=beta_L|y-z|^3/6 and eta-radius, the reverse-Bregman derivative 2c^{sgn z}|z|(z-y) and sublevel-interval argument, prop:a-cert-signs (
- P7b: Read in full: paper-structured-bilevel/sections/05-boundaries.tex, 06-computation.tex, 07-conclusions.tex, appendices/a-fixed-core.tex, b-inverse-approximation.tex, c-quantitative-bounds.tex, d-path-geometry.tex, README.md; plus main.tex, process/coverage.md, process/assessments/stage08-round01.md, process/STATUS.md, results/bilevel-leader-vertex-integrity-boundary.md, notes/audit-20260924-repository-issues.md (relevant entries), code/summarize_experiments.py, code/check_full_task.py, code/original_faces.py, code/run_experiments.py, code/bilevel_reopened/screening_milp_comparison.py, data/stage06-results.json, data/table-*.tex, code/bilevel_nonconvex/benchmarks*.json, code/bilevel_reopened/s
- P10: I read paper-switching-control/main.tex, all fifteen section files, macros.tex and README.md in full, plus the supporting evidence (verification/ logs, stage06 results.json and generated tables, verification/reference/certificates_general_four_block.json, process/stage07-acceptance.md, process/claim-coverage.md, formal/topics/01-switching-control/COVERAGE.md+VERIFICATION.md, formal/topics/17-grid-switching/COVERAGE.md, notes/audit-20260924-repository-issues.md, and the local copy of Sager-Zeile 2021 in literature/papers/sager2020-on-mixed-integer-optimal-control/fulltext.md). I re-derived every nontrivial proof step by hand and ran independent Python (fractions/sympy/numpy) checks. Everythin
- R10: I read all eleven assigned files in full, plus review notes notes/review-pooling-bypass-structure-second.md, review-pooling-quality-rank-extension.md, review-pooling-bypass-vertex-cover.md, review-pooling-contract-exceptions-arbitrary-qualities-benders.md, review-pooling-facial-quality-structure.md, review-pooling-triviality{,-second}.md, review-pooling-degree-two-boundary-projection{,-second}.md, review-pooling-feasibility-output-degree-boundary.md, plus notes/pooling-fixed-rank-contract-exceptions-algorithm.md, the README entries (lines 516-640, 870), notes/audit-20260924-repository-issues.md (R10 rows and coordinator hand-checks), the committed checker logs, and the local literature copie
- R10: Read all 11 assigned files in full plus their review notes, the cited checkers, the README entries (lines 516-529, 605-640, 870-874) and papers/pooling/sections 01, 04, 05. All internal links in the 11 notes resolve. No major or moderate mathematical defect found; the two moderate findings are README scope omissions.

RE-DERIVED AND FOUND CORRECT:
- fixed-core-block: vertex candidates and feasibility signs (2); comparison polynomials (3); F_sigma = H_sigma*(lambda^T w - sum_j rho_j) with H_sigma>0, so (4)<=0 <=> (5); Lemma 2 both directions (an empty block discards every sign condition containing (x,lambda); Minkowski-sum support characterization); polynomially many realizable sign condition

- R9: Checked in full and found correct (no further work needed on these points):

GENERAL ETR (results/pooling-existential-theory-of-reals.md). Re-derived Lemma 4 (each arc lies in at most two forced groups; costs exactly {0,-1,-2}; profit = sum of group totals <= zeta with equality iff all forced nodes saturated). Lemma 5 emission: at the saturated terminal t (cap 2, pinned 1/(2B)) the mass equation is a*x_Qt = 1, forcing a>0, x_Qt = 1/a <= 2, hence a >= 1/2; relay quality is 0 whether or not p' carries flow; converse checked including the boundary cases a=1/2 and a=2. Quality flip (4.3) verified: free arc of s_3 carries x_{s'p_2}; t_2 vacuous so p_2,p_3 qualities are irrelevant. Range enforceme

- R12: No mathematical error, proof gap, or false statement was found in cluster R12. Verified in detail (re-derived or symbolically checked, not merely read):

(1) cia-three-switch-heavy-mode.md: normalization/extension to T=5E and the one-block endpoint rules max{A_i(b), m_i-ℓ} (positive) and max{0, ℓ-A_i(b+ℓ)} (negative) are correct from monotonicity of A_i and of t-A_i. All three mass cases (m_q>=3; at most one mass >2; two masses >2) are exhaustive and each schedule's four-block discrepancy checks hold, including the deadline-order contradiction argument (both the pre-q slot start ℓ-1 and the post-q slot start ℓ+1 versions, with the non-strict contribution A_q>=1 sufficing). Case 3's bounds b>

- R9: Checked in full and found correct (no math errors located):\n\n(1) results/pooling-existential-theory-of-reals.md. Re-derived Lemma 4 (cost = -(#forced groups), costs in {0,-1,-2}, group-sum identity, equality iff saturation), Lemma 5 (w_Q=a/B, w_{p'}x_{p't}=0 in both throughput cases, a·x_{Qt}=1 ⟹ a>0 and 1/a≤2, relay-source split, converse), the quality flip, Section 4.4 inverse pools and the range derivation 1/v≤2, 1/(5/2-v)≤2 ⟹ v∈[1/2,2], the inversion gadget ((x/B)y=1/B ⟹ xy=1, x=y case), the addition gadget (w_{p_+}=0, x_{R̄_z t}=5/2-x-y=5/2-z ⟹ x+y=z, infeasibility when x+y>5/2 is harmless), 4.7 slack/diluent bookkeeping (slack ≥ B-2M=3, diluent B-a≥0), the M count (P_v ≤ m+1, R_v ≤ 2
- R11: I read all nine assigned files in full plus notes/review-cia.md, review-cia-three-mode.md, review-cia-two-switch-equal-masses.md, review-cia-two-switch-global.md, review-cia-exact-two-switch-general.md (and headers of review-cia-exact-two-switch-root.md, review-cia-distinct-reach-general.md, review-cia-reopened-{finite-grid,finite-grid-code,practical-algorithm,fixed-budget,grid-transfer,small-grid}.md), README.md lines 888-920, formal/topics/17-grid-switching/COVERAGE.md and VERIFICATION.md, code/cia_reopened/minimax.py, and the local Sager-Zeile fulltext.

VERIFIED CORRECT (re-derived by hand, step by step):
- cia-uniform-switching-obstruction.md: the n=5,N=T=45,s=1 counterexample (D(k)=max

- R12: Read in full: results/cia-exact-three-switch-worst-case.md, cia-three-switch-global-upper.md, cia-three-switch-heavy-mode.md, cia-arbitrary-block-one-sided-bound.md, cia-universal-heavy-mode-rounding.md, cia-arbitrary-switch-global-bound.md, cia-seeded-arbitrary-switch-bound.md, cia-five-mode-four-block-reach.md, cia-general-four-block-reach.md; all six matching review notes plus notes/cia-reopened-general-reach.md and notes/review-cia-reopened-general-reach.md; dependency results/cia-exact-two-switch-worst-case.md (three-block reach) and results/cia-uniform-switching-obstruction.md (uniform value, valid for 0<=s<=n-2, so s=3 needs n>=5 as used); code verify_general_four_block.py, verify_n5_

- R13: I found no major or moderate defect in cluster R13. Verified in detail:

FIXED AGGREGATE (results/bilevel-fixed-aggregate-response-algorithm.md): polyhedral KKT necessity without CQ (valid: normal cone of a polyhedron is generated by equality + active inequality normals); the clipping equivalence z_i=clip(-B_i/a_i) and the threshold signs L_i=B_i+a_i l_i>=0 -> z_i=l_i, R_i=B_i+a_i u_i<=0 -> z_i=u_i (re-derived from the box normal cone, correct); Z_i^sigma = l_i Q, u_i Q, -B_i prod_{j!=i}a_j and degree (N+1)delta; R_sigma = Q^2 f(x,z^sigma) (verified algebraically); upper-monomial clearing c x^alpha prod Z_i^{e_i} Q^{delta-sum e_i} of degree O((N+1)delta^2); polynomial monomial count binom(M+

- R13: I attacked all seven statements for counterexamples inside the stated hypotheses, checked boundary regimes, and compared note/README/paper wording. I found no major or moderate defect. Verified in detail:\n\nFIXED-AGGREGATE (results/bilevel-fixed-aggregate-response-algorithm.md): polyhedral normal-cone KKT necessity without CQ; equivalence of box stationarity with clip(-B_i/a_i) using a_i>0; correctness of the threshold signs L_i=B_i+a_i l_i, R_i=B_i+a_i u_i and the degenerate cases L_i>=0 & R_i<=0 (forces l_i=u_i) and boundary agreement; realizable-sign-condition count O((N delta)^k) polynomial for fixed k (no 3^N product); Z_i^sigma = -B_i prod_{j!=i}a_j and Q z_i identities; R_sigma = Q^2
- R16: I worked through every theorem, lemma and constant in the ten assigned files, recomputed the displayed constants, and re-derived the inequality chains. I found no mathematical error, no unproven step, and no unsupported verification label. Details of what I verified as correct:

QUADRATIC-INTEGER-PRECISION-APPROXIMATION-HARDNESS: max over box of the convex f_G equals M(G); the zero-integer LP {0<=x<=1,0<=w<=eps} is valid iff M(G)<=eps; the midpoint obstruction ((1/2)1, M(G)) with f_G((1/2)1)=0 gives the converse; eps=k-1/2 makes p_conv=0 iff M(G)<k (coNP-hard on the family). Parity packing of 2^t points forces p>=t. The exponent arithmetic C(tn)^(1-delta)/t = C n^(1-delta-q*delta) < 1 for q 

- R15: I read all nine assigned files in full, with their review notes and cited check scripts. I recomputed the main steps; everything below holds.

(1) results/quadratic-rank-integer-complexity.md
- Geometric lemma checks out: maximal-simplex enclosure via Cramer (|c_i|<=1); polarization bounds |G_ii|<=2δ and |G_ij|<=3δ; row norm <=3√d δ; Hadamard; det G=(det A)^2 det M. The δ=0 case is handled.
- Midpoint deviation is (1/8)(s-t)^T H(s-t), so δ=4ε. Volume summation gives exactly the constant |det H|^(1/r) V^(2/r)/(48√r).
- A nonsingular principal r-minor exists because e_r(eigenvalues) equals the product of the nonzero eigenvalues.
- Sawtooth upper: L=ceil((1/2)log2(A/(4ε))) gives A 2^(-2L-2)<=ε.
- R15: I checked every main proof in cluster R15 step by step and found no major or moderate errors. Details:

- **Scalar rank note.** The maximal-simplex enclosure, the polarization bounds (|G_ii|<=2δ, |G_ij|<=3δ), Hadamard's inequality and det G=(det A)^2 det M are correct, including the δ=0 case. The midpoint identity (1/8)(s-t)^T H(s-t), which gives δ=4ε, is correct. I re-derived the constant 48√r. The principal-minor existence argument and the slice restriction for rank r<n are correct. The sawtooth upper bound's depth L=ceil((1/2)log2(A/(4ε))) and binary count rL are correct.
- **Inertia note.** The negative-eigenspace slice, the one-sided midpoint gap m||s-t||²/8, the isodiametric constant ε
- R11: I found no major or moderate issue in cluster R11. I read all nine assigned result files in full, checked every main proof step by step, and tried counterexamples and boundary cases. Checks and outcomes:

(1) cia-uniform-switching-obstruction.md
- The n=5, N=45, s=1 counterexample holds: D(k)=max{9,4k/5,36-k}, the optimum is 16 at k=20, and the conjecture gives 15.5. The 16m versus 15m+1/2 scaling is also right.
- The continuous uniform formula E_{n,s} is correct. The lower bound allows repeated modes, the block endpoints t_j=T(r^j-1)/(r^m-1) give discrepancy exactly -E_0, and the s=1 specialization and the limit T/(s+1) hold.
- The discrete recurrence theorem is correct, including the repai

- R16: I found no mathematical error, no proof gap and no materially false verification label in cluster R16. I rederived the following steps and found them correct.

GENERAL NORM: the output-image section p(f,K) = p(g,K_eff) holds in both directions and needs no error-in-image assumption. The radii (3) and the nonzero pulled-back separator are correct. The volume threshold eta rules out the small-volume branch because the cube [-r/d,r/d]^d lies inside the inner ball and has volume > eta. Symmetric averaging gives E_0 subset K_eff subset beta E_0 with W = d(d+1)^2 A. The direction of (5) is right: a larger error body gives a smaller minimum. Scaling P/alpha gives (6). With d <= n(n+1)/2, the additi

- R14: I read all seven assigned result files in full, plus their review notes and the cited checkers. I found no major or moderate defect. Every claim below was re-derived by hand and found correct.

(1) scalar-leader-spd-box-np-completeness:
- 3SAT normalization to three distinct variables per clause.
- Identity r_i(x_b,b) = b_i - 3t_i + 1, with residual ranges [1/(2*3^(n-i)),1] and [-1,-1/(2*3^(n-i))].
- Cross-term bound 6rho/(1-3rho) < 1/(10*3^n) and margin (1).
- Conditional minimizers for p and v. Auxiliary feedback 2eta + 2m*xi < 4eta = w_n/(25*3^n).
- Identity F = 2D + 2*sum shortfall. The rounding argument, including ties at 1/2, gives F >= 2.
- Continuity and attainment, bit lengths, and 
- R19: I found no major or moderate issue in cluster R19. Items checked and found correct:
(1) spatial-bb-exponential-lower-bound. Lemma 1 (vertex argument). Chord domination of every convex underestimator, including McCormick with y=1-x and alphaBB at alpha=1. Step 1 bound |M∩R| > h. Step 2 hypergeometric avoidance bound, with min correctly replaced by the max of the bases (the first review's max/min error is fixed in the current text). Specialization (3/2)^{t(1/4-eps)}, and (3/2)^{n/24} at eps=1/8. Bound at most e^{k/4} for fixed k, using m <= n-k. Proposition 2: node count 2^{n+2}-3, and the (1-alpha)/2 corner bound. Remark 7: tree size n^2+n-1 nodes and n(n+1)/2 leaves for k=1; C(n+1,k+1) leave

- R18: I found no major or moderate errors in the 12 R18 notes; the three minor items concern verification evidence and consistency, not the proofs. I checked each proof line by line and recomputed the constants.

(1) convex-vector-curvature-rank: correct.
- The level-cut lemma gives 2H-1 intervals, including plateau and exact-level cases.
- The max-determinant basis gives |c|<=1, and nonnegative gaps of original outputs give g_j<=g_Psi despite signed coefficients.
- The parity-hull midpoint argument needs no closedness of the lift, and max gap is at most twice the midpoint gap.
- The finite bound (4r-1)2^p is correct.
- Determinant-exchange termination is correct: min minor >= q^-r >= 2^-rL, max <
- R21: I found no major or moderate issue in cluster R21. The main theorems, proofs, and displayed constants check out line by line; the only finding is one minor unsupported claim that an independent reviewer reran the parallel-path verifier. Lean builds and the repository's experiments were not run, as instructed.

Common-factor notes:
- Reciprocal-anchor hulls: the one-leaf moment-interval proof and the zero-denominator cases are correct. The PSD congruence holds; I recomputed it from the (m, 1, 2w-m; t, 2q-1; m) moment-cut matrix. The two-leaf witnesses are exact: both have mean 2, reciprocal moment 3/5, and one-leaf bound equality. The Cauchy-Schwarz support argument is sound. Both tangent-def

- R21: I found no major or moderate issues in cluster R21. All three findings are minor: a wrong review-section reference in the fixed-linking note, a one-sided (partly self-referencing) LP check for the continuous many-leaf hull, and one comparison sentence in the series–parallel note that overstates.

What I checked and found correct, attacking statements and boundary cases:

**Universality** (results/network-simplex-universality.md):
- The local De Loera–Onn full text confirms the layer-one injection sigma(i,j,k)=((i,j),(1,k),1) in Section 3.3.
- The padding row/column makes all layer totals D_k positive.
- Lemma 1: section equations (2)–(3) give exactly the three margin families, layer 3 follow
- R20: I reviewed the R20 cluster (12 result files) line by line, together with their review notes and cited code. I found no major or moderate issues. What I checked and found correct:

(1) rank-one-correlation-face-conic-lower-bounds:
- Lemma 1: the trace-face characterization.
- Theorem 1: the face F_m is affinely isomorphic to COR(m), including the inverse map.
- Lemma 1b: the exposing functional g, with every inequality step rechecked and coefficient magnitude 4m+2.
- The lift transfer under affine sections.
- The Fawzi-Parrilo constants c(d)=(1-3^-d)^(-1/d) and kappa(d)=(3^d-1)^-(1-1/d), checked against the arXiv PDF Theorem 1 with m>=d.
- The SOCP-to-S_+^2 reduction and the n=2 nonpolyhedral
- R14: I read all seven assigned result notes in full, along with their review notes. These were: review-bilevel-well-conditioned-box-exact-hardness, -hardness-second, -near-identity-corollary-second, -conditioned-box-additive(+second), -bounded-power(+second), -fixed-resource(+second, including the Section 8 and one-resource Section 9 addenda), -one-resource(+second), -leader-vertex-integrity(+second), and -dense-box-hardness(+second). I also read the matching sections of paper-structured-bilevel (05-boundaries.tex lines 1-622 and 04-accuracy.tex lines 1-280) and the README.md entries. I compared the notes/ predecessors with the results/ versions: the differences are status and source paragraphs p
- R17: I found no major or moderate issues in R17: every main theorem, constant, and verification label checked holds up. Most steps were re-derived by hand. Three quick numerical stress tests support them: the scaled Jensen inequality (9), the scaled chord bound (11), and the layer curvature bound (6).

rational-power-compiled-integer-precision:
- Section 2 bisection is correct: the error induction (a+b-1)2^-P, the enclosure logic, tau <= u/16, and the mean-value bound 2tau/u <= delta/8.
- Section 3 chord bound is correct: (D-1)/(2D)(b/a)^{2-2alpha}h^2 <= 2h^2, the first-interval formula h^2(theta-theta^D), the band (4), and the error 4h^2 + 2D*delta <= 3p/8 with L = ceil(.5 log2(1/p)) + 2.
- The 
- R17: I re-derived every main step in the 11 assigned notes and found no major or moderate issue.

rational-power-compiled-integer-precision:
- Section 1: circuit compilation, the AND/NOT and product constraints, and forcing of integral wires are sound.
- Section 2: the rounded-power error (D-1)2^-P (induction (a+b-1)), the uncertain-comparison inverse bound 2tau/u<=delta/8, and the bisection and precision counts are correct.
- Section 3: the chord bound [(D-1)/(2D)](b/a)^(2-2alpha)h^2<=2h^2, the first-interval bound h^2, 4h^2+2D delta<=3p/8 with h^2<=p/16, and polygonal-path coverage with non-monotone knots are correct.
- Section 4: the count Phi+3r+1/(2ln2), and (6) with A_r<7r/2, are correct.
-
- R18: No major or moderate issues found in R18. Every theorem's proof chain and constants were checked step by step, and each was attacked with edge cases. (1) Curvature-rank box theorem: the direct level-cut lemma giving 2H-1 intervals (plateaus, level equal to the maximum, no retained level); the max-determinant basis coefficient bound of 1 and the determinant-exchange bound of 2 with termination count 2rL+log2(r!)+1; that signed coefficients are harmless because the basis consists of original convex outputs; parity-hull midpoint gap <= r and full gap <= 2r; the (4r-1)2^p and (8r-1)2^p counts; the band error 1/8+13/16=15/16; 486*(8r-1)<4096r. (2) Facet version: rank-zero via positive column entr
- R20: I read in full all 12 assigned notes, their review notes, the README entries, and the matching sections of paper-relaxation-limits (appendix-rank-one, 01-foundations bilinear section, appendix-fbbt, appendix-scaling). No major issue was found. Findings are four minor items: a log factor dropped by a cited headline bound, two unsaved or missing verification scripts, and a redundant inequality in a facet list.

Correct by step-by-step checking:

**Conic lower bounds note**
- Lemma 1 (trace face) and Theorem 1 (nested faces giving COR(m), including the block inverse).
- Lemma 1b: T <= m+2mB+4mD, coefficient bound 4m+2, and g >= B+D.
- Lemma 2 (affine sections and images of lifts).
- The Fawzi-P
- R19: I found no major or moderate problems in cluster R19. I read all nine result files in full, together with the reviews notes/review-spatial-bb-{lower-bound,second,sdp-rlt,higher-sos,product-domain,relative-gap,bounded-monomial-lift,beyond-clique,beyond-clique-second}.md, notes/review-mip-relaxation-binary-lower-bounds.md, notes/review-geoffrion-property-p.md, notes/mip-binary-lower-bound-extensions.md and notes/spatial-bb-known-clique-cut.md. I also read the code in code/spatial_bb_lower_bound/*.py and code/geoffrion_property_p/check.py, and checked the relevant parts of Schoenebeck's primary PDF (Theorems 11-12, Lemma 13). Checked step by step:

(1) Separable-relaxation theorem. Lemma 1 (ver

- N5: I found no major or moderate issue in cluster N5; the four findings are minor wording, consistency and provenance problems.

constant-data-messages: I rederived identity (3), D_z, the Cauchy-Schwarz equality point (attained and feasible), centers in [0, θ/(1-θ)], and the minimum separation θ^n, which needs θ²-3θ+1 ≥ 0. I also rechecked the θ^n/3 unique-activity window (C_θ < 4) and the polynomial-identity lower bound of Theorem 2. For the matrix K, I rechecked the entries (-θ, -θ, θ²), the row sums (internal state 3θ+θ², control θ+θ², terminal 2θ) and the Gershgorin bounds (4). I checked the graph, the Prop 3 lift (d_i ≤ -4, bound n+10.2k, baseline n+t²) and the linear-coefficient bound of 8

- N1: What I checked and found correct:

DAG approximation set (notes/research-20260912-dag-psd-approximation-set.md):
- Rational LDL factors without square roots; zero leading pivot of a PSD matrix forces a zero row and column.
- L, Pi, T, K identities: TK = I, KT = Pi, and Q = K(TQT^T)K^T, which needs both symmetry and the exact range test.
- Existence of the dyadic tau with 1 <= tau^2 w < 4.
- Lower bound (6), A(P) >= I_r, via owner forcing.
- Maximum-volume argument |x_i| <= 1, giving transformed coordinates below 2 and diagonal entries at most 4p for the target's prior and edges.
- Signed-floor residuals in [0, Nh) and |Delta_ij| < Nh even for paths of different lengths; row-sum bound ||Delta
- N7: I read all 12 assigned files in full, plus the related sections of results/infinite-quadratic-aggregation-hhc.md, results/cluster-free-branch-and-bound-constrained-minima.md (header and strict-complementarity section), results/four-aggregation-strict-pdlc.md (header), paper-quadratic-aggregation sections 05 and 07, appendix three-dimensional-span.tex, the formal overview (09) and formal accuracy (94) sections, the Lean topic 31 README, CLAIMS, COVERAGE and VERIFICATION files with build and axiom logs, the Lean AccuracyModel and Accuracy theorem statements and core definitions (Good, closedRegion, feasible), code/research_20260922/check_infinite_aggregation.py, and the relevant BDS statements
- N3: Checked in full, with independent recomputation. I found no major or moderate issues in this cluster.

(1) Noisy-Markov memory theorem (scalar):
- Coefficient bound (4) and excluded-covariance bound (5), derived via fresh-filter propagation.
- Residual-pair majorants (6a) and (6b), including the overlapping-history range d in [L+1-h, L].
- Two-sided row sum and closed forms: sympy/numeric checks confirm that the row sum equals delta_L in (2) and the gain version (2g) = base_tail + kappa(delta_L - base_tail).
- B B^T vs B^T B congruence argument for (3); information sandwich; bounds (7)-(11), including the prior-aware tangent.
- Exact example Cov(Z3,Z2) = -1/32, verified in sympy.
- Random-in
- N6: I read all 12 assigned files in full, plus the linked reviews: vc-grid-moments, higher-gap-cover, planar-curvature and planar-topology (partly), and oracle-transfer. I also read the hardness result the magnitude note uses, the results and README entries that cite these notes, and the checkers check_approximation_exact_smoothing.py, check_envelope_higher_moments.py, check_moment_control.py and check_smoothed_block_dp.py. I found no major or moderate error. All four findings are minor. Proofs checked step by step and found correct:

(1) Approximation-exact-smoothing:
- The affine-rank bound: at most 2^d binary points in a d-dimensional affine subspace; the unimodular volume bound; the union co
- N2: I found no mathematical errors in the ten N2 notes. The three findings are minor wording and status-label issues.

The following were checked step by step and found correct.

Fixed-parameter D-optimal FPTAS:
- Rational pivoted-LDL factorization of singular PSD matrices.
- Maximum-volume basis coordinates |x_i|<=1 and the dyadic normalization I<=TBB^T T^T<4I, which gives transformed diagonal entries <4p and entries <=4p.
- The owner-mask requirement giving A*>=I.
- Signed-floor residuals in [0,Nh), then ||A_hat-A*||<=pNh=eta/p, (1-eta/p)^p>=1-eta, and the zero-optimum fallback.
- The state bound C=ceil(8p^3N^2/eta+N)+2.
- The noisy corollary: (1-eta)[(1-delta)/(1+delta)]^p>=1-epsilon with del
- N4: I read all 12 assigned notes in full, plus their review notes: latent-separator theory, implementation and certificate reviews; robust-certificate, robust-solver and robust-dense reviews; dense-certificate and kinetics-dense reviews; polynomial-tube, rational-flow, ODE-theory and fixed-physical-grid reviews. I also cross-checked README lines 98-108, the closeout, and paper-correlated-measurements sections 04-certification (robust and separator subsections) and 05-computation (robust, grid and nested-anchor subsections). No major or moderate issue survived checking.

Latent-separator theory and certificates:
- Checked: the Woodbury/Schur identity; completing the square for arbitrary G, giving

- N10: I read all 16 assigned notes in full, plus their review notes, the relevant README/results/paper passages, and the saved checker logs.

What I verified and found correct:

**all-product-contracts (quasipolynomial feasibility)**
- Local elimination, rows (2), and the global identities (1)-(3), including the zero-throughput case.
- Isolated nodes (q=B_j) and cycle opening with the diagonal constraint.
- The Section 7 capacity counterexample: V_A=1/(2q), V_B=1/(2(2-q)), T=1/(q(2-q))>=1, q in [1/2,3/2]. Recomputed.
- The quasipolynomial bound depends on the separately reviewed one-parameter path theorem, which I did not re-derive.

**bounded contract exceptions**
- The global equations recover p
- N9: I found no major, moderate, or minor validity issues in cluster N9. I read all 13 notes in full, plus their review notes and the relevant README.md, paper, and coverage entries. I recomputed each proof step by hand; the checks below are what I verified.

certified-positive-polynomial-inverse-approximation:
- Term-by-term bounds (2). Derivative majorant (3): (1+1/(4P))^(P-1)-1 <= e^(1/4)-1 < 1/3.
- Boundary comparison: 1/3 + 1/2 = 5/6 < 1, using z0 g'(z0) >= t0. Uniqueness via Rouché and the real-branch identification.
- Panel geometry: half-width tau/(64P); bisection error tau/(128P) <= tau/(64P); ratio 16/63 < 1/2.
- Bottom truncation z <= t^(1/P) <= 2^(-m). Reversion recurrence (8) and the
- N8: I checked every assigned note step by step and recomputed the key constants. No major or moderate errors were found.

- **P-split rotation gap:** Checked the witness p=(2D/3,D/3) lift (bounds 8D^2/9<=U), the distance D/(3sqrt2), the diamond bound (sqrt2-rho)^2+rho^2<=2, and the rational 3-4-5 version (t(p)=34D/15, w(p)=4D/5, inverse-map bounds). Also checked the Section 5 obstruction for any convex Q containing F(0),F(v), since 4v^2/9<=v^2/2, and the Section 6 exactness: f(c)=(d+sqrt(1-c))^2 is concave and decreasing, the intersection of intervals gives the capsule, and the conic representation is right. The determinant claims are right.
- **P-split correction:** Checked that the box vertice
- N11: I checked the assigned notes step by step and found no major or moderate errors. Findings: two minor wording and scope points.

(1) Affine-strip projection (path, tree, fixed total cycle rank). Checked: prefix-product normalization with sign-dependent bound order; shortest-path distances on a bidirected path or tree with nonnegative 2-cycles; the all-pairs condition (1) and the min-formula recovery; the explicit alpha<=beta requirement, which (1) does not imply; zero-gain splitting; reciprocal gains for arbitrary edge orientation; the infimum-versus-attainment scope. The objections in both reviews are resolved in the text.

(2) Path-cut clamp. Rederived the DP recurrence, the identity min(D,

## 6. Limits and method boundaries

- Neither the original audit nor this reassessment reran Lean builds or
  computational experiments. The original audit reports small independent
  arithmetic probes and an import-coverage script run; those historical
  executions were not repeated here. This reassessment inspected retained
  data and code without treating saved PASS labels as fresh verification.
- Novelty and publication priority were not assessed. Literature was consulted
  only where needed to check the scope of a cited result. A discrepancy in a
  source's proof presentation is distinguished from a false repository claim.
- CI status and logs were not inspected. CI-related conclusions concern only
  committed workflow configuration and the wording of repository records.
- The original audit records all 108 assigned auditor tasks as complete.
  Coordinator hand-checks were selective. Completion of an assignment list
  does not establish exhaustive proof or software correctness.
- The original skeptic pass had exceptions, described in Section 7. All 300
  numbered rows were revisited for this reassessment; this is not a rerun of
  every underlying proof audit, solver study, or formal verification.
- A missing artifact, mismatched digest, or old review date establishes only
  the specific provenance limitation supported by the evidence. It does not
  prove a check failed, a review did not occur, or a theorem is false.

## 7. Original adversarial verification record

The table below records the original skeptic pass, before this document
reassessment. Its verdicts and severity labels are historical; the revised
issue tables above give the current conclusions, including M7's downgrade
and the additional refutations.

Every finding the coordinator rated major or moderate after first review was
sent to independent skeptic agents instructed to refute or downgrade it,
except M16 and M17, which the coordinator downgraded without a skeptic for
consistency with the outcome for the formal-record findings. Auditor-rated
moderates that the coordinator recorded as minor from the start (for example
m37, m46, m47 and m272) were not sent. The skeptics rechecked each fact
against the repository (read-only; no Lean builds, no reruns of experiments,
no CI inspection). The two major candidates each received two skeptics, one
rechecking facts and one arguing the case against the severity; each moderate
received one. Outcomes:

| Finding | Verdict | Result |
|---|---|---|
| paper rewrite (former J1) | facts hold, overstated (both skeptics) | now M27, narrowed; several claims withdrawn |
| formal records (former J2) | facts hold, overstated (both skeptics) | split: M19 moderate, the rest minor (m189-m196) |
| M1 | stands | moderate |
| M4 | stands | moderate, repair path added |
| M7 | stands | moderate, mitigation added |
| M10 | stands with corrections | moderate, wording corrected |
| M15 | stands with corrections | moderate, location and scope corrected |
| M19 | stands with corrections | moderate, sharpened with git history |
| M25 | stands | moderate |
| M2 | overstated | minor (m199); most outputs are saved in paper verification folders |
| M3, M5, M26 | overstated (M26 rated moderate by its skeptic) | minor (m200, m201, m204); errata precede the stale body text |
| M11b | overstated | minor (m202); the injected bounds come from SCIP's own presolve |
| M21 | stands with corrections, minor | minor (m186) |
| M22 | overstated | minor (m187); the defect cannot fire on the benchmark families |
| M23 | overstated | minor (m188); the notes cite a correct theorem |
| M24 | stands with corrections, minor | minor (m203) |

After the original M2 correction, the coordinator located saved outputs
that refuted m2, m6 and m113 and partly contradicted m17 and m156. Those were
the original adjudications; the issue tables contain the current reassessment
of missing-output claims.

## 8. Reassessment checks, 2026-09-25

The reassessment used 15 reviewers: 12 groups covering m1–m292, two groups
covering the eight original moderate findings, and one narrative-consistency
review. The coordinator integrated the findings, reconciled conflicting
readings and duplicate reports, and checked the resulting document. All 300
original IDs remain; m293 gives an ID to the broken link already reported in
the original narrative. Refuted and superseded rows are retained as an audit
trail, not as additional defects.

Targeted commands actually run included:

- `git show fa3ed328:formal/topics/17-grid-switching/verification/run.log`:
  located the earlier build/import/replay record used to narrow M19.
- `git show 90eb77ce -- formal/Formal/GridSwitching/Coarsening.lean formal/topics/17-grid-switching/VERIFICATION.md`:
  confirmed that the later change cited in M19 was a comment change.
- `git show 6903d2ec^:code/row_hull/rowhull/rows.py | sha256sum`:
  matched the historical experimental fingerprint, refuting m71.
- `rg --files notes | rg 'gdp.*catalog|catalog.*gdp|gdp.*instance'`:
  found no retained catalog for the broken link in m293.
- `python /tmp/audit-m051-m075-checks.py`: this temporary, read-only review
  script inspected six named manifests, selected archives and existing JSONL
  records. It confirmed all 27 distributed certified-MINLP core files match
  V3 (m57), reproduced 8.21868/8.40256 s using the documented unsolved-run
  penalty (m68), and corrected the saved-data ratios in m72 and m74. It did
  not run a solver, experiment, build or repository verification script.
- Other targeted `rg`, `sed`, `git log` and `git show` reads checked the cited
  passages and their context. Short read-only Python snippets compared
  specific file/archive hashes and recomputed summaries from saved data.
- `git diff --check -- notes/audit-20260924-repository-issues.md`: passed.
  A document-only Python consistency check passed for all 301 unique IDs,
  preservation of the 300 original IDs, seven moderate rows, M7's minor
  placement, four-column finding tables and absence of unchecked candidate
  states.
- `git status --short`: only this audit document was modified.

These are local source, evidence and document checks. No CI check was run or
inspected, and no fresh solver, Lean or manuscript-build result is claimed.

## 9. Fix pass, 2026-09-25

This pass applied the remedies for the 127 rows that remained open after the
reassessment. Refuted and superseded rows needed no change. Fixes were limited
to work that needs no new experiment, solver run, Lean build or replay. Where
a row offered a documentation remedy (label a check as unarchived, identify a
historical snapshot, qualify a scope), that remedy was used. Historical
fingerprints, logs and review records were preserved: they were qualified with
their checked revision, not rewritten. No new review is claimed.

Nine agents applied the fixes, each on a separate set of files. Three
further agents then independently reviewed the resulting diff: one for
mathematics, one for numbers against saved data, and one for provenance
claims. Their corrections are included below.

### 9.1 Work that remained after the first pass

Section 10 records how this work was completed.

| # | Done in this pass | Remaining work |
|---|---|---|
| M19 | Topic 17 records now label build, coexistence and kernel replay as checked at `fa3ed328` and the axiom audit at `80f36418`, and link the earlier log. They state that no retained record covers a build or replay after `80f36418`. | A warning-free build and kernel replay of the current topic 17 sources (Lean rerun). |
| M27 | Every paper-folder README now identifies the revision and date covered by its reviews, archives and manifests. It states that sources changed later (`aee2afbf` and this pass) and that nothing was refreshed or re-reviewed. | If the revised manuscripts are to be distributed: a fresh review of the changed claims, then rebuilt source archives and delivery manifests. |
| m35 | The curve-hull report now lists the actual reruns and records the failed lnts100 model check. It also discloses that the final subtraction in `_piece_lower` is rounded to nearest; the research README repeats this caveat. | Outward rounding in `_piece_lower`, then regenerated cuts and reruns. The scaling version of controls that were not rerun cannot be identified from saved data. |
| m177 | The results note now says historical negative verdicts were classified from the incumbent alone and may include inconclusive runs. | Changing the checker to use the solver bound and status, then rerunning the solver and keeping those fields. |

These rows are marked fixed, but a rerun could strengthen them further:
- M10: validating the `ex8_4_7` linked2 solve on the original model.
- m29: resolving the inconsistent CPU clock in the saved timings.
- m32 and m15: tables regenerated with outward rounding; they are now labelled as nearest-rounded approximations.
- m63: a new extension manifest backed by a fresh run.
- m73: fresh current-code runs for the `uniform` and `uncap` rows.

The archival rows are now labelled, but their missing artifacts could not be
recovered: M1, M7, m4, m7, m26, m43, m76, m86, m109, m133, m162, m173, m178,
m179, m196 and m261.

### 9.2 Changes by area

- **Top-level README:**
  - M25, m3, m24 (BARON three of four), m55, m117, m134, m198, m205, m224, m236, m266.
  - Two further corrections: the SCIP node-separation slowdown is now 4.4–6.3 times, and the `heatexch_gen1/2/3` sentence is limited to numerical evidence for gen1 and structural checks for gen2/3 (see m268).
- **Computational notes:**
  - M10, m22, m23 (shared-variable links).
  - M15, m13, m69, m74 (vertex binarization).
  - m20, m70, m86, m202 (univariate envelopes).
  - m24, m72, m73 (row hull). The saved data also corrected a depth-8 "adds 8–12 s" to 4–9 s.
- **September 22 research folder:**
  - M4 (Section 4b now uses the clipped Definition-9 procedure). The finite-box uses of Lemma 1(b) are justified for that rule. The quadratic results and the 0.7247 rate did not depend on the gap.
  - m31, m201 (iterated OBBT).
  - m12, m28, m29, m30 (ridge envelopes).
  - m78 (research README).
  - m15, m32, m33, m34 (benchmark observations and nuclear).
  - m35 (partly), m75, m185 (curve hulls).
  - m76, m77 (Eigen-CG).
- **Formal records:**
  - M19 (partly), m46, m170, m103 (comment-only change, recorded in topic 17's VERIFICATION.md), m118, m125 (the page count is corrected from 88 to 89), m126, m133, m192, m195.
  - Certified-MINLP formal records: m63, m130, m131, m190, m196.
- **Papers and delivery:**
  - M27 (partly), m49, m79 (cubic gap handled the same way), m94, m144, m146.
  - Manuscript fixes: m53, m143, m145, m151, m270.
- **Results and notes:**
  - M1, m4, m98, m111, m137, m138, m184 (positive multilinear).
  - m43, m44, m162 (spatial branch and bound); m211.
  - m7, m10, m105, m109, m186 (potential flow).
  - m122, m123 (AC power flow). All of audit B's remaining minor requests are now addressed, including the Jeeninga et al. title.
  - m178, m179, m181 (CIA); m217, m218; m127, m207, m208, m225, m226, m230.
  - m172, m173, m174, m175, m177 (partly), m262, m272 (pooling); m14, m17, m223, m267, m268.
  - M7, m25, m26, m167, m168, m169, m238, m242, m243, m244, m245, m246, m250, m253, m254, m257, m259, m261, m293.

### 9.3 Manuscripts and rebuilt PDFs

Source edits were needed in four papers. Each was rebuilt with its documented
`latexmk` command, with no errors, warnings, undefined references or overfull
boxes. Page counts are unchanged.
- **Quadratic aggregation (m53):** `paper.pdf` and `build/final/main.pdf`, 42 pages. The formal supplement does not include the edited section and was not rebuilt.
- **Pooling (m143, m270):** `main.pdf`, 105 pages.
- **Potential flow, Paper A (m151):** `complexity/main.pdf`, 214 pages, built by `reproducibility/build_paper.py`, whose build check passed.
- **Power flow (m145):** `build/main.pdf`, 31 pages. This file is ignored by Git, and the paper has no tracked PDF.

The other fixes' paper counterparts were checked. They already stated the
corrected scope, so none was edited. The paper passage for m184 was left
unchanged because m100 refutes the same complaint against it.

### 9.4 Side effects and observations

- **Recorded digests now differ from current files** because of these edits:
  - The LB-ESH theory and results notes (m168, m169). The theory note states that review digest `7f1a0d0e…` refers to its pre-edit version; the archived publication bundle is unaffected.
  - The cubic-gap and multilinear-gap READMEs, which are listed in their own `SHA256SUMS`. Their mismatch lists say so.
  - Indexed pooling and topic-20 result notes. The topic-20 record now says which fingerprints still match.
  - The source archives and delivery manifests were not refreshed (see M27).
- **Checker output strings left unchanged:**
  - m44: the checker message is corrected, but the saved transcript `paper-relaxation-limits/verification/repository-checks/check_sdp_rlt_strengthening.txt` keeps the old wording as a historical output.
  - m105: the checker's print string is unchanged, because the potential-flow process manifests pin the checker's hash. The results note is corrected.
- **Noticed during review, not changed:**
  - `research-20260922/ridge-envelopes/numerical-verification.md` says the grid gap is "about 1e-3 at N=6". Saved medians are 3.7e-4 (n=2) and 7.4e-5 (n=3), with a maximum of 2.15e-2.
  - `code/row_hull/results/bb_nodes_5x7.txt` duplicates the file in `superseded_pricing_bug/`.

### 9.5 Checks run

- **Numbers:** read-only Python over saved JSON, JSONL, log and text files, to recompute every changed number. The fix pass also ran the repository's read-only summary scripts `compare_rules.py`, `consistency.py` and `review/volume.py`.
- **Provenance:** `git log`, `git show` and `git archive` against every cited revision. `sha256sum -c` of the affected manifests, both on the current tree and on archived snapshots. Byte comparisons of archive contents against their cited revisions.
- **Files:** `python -m py_compile` on the two edited Python files. A relative-link check of the edited Markdown files. `git diff --check` on the whole working tree.
- **Papers:** `latexmk` builds of the four edited papers, then `pdfinfo` and `pdftotext` to confirm page counts and that the corrected wording appears in each PDF.

No experiment, solver run, Lean build, replay, axiom audit or project-wide
verification was run, and CI was not inspected.

## 10. Second fix pass, 2026-09-25

This pass did the remaining work that needs no large experiment. After an
out-of-memory restart, every computation ran one process at a time. A
separate agent then reviewed all changes; its corrections are included below.

### 10.1 Rows completed

- **M19:** Topic 17 was rerun on current sources at `549a5786`, with each
  module rebuilt from source. Results:
  - `lake build --wfail`: 23 of 23 modules, zero warnings.
  - Coexistence import and import coverage (813 modules) passed.
  - Axiom audit: 1,921 declarations, only `propext`, `Classical.choice` and
    `Quot.sound`.
  - `leanchecker` kernel replay: 23 of 23.

  Log: `formal/topics/17-grid-switching/verification/run-2026-09-25.log`.
  The module line count in VERIFICATION.md is corrected to 15,481; the
  earlier 15,432 matches no recorded revision.
- **m35:** `_piece_lower` now rounds its final subtraction downward. The new
  script `research-20260922/curve-hulls/code/cuts_rounding_check.py`
  rechecked all 16,539 saved cuts in 30 files. None is stronger than a
  certified bound:
  - 1,462 equal the corrected constant.
  - 15,066 of the rest were certified by the corrected code.
  - 11 with slacks below the float margins were certified with 200-bit
    interval arithmetic.

  No solver rerun was needed. The lnts100 model check now passes
  (`modelcheck_lnts100.out`). Two limits remain:
  - Cut files that later runs overwrote cannot be rechecked.
  - The scaling version of the controls that were not rerun is still unknown.
- **m177:** A NO verdict from the pooling checker now requires INFEASIBLE
  status or `ObjBound` below the threshold minus 1e-6. The reviewing agent
  removed a first-draft shortcut that accepted any OPTIMAL status, because
  OPTIMAL only guarantees Gurobi's default relative gap. On the rerun, all
  eight cases were decided: the three unsatisfiable cases have bounds
  50.5045, 122.2500036 and 71.0010 against thresholds 52, 124 and 72. Log:
  `code/pooling_existential_reals/one_pool_build_and_check-2026-09-25.log`.
- **M27:** The author decided that the September 24 manuscript rewrite needs
  no further review. The paper READMEs still identify which revision their
  reviews, source archives and manifests cover. The delivery archives were not
  rebuilt and remain historical snapshots.

### 10.2 Fresh runs and new reproductions

- **M10:** Re-solving `ex8_4_7` reproduced both saved results exactly. Checked
  against the original model, the points still violate constraints:
  - linked2: 5.9e-5 on row 39;
  - native: 8.9e-4 on row 25.

  Neither is counted as a valid solve. The likely cause is Gurobi's absolute
  feasibility tolerance on rows whose variables are around 1e-3; a
  tighter-tolerance solve was not tried.
- **m15, m32:** `nuc_verify.py` now stores exact certified values, and a
  `--reuse` flag re-verifies the saved certificates without a solver. The
  generated tables are rounded outward and match the conservative table in
  `nuclear-bounds.md`.
- **m63:** Both audit programs passed on current sources: `Verify.lean` with
  1,207 declarations and `ExtensionAudit.lean` with 1,112. The new manifest
  `extension-SHA256SUMS-2026-09-25` passes 34 of 34 entries, and the old one is
  kept as the `875a71ab` record. The appendix of the paper's reproduction
  section still names the old manifest. That is correct for the source archive
  it describes: the archive was captured on 2026-09-18, before `fa2a6f42`.
- **m73:** The `uniform` and `uncap` rows were rerun on current code:
  - `uncap` counts are unchanged.
  - `uniform` counts changed by at most 5%.
  - The ratio range over the nine rows is now 5–30 (was 5–29).
- **m76:** `t6.py` reproduced 6,036 cuts. The smallest value is -2.84e-13
  (the note had -2.3e-13), and the output is now archived.
- **m261:** The rate-one widths were reproduced with the existing ODE code and
  archived.
- **m196:** A supplementary independent review
  (`paper-certified-minlp/formal/REVIEW-CM04-CM34.md`) passes CM04 and CM34.
  All 49 obligations are now reviewed.
- **New independent checkers** reproduce reviewer-reported checks whose
  programs were never archived. In each case the reviewer's run stays
  labelled unarchived, and the new run is dated and archived.
  - M1: 150 new reduction instances agree exactly.
  - m4: the L=2,3 full-vertex LP values match, with exact certificates.
  - m43: every item is reproduced. The review's sentence that `1/n <= d`
    fails for every pair with `n >= 2k` is wrong: it fails at 22 of 36 such
    pairs. The review's conclusion is unaffected, and the error is now
    recorded in the review.
  - m162: 2,660 identities per configuration, matching.
  - m173: 240 new networks pass. The counts differ from the reviewer's,
    because the reviewer's generator is unknown.
  - m179: 1,276 conditions pass on 360 new inputs.
  - m44: a fresh transcript with the corrected message.
- **Ridge wording:** "about 1e-3 at N=6" is replaced by the saved medians
  (3.7e-4 and 7.4e-5) and maxima.

### 10.3 What remains

- **m29:** Rerunning the neural-network branch-and-bound timings would take
  about 10 CPU-hours, and they must run one at a time to be meaningful. This
  was treated as a large experiment and not done. The saved timings remain
  labelled with their clock inconsistency. No paper uses these results. The
  report, its summary tables and the research README now say that the
  timings must be rerun, after a one-clock fix, before any publication.
- **Unrecoverable records:** these rows concern review text, drafts or
  records that were never kept, so no computation can restore them. They stay
  labelled.
  - M7: the reviewed bytes are unknown.
  - m7, m26: drafts were not pinned.
  - m86: the kriging expression was not recorded.
  - m109, m133, m178: review records were not retained.
- **Recorded, left unchanged:**
  - m105: the potential-flow checker's printed message; its hash is pinned
    by process manifests.
  - The old SDP-RLT transcript, kept as history.
  - `nuc_solve.py` builds a solver cut from a nearest-rounded float. This is
    about one ulp, far below solver tolerances.
  - The duplicate `code/row_hull/results/bb_nodes_5x7.txt`, which a review
    cites by path.

### 10.4 Checks run

Targeted runs only, each run alone:
- **Lean:** per-module builds and replays for topic 17, and the two
  certified-MINLP audit programs.
- **Solver reruns:** the pooling checker, `ex8_4_7`, the row-hull `bb.py`
  runs, and `t6.py`.
- **Recomputation from saved certificates:** the nuclear bounds and the
  curve-hull cuts.
- **New and existing checkers:** `test_curvehull.py`, the new reproduction
  checkers, and `check_sdp_rlt_strengthening.py`.

The reviewing agent reran every fast checker one at a time and confirmed each
saved log. It also checked the numbers against saved outputs, confirmed
relative links and ran `git diff --check`. No project-wide verification was
run, and CI was not inspected.

### 10.5 Lean follow-up check

A read-only comparison checked every Lean module against the revision at
which its topic's build, audit or replay last passed. The Lean and Mathlib
pins have never changed. It found one proof change that no recorded check
covered: topic 18's `BilinearGraph.lean`, where `748a8b28` added about 97
lines, including new odd-case theorems. The audit had missed this.

That gap is now closed:
- Topic 18 was rerun on current sources: `lake build --wfail` on 19 modules,
  the axiom audit (1,214 declarations, up from 1,205 by exactly the nine new
  ones; standard axioms only), and `leanchecker` replay of all 19 modules.
  All passed. The audit now names the five new public theorems.
  Log: `formal/topics/18-positive-box/verification/run-2026-09-25.log`.
- Audit programs changed only by line rewraps in `fa2a6f42` were rerun and
  passed:
  - topic 13 `Audit.lean`: 1,936 declarations;
  - topic 15 `Audit.lean` (4,261 declarations) and `ReviewObserved.lean`;
  - `Verify.lean` in `paper-cubic-gap/formal` (1,247) and
    `paper-multilinear-gap/formal` (827).
- The records for topics 04, 07, 08, 09, 13 and 15 now explain which
  delivery fingerprints fail on current sources and why. Each failing file
  was rechecked by a later run or changed only in documentation.
