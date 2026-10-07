# Post-addendum final scoped review, Sol R1 with final R2 followup

## Verdict

**PASS for the changed mathematical arguments, model clauses, companion attribution, prose, and affected PDF passages. No unresolved defect remains in this scope.** The actual final target is submission-addendum-r2, not the intermediate R1 candidate. Its two final introduction refinements were checked after the independent R1 review.

This verdict covers the late companion P2 addendum and the six findings from the completed late Opus mathematical review. It carries the earlier final-editorial-sol-r2 review forward only for material verified unchanged. It is not a fresh audit of every proof, a certification of absolute priority, or a guarantee of journal acceptance. No manuscript repair is requested by this review.

## Frozen targets and independent verification

The predecessor is evidence/snapshots/final-submission-r4. Its manifest SHA-256 is:

    0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061

The initial addendum target is evidence/snapshots/submission-addendum-r1, captured at 2026-10-06T06:10:01.592374+00:00. Its manifest SHA-256 is:

    fc756e30029d3d1d430b6e77e1d6b557bbb7e7d7a55b24599b95be5cd28b87f9

The final target is evidence/snapshots/submission-addendum-r2, captured at 2026-10-06T06:18:14.234745+00:00. Its manifest SHA-256 is:

    0f1ff4db085a5d732b4e476309deafd2a2793225103a7a0773ae3ae84c2c2d94

I independently verified all 21 source hashes and line counts in each of these three snapshots. All 21 live manuscript files matched the final R2 snapshot at verification. The regenerated R4-to-R1 diff matched evidence/submission-addendum-r1.diff exactly. Exactly nine source files changed; no stale replacement of Section 2 survived.

| Changed source, relative to the frozen snapshot | Final R2 SHA-256 |
| --- | --- |
| sections/01-introduction.tex | 2540bc871e574afddea4818d5a82916983fefbe04cf9b58ed8c26367e1c4598d |
| sections/02-model.tex | 867c8675779f8657087a77b1d91c37bcb2ad0abc016be83d2feb91aa27d98970 |
| sections/04-quadratic.tex | 3e94534ea4c3eceb2022e5ec36a6e80290bb4c208ae1a9e48f658a72904df824 |
| sections/05-sparse.tex | 1709549e2fa56a0b8adfbf24362cbf5774fb8b9deb5b8236a034c60945ecf60e |
| sections/06-constraints.tex | 2d3c87b336c67119979bdb2d7794eeb5c155e912cc24631915281a4f0552dd46 |
| sections/07-recourse.tex | 381a032fbe829f8b023314c41ecfa7b22aad9a3247e9f15020178c95563d72fe |
| sections/08-integer.tex | bf6c8d6bc3027b6f49558e47e6f5a320c88561bff3bc4c4c08a263da061c76ab |
| sections/09-boundaries.tex | 99453c48a928b58ce2dc1167fe4dd214cf6dd8653898e67ad37480f826b2af4f |
| appendices/F-integer.tex | 8c2208bc4603195f3e2e1d021ce0486ab4b6c1d2696119d4935189ef7456077a |

The protected-block comparison was checked with an independent balanced begin/end parser, including nested environments. From R4 to addendum R1, the changed mathematical environments are the uniform-resolution proposition and its nested enumeration, the original-objective regret remark, and the affine-margin proof. The other 137 proof blocks, all 410 labels, the displayed-equation blocks, and the bibliography are unchanged. This is a source comparison, not an assertion that a changed proof is automatically correct.

From R1 to final R2, only sections/01-introduction.tex changed. The independently regenerated diff matches evidence/submission-addendum-r2.diff exactly. All balanced mathematical environments, all 138 proof blocks, all 410 ordered labels, and the bibliography are byte-identical to R1. I checked the two changed clauses and their surrounding paragraphs directly.

## Evidence and reading scope

I read the complete attribution-addendum-review-brief.md, both Opus author reports for this addendum and the late mathematical repairs, the historical front author's withdrawal of the deterministic-filter novelty claim, the completed opus-math-r1.md, and the final late-opus-math-disposition-sol-r1.md. I also revisited the old Opus editorial A8, A9, A12, and A13 findings and the prior final editorial review. Findings aimed at an earlier snapshot were assessed against the actual new text rather than treated as automatically current.

The local companion source contracts come from the complete Luna audit, companion-overlap-addendum-luna.md, whose SHA-256 I verified:

    fbd34b464a1b4f3272fa667498510bc1e6aadb8c64786c963f53eaa64ce01d5a

Its dated followup explicitly supersedes the initial family-B non-reproduction claim. I used that corrected contract. I did not conduct literature research or read the companion primary manuscripts myself.

The final independent six-finding disposition has verified SHA-256:

    abede7bbdc92c0ad83694fed7102ecbd56ea1acccf65f75f824f356707740e91

The completed late Opus mathematical report has verified SHA-256:

    dc6b43ed96450f69d7c9417c17f7afdb15bc4e077d903c5ceb0eb6fb970d2d47

That Opus report targets the original proof draft. Its six new findings were checked separately against this final candidate; its other historical integration comments do not describe the current snapshot.

The prior main literature audit is unchanged, with verified SHA-256:

    24761a995eaf1ff4de06135b4b479874731a176d483025489846b37609ac622a

Its source-access qualifications and the earlier final editorial review remain applicable. No new source or citation key was added. The final bibliography is byte-identical to R4: exactly 47 distinct used citation keys match its 47 entries, with no missing or unused key.

For actual source review, I read every changed passage with its neighboring result and proof. This includes introduction:447–547; model:94–245 and 403–522; quadratic:618–650; sparse:582–696; constraints:782–834; recourse:81–264; integer:447–535 and 650–746; boundaries:216–351; and Appendix F:865–979 and 1120–1205. I followed the universal-law argument in counting:643–758 and Appendix A:678–782, the local rowwise counting contract, and the actual star variant in Appendix E:820–860. The specialized positive-definite box-QP oracle and general face-QP enumeration were checked where relevant to the old duplication concern.

## Six mathematical findings: actual dispositions

All source locators below refer to the final R2 snapshot.

| Finding | Actual final treatment | Decision |
| --- | --- | --- |
| NEW-1: arbitrary-vertex affine-margin proof | Appendix F:937–958 uses a coordinatewise minimizer and changes only nonzero-slope coordinates. The symmetric negative-value and empty-zero cases are explicit. Its downstream bilinear application is at 960–973. | Resolved; independently checked as described below. |
| NEW-2: row-specific lattice scales versus the common-marginal model | Model:125–134 states the row-scaled extension, fixes one common resolution, and limits each theorem to its stated law. Proposition part (a), model:197–200, explicitly preserves each supplied scale. Model:231–235 and integer:656–683 agree. | Resolved without broadening the other aligned theorems. |
| NEW-3: lattice-search reference | The predecessor repair survives unchanged. Integer:711–719 and Appendix F:1120–1205 use the intended search and objective-value lattice, with a common denominator across rows. | Resolved before this addendum; checked in the current text. |
| NEW-4: unqualified sampling-height assertion | Counting:606–616 retains the parameter-dependent exception; model:177–184 and 204–213 distinguish polynomial from parameter-dependent sampling precision and charge the envelope computation. | Resolved before this addendum; not silently generalized. |
| NEW-5: ambient-uniform count called FPT | Model:411–435 now names aligned/Gaussian-like low-rank bounds separately and expressly excludes the ambient-uniform dimension power from structural FPT. Numerical ratios remain joint parameters. | Resolved. |
| NEW-6: regret bound used auxiliary widths | Quadratic:635–648 uses original-domain coordinate widths for ambient coefficient noise, retains the Gaussian support factor, and uses the projected row widths for aligned noise. | Resolved; the conflicting auxiliary-width interpretation is removed. |

For NEW-1, a nonempty affine zero set forces a nonzero slope. For a positive value, the chosen point minimizes the affine function on the cube, so its value is nonpositive. Every moved coordinate decreases the function, at rate at least the smallest nonzero absolute coefficient. The first zero is reached after an ℓ1 path of length at most p(x)/π_min. Euclidean distance is no larger than that path length, and rational coefficient height gives π_min ≥ 2⁻ᴴ⁰. Zero-slope coordinates stay fixed. Negative values use the same argument for −p. A nonzero constant belongs only to the empty-zero case. In that case the function has one sign, its least absolute value occurs at a vertex, and the product of at most q+1 coefficient denominators gives the stated lower bound. Thus the repaired proof establishes the unchanged lemma, including these edge cases.

The downstream bilinear proof uses μ₀ = 2⁻⁽ᵏ⁺¹⁾ᴴ⁰ δ/2. For a chart with zeros, the distance δ/2 supplies at least this margin. For a chart without zeros, its dimension is at most k and the vertex-denominator bound is at least this margin because δ/2 ≤ 1. Base coefficient height and log(1/δ) have polynomial length; multiplying height by k remains polynomial in the explicit input length. The claimed polynomial sampling precision therefore survives, as do the bilinear-flow corollary and its TU specialization. No new external theorem is needed for this repair.

The row-scaled model clarification is also consistent with the universal-resolution proof. Appendix A:753–776 explicitly uses the same M(I) rescaled by each row's supplied σᵢ and explains the lattice cap reset and common value denominator. The local count permits independent marginals with separate scales. The compact model proposition spells out this specialization; it does not assert a new general law or alter the objective by rescaling T. The lattice terminal curvature error is compared with spacing of the original attainable objective values, rather than spacing of auxiliary squared-noise expressions.

For regret, the replacement is a bound on γᵀ(x−y) over the original feasible set. Ambient support bounds use the sum of original coordinate widths; continuous-relaxation widths upper-bound mixed feasible widths. The Gaussian support factor (b+20)σ remains. The common-scale aligned theorem uses the original projected row ranges. This matches the model's general original-objective proposition and leaves the numerical work/regret tradeoff qualified.

## Companion attribution and contribution

The introduction and direct local attributions now agree with Luna's supplied contracts.

| Inherited result or example | Checked final locations and distinction |
| --- | --- |
| Fixed-feasible-set value-function curvature | Introduction:491–494 and recourse:126–130 credit the companion antecedent of lemma 7.2(b). The fixed feasible set is explicit; no convexity of the residual objective is added to this upper-curvature inheritance statement. |
| Certified bag-local filtering | Introduction:496–497, sparse:596–599, and boundaries:298–301 credit deterministic parts (a) and (b). Part (c) is the finite-law expected tuple count. The neighboring prose retains the conditional-oracle costs and supplies no efficient general outside-value oracle. |
| Deterministic CORE search | Introduction:494–496 and recourse:253–258 credit retention, value-interval, and witness guarantees (a)–(c) with an exact oracle. The companion's growth-dependent query bound is separate. The present certified-error extension and expected query count are identified; the companion's additional lower-bound-record output is not claimed wholesale. |
| Star family A | Recourse:178–181 and boundaries:224–229 credit the deterministic example. The small-noise every-draw failure and failure of closure at level zero are the stated additions. The proposition's actual noise and stopping-depth restrictions remain. |
| Positive-definite star family B | Recourse:183–189 expressly identifies the variant as the h=1/4 case of the second companion family. The actual Appendix E formulas agree with the corrected Luna followup. The initial broader non-reproduction assertion is not retained in the manuscript. |
| General TU coupling | Introduction:499–502 and constraints:789–803 distinguish fixed-degree approximation from rational-quadratic exact output. Exact quadratic termination needs neither uniqueness nor growth; set growth bounds levels. Accuracy-independent operation bounds also need a separate bound on each optimal coordinate projection's cardinality. |
| Dyadic TU rounding and pruning | Constraints:804–816 keeps the classical integral-vertex citation and directly credits the companion's deterministic rounding, allowance, and filtering layer. Missing smoothed counts and closure/tail estimates are distinguished from the existence of deterministic algorithms. |
| Strongly convex face enclosures | Introduction:528–536 credits the inherited enclosure concept, including free-coordinate growth, strict complementarity, and reciprocal-margin bit dependence. The descriptor can represent an irrational optimizer. The addition is the finite-law margin/count/fallback composition, not the enclosure concept alone. |

The earlier graded-grid formulas, restricted rETH conclusion, growth-tail integration limitation, exact-arithmetic companion's all-precision finite-law property, cubic positive theorem, quartic obstruction, and algebraic-versus-Cauchy output distinction remain present. The addendum does not erase original P1–P5 qualifications. General TU constraints on searched coordinates are excluded from this paper's smoothed guarantees, not from all deterministic optimization methods.

The R2 followup improves two already nonblocking R1 phrases. Introduction:501 now requires “a bound on the size of each optimal coordinate projection,” matching constraints:799–801. Introduction:526 now names “finite-noise bounds on closure failure,” so the addition list does not invite a reading that sound closure tests themselves were wholly new. Both exact replacements are present in the frozen source and rendered PDF. No additional priority claim was introduced.

## Editorial concerns from the older full review

The old A8 restructuring recommendation is not a substantive blocker in the current text. Section 8 has explicit subsections, and its opening explains that the final two integer-related routes use different mechanisms. Preserving that grouping does not obscure their theorem scopes.

The old A9 forward-reference concern is addressed by the present compact specialization of the later universal-law corollary. The proposition states the replacement laws, numerical factors, parameter-dependent exception, and cap changes. Its short proof points to the routewise appendix verification. It is not an undefined promise or a substitute for that proof.

For A12, the positive-definite box-QP oracle and general face-QP enumeration have different local roles and compatible contracts. Restating a specialized oracle where used creates no contradiction or mathematical gap. The paper's allowed length does not require deleting useful specialized statements.

For A13, the concrete regret-width collision identified by NEW-6 is repaired. The reviewed local meanings of the remaining repeated conventional symbols are explicit enough to follow the arguments. I found no further substantive notation ambiguity in the changed passages. Broad reorganization, compression, or global renaming is not required for this scoped verdict.

## Actual PDF and final R2 followup

The completed R1 PDF that I inspected had 182 pages and SHA-256:

    ac18317098be35feca176e5f5112b3d5d3c6403049ee1245553d2faa0bcfb458

I visually inspected pages 11, 12, 14, 15, 16, 18, 19, 40, 52, 70, 72, 73, 74, 90, 95, 96, and 169. These cover the changed attribution, model, FPT, regret, lattice, star, and affine-proof passages. Text, formulas, theorem references, and page boundaries were legible, with no clipping or unresolved reference visible.

After the explicit final build-completion handoff, I independently opened the R2 PDF. It has 182 pages, 1,788,838 bytes, and SHA-256:

    72dfac22092c60dcebd8f0b081b6baa27d37e35fde0a113e107b9437b2659e9b

I read and visually inspected its updated pages 11–12, including both replacement clauses and the transition into Section 2. The changes render cleanly. Review of the remaining changed source passages transfers from R1 by their verified byte identity; this is not a claim that every R2 page was visually inspected.

The final full-PDF text extraction contains no [?], ??, or replacement-character marker. All 1,505 internal GoTo links have existing named destinations. There are 54 external URI links; I did not visit their targets. Root reports the successful build, clean final TeX log, and the same three expected anonymous-companion BibTeX sort warnings. I did not run the build or independently audit those logs or the delivery archive.

## Checks and limits

Targeted checks actually performed were Python hash/line-count verification of the three 21-file manifests and live final source equality; independent difflib comparisons against both supplied diffs; balanced-environment, ordered-label, displayed-equation, proof, and bibliography comparisons; citation-key reconciliation; pypdf fingerprint, text-marker, and internal-destination inspection; and pdftoppm renders viewed with view_image for the listed pages. These are source and presentation checks, not optimization experiments.

The inline check commands ran through python - <<'PY' and exited successfully. The final focused render command was:

    pdftoppm -f 11 -l 12 -scale-to 1800 -png paper-smoothed-global/main.pdf /tmp/smoothed-final-layout-gjqesmk9/editorial-addendum-r2

It exited 0; both generated images were inspected with view_image. The earlier R1 page renders were inspected separately. These checks do not report CI results.

The earlier source-access gaps remain recorded in the unchanged main audit. New companion comparisons rely on Luna's exact local contracts and corrected dated followup. I read the parallel Opus addendum review after completing my independent R1 source, mathematics, and PDF checks; its optional wording suggestions agree with the final R2 refinements but do not replace those checks.

No manuscript source, bibliography, KB, or project artifact was edited by this review. No project-wide verification, CI inspection, new literature search, experiment, or delegation was performed. The only authored project file is this report. The scoped final PASS is complete; no further review action is requested.
