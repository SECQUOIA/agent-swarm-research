# Final whole-manuscript review 01, Stage 5 round 01

Reviewer: `/root/reviewer01`. Date: 19 September 2026.

## Definitive verdict

**Approve the manuscript in its present scientific scope. No unresolved major or minor issue found. No correction is requested.**

I reread the current complete manuscript, including every included section and appendix, all 17 tables, the 27-entry bibliography, and the reproduction instructions. This is a whole-paper judgment, not merely confirmation of the latest wording changes. The paper is a defensible standalone computational/methodological submission about matched radial versus point separation in one NLP-assisted GDP implementation. Its scope and empirical limitations are plainly stated; it does not rely on an unsupported new-algorithm claim to justify the work.

I did not read other current final-review reports, edit manuscript sources, or spawn agents. This report does not promise journal acceptance or claim that a future reader cannot suggest additional research. I found no present scientific or presentation defect requiring resolution before submission of this scoped paper.

## Mathematical assessment

- **Definitions and target.** The original integer coordinates, GDP indicators, continuous term sets, finite row collections and compact boxes are clearly separated. The joint domain for nonlinear global rows includes the indicators. Smoothness/convexity are stated assumptions, not properties inferred from extraction. The relaxation target is the intersection of individual disjunctive hulls and global/logic constraints, not the full integer GDP hull.
- **Cuts and closure.** The affine perspective identity, zero tangent constant, completeness of all tangents, and inactive-origin convention are correct. The explanation explicitly distinguishes empty positive-weight lifts from the intended inactive origin, avoiding a false closure assertion. The convex-combination proof for an individual union hull works with empty terms and grouped alternatives. Finite valid box-derived big-M coefficients are distinguished from the hull construction.
- **Compact epigraph.** The lower tangent minimum and finite gradient-based upper bound preserve an optimal lift while not purporting to preserve arbitrary redundant epigraph values. The prototype's lack of automatically installed upper epigraph bounds is stated where its consequence matters.
- **Separation and packing.** I reconstructed the anchor supporting inequality, the `delta*v/(L*D)` margin, and the original/transformed coefficient bounds. The integral theorem packs row-assigned candidates only when earlier cuts hold and the term is active. The fractional theorem packs lifted blocks using weighted residuals and a normal bound independent of the selection weight. Constant rows and joint global coordinates are handled. Neither theorem is silently converted into exact incumbent production or finite objective-gap closure.
- **Small weights and repair.** The residual-calibrated omission rule, positive denominator floor and weaker fixed-cutoff residual bound follow from the stated finite row bound. The geometric repair is a convex combination with the correct coefficients and distance estimate. Its weighted summation is confined to a single disjunction. The square-root counterexample correctly disproves a uniform linear objective-error inference after intersection with global constraints. The conclusion now states this precise linear scope.
- **Value and callback conclusions.** Common compactness and vanishing residuals give feasible cluster points; asymptotically optimized valid outer masters give the matching upper inequality in the value argument. Integrality remains closed at limits. The single-tree theorem expressly restricts fresh cut generation to old-cut-feasible callbacks and requires finite old-cut resolution, complete master solving and finite optional refinement. The algorithm description does not claim that the numerical implementation establishes these hypotheses.
- **Finite arithmetic.** Retaining the full function offset at approximate roots preserves exact tangent validity. The example with an omitted offset is correct. The coefficient perturbation scheme needs two error allowances plus solver feasibility tolerance, as stated, and now explicitly takes a positive normal bound. Numerical feasibility, gap and reference tests are not represented as interval certificates.
- **Representation and geometry.** The same-anchor/exact-root invariance has the necessary increasing-convex transformation and positive boundary derivative conditions. The ECP weakening is a same-point result. The scalar recurrence describes actual retained-cut master optima, has the claimed strict transient lower bound, and agrees with its Newton expansion at fixed representation. The centered ellipsoid result is confined to that geometry. Both off-center disk witnesses correctly establish non-containment in opposite directions, including at perspective weight one.
- **Generated models and cones.** The allocation and region equations, draw order, dimensions, domain margins, convexity and explicit feasibility witnesses are internally consistent. Cost-law monotonicity is now correctly confined to the nonnegative interval while neighborhood convexity/smoothness remain available for the main assumptions. The positive-weight scalar exponential/log/reciprocal/quadratic cone identities are correct. At zero weight, bounded copied variables and the aggregate positive-coefficient cost constraint remove spurious positive auxiliaries. Region exponential auxiliaries similarly vanish. The exact quadratic slack representation has the correct closure, and its source scope is not confused with general nonlinear conic representability.

No proof gap, invalid theorem, unsupported dominance assertion or incorrect model transformation emerged from this reconstruction.

## Question, literature, evidence and implementation

The literature section identifies the essential antecedents: disjunctive hulls, logic-based OA, perspective cuts, Veinott/ESH, the gauge relationship, SHOT's combined ESH/ECP and NLP strategies, disjunctive cut strengthening, basic steps, exact cone hulls and conic OA. It distinguishes the proposed termwise radial procedure from fixed-normal optimization-based strengthening without claiming dominance. The current abstract also correctly distinguishes hull perspective cuts from big-M deactivated tangents. I checked the SHOT comparison against the primary publisher article in this final round; it supports the stated algorithmic precedent and metadata.

The original contribution remains the measured matched-policy tradeoff, its executable explanatory diagnostics, and explicit accounting/verification of its conditions and limitations. The elementary proofs are useful self-contained foundations without a priority assertion. The experiment answers a concrete solver-design question even though the timing advantage is modest and the strongest supported conic alternative is faster on the declared common cohorts.

The numerical and exact contracts are consistently separated. Shared ECP interiors, rowwise boundary searches, approximate exterior endpoints, untransformed rejection checks, absent intermediate finiteness guards, numerical normalization risk, fixed weight cutoffs, LP stalls, nonlinear incumbent recovery and callback cut retention are all described at the right level. Internal and independent benchmark gap/feasibility formulas are distinct. The negative no-integer-NLP ablation is compatible with the conditional theorems and is not advertised as an NLP-free method.

The 1,464 benchmark records and 420 reference calls have separate, complete accounting. Related generated controls, same-seed repetitions, untuned-but-not-unseen held-out references, concurrent scheduling and external expression scope limit inference. Common-solved shifted means, full-cohort PAR10 penalties, arithmetic work means and paired medians are not conflated. The cone comparison is conditional timing with mixed external coverage. Invalid witnesses, missing interface outputs, time limits, unsupported cases, inaccurate roots and followups retain their original cohorts. Numerical conic dual estimates and infeasible assignment statuses remain uncertified.

The model and algorithm are in the main article; complete proofs, oracle/model details and secondary tables are accessible in appendices. I found the organization coherent and the required definitions, equations, evidence and qualifications present without dependence on repository notes. The title, abstract, results, discussion and conclusion tell the same scoped story. No broad new baseline or further theorem is necessary to substantiate that story.

## Delivery and presentation

The paper and research supplement have separate roles, manifests and commands. Table regeneration is not described as fresh primal validation; the independent arithmetic audit honestly reuses the original-model checker. The portable audit instructions choose extracted model sources and acknowledge reuse of an existing pinned environment. Anonymous authorship and the lack of an invented public DOI are appropriate for the delivered anonymous source package. Third-party attribution remains intact.

I independently viewed current rendered pages 17 and 27: the work table/figure and the value/callback proof material are legible and unclipped. Every citation key and reference target resolves in the source check below. The prior artifact relocation, fresh-witness and clean-build records remain applicable, and the current final fingerprint confirms the reviewed delivery has not changed.

## Actual checks in this final round

1. Fresh `cat`/`sed` reads of `main.tex`, all included section/appendix files, `references.bib`, every `tables/*.tex` fragment, the main README and the Stage 5 author/fingerprint records. Targeted follow-up reads recovered portions truncated by a combined tool output.
2. Inline standard-library Python checked all **68 paths** in `process/stage05-round01-source-sha256.json`: all matched.
3. The same independent check found **83 unique labels**, **62 distinct parsed reference targets**, and **27 cited bibliography keys**, with no duplicate label or missing target/key. The current submission PDF is byte-identical to `main.pdf`.
4. Independently recomputed the eight compact-record batch counts and the six held-out single-tree ESH/ECP comparisons directly from `data/records.json`, without importing the paper regeneration script or study analyzer. Counts were 663, 132, 132, 9, 351, 144, 9 and 24. ESH/ECP solved counts were 33/32 with hull and 33/31 with big-M in every repetition. Shifted-mean ratios were 0.940589/0.957429, 0.950588/0.946034 and 0.940539/0.937646 by schedule; these support the printed 4–6% description and rounded table entries.
5. Rendered only the current pages inspected, with outputs isolated in `/tmp`:

   ```bash
   pdftoppm -f 17 -l 17 -singlefile -scale-to 1400 -png \
     paper-lbesh/main.pdf /tmp/lbesh-final-r01-page17
   pdftoppm -f 27 -l 27 -singlefile -scale-to 1400 -png \
     paper-lbesh/main.pdf /tmp/lbesh-final-r01-page27
   ```

   Both completed successfully, and both images were inspected.

6. Opened and read relevant portions of the primary [Lundell–Kronqvist–Westerlund SHOT article](https://link.springer.com/article/10.1007/s10898-022-01128-0), confirming its published metadata and support for the ESH/ECP, fixed-integer primal-heuristic, single-tree and ECP-fallback discussion. Earlier primary-source inspections are documented in my staged reports and were not represented as fresh executions here.

No shared manuscript or delivery file was modified. No optimizer benchmark, full raw-data audit, artifact repackaging, project-wide verification or CI inspection was repeated. There are no requested fixes and no deferred valid minor issue in this report.
