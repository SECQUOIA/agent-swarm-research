# Stage 1 independent review 04, round 1

Date: 19 September 2026. Scope: authored introduction, related work, bibliography, scaffold, and coverage/literature maps. Later empty sections were treated as intentional. No other current review reports were consulted.

## Verdict

Proceed after minor corrections. I found no major mathematical, empirical, novelty, or scope problem in the authored Stage 1 material. The research question is concrete and meaningful: the cost and measured benefit of changing radial versus point separation inside a fixed GDP solver. The manuscript accurately limits originality to the particular empirical comparison, diagnostics, and documented contracts. It does not confuse established perspective cuts or ESH with a new inequality family.

The coverage map is comprehensive for the developed topic: it includes mathematical assumptions and counterexamples, the proof/prototype distinction, generated and external experiments, conic alternatives, unsuccessful ablations, baseline followups, and provenance. It makes the intended paper substantially more than a favorable performance summary. This verdict concerns that plan and the authored introductory material; it does not certify proofs or sections that have yet to be written.

## Major findings

None.

## Minor findings requiring correction

1. **Qualify the disaggregated-master comparison as the hull variant.** `sections/related-work.tex:17` says that the present implementation maintains disaggregated variables. The paper also studies a big-M variant, which has no such copies. The source confirms that `Master._add_disjunction` introduces `nu` only inside `formulation == "hull"`, and `cut_expr_disjunct` has a separate original-variable big-M branch (`code/minlp_solver_lab/lbesh/master.py:85`, `:158`). Change the sentence to identify the hull variant explicitly; optionally add that the same original-space radial policy is also studied with big-M masters. Similarly, the final sentence of `related-work.tex:12` should qualify the displayed perspective formula as describing the hull variants. This preserves the exact and useful comparison with Kronqvist–Misener without describing all eight methods as disaggregated perspective methods.

2. **Introduce the quadratic row and lift variable before the conic equations.** `sections/related-work.tex:22–27` introduces `Q`, `c`, `d`, and `t` without stating the original row or the role of `t`. Write, for example, “For a row $g(x)=x^TQx+c^Tx+d\le0$ with $Q\succeq0$, a nonnegative lift $t$ gives …”. The displayed system itself is correct: eliminating $t$ at positive weight gives the quadratic perspective inequality, while scaled bounds force $v=0$ at zero weight and the other inequality forces $t=0$. Explicit definitions make this a standalone explanation for the intended reader.

3. **Name the timing statistic in the introductory numerical claim.** `sections/introduction.tex:12` calls the 4–6% values “timing averages.” They are one-second-shifted geometric means of end-to-end wall time on fixed common-solved cohorts, rather than arithmetic averages or a typical per-instance improvement. “Common-solved shifted geometric mean wall times” is a concise accurate replacement; the shift formula can remain in the later methods section. The reported rounded percentages are supported by the saved summaries.

## Actual checks and evidence

- Read all Stage 1 TeX, `main.tex`, `README.md`, `references.bib`, `evidence/coverage.md`, and `evidence/literature.md`.
- Read the source development theory's assumptions and perspective/separation sections, its later section inventory, the development literature assessment, and the completed study-results note. Matched the advertised future coverage against those materials, including the no-NLP qualification and separate followups.
- Inspected the local primary fulltexts for Bestuzheva–Gleixner–Vigerske (perspective linearization equivalence) and Coey–Lubin–Vielma (conic OA and subproblem alternatives).
- Opened the primary Kronqvist–Misener manuscript at https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf. Its Section 3/equations (11)–(13) support the description of fixed normals and termwise optimization; its introduction and Section 2 support the ESH/disjunction and nonlinear-perspective precedent. The manuscript does not justify claiming that the present method dominates that strengthening method, and the draft correctly avoids such a claim.
- Opened the primary v2 quadratic-hull paper at https://arxiv.org/html/2508.16093v2 and checked the CEHR subsection; the draft's quadratic lifted system and limited equivalence claim agree with it.
- Opened the Serrano–Schwarz–Gleixner publisher article, https://link.springer.com/article/10.1007/s10898-020-00906-y, the Nguyen–Pulsipher arXiv record, https://arxiv.org/abs/2608.27707, and official discopt documentation, https://kitchingroup.cheme.cmu.edu/discopt/mip_nlp.html. The draft appropriately treats the last item as current software context and the infinite-dimensional paper as adjacent context, without claiming a tested baseline or detailed theorem equivalence.
- Used read-only Python JSON inspection to count the primary 663 records, two 132-record repeats, and nine quadratic conic records. Inspected final `stability_context.json`, `ablations_references.json`, and `legacy_scope.json`. The saved hull timing ratios are approximately 0.941, 0.951, 0.941; big-M ratios are 0.957, 0.946, 0.938. These support “approximately 4–6%.” The ablation and external summaries agree with the introductory interpretation. This was a summary/record consistency check, not a fresh witness audit or optimization run.
- Algebraically checked the displayed perspective tangent by differentiating the positively homogeneous perspective and the CEHR identity by eliminating the lift variable. No incorrect equation was found.
- No source files were edited, no solver benchmarks or project-wide tests were run, and no CI status/logs were inspected. No compilation was needed for this content-focused review.
