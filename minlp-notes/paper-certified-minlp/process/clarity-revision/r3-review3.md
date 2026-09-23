# R3 final independent whole-paper review 3

Verdict: **No major or minor issue identified.** No correction is requested. The integrated scientific framing is clearer, and its claims remain supported by the mathematical and empirical evidence within the stated trust boundary.

## Review scope

I freshly read the complete current abstract, all nine section files, all generated LaTeX tables/result fragments, all 27 bibliography entries, and both current evidence maps. This was a whole-manuscript review, not a review restricted to R1/R2 differences. I checked the connections between the early contribution claims, mathematical contracts, executable/formal coverage, main scientific results, conclusions, and supporting appendices.

Earlier direct primary-source and artifact checks remain evidence: these include the Baes and Halbig statements, rigorous-bounding precedents, Wood/CakeML/CvxLean distinctions, exact local proof-step audits, original-model/source audits, and formal-source correspondence. In R2 I also directly verified the GAMS 53 status table now cited in Section 6. No source claim in the final integration required an additional search. I did not rerun unchanged numerical experiments, full proof campaigns, Lean builds, archive hashes, or packaging. I did not read any peer R3 report or delegate work.

A fresh source-consistency scan found nine section files, 27 cited bibliography keys with no missing or unused entry, and 59 unique labels with no unresolved `ref`/`eqref`. This does not substitute for a build or mathematical review.

## Scientific coherence and supported contribution

The abstract and introduction now identify the research problem before presenting implementation details: a discrete proof must be connected both to justified nonlinear cuts and to the exact intended master. Section 3 supplies the conditional composition result, Section 4 makes its operational obligations explicit, and Sections 5–6 distinguish formal validation from measured executable behavior. The capability/failure/cost organization in Section 6 answers the introduction's scientific questions. Appendix B retains the full evidence accounting instead of requiring the main argument to follow the repair chronology.

The method, empirical findings, validation, and reusable artifacts remain distinct contributions. The paper does not turn a test count, formalized abstract implication, or catalogue union into a stronger mathematical or algorithmic claim. The conclusion draws scientific lessons about model interpretation, failure classification, primal feasibility, and exact representation through reporting. These lessons follow from the supplied examples and audits; the paper does not claim a general performance or completeness theorem.

## Detailed whole-paper assessment

- **Prior work and novelty:** Halbig et al. remain the closest computational comparison. Baes's certificate-point bound is not recast as bit complexity. Classical outer approximation, rigorous supporting-affine minimization, rational safeguards, discrete proof formats, and earlier formal optimization/checking work receive explicit credit. Jansson, Messine–Trombettoni, and Elloumi provide the nonlinear-bounding context; Wood, CakeML, and CvxLean retain correctly differentiated coverage. The work is presented as a concrete integration and reliability study, with no unsupported first-system, missing-prior-capability, or superiority claim.
- **Model and mathematical contract:** Exact stored coefficients, original domains, propagation, support data, and master identity refer to the same loaded model. Finite and infinite coordinate cases, interval signs, fixed-coordinate treatment, and the epigraph slope condition agree across the mathematical and formal sections. Support and true-enclosure premises are not replaced by numerical finiteness alone. The discrete invariant retains assumptions and weak incumbent semantics. The transfer and primal results have the inclusion, objective, feasibility, and infimum premises they require.
- **Implementation and formal scope:** Complete checking in a restricted grammar is distinct from universal proof-format support. Partial results expose no certified bound. The public finite-bound API is not enlarged by a broader infeasibility implication in the mathematics. Lean proves selected implications from genuine support/enclosure and semantic premises; it does not verify the Python stack, concrete proof parsing, or benchmark artifacts. Shared trusted components, source construction, hash limitations, and execution assumptions remain explicit.
- **Capability and denominators:** The 203/289 primary replay result is consistently separated from 198 accepted producer returns, with four timeout survivors and one worker-error survivor. Historical 188/92/9, separate twelve-case V2 generation/replay, two targeted V3 checks, expected-but-unrun full V3 204/18/67, and the 222-model/405-record catalogue retain their distinct meanings. Moving their details into Appendix B has not hidden unsuccessful attempts or revised the frozen outcome.
- **Strength and failures:** Signed reference differences remain comparisons with unverified reference strings, not optimality gaps. Exact original-model witnesses support the two exact-optimum examples. Invalid local supplied combinations or disjunctions are not called false final bounds; insufficient safe-intercept or curvature tests are not called refutations. Printed SBB/SHOT point violations retain their precision, model-status, source-interpretation, and historical-memory qualifications.
- **Costs and reproducibility:** Search requests, outer wall limits, replay limits, hashing, external corroboration, concurrent sums, elapsed times, and proof-completion threads remain distinguished. Large storage totals support a practical cost observation, not a certificate-size ranking. Index-array and live-row memory dependence is retained, without inventing a peak-memory measurement. The two appendices give a coherent route from the fixed protocols and versioned accounting to the separate paper, core, and bulk materials.

I found no hidden loss of a qualification during the revision and no gap between the current abstract's promises and the content supplied. Further work such as wider admission, independent executable verification, or controlled comparisons could constitute separate research developments; it is not a missing premise of the submitted contribution as now stated.

## Reviewed framing fingerprints

| File | SHA-256 |
|---|---|
| `main.tex` | `a0974eb5a94f9a93b0403fa0a315221605f5828135165548a50c75f3ec769fe9` |
| `sections/01-introduction.tex` | `924dd223b031a54d3304173ceb7121f7821f31c49c517437bd21ab7e33da3be2` |
| `sections/06-experiments.tex` | `a0c484168ad499becbcc9a8c4e82539b508eeac1bfb7b2603f70c476351688f5` |
| `sections/07-discussion.tex` | `e6e62fe39a742bc8a6e81bf2a661ef093d8580555ea7b865d734436430830645` |
| `sections/09-experimental-accounting.tex` | `e748fa24d66ce28fb8133c669983ac81ab8dd26f7061c7526e95f2178b66f61f` |
