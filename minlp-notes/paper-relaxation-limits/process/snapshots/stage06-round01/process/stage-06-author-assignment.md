# Stage 6: integration and supporting comparisons (after Stage 5 acceptance)

Act as the sole integration author. Read the entire cumulative manuscript and the accepted stage ledgers, scope map, primary-source records and unresolved boundaries. Preserve accepted mathematical content unless an integration defect needs correction; record any such change explicitly for the ensuing review. This stage receives its own 15 full-stage reviews, then the user requires a separate 15-reviewer whole-paper loop after all stage issues are fixed.

Rewrite title if needed, abstract and introduction around the final paper, with a coherent reader's route. Explain how simultaneous envelope laws, structural bounds, physical-box geometry and oracle-specific spatial certificates address complementary questions. Do not suggest that positive gap examples are the signed XOR spatial family, or that a pointwise width ratio is an approximation ratio or tree lower bound. Clearly identify classical antecedents and the specific developments presented here without an unsupported novelty claim. Keep internal agent history in PROCESS.md, not manuscript prose.

Read all Stage6 rows of scope-proposal.md and their corrections. Include the following supporting material at a scale appropriate to this paper, using appendices for distinct calculations:

- The point-packing benchmark has four established RLT/SDP exact values, proved previously by Khajavirad2024. Give a compact self-contained variance/averaging proof and the actual feasible covariance constructions, symmetry secants updated with the box, RLT redundancy, n>=2 or n>=5 as appropriate, and dimension-scaled version. Root independently checked151032RLT inequalities across55 finite constructions in verification/check_point_packing.py; the analytic projection-block formula proves PSD for all n. Do not turn the numerical n<5 symmetry observations or unimplemented ORD models into exact claims.
- Scaling: explain two-endpoint interpolation, identical units with shared intensive variables and the disaggregated exact hull, including zero scales. Retain the counterexample to unconditional scale-cost separation, correct extensive-only perspective formula and rectangularity criterion for universal scale-only cost separation. These are short distinct derivations; identify classical disjunctive/perspective machinery. Integral-count-polytope extension and Shapley–Folkman scope can be concise. Do not claim that adding global linking balances preserves a local hull or that intermediate catalog sizes can be deleted from the feasible model.
- P-split: directly inspect the published formulation, minimal sharing assumption, retained-domain convention and Theorem6 before discussing its universal nonexactness claim. Give the retained-box counterexample and its explicit lift, finite-link local directional repair, then the completed exact translated-ball basic projection/Hausdorff formula. The earlier correction note's proposed ball follow-up is stale: notes/common-factor-p-split-balls.md already solves it. Include rational coordinate comparison and strongest exact-image result: arbitrary convex auxiliary-only strengthening retains the original witness, while aligned exact-image epigraph convexification is exact. Separate exact auxiliary-image hull from the full feasible graph, and use exactly transformed retained domains. The mathematical correction concerns a theorem's universal statement, not validity of the formulations. Root directly checked the source HTML and these proofs; see literature-screen-additions.md.
- Rank-one global lift size is a separate resource: describe the explicit correlation face and stability/approximate transfer with their hypotheses and norm/accuracy scale. Clearly credit inherited conic lower-bound inputs. Exact fixed-block/SOCP growth and unrestricted PSD superpolynomial order are different statements; fine entrywise-l1 approximation is at explicit order m^-2. No inference of a spatial tree lower bound merely from lift size. These supporting comparisons need not reproduce the complete independent rank-one research program.
- FBBT: describe the exact primitive contractor/fair-update model, PosSLP-hard limiting-bound approximation (PosSLP is not known NP-hard), and the small bilinear circuit yielding at least2^(2^n-1) primitive updates. Explain residual versus distance-to-limit and the limitation concerning accelerated/global contractors. Inspect the actual reduction/recurrence and original fixed-point/slow-convergence sources before retaining any precise claim; do not infer hardness from existing PASS labels.
- Briefly contrast the adjacent integer-precision topic using the scalar and simultaneous-bilinear accuracy results. They count binary assignments or parity classes, not certified spatial regions. Keep this a resource comparison rather than annexing topic1's full theory.

Add a concise synthesis/open-questions discussion. Genuine open problems include exact cubic constant, second-order lower asymptotic, finite-aspect optimum, width>=3 structural constants, unequal-aspect frequency-two bound and unrestricted affine branching. Describe completed refinements accurately: fixed-ambient balanced orientation, coefficient-regularity cardinality improvement (if accepted), and degree-loss-free local graph lifts (if accepted). Do not imply every open problem must be solved to complete the paper.

Unify notation, theorem hypotheses, citations, cross-references, formula versions, appendices, and figure/table formatting. A compact roadmap/results table may help readers, but avoid a massive duplicate theorem list. Keep the main narrative readable while retaining full proof/certificate substance in appendices. Do not invent authors, affiliations, journal acceptance, comprehensive priority clearance or formal verification.

Supply an exhaustive source-to-final-label coverage ledger in process/claim-coverage.md, explicitly distinguishing full core proofs, supporting comparisons and topic1/out-of-scope files. Record every bounded development attempted, completed or left open. Update README build/replay instructions and a clear process/stage-06-author.md with changed-file list, original-source checks/access limits and validation. The final coordinator will write the final process accounting after review.

Compile using verification/build_and_check.py; resolve undefined/multiply-defined references and overfull boxes. Check tables, displayed equations and code blocks visually, including pages changed by new content. Make code listings usable and exact-check programs reproducible. Do not modify frozen snapshots, literature or other paper directories. Return only when the complete integrated manuscript is written, checked and compilable.

Integration and navigation: the cumulative accepted Stage3 draft is already
62 pages. Keep the required full proofs and coverage, but organize the final
paper so readers can identify the central results and their dependencies.
Provide a concise roadmap and a contents list appropriate to its eventual
length. Separate central theorem statements from distinct supporting proofs
in appendices where that improves reading. Do not remove assigned results
merely to shorten the paper, and do not claim that length, internal review,
or compilation establishes suitability for a particular journal. Rewrite
PROCESS.md into a clear final status and chronological audit with exact round
and report counts, rather than retaining contradictory present-tense statuses.
Keep the complete referee reports, adjudications, correction logs and snapshots
available as process evidence. The paper itself should contain mathematical
content and reproducibility information, not the internal agent conversation.

Additional preparation: verification/stage06-additional-primary-checks.md records
direct primary checks of Braun Theorem6(i), Starr Appendix2 Lemma2/corollary,
and the Esparza/Stewart slow-convergence antecedents. Use precise version
locators and keep primitive FBBT distinctions. New Stage5 order-one
refinement remains pending until its stage gate passes; include it in
final synthesis if accepted.
