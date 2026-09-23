# Development and review record

The user requested a complete standalone paper on conic reformulation complexity, with critical mathematical verification and five independent reviews at every stage and after integration. Existing notes are evidence to investigate, not mathematical authorities.

## Planned stages

1. Source coverage, definitions, local contact bounds, and the selection-free single-ball certificate-rank frontier.
2. Global regularity, factor and dimension complexity, product sharing, and sharp constructions.
3. Restricted standard-barrier parameters, recession arguments, rigidity, and the status of divisible regimes.
4. General cone formulations, grouping and packing tradeoffs, movement consequences, and the boundary of query interpretations.
5. Literature synthesis, introduction, integration, submission packaging, and full-manuscript review.

The source audit may change the grouping. A stage is complete only after the author finishes, five independent reviewers report, the root assesses all findings, and a different author fixes every accepted issue. Any accepted major issue triggers another five-reviewer round. Remaining minor issues are repaired before proceeding. A separate five-reviewer whole-manuscript cycle follows the completed draft.

## Initial state

- New deliverable directory: `conic-lift-complexity/`.
- Existing `formal/` is untracked user work and is left untouched.
- Existing manuscripts and research notes are left unchanged.
- Run project scripts through `/home/sgusev/miniconda3/envs/qipm/bin/python` or `conda run -n qipm`.
- Priority claims require source-specific comparison. A negative literature search does not establish novelty.

## Stage 1

Author dispatched. Root independently investigates coverage and primary literature.

Root preliminary reading of the two mathematical sections found a minor interval-edge construction error: a primitive face is a ray, so its affine sections cannot produce a nondegenerate bounded interval. The author was asked to replace it by a two-ray frame section or the one-coordinate fixed-tail paraboloid construction before review. The real 2-by-2 specialization of the Peirce-perspective determinant and rank-one completion formulas was checked by hand and is consistent. The first build produced a nine-page PDF. These preliminary checks are not a substitute for the required independent review.

Five reviewers completed their independent reports, all finding no major mathematical issue. Root accepted the minor findings and consolidated them in `stage1-assessment.md`. A different author is assigned the corrections before Stage 2 starts.

The correction author implemented all eight consolidated items and verified the original norm-tree citation. Root checked the revised passages and correction record. Stage 1 is complete; the corrected nine-page PDF builds without warnings.

## Stage 2

Author dispatched for product certificates, global smooth regularity and topology, exact no-sharing/frontier statements, and essential counterexamples. Source-map Stage 2 notes are to be consolidated into proved general results; no workbench theorem is accepted solely on its status label.

The author completed Sections 3–5 and a clean 22-page build. The selected-rank theorem was unified across all simple EJA dictionaries. An independent author-side topology check simplified the real PSD exception proof to an affine-kernel argument. Unique general-cone topology and product-orbit extensions were explicitly routed to Stage 4.

An interruption occurred during reviewer dispatch, before any review report was saved. On resumption, five fresh independent reviewers were dispatched under `stage2_resume_review1` through `stage2_resume_review5`. Their reports use the planned `stage2-review1.md` through `stage2-review5.md` paths. No Stage 3 author work begins before this review/correction cycle is complete.

All five reviews are now complete, with no major findings. Root accepted seven consolidated minor corrections in `stage2-assessment.md`, including a short omitted worst-pure-row-certificate frontier and a corrected general-cone source disposition. A different author is assigned these corrections.

The separate correction author implemented all seven items. Root checked the revised whole-slice compression wording, positive-capacity restriction, and complete coefficient-matching proof of the PSD2 worst-pure-row frontier. The 23-page draft builds without warnings. Stage 2 is complete.

## Stage 3

Author dispatched for restricted standard barriers, fixed-formulation arbitrary-barrier results, exact norm-tree parameters, selection-free one-channel rigidity and wide-cap rigidity, and critical investigation of the remaining bounded narrow-cap range. Root's preparation file records candidate proof improvements and explicit risks. All assertions must have complete proofs or accurately delimited statements; an unproved classification must not be promoted to a theorem.

The author completed Sections 6–7 and a clean 36-page build. Root read both sections and the independent bounded check. Five formal independent reviewers (`stage3_review1` through `stage3_review5`) are now checking the complete new material with different areas of emphasis. No Stage 4 author work begins before this review/correction cycle closes.

All five reports are complete and find no major issue. Root accepted eleven consolidated minor corrections in `stage3-assessment.md`, including two omitted counterexamples and explicit routing of the all-symmetric constant-nullity product theorem to Stage 4A. A separate correction author is assigned all accepted items before the next stage.

The separate correction author completed all eleven items. Root checked the corrected positivity conditions, both explicit matrix examples, attribution, source routing, and final build logs. The 37-page manuscript builds without unresolved references or warnings. Stage 3 is complete.

## Stage 4A

The remaining structural material is divided into sequential stages 4A (topology and support rigidity), 4B (general formulations and packing), and 4C (nonsymmetric barriers and approximation). Each receives its own author, five independent reviews, assessment, and separate correction author. Stage 4A now starts, including the mandatory constant-nullity product theorem and contact-accessibility corollary deferred explicitly from Stage 3.

The Stage 4A author completed the central general-cone covering, all-EJA product equality classification, and compact full-fiber/accessibility theorem. Abstract splitting and individual submersion refinements, projective phase embeddings, restricted near-saturation counts, and the strengthened column-rank nullity theorem are in appendices. The integrated 55-page manuscript builds without warnings, unresolved references, or overfull boxes. Exact source dispositions and primary-literature verification are recorded in `stage4a-author.md` and three bounded author audits. Five independent formal stage reviews are now required before Stage 4B begins.

All five independent reviews are complete. Root accepted three minor hypothesis/scope clarifications and no major issues, as recorded in `stage4a-assessment.md`. A separate correction author is assigned all three before Stage 4B begins.

The separate correction author implemented all three. Root checked the revised hypotheses and comparison, correction report, and clean 55-page build. Stage 4A is complete.

## Stage 4B

Author dispatched for whole-row/minimal-dimension rigidity, bounded-face sharing, connected-extreme balance slices, lp granularity and smooth perspectives, and spectral/chordal packing. Candidate weighted-geometric-mean curvature applications require independent development. Each distinctive source result must be proved, explicitly subsumed, or precisely routed; no unproved source status is authoritative. This stage receives five independent reviews after its author finishes.

The author completed five integrated sections and a clean 80-page build. Five independent reviews are complete. Root accepts the integer-cap clarification and a substantive strengthening of the local sharing bound and global capacity budget, detailed in `stage4b-assessment.md`. Although the original weaker inequalities are valid, the impossible-bonus discussion and materially improvable theorem require a major revision for workflow purposes. A separate fixer is assigned, followed by five further independent reviews before the stage closes.

The separate fixer implemented the strengthened common-annihilator and aggregate-cover bounds and propagated them through the spectral and combined-budget statements. Five fresh independent reviewers then read all five sections and their dependencies. All five second-round reports identify no major or minor issue. Root read every report and checked the corrections independently. The clean 81-page draft closes Stage 4B.

## Stage 4C

Author dispatched for nonsymmetric barrier bounds and their classical attribution, relative-entropy aggregation, conditioned approximation and robust topology, conditioning counterexamples, and exact compiler scope. The author must resolve the source errors identified in `root-stage4-preparation.md`, distinguish hypotheses from unproved classification claims, and record complete source dispositions. Five independent reviews follow completion.

The Stage 4C author completed five main sections and two appendices, with bounded helper authors and full source dispositions. It strengthens the graph-based exponential-factor lower bound and the conditioned C2 error estimate, and corrects a previously unrecognized zero-column boundary failure in the entropy lift. Classical barrier machinery and compiler primitives are attributed, with open optimal nonsymmetric parameters and conditional algorithmic implications clearly delimited. The integrated stage is frozen for five independent formal reviews; no Stage5 author work begins until its review/correction cycle closes.

All five independent reviews are complete, with no major findings. Root accepted four minor precision corrections in `stage4c-assessment.md`. A separate fixer implemented all four, and root checked the changed passages and clean 114-page build. Stage 4C is complete.

## Stage 5A

Author dispatched for reformulation-dependent movement, exposed-minor and dimension-only metric bounds with proper attribution, norm-tree exact distance asymptotics, spectral profiles, and the balance-slice/shared-spectral applications deferred from Stage 4B. The new all-objective weighted norm-tree coefficient is a candidate requiring independent development, not an accepted theorem. The existing companion paper must be compared explicitly. Five independent reviews follow the author's completed stage.

The author completed four main sections and a clean 133-page integrated build. The weighted active/inactive tree coefficient has a full potential lower bound and explicit feasible-curve upper bound; classical and companion movement results are attributed. Root personally read all four sections and checked their main proofs and constants. Five independent reviewers are now checking the frozen stage, with complete reports required before corrections or Stage 5B authorship begin.

All five Stage 5A reviews are complete, with no major findings. Root accepted five consolidated minor corrections in `stage5a-assessment.md`. A separate fixer implemented all five, and root checked the changed passages, correction record, and clean 133-page build. Stage 5A is complete.

## Stage 5B

Author dispatched for resource ledgers, conditional work composition, sparse and reduced Newton comparisons, quantum query/output contracts, and active-constraint compilers. The allocation-aware linear off-center quotient bound in `root-stage5-preparation.md` is a new candidate requiring independent development and review. All prior resource/proxy and access-model qualifications must be preserved. Five independent reviews follow the completed stage.

The author completed all five sections and froze a clean 165-page integrated draft. Root read every new section and checked the central proofs and output contracts. Five independent reviewers have been dispatched; the first has completed its report with no findings. The remaining four reviews must finish before assessment, any corrections, or Stage 5C authorship.

All five first-round reviews are complete and find no mathematical defect. Root accepts reviewer 5's completeness suggestion and chooses to include the precise fresh-update scale-maintenance theorem. Although the reviewer classified this as minor and allowed explicit deferral, root treats substantive inclusion as a major coverage revision so the new persistent-output theorem receives another five independent reviews. A separate correction author is assigned the bounded addition described in `stage5b-assessment.md`.

The separate correction author completed the fresh-update, invocation-service, and fixed-path caching statements with full proofs and an explicit nondestructive quantum value-output contract. Root read the entire addition and correction record. The clean 167-page manuscript is frozen for five fresh second-round reviewers, each assigned all five Stage5B sections and the added theorem. No Stage5C author work has begun.

All five second-round reviews are complete and identify no major or minor issue. Root read every report and independently checked the added proofs and clean build. Stage5B is complete.

## Stage 5C

Author dispatched for the final abstract and introduction, precise contribution and prior-work comparison, reader navigation and notation, current source dispositions, bibliography verification, closing synthesis, and submission-source packaging. All proved developments and scope boundaries must be preserved. This authored stage receives its own five independent reviews before the separate five-reviewer whole-manuscript cycle.

The author completed the comprehensive introduction, abstract, model and notation tables, six-part navigation, closing synthesis, eight primary-literature comparators, and current source routing. Root read the authored prose and helper reports; precision comments were incorporated before freezing. The clean 183-page draft has 499 unique labels, 87 references, and no warnings or unresolved references. Five independent Stage5C reviewers are now checking the integration and its theorem/literature dependencies. The separate whole-manuscript review has not started.

All five Stage 5C reviews are complete with no major findings. Root accepted
five consolidated minor summary corrections in `stage5c-assessment.md`.
A separate fixer applied all five and replaced temporary README/source-map
status text with workflow references. Root checked the corrected passages,
the correction report, and clean 183-page build. Stage 5C is complete.

## Whole-manuscript review

The integrated manuscript is frozen for five fresh independent reviewers.
Each reviewer must personally read every main section and all four appendices,
assess proofs and scientific claims, inspect prior-work attribution and scope,
and review completeness, consistency, organization and readability. Different
emphases do not divide the full-reading obligation. These reviews are separate
from the completed Stage 5C integration reviews. Root will assess all five
reports before assigning any accepted corrections to a separate fixer; any
major correction requires another five independent whole-manuscript reviews.

All five whole-manuscript reports are complete. Every reviewer personally
read the entire manuscript, and none identified a major issue. Root read
every report and accepted the consolidated minor integer-cap correction
in `final-assessment.md`. A separate fixer is assigned the two explicit
hypothesis edits and standing cap convention, followed by a clean build.
No mathematical proof revision or further five-review cycle is required
for these minor corrections. Final artifact verification remains pending.

The separate final fixer applied every accepted correction, and root
checked all changed passages and the correction report. The final clean
build produces 183 pages with 499 unique labels and 87 cited bibliography
entries, with no warnings or unresolved references. Root independently
verified the complete included-file set and inspected rendered pages 1,
42, 123, 135, 149 and 183. The final source/PDF hashes and artifact checks
are in `root-final-artifact.json`; the fixer's validation and complete
build logs are retained. All accepted findings are resolved. All stages
and the separate whole-manuscript review cycle are complete.
