# Stage 1, round 1 — reviewer 13

Primary lens: repository coverage, dependency completeness, and reconciliation of original corrections and audits.

Major findings: 0

Minor findings: 4

## Reviewed snapshot and verification limits

I read `PROCESS.md`, `reviews/PROTOCOL.md`, `reviews/STAGE1-TASK.md`, `reviews/STAGE1-LENSES.md`, and the round snapshot. I read all 1,206 lines of `sections/01-foundations.tex`, the bibliography, macros, main file, and coverage inventory. Independently computed SHA-256 values agree with all five snapshot entries:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I reconstructed the mathematical argument across the whole stage: parity and closure, finite disjunction, square and product bounds, graph allocation, scalar determinant bounds, one-sided inertia, principal compression and real shrinking, covariance and capacity/permanent estimates, smooth oscillatory volume, polynomial prefixes, constant-rank tubes, and perspectives. I compared corresponding proof passages and scope statements in the nine stage-1 canonical result files, with particular depth on the quadratic-system, smooth-map, constant-rank, and original square/product developments. I read the original square/product correction report and extension note, the nonquadratic investigation, relevant audit passages, and selected omitted audit records.

Executed checks: all five hashes match; every local link in `coverage.md` resolves; all manuscript citation keys and local cross-reference labels resolve; content searches across `results/` and `notes/` found the omitted audit records below. These are structural checks, not mathematical proofs. I did not compile or visually inspect the PDF, run numerical formulation solvers, or review every later-stage proof. I checked primary-source text in the supplied GGOW, Wolff, and Nicola cache for the relevant imported statements; I did not independently verify every bibliographic item or the full rational bit-complexity theorem. That theorem is explicitly deferred to stage 2, and I have not counted its absent proof as a stage-1 defect. No literature knowledge-base files were used.

## Overall assessment

The stage presents a coherent standalone argument for its principal precision laws. I found no major mathematical defect in the argument checked. The earlier square/product corrections have largely survived the rewrite, and the stage carefully distinguishes real-coefficient existence, linear size, rational encoding, and construction time. The remaining findings concern coverage fidelity, an incorrect citation locator, and notation. Absence of major findings is a bounded review conclusion, not a guarantee of correctness or novelty.

## Findings

1. **MINOR — the dependency and audit inventory omits relevant review records.** Location: `coverage.md:100–102`, “Dependency and audit index,” and its following table. The inventory includes the substantive source notes but omits eleven directly relevant audit files:

   - `notes/review-covariance-benchmark-dimension-gap.md`
   - `notes/review-small-exponent-rational-formulation-barrier-second.md`
   - `notes/review-positive-polynomial-allocation-degree-gap.md`
   - `notes/review-positive-polynomial-allocation-degree-gap-second.md`
   - `notes/review-positive-polynomial-vector-refinement-obstruction.md`
   - `notes/review-positive-polynomial-vector-refinement-second.md`
   - `notes/review-positive-vector-capset-integer-lower-bound.md`
   - `notes/review-positive-vector-three-witness-integer-obstruction.md`
   - `notes/review-convex-vector-tilted-error-integer-gap.md`
   - `notes/review-convex-vector-tilted-error-integer-gap-second.md`
   - `notes/review-pure-power-degree-independent-count-second.md`

   This is an inventory completeness issue, not evidence that a stage-1 theorem is false. It matters for the later promised correction reconciliation: for example, the second allocation-gap audit records a requested and applied correction to chained asymptotic notation, and the small-exponent second audit checks the strengthened rowwise determinant argument and matching four-binary construction. Suggested repair: add these records with stages 2, 3, or 4 as appropriate, update the count, and trace audit links recursively from the substantive supporting notes as well as the canonical results. Do not treat their PASS labels as replacement proofs.

2. **MINOR — the original matching rate under only `C^2` regularity is not explicitly preserved.** Location: `sections/01-foundations.tex:122–137` and `938–951`; source: `results/mip-relaxation-binary-lower-bounds.md`, Theorem A′ and its “order is right in every dimension” remark. The original result gives the matching upper rate for a `C^2` strongly convex or strongly concave function on a neighborhood of a full-dimensional box. The manuscript preserves its lower bound, but the general smooth upper theorem assumes `C^\infty`, so it does not formally recover the original hypothesis scope. This is a small coverage omission, not a false theorem or a failure of the stronger analytic result. Suggested repair: after the strong-convexity lower bound, add the elementary `C^2` upper argument. A regular grid of side scale `h` has `O(h^{-d})` cells; bounded Hessian norm gives an affine Taylor band on each cell with error `O(h^2)`; finite disjunction then gives `p_bin <= (d/2) log_2(1/eps)+O(1)`. Combined with the displayed lower bound, this preserves the original `C^2` precision law without invoking the oscillatory lemma.

3. **MINOR — three Taylor estimates contain a literal comma where multiplication is intended.** Location: `sections/01-foundations.tex:974`, `977`, and `992`, in the proof of `thm:smooth-ranks`. The expressions are `C_0,2^{-T}` and `2C_0,2^{-T}`. In math mode these print punctuation rather than the intended product, leaving the error-budget inequality malformed. The source proof correctly has `C_0 2^{-T}`. Suggested repair: remove the commas or replace them with `\,`. The surrounding derivation establishes the intended estimate; no substantive new proof is needed.

4. **MINOR — the cited theorem numbers do not include the capacity equivalence.** Location: `sections/01-foundations.tex:529–541`. The paragraph introduces three imported characterizations with the joint locator “GGOW, Theorems 1.4 and 1.17.” In the supplied primary published text, Theorem 1.4 provides singularity, matrix-evaluation, shrunk-subspace, and rank-decreasing equivalences, while Theorem 1.17 gives general rank/inner-rank/decomposability. Neither displayed theorem states capacity positivity. GGOW discusses the positive-capacity implication and credits Gurvits at the end of Section 1.5; Section 2 develops capacity. The original repository result cited “Theorems 1.4 and 1.17 and Section 2” and explicitly attributed the capacity equivalence to Gurvits. Suggested repair: give the capacity statement its own accurate locator and restore that attribution. This is a source-location weakness, not an unsupported mathematical claim after consulting the actual source; the manuscript also supplies the independent permanent route for its qualitative exponent.

## Reconciliation of earlier corrections

The following original corrections and limitations are retained correctly in the present stage:

- The product ceiling uses the exact `log_2(16 ln 2)` constant, avoiding the earlier rounded-constant error.
- The parity cover takes closures of graph contact inputs; it does not require measurable original parity supports, closed projected sections, or bounded integer witnesses.
- General smooth upper constructions use actual bounded polyhedral Taylor bands. They do not assume that convex hulls of smooth graph pieces are polyhedral.
- One-sided square constructions explicitly remove lower output restrictions; the manuscript does not make the former false inference that a two-sided graph relaxation already contains the whole hypograph.
- The logarithmic epigraph LP row lower bound is proved by active intervals and exposed-face counting, rather than left open.
- The four-point obstruction to width constant four, the distinction between width and area, and the absence of a sharp product-graph constant are retained.
- The Hall/permanent alternative, complex-to-real shrinking argument, principal compression, and full-box scope of the quadratic-system lower bound are present.
- The smooth proof retains the anisotropic-contact warning and uses the oscillatory argument to avoid that obstacle. The constant-rank proof bounds error on whole affine tubes, including points outside the parameter cube used to select a tube.
- The exact one-sided convex product constant remains separate from possible finite-LP attainment at the threshold. Positive perspectives encode only binary products and do not claim an unrestricted-integer upper transfer.

No manuscript, bibliography, original research, or other review report was edited.
