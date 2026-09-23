# Stage 1 independent review 1

Verdict: **No major issues found. One minor citation-locator correction is warranted.** The introduction gives a substantially clearer, appropriately qualified account of the contribution and its relationship to prior work. This verdict concerns the frozen Stage 1 introduction and bibliography; it is not a certification of every unchanged core proof.

I read the frozen introduction and bibliography in full, the author report and literature audit, and checked the introduction against the AC, structural, algebraic and numerical statements and arguments. I independently read the pertinent primary-source passages listed below. I did not read any other new reviewer report and did not edit the manuscript.

## Required minor correction

**R1.1 — The Jeeninga citation locator should include the convexity theorem.**

Locator: `stage1-snapshot/sections/00-introduction.tex:116–118`.

The sentence cites Theorem 3.22 for the combined assertion that the authors characterize feasibility/interior feasibility by matrix alternatives and establish convexity. The primary text's Theorem 3.22 is indeed the matrix-alternative result, but the explicit closedness/convexity theorem is Theorem 3.18. This does not invalidate the comparison, and it is not a mathematical or novelty error. It is a small precision issue in a passage whose purpose is careful source attribution.

Correction: use `\citet[Theorems 3.18 and 3.22]{JeeningaEtAl2023}`, or give the convexity and matrix claims separate locators. The current model distinction—independent operating voltage limits and source injection restrictions, rather than signed demands—is correct.

## Optional bibliographic improvement

`references.bib`, `OhmotoShiota2017`, currently gives the explicitly identified arXiv version. That is a legitimate source citation, not an error. For a submission bibliography, however, the published source is available: *Journal of Topology* 10(3), 765–775 (2017), DOI `10.1112/topo.12024`. The author's publication page and publisher agree. The article can be cited with an additional note retaining the inspected arXiv version. This is optional publication polish and does not warrant another major-review cycle.

Primary metadata: [publisher record](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/topo.12024); [Ohmoto's publication page](https://www.math.sci.hokudai.ac.jp/~ohmoto/activity.html).

## Substantive assessment

1. **Complexity and restrictions.** Introduction lines 14–38 and the comparison table track the restricted resistive theorem. The contribution is the solution-preserving electrical arithmetic realization and simultaneous graph/data restrictions. It explicitly avoids claiming a strict separation of NP and existential-real complexity. It also correctly refrains from claiming that its graphs are trees or that its AC result subsumes lossless fixed-magnitude hardness.

2. **Closest hardness predecessors.** I checked the primary local texts of Bienstock–Verma and Lehmann–Grastien–Van Hentenryck. The former uses the lossless sine-flow model with fixed magnitudes and unconstrained reactive quantities; the latter proves star/tree hardness with fixed unit magnitudes and active/reactive constraints. The new prose accurately distinguishes both. Bienstock–Verma's statement and publication metadata were additionally confirmed against the publisher and arXiv records. The references to their exact complexity results are not being used to infer unsupported rational-certificate conclusions.

3. **Resistive tractability precedents.** Gan–Low's sufficient relaxation-exactness conditions are not unconditional feasibility or exact Turing complexity results. The introduction describes them accordingly. Jeeninga et al.'s demand model has different operating constraints from the constructed instances. The manuscript makes the relevant difference explicit, including singleton voltage and injection intervals at the same bus.

4. **Angles and winding.** The added Farivar–Low, Delabays et al., and Jafarpour et al. lineage is important and apt. The prose distinguishes modulo-2π recovery from vanishing real cycle sums and credits established winding/uniqueness ideas. The claimed additional contribution is the explicit rational polynomial encoding and transfer, which matches the supplied crossing-count construction. The formulation includes rational negative cosine limits, unequal positive magnitudes, endpoint conventions, and a polynomial number of cycle predicates. The positive principal-window corollary's nonconstant cosine alphabet is disclosed. No broad novelty claim about winding or equal-angle equilibria remains.

5. **Universality and fields.** The introduction accurately states the distinction between compact basic closed rational universality and general compact semialgebraic topological universality. I checked the basic-closed invariant argument and the three-quadrant counterexample; they support the limitation stated. Dynamic Toolbox v1's Theorem 1 and Definition 4 do state the broader universality with rational coordinate maps, so this is a real scope issue rather than an invented distinction. The text appropriately relies on its own conjunction-only proof instead of claiming to import Boolean preprocessing. The original contribution is identified as the restricted electrical realization, with bounded arithmetic and triangulation credited.

6. **Algebraic predecessors.** Mareček–McCoy–Mevissen's generic complex solution-count analysis is a relevant comparison. Realizing prescribed compact feasible sets with inequalities is different from generic root counting. The introduction does not claim to originate polynomial power-flow formulations or all algebraic analysis of power flow.

7. **Numerical claims.** The introduction tracks the actual ordinary-construction residual transfer, tiny-residual family, and polynomial-minimum bound. It does not silently transfer the quantitative example through planarization. The distinction between an exponential precision requirement for residual-threshold certification and a lower bound on all exact algorithms is explicit and necessary. The gap-promise certificate is correctly described as a supporting rounding argument, not a new general approximation principle. The Bienstock–Muñoz preprint's Theorem 7 and Corollary 8 do give the cited network/AC approximation results with scaled tolerances; the introduction does not conflate them with exact decision.

8. **Readability and significance.** The result map ties the consequences to one construction and explains why sparsity, finite data, topology, and numerical separation matter. The table helps distinguish incomparable physical subclasses. The limitations are mostly adjacent to the claims they qualify. No additional introductory subsection or broader list of remote predecessors is needed.

## Independent evidence and limits

Primary local material inspected included `literature/papers/bienstock2019-strong-np-hardness-of-ac/fulltext.md` (model and main construction), `lehmann2016-ac-feasibility-on-tree-networks/fulltext.md` (model and star theorem), `jeeninga2023-dc-power-grids-with-constant/fulltext.md` (Theorems 3.18 and 3.22), `abrahamsen2019-dynamic-toolbox-for-etrinv/fulltext.md` (Theorem 1, Definition 4, and algebraic corollary), and the Bienstock–Muñoz primary extraction (Theorem 7 and Corollary 8). I also inspected the cached primary Gan–Low, Farivar–Low and Jafarpour texts and the JPT theorem/example locators.

Fresh web queries included exact combinations of power flow with existential theory, existential-real complexity, and universality, plus targeted searches for the closest hardness predecessors and bibliographic records. Broad exact-complexity searches were noisy and did not reveal a closer matching restricted resistive completeness or prescribed-set realization theorem. This is not proof that no such paper exists. The manuscript's model-specific, qualified novelty language is commensurate with this evidence.

I did not rebuild because this review required no edits and Stage 1's build/visual table check is recorded; mathematical and attribution checks were the independent focus. The already noted numerical-section JPT theorem-number verification belongs to the subsequent numerical stage, rather than a new Stage 1 objection.
