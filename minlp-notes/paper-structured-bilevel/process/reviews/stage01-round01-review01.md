# Stage 1, round 1: independent review 01

Reviewed snapshot: `process/snapshots/stage01-round01`. Its `SHA256.json` digest is `2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`. All five listed file hashes match. Locations below refer to that frozen snapshot, not subsequent working-source edits.

Recommendation: accept stage 1 after two minor wording corrections. I found no major defect in this stage's model, algebraic tools, substitution proof, or inventory. This is not approval of the later proofs or experiments. The abstract and main results are expressly assigned to later stages and are not missing stage 1 deliverables.

## Findings

### R01-1 — Minor: restrict the universal algorithm-output promise

Location: `sections/01-foundations.tex:187–191`, especially “All algorithms report infeasibility separately, and state whether the finite optimum value is attained.”

As a statement about the paper's exact optimization algorithms, this is appropriate. As written, it also covers the response-constrained approximation algorithms that the same foundation and coverage map promise. Those algorithms do not always decide original feasibility or exact attainment. In `results/bilevel-response-constraint-accuracy-bit-algorithm.md`, Section 4, the outer algorithm can return an approximately feasible point without certifying original feasibility. The inner algorithm can report an empty surrogate without certifying original infeasibility. Their guarantees should not inherit a stronger general output contract from the foundations.

Proposed correction: explicitly restrict this sentence to the exact optimization algorithms. State that the approximation algorithms specify their own feasible-output, violation, and empty-surrogate guarantees. This is a local scope correction; the inventory already assigns the correct distinctions to stage 4.

### R01-2 — Minor: retain numerical degree in the algebraic-output bound

Location: `sections/01-foundations.tex:211–213`, “They are bounded polynomially in the input size in the stated fixed dimensions.”

Lines 195–205 explicitly allow sparse binary exponents while promising polynomial time in `(L, delta)`, with polynomial time in `L` alone conditional on degree control. The output sentence drops that condition. Fixed dimensions by themselves cannot bound output degree polynomially in binary input length. For example, let the compact leader domain be `{x in [1,2]: x^(2^t)=2}`, add a trivial fixed scalar quadratic follower on `[0,1]`, and use a constant upper objective. The unique leader has degree `2^t` by Eisenstein's criterion applied to `T^(2^t)-2`, while the sparse input has length `O(t)`. Any common field containing that leader has degree at least `2^t`, so permitting a nonminimal defining polynomial does not remove the obstruction.

Proposed correction: replace the quoted bound by “polynomially in `(L, delta)` for the stated fixed dimensions, and polynomially in `L` under the degree-encoding condition above.” This makes the output paragraph agree with the already correct running-time paragraph and the planned sparse-degree boundary.

## Mathematical assessment

- The primary model matches the actual fixed-normal block theorem: local dimension is fixed, local row counts can grow, shared row counts are separate, and positive definiteness belongs to local blocks. Continuous polynomial coordinate bounds over compact `C` give uniform follower boundedness, including when some fibers are empty. A nonconvex aggregate can produce multiple global followers without contradicting local strict convexity.
- The optimistic, pessimistic, and cost-near-optimal definitions consistently exclude empty followers and do not use upper constraints to filter follower choices. Fixed-leader compactness supports the stated maxima. The warning about leader nonattainment agrees with the explicit quartic example in the canonical response-semantics result. The robust measurement restriction is correctly distinguished from unrestricted polynomial upper criteria for exact global responses.
- The substitution lemma is sound. Clearing an explicitly listed monomial uses `D^(delta-|gamma|)`, with a nonnegative exponent. Its total degree is at most `delta(1+T)`. In fixed dimension the number of expanded monomials is polynomial; the number of factors and coefficient-bit growth are also polynomial in the stated numerical degrees and input lengths. Positivity of `D` handles inequalities and equalities without a parity exception.
- The real-algebraic discussion correctly fixes the total free and bound dimension, rather than only the leader dimension. The actual source formula in `results/bilevel-compressed-response-infimum-semantics.md`, Section 2, keeps a constant number of quantified response copies and puts growing regime/row lists inside quantifier-free predicates. The inventory expressly preserves this obligation. Common-field recovery is consistent with fixed-dimensional simultaneous sampling and rational reconstruction; independently requested robust witnesses are correctly qualified.
- The Hoffman statement correctly uses matrices fixed with respect to the leader and is uniform in the right-hand sides. Its existence-only and quantitative uses are separated. It does not silently extend the fixed-normal attainment argument to moving normals.

## Coverage assessment

I checked the inventory against the repository result files and supporting notes, not their historical PASS labels. All 14 canonical `results/bilevel-*.md` files are named. All 72 explicitly named source paths checked exist. This mechanical check was supplemented by reading the exact scalar/block and response-semantics results, relevant robust/approximation statements, the fixed-rank and moving-normal notes, scope/complexity maps and closeouts, and the section structure of the substantial inverse, path, and executable-algorithm dependencies.

The map preserves the material distinctions: the two dense SPD hardness constructions; near-identity exact hardness versus inverse-error approximation; the leader-interaction path versus the follower-constraint path; square-root-sum arithmetic versus hardness; one-resource identities versus multi-resource residual certificates; positive versus signed inverse estimates; separate robust witnesses; and true nonconvex response contact versus convexified false choices. It includes the fixed-core support-function dependency, the note-only Klee–Minty reduction, and the narrow affine-strip feasibility result with its limitations. The retained unfavorable screening experiment and unequal-task fixed-price benchmark limitation are explicit. I found no substantive bilevel result missing from this stage's map. The binary path-cut/clamp notes concern the separate pooling-capacity development and are not a missing dependency of the mapped bilevel results.

The inventory is a sound assignment of future work. Section-heading and scope inspection is not a new complete proof audit of every later result; those audits remain necessary at their assigned stages.

## Verification and source access

Verification artifacts are isolated under `verification/reviewer01/stage01-round01/`. No frozen source or manuscript source was changed.

- Verified the manifest and each file hash; retained `hash-check.json`.
- Copied the five source files into the isolated directory and ran the README's `latexmk` command. It exited successfully and produced a six-page PDF. The final TeX log has no undefined citations/references, multiply defined labels, overfull/underfull boxes, or warnings. Retained the build log and `inventory-build-check.json`.
- Read `literature/AGENTS.md` before accessing literature. Inspected Basu–Pollack–Roy's local primary full text for Theorem 1.3.1, the bit-size qualification, and Section 3.1.3 sampling; visually checked the original PDF at PDF pages 4 and 28. The cited theorem/section locators are real and support the fixed-dimensional use. Rendered page images are retained. The first rendering attempt lacked PyMuPDF; `pdftoppm` succeeded.
- Checked the exact arXiv version metadata and stated comparison against the primary pages for [Ketkov–Prokopyev v2](https://arxiv.org/abs/2511.15592v2) and [Sugishita–Carvalho v2](https://arxiv.org/abs/2510.21126v2), and opened [Megiddo–Tamir's author manuscript](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf). The cited 2026 version dates and scalar-leader comparison agree. I did not independently retrieve every historical original or re-prove the cited external algorithms; no exhaustive literature-priority conclusion is claimed.

I did not read another current reviewer report, coordinate findings with another reviewer, author manuscript material, or delegate this review.
