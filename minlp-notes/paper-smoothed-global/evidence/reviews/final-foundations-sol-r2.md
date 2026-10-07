# Focused foundations review, mathematical revision, round 2

**Decision: F1–F4 are resolved in the actual round-two snapshot.** No additional
mathematical or formal-contract defect was found in the changed passages.
The assigned foundations scope passes this focused review, subject to the
unchanged pending classical-source and bibliography checks. This does not
approve the whole paper for submission.

## Review target and scope

I reviewed only the immutable TeX source in
`evidence/snapshots/mathematical-revision-r2/`, captured at
`2026-10-06T04:04:44.496806+00:00`, and compared it to the immutable
`integrated-mathematical-draft-r1` source reviewed previously. I did not read
or modify live manuscript source.

Context was the original `BRIEF.md` and `independent-review-brief.md`,
`reviews/final-foundations-sol-r1.md`,
`review-disposition-final-r1.md`,
`reviews/mathematical-revision-r2.diff`, the relevant final-author-report
passages, and `reviews/shared-root-universal-independent-sol-r1.md` and
`reviews/shared-root-universal-independent-sol-r2.md`. The latter round-two
report reviewed the earlier `integration-repairs-r1` capture; I checked the
repairs in this later capture directly instead of treating that verdict as
proof of their presence here.

As disclosed in round one, I developed the earlier universal-budget report.
This remains a review of its integration and contracts, not a fresh
independent review of my own development. The separate shared-root/universal
reviewer provides that independent check. I did not develop the shared-root
construction.

All 20 files match the new manifest. The old 20-file manifest also matches,
so the comparisons have a verified baseline. Principal new hashes are:

| Frozen file | Round-two SHA256 |
| --- | --- |
| `sections/02-model.tex` | `b2ee85b74131bf95659b085dbfe7976e63746acfccfe1500eb060e088891c8ca` |
| `sections/03-counting.tex` | `28141913b9357189bace34ee2f3e5ee19fd9d04fdfdfcbdaab9edeb375f4c7c8` |
| `appendices/A-finite-noise.tex` | `895d4ce273e88a2ab9e9a7a4196b950a619ffdf829a2033536c43dc59295a6d8` |

All locations below refer to `mathematical-revision-r2`.

## Disposition of the four findings

| Finding | Actual repair and new locations | Disposition |
| --- | --- | --- |
| F1: computing the parameter envelope was not charged | Section 03:690–700 requires a nondecreasing positive integer-valued `F`, evaluation work `(1+size(K)+F(K))^{c_F}`, a fixed `c_F`, and inclusion of `K` in the base data. The final overhead exponent explicitly depends on `c_F`. Appendix A:706–714 charges evaluation first. Appendix A:811–813 chooses an envelope with that property for the explicit flow/TU parameter powers. Section 02:192–215 carries and invokes the same convention. | Resolved. |
| F2: the remaining polynomial factor could hide sampling-parameter dependence | Section 02:283–285 says the expected fallback term is polynomial in `I+b` and retains the stated parameter factor. Section 02:381–385 says refinement retains sampled-length and requested-precision dependence, including the sampling-parameter factor. | Resolved. |
| F3: empty-retained-set minimum was undefined | Section 03:210–212 defines that minimum as `+infinity`. | Resolved. |
| F4: measurability prose could use `infinity * 0` on a singleton | Appendix A:239–249 uses only the finite coefficient `epsilon`, takes limits of admissible coefficients when necessary, and explicitly treats the singleton inequality as vacuous. | Resolved. |

For F1, `size(K) <= I`, so the new evaluation premise gives

`(1+size(K)+F(K))^{c_F} <= (1+I)^{c_F}(1+F(K))^{c_F}`.

Computing the grid exponent and sampling its index also fit a fixed polynomial
in the encoded data and the resulting exponent. Substituting
`b = O(F(K) P_0(I))` into any fixed polynomial in `I+b+q` gives a fixed
polynomial in `I+q` times a power of `1+F(K)`. The repaired exponent can cover
both this substitution and `c_F`. No exponent of `I`, `b`, or `q` depends on
`K`. Positivity ensures that the grid has at least two points.

The explicit flow/TU powers previously inspected admit such an integer
envelope. The new paragraph makes its choice part of the construction.
The underlying flow-boundary precision/work proof is unchanged; the repair
does not replace it or infer polynomial precision independent of the core.
The supplied `k <= K`, the cost after choosing `K=I`, and the retained actual
numerical factors are still stated at Section 03:719–730, Section 02:218–227,
and Appendix A:814–820.

For F2, the accounting still cancels only the base multiplier `B`. It leaves
the bounded sampled-height polynomial. The new text therefore agrees with
the parameter-dependent flow/TU contracts rather than silently promising
base-polynomial work for every growing core.

For F3, an empty retained set now gives `underline U_j=U_j`. Item (ii)
already proves `U_j=F*` in that case, so the lower/upper certificate is exact.
The proof is otherwise unchanged.

For F4, positive finite growth thresholds force a unique minimizer. When the
supremum equals the threshold, admissible finite coefficients approach it at
that same minimizer, so the inequality persists in the limit. On a singleton
every finite inequality holds vacuously. The existing compactness and lower
semicontinuity argument then proves closedness of `{g_* >= epsilon}` without
an infinite coefficient. The later proximal/area/trace argument is unchanged.

## Unchanged dependencies

I asserted byte equality of 17 relevant blocks between the two verified
immutable captures. Their round-one mathematical dispositions carry forward;
I did not rerun mathematical diagnostics or rederive the unchanged
common-root and parts (a)/(b) proofs.

| Unchanged block | New locations |
| --- | --- |
| Local interval/count statements and balanced meshes | Section 03:34–172 |
| Finite-law transfer and sampler statements | Section 03:273–340 |
| Sharp growth, finite/active tails, and rare accounting statements | Section 03:341–509 |
| Exact fallback statement and explanation | Section 03:510–603 |
| Common-law schedules and parts (a)/(b) | Section 03:643–689 |
| Local/search/transfer/sampler proofs | Appendix A:1–227 |
| Growth conjugate, proximal map, area formula, trace, and integration | Appendix A:251–328 |
| Renegar and finite/active/rare-tail proofs | Appendix A:329–438 |
| Shared-root construction and canonical fallback proof | Appendix A:439–676 |
| Common grid/Gaussian resolution proof | Appendix A:679–705 |
| Format/height, grid/lattice, and Gaussian route premises | Appendix A:720–796 |
| Output format definition | Section 02:308–341 |
| Exact smoothed algorithm definition | Section 02:245–261 |
| Original-objective regret and calibration | Section 02:418–527 |
| Flow-boundary precision and work proof | Appendix F:808–867 |
| Gaussian support and precision schedule | Appendix B:664–725 |
| Separable Gaussian support schedule | Appendix B:880–889 |

The shared-root/fallback proof block has SHA256
`12f8dfd3bef099d1628b0d0903f25faac5cce5fc6d5e8bb663ff805b5aeb97cf`.
The common-law schedule/parts (a)/(b) statement block has SHA256
`813d39a14b741754ddaa04216948bc0269310b67144b2ab9d03b8f439245afa5`;
their proof block has SHA256
`706e2a1ca958aa9a95dba1814904596b1462aac9282f00881b436715ecdc51a3`.
Each hash is the same in the old and new captures.

Whole-file identity also holds for the main file, macros, abstract, Sections
04–07, and Appendices C–E and G. The changes in Appendix B outside the
schedule block and in Appendix F outside the boundary-flow block belong to
their focused reviewers. These identity checks are not approval of entire
other chapters.

## Changed model and front contracts

The factor parameter is now correctly stated as the supplied row count
where that factor is used: Section 02:51–55; Section 01:67–72 and 133–164.
This does not assume independent rows merely because an auxiliary dimension
is denoted by `k`. The theorem-specific intrinsic-inertia and frame premises
remain their own contracts.

Section 01:308–316 now bounds expected proof-record length by the
corresponding structural and numerical work bound. It preserves the
distinction between a compact optimizer descriptor, its global proof record,
and long fallback algebraic data. Section 10:83–95 correctly states
base-exponential per-draw fallback bounds, expected length/work bounds, and
the per-draw parameter bounds for small-core algebraic outputs. It retains
one common root per component and a symbolic sum of component values.

Section 02:355–376 continues to distinguish point approximation from exact
active-coordinate recognition and exact value comparisons. The added
companion comparison at Section 02:370–373 and Section 01:476–484 makes no
new promise of those stronger operations. Its cited source accuracy is
Luna's responsibility; I checked consistency with the manuscript's output
contract without doing literature research. The new attribution of a
strongly convex face descriptor and strict-complementarity/runtime premises
at Section 01:512–520 also leaves the manuscript's own finite-noise margin
and fallback proof obligations intact.

The revised independence sentence at Section 01:242–247 correctly distinguishes
the dependent factor/residual decomposition under uniform ambient noise from
the continuous Gaussian proxy. It does not assert independence of the actual
finite approximation after an orthogonal decomposition.

No new defect was found in these changes. Rational feasible approximation
scope, exact implicit lifts, same-draw evaluation, base-only fallback degrees,
added-bit height dependence, finite atoms, and geometric/oracle qualifications
remain as reviewed in round one.

## Checks performed and remaining limits

Actual targeted commands were `cat` on the briefs, prior reports, disposition
and supplied diff; `rg --files` to locate the frozen files and review reports;
`rg -n -F` on the four final author reports for the relevant shared contracts;
and `nl -ba ... | sed -n ...` on the new 01/02/03/A/10 passages listed above.
An inline Python check using `pathlib`, `hashlib`, and `json` verified both
20-file manifests and asserted equality of the 17 blocks. All assertions
passed. A final report-only check covered the final newline, trailing
whitespace, and control characters.

Only this report was written. No manuscript/source-note edits, delegation,
optimization or sampling experiments, saved proof-diagnostic reruns,
compilation, project-wide checks, or CI inspection were performed.

No assigned-scope mathematical repair remains. Classical source identities,
exact locators and applicability, complete bibliography, other route proofs,
and final submission/layout readiness remain outside this focused verdict.
The unchanged round-one qualifications about those dependencies still apply.
