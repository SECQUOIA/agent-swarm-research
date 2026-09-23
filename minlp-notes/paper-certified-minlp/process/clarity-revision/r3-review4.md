# R3 final whole-manuscript review 4

## Verdict

No actionable major or minor issues identified. The complete revised manuscript presents a coherent, adequately explained scientific result: an implemented nonlinear-to-linear certificate interface, its conditional soundness proof, a precisely bounded formalization, and reproducible evidence of capability and specific failure mechanisms. The abstract, contributions, proofs, experiments, conclusion, and appendices agree on what has been established. I recommend acceptance of the clarity revision within this review's scope.

This is a fresh assessment of the whole paper, rather than an extension of the R2 verdict. It is not a guarantee of journal acceptance or a proof of executable correctness.

## Material reviewed

I read `main.tex`, all nine section files, all five generated table/text inputs, the paper and supplement READMEs, the formal README and coverage table, and both current claim-to-evidence/literature maps. I examined the current 33-page PDF and its extracted text, including the bibliography. Fresh rendered-page inspection covered pages 1, 9, 12, 14, 20, 27, and 33; the unchanged R2 rendered inspections of pages 22, 24, 26, and 30 remain applicable. These inspections cover the opening, correction and curvature tables, architecture figure, formal explanation, principal experimental table and audits, conclusion, reproduction instructions, supporting accounting, and bibliography. No unresolved citation markers appeared in the PDF text. The preceding label check found no unresolved or duplicate internal labels, and the relevant cross-references remain consistent with the present sections.

I did not read peer R3 reports, delegate work, edit manuscript or code, regenerate experiments, or repeat large archive checks. Source extraction/build, numerical replay, and full Lean execution are separate verification tasks; this review assesses the complete scientific argument and its presentation against the delivered material.

## Whole-paper assessment

### Problem, contribution, and relationship to prior work

The first page states the problem directly: exact MILP evidence does not certify a nonlinear bound unless the cuts are valid for the intended model and the proof input matches the justified master. The introduction then states the desired pointwise bound and explains why rounding and translation matter. The reader encounters the problem and proposed connection before implementation detail or repair history.

The four contribution categories remain distinct throughout the paper. The method is the concrete checking interface; empirical findings concern accepted artifacts and exact failure witnesses; tests and Lean proofs are validation with different coverage; the catalogue and bundles are reusable artifacts. The conclusion synthesizes the lessons of these components without turning the catalogue into an algorithmic guarantee or the test suite into a soundness theorem.

The related-work discussion acknowledges convex-MINLP certificates, supporting-plane outer approximation, rigorous support minimization, rational MILP proofs, and existing formal optimization/checker work. The closest certificate method is discussed in enough detail to explain the differing verification procedure. The paper describes its integration directly rather than asserting an unsupported first result, improved certificate size, or superior solver performance. The conditional result's lack of a Slater or attainment premise is explicitly separated from any completeness theorem, avoiding a misleading comparison with certificate-existence results.

### Model and mathematical argument

Section 2 fixes the exact loaded expression interpretation before stating the implementation's conclusions. The binary-leaf aggregation example explains why this is a mathematical issue rather than merely a serialization convention. The domains, propagated box, feasible set, epigraph, objective constant, integer restrictions, and primal-witness obligations are sufficiently explicit for the later proofs.

The argument in Section 3 has the necessary logical order. Rational propagation preserves the feasible set; the residual support correction proves affine underestimation; the discrete invariant accounts for both assumptions and weak incumbent cutoffs; objective-preserving inclusion transfers the master bound; an independently feasible witness supplies primal completion. I checked the direction and endpoint conditions in the correction tables, the rounded-slope example, the use of integrality in rounding and unsplitting, the incumbent's role in extending the restricted-set bound, and the sign normalization of maximization. I found no inconsistency or missing premise in those arguments. The claims remain pointwise when the feasible set is empty and do not silently use optimum attainment.

Section 4 supplies the mathematical and software explanations needed to understand the admitted method. Its quadratic and monomial proofs support the recognizers without claiming universal recognition. The distinction between convexity, expression definedness, and a valid supporting derivative is retained, including the boundary example where finite coordinate derivatives would not establish support. Exact LP/VIPR matching, full-file proof checking, partial-check results, and two-pass memory use are described in terms that connect directly to the soundness obligations.

### Formalization and implementation trust

Section 5 explains what the formal theorems prove, not only their names. The coordinate cases and finite-sum composition establish useful universal inequalities, while support and genuine enclosure inequalities remain explicit premises. The epigraph construction, cutoff lifting, and primal completion are distinguished from executable propagation or VIPR replay. The coverage table and README agree with that account. Nothing in the abstract or conclusion implies that Lean has checked the Python checker or the benchmark certificates.

### Experiments and their interpretation

Section 6's capability/failure/cost structure works as part of the complete paper. It answers whether the method produces checkable bounds, what exact failures establish, and what replay requires. The principal 203/289 result is tied to its frozen protocol and distinguished from 198 successful producer returns. Signed differences from unverified reference objectives are defined and kept separate from the two completed optimality examples.

The failed-inference audits support claims about supplied justifications, not necessarily false final bounds. Sufficient nonlinear rejection is likewise not treated as refutation of an inequality or of convexity. The returned-point examples state the violated original conditions and the source-equivalence boundary; the matching primal witness supports the stronger optimum claim for the loaded model. These distinctions are maintained from introduction to conclusion.

Timing populations, concurrent elapsed time, requested search limits, complete process limits, archive sizes, and memory dependencies remain clear. Appendix B preserves the full production and versioned-repair accounting without turning the main results into a chronological development record. Its anticipated V3 primary tally is explicitly separated from a performed full replay. The 222-model catalogue is consistently identified as a union across compatible recorded protocols.

### Standalone presentation and delivery

The notation is introduced before use and is locally clear even where familiar letters are reused for different explicitly defined purposes. Tables and the architecture figure are legible in the delivered PDF; equations, theorem statements, code commands, and long references remain within the page. Ordinary float and page breaks do not obscure the reasoning. The prose is technical but provides the definitions, examples, and proof explanations an optimization reader needs without consulting repository notes.

Appendix A and the READMEs distinguish the paper/formal source package, small checker core, and large proof collection. They identify dependencies and commands for the advertised levels of reproduction, retain source/version qualifications, and do not assert a nonexistent public deposit. The conclusion introduces no unsupported result or new prerequisite. Some trust qualifications recur at their relevant interfaces; these repetitions prevent materially different claims from being conflated and do not warrant removal merely to shorten the manuscript.

## Required corrections

None identified in this whole-paper review. The scoped contribution is scientifically clear, its limitations are stated where they affect interpretation, and no additional experiment or theoretical development is needed to resolve a reader-facing gap identified by this review.
