# Stage 1 correction report

Correction agent: `stage1_fixer`, separate from the stage author and all fifteen reviewers. Scope: root's accepted actions A1–A9 in `reviews/stage1-round1/adjudication.md`. The reference baseline is the immutable `reviews/stage1-round1/source/` copy, whose hashes root checked against the round snapshot.

Edited manuscript files: `sections/01-foundations.tex`, `references.bib`, and `coverage.md`. This report is the only additional authored file. No original research, literature package, review report, snapshot, adjudication, main file, macro file, or later-stage section was edited. The existing stage labels and proofs are preserved; the new corollary adds `cor:c2-strong`. The stage gate remains for root to decide.

## Accepted actions and independent checks

| Action | Correction and location | Verification |
| --- | --- | --- |
| A1 | Replaced the three literal commas in the Taylor bounds by multiplication spacing in the proof of `thm:smooth-ranks`, retaining the factor two in the error budget. | The cell remainder is bounded by the sum of Hessian-entry bounds times coordinate displacement products. Each allowed product contributes at most a fixed constant times `2^(-T)`. The band radius and the Taylor error are each at most `epsilon/2`. |
| A2 | Split the rank/evaluation and positive-capacity citations around `eq:shrunk`, `eq:evaluation`, and `eq:capacity`; explicitly credited Gurvits and cited GGOW Section 1.5's concluding p.237 discussion and Section 2. | Read the published GGOW source in `build/source-cache/ggow2020.txt`, especially printed p.237, and checked that its capacity discussion distinguishes positivity from the quantitative input-height lower bound. Theorem 2.18 remains cited only for the deferred integral-data bit estimate. |
| A3 | Added classical embedding credit after `lem:disjunction` and the `vielma2018` bibliography entry with journal, volume, issue, pages, DOI, and arXiv link. | Read `literature/AGENTS.md`, the retrieved primary manuscript's Section 2/2.1 and Assumption 1, and Proposition 1/Corollary 1. Confirmed these statements directly from PDF pages 6–7 using `pdftotext`, because the cached Markdown omits some displayed formulas. The source imposes rationality, common recession cones, and extreme-point hypotheses. Our retained proof works with real rows and lineality: inactive homogenized variables lie in the common recession cone and can be absorbed into the unique active member. No ideality claim was added. |
| A4 | Qualified `eq:ncrank-finite` explicitly by `r>0`; dispatched the affine case at the start of the proof of `thm:ncrank`. | Noncommutative rank zero forces the pencil, hence every Hessian, to vanish. An affine graph over a box is a polyhedron. All divisions by `r` now occur in the positive-rank case. |
| A5 | Required `K=-K` in the error-body definition and made the corresponding coverage obligation explicitly origin-symmetric. | A convex full-dimensional symmetric body contains zero in its interior, so centered graph errors and exact graph containment use a consistent definition. Translation to an arbitrary symmetry center is no longer implicitly permitted. |
| A6 | Retained affine coordinate identities and original domain inequalities explicitly in the polynomial branch; enlarged the Taylor constant over the whole normalized enclosing box; supplied `T=max(0,ceil(log2(2 C_0/epsilon)))` with `C_0>=1`. | The enclosing-box extension is valid only because forbidden polynomial Hessian entries vanish identically. For the normalized box one can take `C_0 >= max(1,(1/2) max_j sum_(i,k) sup_box |partial_ik f_j|)`. Every nonzero entry has `alpha_i+alpha_k>=1`, so the prefix displacement products are at most `2^(-T)`. Both prefix and endpoint lie in the enclosing cube, so the entire Taylor segment stays there. Original domain rows prevent unintended input points. If `epsilon>=2 C_0`, depth zero suffices; otherwise rounding upward proves the displayed budget. Zero Hessians are covered by the affine case, and the positive enlarged constant avoids `log(0)`. |
| A7 | Added eleven named audits and ten further dependency paths to `coverage.md`, increasing its note index from 173 to 194. Canonical results remain 43; the substantive supporting-development table remains 32. | Read the omitted audit records for the claims and correction evidence they cover, followed direct Markdown links and explicit backticked `notes/` or `results/` paths recursively, and inspected the additional paths. The resulting closure has 237 distinct Markdown files: 43 canonical results and 194 notes. All coverage links resolve, and that dependency closure has no unindexed local Markdown paths. The exact additions and their stages are below. Their earlier verdicts are historical evidence, not a substitute for later-stage proof review. |
| A8 | Added `cor:c2-strong` and its complete Taylor-grid/disjunction proof after the strong-convexity lower bound; mapped it in the original square/product source row in `coverage.md`. | Compared the original result's Theorem A′ and matching-order remark. On a box in dimension `d>=1`, compactness and `C²` give a finite Hessian norm bound `M>0`. Cells of coordinate side at most `h=sqrt(epsilon/(Md))` have diameter at most `sqrt(d)h`, giving Taylor error at most `epsilon/2`. Their affine bands have width `epsilon`, contain every graph point, and admit at most `epsilon` vertical error. The number of cells is the product of coordinate subdivision counts, `O(h^(-d))`; taking its binary logarithm yields coefficient `d/2`. The existing strong lower estimate and `p_conv<=p_bin` give the same expansion for each minimum. No smooth oscillatory estimate, rational knot encoding, or compact formulation-size claim is required. |
| A9 | Replaced the implicit inertia depth with `A=sum c_j+sum d_j>0` and `L=max(0,ceil((1/2)log2(A/(4 epsilon))))`, followed by the exact leading count. Dispatched the affine case and restricted the nontrivial lower proof to `k_->0`, with `p>=0` for `k_-=0`. | If `A/(4 epsilon)<=1`, `L=0` gives `A/4<=epsilon`; otherwise `2^(-2L)<=4 epsilon/A`. At fixed data, the ceiling contributes less than one, so `k_- L=(k_-/2)log2(1/epsilon)+O(1)`. Positive squares require no binaries; negative squares use `L` each. Unbounded one-sided outputs and exact epigraph containment are preserved. No zero-dimensional strong-volume formula is used. |

## Primary-source details

Vielma: *Embedding Formulations and Complexity for Unions of Polyhedra*, Management Science 64(10):4721–4734 (2018), DOI `10.1287/mnsc.2017.2856`. The read source is the open arXiv manuscript in `literature/papers/vielma2018-embedding-formulations-and-complexity-for/original.pdf`, retrieved from `https://arxiv.org/pdf/1506.01417`. Its Assumption 1 is on PDF p.5, Proposition 1 on pp.6–7, and Corollary 1 on p.7. Its core encoding uses pairwise distinct binary vectors with dimension at least `ceil(log2 n)`. The manuscript bibliography records the journal publication and links the open version. No literature metadata or read-status field was changed.

GGOW: the published FoCM text has the required Gurvits attribution and positive-capacity implication on printed p.237, at the end of Section 1.5. Section 2 supplies the capacity framework. The already retained positive-capacity equivalence is distinct from the quantitative integral-data estimate used only in the rational preview. The separate Hall/permanent proof of the qualitative exponent remains intact.

## Audit and dependency additions

All entries below are under `notes/`. Stages 2–4 remain pending mathematical verification in this manuscript process.

| Stage | Added path | Evidence or relationship inspected |
| --- | --- | --- |
| 2 | `review-covariance-benchmark-dimension-gap.md` | Finite Frobenius benchmark gap and its distinction from algorithmic hardness. |
| 3 | `review-small-exponent-rational-formulation-barrier-second.md` | Strengthened rowwise determinant accounting and matching four-binary rational construction. |
| 3 | `review-positive-polynomial-allocation-degree-gap.md` | Allocation benchmark obstruction and real-coefficient upper scope. |
| 3 | `review-positive-polynomial-allocation-degree-gap-second.md` | Correction separating the two asymptotic minima rather than claiming exact equality. |
| 4 | `review-positive-polynomial-vector-refinement-obstruction.md` | Non-midpoint witnesses, scalarization comparison, and finite box/body corollaries. |
| 4 | `review-positive-polynomial-vector-refinement-second.md` | Independent reconstruction and addendum preserving the half-body error budget. |
| 4 | `review-positive-vector-capset-integer-lower-bound.md` | Imported finite-field bound and the specific contact application; no general binary/integer separation inferred. |
| 4 | `review-positive-vector-three-witness-integer-obstruction.md` | Exact three-component integer obstruction and its limited scope. |
| 4 | `review-convex-vector-tilted-error-integer-gap.md` | Convexification of the scalar construction and dependence on growing error-body conditioning. |
| 4 | `review-convex-vector-tilted-error-integer-gap-second.md` | Whole-projection inclusions, rational encoding, and conditioning calculation. |
| 3 | `review-pure-power-degree-independent-count-second.md` | Explicit cell-domain correction; finite real-coefficient count versus compact rational compiler. |
| 2 | `review-commuting-quadratic-covariance-reduction.md` | Additional direct audit dependency: sign-flip geometric-mean symmetrization and scalar allocation. |
| 4 | `review-componentwise-convex-fixed-condition-integer-gap-root.md` | Additional direct audit dependency: conditioned-body and simplex-band comparisons. |
| 3 | `review-pure-power-degree-independent-count.md` | Additional direct audit dependency: uniform chord bound, finite encoding, and row/nonzero distinction. |
| 3 | `review-small-exponent-rational-formulation-barrier.md` | Additional direct audit dependency: strengthening from the coarse denominator bound and matching encoding theorem. |
| 4 | `compiled-convex-vector-knot-overlay.md` | Promotion pointer to the already indexed canonical convex-vector compiler. |
| 4 | `compiled-polynomial-vector-overlay-precision.md` | Promotion pointer to the already indexed general polynomial-vector compiler. |
| 4 | `convex-vector-unconditional-log-product-precision.md` | Promotion pointer to the already indexed unconditional-body compiler. |
| 3 | `positive-polynomial-linear-dimension-shape-precision.md` | Promotion pointer to the already indexed separable convex-graph result. |
| 3 | `small-exponent-rational-formulation-barrier-novelty.md` | Bounded source assessment and explicit encoding-model distinctions. |
| 3 | `small-exponent-soc-formulation-separation.md` | Promotion pointer to the already indexed MILP/SOC encoding separation. |

The ten additional paths comprise four audit records, five promotion pointers, and one source assessment. These are inventory additions within A7; they do not add later-stage theorem claims to the manuscript. Root was notified of, and accepted, this inventory expansion.

## Executed checks and remaining gate

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` completed successfully from the paper directory and produced `build/main.pdf`, 19 pages. The final log contains no warnings, undefined references, or overfull/underfull boxes.
- `python paper-integer-dimension/verification/check_manuscript.py` passed: 57 labels, 12 bibliography entries, no duplicate labels/keys and no unresolved references/citations. The old snapshot was deliberately not supplied, because these authorized corrections change its inputs.
- Inspected the complete manuscript diff against the archived source. All original labels remain, the full existing proofs remain, and the only new theorem-like statement is the C² corollary.
- Checked every local coverage link and recursively followed the recorded local Markdown dependencies: 237 files, no missing inventory target in that closure. This checks explicit dependency links, not every implicit mathematical dependence or a new literature search.

No substantive new mathematical issue was uncovered during this correction pass. Later-stage proofs, the rational bit-complexity preview, and final whole-paper review remain outstanding as recorded in the process. This report does not mark the stage gate passed; root must inspect the corrected files and build.
