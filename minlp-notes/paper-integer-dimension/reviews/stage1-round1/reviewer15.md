# Reviewer 15 — independent synthesis audit

Reviewed round: `stage1-round1`. Primary lens: reconstruct the full proof chain, consistency, and hidden assumptions.

Major findings: 0

Minor findings: 3

## Snapshot and coverage

The following SHA-256 hashes were computed with `sha256sum` and match every corresponding entry in `reviews/stage1-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |

I read all 1,206 lines of the stage, the process and review protocol, bibliography, macros, main document, and coverage inventory. I reconstructed every stage-1 proof rather than limiting inspection to the central quadratic theorem. I compared the principal arguments with the original results for noncommutative rank, constant scalar Hessian rank, bilinear graphs, scalar rank, covariance certificates, one-sided inertia, smooth maps, perspectives, and square/product lower bounds. Supporting comparisons included `notes/mip-binary-lower-bound-extensions.md`, `notes/nonquadratic-integer-precision-investigation.md`, and the earlier constant-rank and noncommutative-rank audits; their favorable verdicts were not used as proof.

Primary-source inspection used the cached GGOW text (Theorems 1.4, 1.17 and 2.18, capacity discussion), Wolff's Theorem A and its proof on printed pages 50–51, and Nicola's Definition 1.1 and following paragraph on printed page 3. I did not independently verify every bibliography entry or the IQS algorithm's detailed bit bounds. Those bounds are expressly deferred to stage 2. I did not audit every later-stage source in the inventory, compile the manuscript, or claim to establish publication priority.

## Overall assessment

The main mathematical chain is coherent. I did not identify a false main theorem or a material unproved step in the completed stage. In particular:

- Parity closures correctly remove measurability and lift-closedness assumptions without treating a parity class as a convex section.
- The quadratic lower proof uses an original-coordinate principal compression of the Hermitian free-field pencil, then a positive covariance determinant bound and a compact parity cover. Both the capacity route and the independent Hall/permanent route supply the required exponent.
- The upper proof establishes real descent before using symmetry to obtain the zero blocks. The exponents on those blocks sum to half the noncommutative rank, and the shared-prefix residual products achieve the stated tolerance without new integer coordinates or loss of graph containment.
- Scalar rank, interaction graphs, and the cross-product gap agree with the general system law. Their different finite constants do not create a contradiction.
- The smooth lower proof uses matrix evaluation and an oscillatory estimate to control arbitrarily shaped contacts; it does not rely on an invalid perturbation argument for thin sets. The polynomial upper proof explains why zero Hessian blocks persist outside the transformed original domain.
- The constant-rank scalar construction produces actual polyhedral tubes in the original coordinates. Its compactness argument covers boundary points and does not assert a free nonlinear change of variables in a convex lift.
- The one-sided and perspective results retain their stated domain and formulation distinctions. The exact product one-sided constant is restricted to convex lifts; the finite linear threshold is explicitly left unasserted.

## Concrete findings

1. **MINOR — definition precision: the error body's center is unspecified.** Location: `sections/01-foundations.tex`, lines 14–17, before Definition `def:dimension`. A “centrally symmetric” convex body can have a nonzero center; the definition does not expressly require `K=-K`. For instance, `[1,3]` satisfies the literal geometric conditions but excludes zero, so graph containment and the stated error condition cannot both hold on a nonempty domain. All actual stage-1 tolerances are centered boxes, so this does not invalidate the stage's theorems. Repair: say “centrally symmetric about the origin,” or explicitly impose `K=-K`.

2. **MINOR — malformed multiplication in the smooth Taylor estimates.** Location: proof of Theorem `thm:smooth-ranks`, lines 974, 977 and 992. The source has `C_0,2^{-T}` and `2C_0,2^{-T}`. These are printed commas, not multiplication or spacing commands. The intended bounds are unambiguous from the remainder proof, but the displayed error budget should read `C_0\,2^{-T}` and `2C_0\,2^{-T}`. This is a typesetting defect, not a failure of the Taylor estimate.

3. **MINOR — source pinpoint does not cover the stated capacity characterization.** Location: lines 529–541, particularly the citation “[Theorems 1.4 and 1.17]” preceding equations `eq:shrunk`, `eq:evaluation` and `eq:capacity`. I checked the cached primary GGOW paper. Theorem 1.4 states singularity/matrix-evaluation/shrunk-space/rank-decreasing/null-cone equivalences; Theorem 1.17 states the general rank/decomposability equivalences. Neither theorem, as printed, states positive capacity. GGOW does state the relevant positivity fact in its capacity discussion, including the paragraph on printed page 237 crediting Gurvits, and defines capacity in Definition 2.6. Repair: give the capacity equation its own accurate source pointer, such as GGOW Section 1.5's concluding discussion and Section 2, or cite the underlying Gurvits result directly. The mathematical fact is supported by the primary paper; this is a citation-location defect rather than an unsupported main claim.

## Executed checks and limits

A direct SymPy check passed for all six pairwise identities in the four-point width obstruction, the displayed Hessian and rank of the four-variable smooth example, the cross-product identity `sum_j H_j^2=2I_6`, and the centered fourth-moment covariance identity on an exact rational finite distribution. These checks supplement the algebraic reasoning and do not verify the analytic or free-field theorems by computation. No manuscript or original research files were edited.

No major finding was identified within this review's stated coverage; this is not a claim of formal verification or certainty.
