# Stage 1 independent review 05, round 01

Reviewer: `/root/reviewer05`. Date: 19 September 2026.

Scope: manuscript scaffold, introduction, related work, bibliography, README, and coverage/literature maps. Later sections are deliberately empty and are not defects in this stage. I did not read other current review reports or edit manuscript sources.

## Verdict

**No major issue identified in this bounded stage; three minor precision corrections are recommended before advancing.** The scaffold builds as a standalone document, all citation keys resolve, the relationship to the main precedents is appropriately qualified, and the introduction presents both the empirical benefit and the important negative findings. The main text does not claim an unsupported new cut family or general dominance. This verdict does not certify the mathematical results or raw-data analysis assigned to subsequent stages.

## Actionable minor findings

1. **Include the objective in the opening definition of convex GDP.** Location: `sections/introduction.tex:2`, sentence beginning “In a convex GDP”. Convex nonlinear constraint functions alone do not make a minimization GDP convex within each alternative when the objective can be nonconvex. State that the minimization objective is convex (or represented by a convex epigraph), with convex inequality functions and affine equality constraints. This is a local definition correction; it does not challenge the topic's intended assumptions.

2. **Name the aggregate used for the headline timing result.** Location: `sections/introduction.tex:12`, “Common-solved timing averages favor ESH by approximately 4--6\%”. The retained results report shifted geometric means rather than generic averages. Say “common-solved shifted geometric mean wall times” and explicitly attach this result to the single-tree comparisons. In the following sentence, say “lower mean cut counts and LP iteration counts on the matched cohorts” to make clear that the statement is an aggregate result rather than a per-instance guarantee. The values themselves agree with `notes/lbesh-study-results.md`: the six single-tree ratios range from 0.938 to 0.957; the four work tables report arithmetic means with lower ESH cut/LP values.

3. **Restrict the disaggregated-variable description to the hull variant.** Location: `sections/related-work.tex:17`, “The present implementation instead maintains disaggregated variables”. The paper explicitly studies both hull and big-M masters. This unqualified sentence describes only the hull implementation and can mislead readers about the big-M comparison. Write “Our hull variant instead maintains disaggregated variables ...” and, if needed for the contrast with Kronqvist--Misener, explain that term-specific radial tangent generation is also used with the big-M master. The subsequent algorithm section can give the complete formulas.

## Scientific and bibliographic assessment

- The displayed perspective-cut equation is the valid affine homogenization of a tangent, and for positive selection weight it is the tangent of the perspective at any point whose normalized argument is the stated base point. The local Bestuzheva--Gleixner--Vigerske fulltext, Section 3 and Theorems 1--2, supports the equivalence and extension discussion.
- The CEHR inequalities in `related-work.tex:23--27` correctly encode the bounded convex quadratic perspective target when accompanied by the stated scaled bounds. The [primary v2 manuscript](https://arxiv.org/html/2508.16093v2) confirms the title, authors, 17 March 2026 revision, and that CEHR is a re-derived rotated-cone formulation. No spurious first-priority claim is attributed to it here.
- The [primary Nguyen--Pulsipher record](https://arxiv.org/abs/2608.27707) confirms the recent adjacent work's title, authors, and extension of logic-based outer approximation and cutting-plane reformulation to infinite-dimensional GDP. The narrow statement in the paper is supported.
- The [official discopt documentation](https://kitchingroup.cheme.cmu.edu/discopt/mip_nlp.html) supports treating algebraic ESH as relevant existing software context. Its citation is appropriately marked as documentation rather than a tested comparator or peer-reviewed priority source.
- The literature and coverage maps distinguish planned later work from completed evidence, fixed-cutoff implementation from the theoretical residual rule, floating-point acceptance from exact certification, and independent-disjunction hulls from the full GDP hull. Those distinctions should be preserved in later stages.

## Executed targeted checks

1. Read `main.tex`, `README.md`, both authored sections, `references.bib`, the two evidence maps, and the Stage 1 author record. Inspected the relevant numerical summary and work-statistics passages in `notes/lbesh-study-results.md` and conditional hull handling in `code/minlp_solver_lab/lbesh/solver.py`.
2. Copied the manuscript to the isolated directory `/tmp/lbesh-stage01-review05.bBRQk6`. Ran `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex` there, forcing a clean rebuild. Result: success, five-page PDF. The final `main.log` has no undefined citations/references, overfull/underfull boxes, or warning lines. Initial-pass undefined citation messages in the combined console log resolve in the normal BibTeX/rerun cycle.
3. Used `pdftotext -layout main.pdf main.txt` to inspect the compiled reading order and rendered bibliography. The title, equations, reference numbering, diacritics, and URLs survive the build; no missing content was detected in the completed stage.
4. Ran a Python regular-expression inventory over `sections/*.tex` and `references.bib`: 16 bibliography entries, 16 unique keys, no missing cited keys, and no uncited entries.
5. Read the local Bestuzheva primary fulltext's cut-equivalence passages and opened the three primary/official web sources linked above.

No project-wide checks, optimizer runs, or CI inspection were performed.
