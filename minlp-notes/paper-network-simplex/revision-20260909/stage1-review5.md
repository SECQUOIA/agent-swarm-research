# Stage 1 independent review 5

Reviewed 2026-09-09. Snapshot: `stage1-round1/paper-network-simplex`, with the sibling frozen `code` directory. Locators below are source-file line numbers relative to that paper snapshot. I read `process/REVIEW_GUIDANCE.md`, the complete revised abstract, introduction, prior-work subsection, conclusion, and bibliography, and supporting formulation and computational material. I consulted the author report and literature audit as guides, then checked the evidence identified below. I did not read other current reviewers' reports, coordinate judgments, edit the submission, or delegate work.

**Verdict: no major issue identified in the Stage 1 positioning and exposition; one minor scope clarification should be made before this stage closes.** This is not a verdict on the complete mathematical manuscript or the later proof and implementation audits.

## Scientific assessment

The revision states a meaningful contribution without claiming that sparse product selection creates a previously unknown convex hull. The opening credits disaggregation and the complete EC&R framework, and the contribution list places the work inside that established hull. It distinguishes the particular residual-coordinate construction and individual-product completion from unrestricted extension complexity. The coefficient lower bounds are described as restrictions on actual retained product coordinates, invariant under affine-hull equations, rather than as conclusions from one nonunit dual multiplier. Those distinctions materially improve the scientific position.

The potential importance is clear: structural descriptions with controlled coefficients, exact separation and constructive membership certificates for specified graph classes, and examples showing the limits of simple projected inequalities. The paper does not need a generic optimization speedup to make those contributions worthwhile. The introduction and conclusion correctly preserve equality conservation, the directed unit-data flat-chain topology, and the separate treatment needed for additional coupling constraints. The statement about small treewidth and growing coefficients is consistent with the simple series–parallel family; it does not assert the fixed-label threshold for all series–parallel networks.

The practical claims are appropriately narrow. In particular, `sections/00-introduction.tex:140–152` and `sections/09-conclusion.tex:28–33` do not infer speed from fewer variables or from a rational-operation bound. The retained records support the specific introductory example. Independently recomputing the five-run medians gives 30.3635 ms for full disaggregation, 30.3763 ms for global merging, 10.1565 ms for initial compression, and 18.3895 ms for elimination in the all-labels-observed control. Their respective variable counts are 7,215, 7,215, 495, and 367. Thus the introductory rounding to approximately 30 and 10 ms is faithful, and the statement that elimination is smaller but slower is supported. On the original sparse instance, global merging takes 4.2506 ms versus 4.8228 ms for initial compression; on the budgeted instance the corresponding medians are 4.3327 and 5.8403 ms. These comparisons support the caution in the revised abstract.

Exact and numerical outputs are also distinguished adequately. The full computational section explicitly treats numerical feasibility as weaker than exact membership. Inspection of the frozen `network_simplex_compressed/certificate.py:71–131` confirms that a returned Farkas cut requires nonnegative rational multipliers, exact cancellation of the auxiliary columns, and strict rational violation; unsuccessful reconstruction returns an uncertified status. This supports the exposition about certificate semantics, but is not a complete verification of the model assembler or all recovery procedures. The introduction's general structural procedures should be read together with the implemented-scope table, which clearly labels the bounded-rank implementation as a verification prototype.

## Enumerated findings

1. **S1-R5-01 — Minor: restrict “all state products” in the completion summary to the locally observed labels.**

   **Primary locator:** `sections/00-introduction.tex:63–65`, specifically the claim that the summed residual ranks are the minimum number of additional individual products needed to recover “all state products” on the ambient circulation space. **Related locator:** `sections/09-conclusion.tex:4–9`, which refers to “each unobserved block–state subgraph” without repeating the locally observed-label restriction. The abstract has the correct restriction at `main.tex:49–51`.

   The actual proposition is explicitly for `B` and `j in J_B` (`sections/02-compression.tex:314–322`). States absent from a block are merged; their individual flows are not determined by the observations and balance equations. Their proportional refinement is a valid choice of completion, not unique recovery of every possible original state flow.

   For a concrete example, take two parallel arcs from a source to a sink, unit capacities, unit total flow, and two explicit labels with weights `y_1=y_2=1/3`. Set the aggregate flow to `(1/2,1/2)` and observe only the first arc in label 1, with product `1/6`. The only locally observed label has a forest complement, so the sum of residual ranks is zero. Nevertheless, the state flows

   - `f^1=(1/6,1/6)`,
   - `f^2=(t,1/3-t)`, and
   - `f^0=(1/3-t,t)`

   are feasible for every `0 <= t <= 1/3`, with identical original observations and aggregate flow. The label-2 product is therefore undetermined. Zero additional coordinates suffice to describe the sparse hull and to choose one valid global decomposition, but not to determine all original state products on the ambient space.

   **Requested repair:** say “all products for each locally observed block–label pair,” or equivalent wording, and repeat that restriction in the conclusion's cycle count. Keep the separate statement that merged states can be refined into a valid global decomposition.

   **Why minor:** the theorem, proof, and abstract already have the right domain, and the surrounding introductory definition of the summation points toward the intended meaning. This is a local overstatement in the summary, not a defect in the formulation or a new lower-bound objection. The executable rational example is retained in `stage1-review5-evidence/check.py` and its output.

## Primary-literature checks

- **Khademnia–Davarnia:** read the locally retained published text around Theorem 1, the tree/forest discussion, and Example 2. The complete hull claim and the multiplier-two precedent are present. The revision correctly distinguishes the general complete projection class from the more specific forest construction. In particular, Example 2 establishes a nonunit aggregation weight; it does not by itself establish the invariant product-coefficient obstruction claimed here. The primary published text is available through the [NSF-hosted article](https://par.nsf.gov/servlets/purl/10546393).
- **Davarnia–Richard–Tawarmalani and Davarnia's dissertation:** independently opened the [author-submitted Optimization Online record](https://optimization-online.org/2017/02/5864/), which supports the polytope-times-simplex simultaneous-convexification baseline. Read Proposition 2.6 in the retained dissertation text: its componentwise convexification identity supports the gluing attribution. The manuscript correctly assigns the detailed proposition locator to the dissertation rather than to the journal paper. I did not obtain the complete journal article during this review.
- **Liberti–Pantelides:** read the local primary text of Theorem 3.1 and the following discussion. It supports the rank-based elimination of common-factor products, including the explicit warning that the eliminated products' McCormick relaxations need not become redundant. The revised comparison preserves this essential distinction.
- **Kis–Horváth:** read the local primary text surrounding Proposition 22 and equations (30)–(31). The lower-bound shift, network feasibility characterization, and cut projection are present. The current manuscript treats these as established mechanisms specialized to state slices, which is fair.
- **De Loera–Onn:** checked the local primary text around Theorems 1.1 and 1.2 and the coordinate-erasing formulation. These support the universality baseline and bitransportation interpretation. This review does not independently certify the new transfer proof.
- **Almoghrabi–Skutella–Warode:** independently opened the [published full text](https://link.springer.com/article/10.1007/s10107-026-02392-8). Its Remark 1 explicitly distinguishes decomposition of aggregate arc flows from decomposition of the full commodity-flow vector, supporting the exact distinction made in the revised prior-work paragraph. The publication date and authors agree with the bibliography.
- **Davarnia–Rahimian:** independently opened the [versioned arXiv record](https://arxiv.org/abs/2510.15861v2) and read the retained primary text's introductory comparison. The title, authors, August 11, 2026 revision date, binary simplex variables, and projection into the x-variable space match the new entry and paragraph. The explicit preprint/version designation is appropriate.

These checks support the restricted novelty wording. They do not prove an exhaustive absence of predecessors. I found no concrete source that contradicts the listed specific developments.

## Checks performed and limitations

- Inspected the full assigned revised prose, bibliography, and relevant baseline comparison; retained the five-file unified diff in `stage1-review5-evidence/assigned-scope.diff`.
- Read the observation-sensitive formulation, minimum-completion proposition, forest corollary, their restrictions and recovery discussion, and the complete computational section to check consistency with the opening and conclusion.
- Independently recomputed raw five-run total-time medians for every method in all three optimization cases, checked agreement with stored summary statistics, checked stable variable counts across the runs, and checked successful numerical statuses. Results are in `stage1-review5-evidence/check-results.json`; the benchmark file hash is recorded there.
- Inspected the exact Farkas acceptance conditions and noncertifying statuses in the frozen implementation.
- Ran the rational completion-scope example above, checking every state balance, bound, aggregate equality, and retained observation exactly.
- Performed the primary-source inspections listed above. The author and literature reports guided discovery but did not substitute for the specific source checks.

I did not rerun the benchmark workload, certify its numerical optimization answers independently, audit every bibliography entry's metadata, rebuild the PDF, inspect all rendered pages, or redo the bounded-rank, fixed-label, Fibonacci, or universality proofs. The review therefore accepts neither general correctness from finite tests nor a universal runtime ordering from the retained measurements. Those are substantive limits of this Stage 1 review, not additional findings.

## Optional preferences

None requiring action. The existing scope and normalization qualifications should be preserved during any shortening of the opening or conclusion.
