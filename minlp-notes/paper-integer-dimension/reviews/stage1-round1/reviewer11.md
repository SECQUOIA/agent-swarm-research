# Reviewer 11 — stage1-round1

Primary lens: quantifiers, degeneracies, domains, constants, and boundary counterexamples.

Major findings: 0

Minor findings: 3

The stage's main proof chain withstands my checks. I found no false precision law or material missing hypothesis in the substantive positive-rank arguments. In particular, the closure of parity contacts, unrestricted integer ranges, endpoint coverage of prefixes, rank-deficient slices, and positive perspective scaling are handled correctly. The findings below concern an undefined rank-zero specialization and two local presentation issues. This assessment is limited to the reviewed stage and is not a guarantee of correctness or priority.

## Snapshot and coverage

I read `PROCESS.md`, `reviews/PROTOCOL.md`, `reviews/STAGE1-TASK.md`, the lens list, the complete `sections/01-foundations.tex`, `coverage.md`, `references.bib`, `macros.tex`, and `main.tex`. SHA-256 checks against `reviews/stage1-round1/snapshot.json` all matched:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I compared relevant proof passages in the original bilinear-graph, scalar-quadratic-rank, quadratic-system-covariance, noncommutative-rank, one-sided-inertia, smooth-map, constant-Hessian-rank, and perspective results. I also read the lower-bound extension note and the existing constant-rank and perspective audits, checking their reasoning against the manuscript rather than treating their verdicts as proof. I examined the cached primary-source passages in GGOW (Theorems 1.4, 1.17, and 2.18), Nicola (Definition 1.1 and the following paragraph), and Wolff (Theorem A and its proof). I did not audit every bibliographic entry, external novelty, all 173 supporting notes, or the complete deferred rational bit-complexity proof. The rational construction is explicitly a later-stage preview, which is permissible under this review task. I did not compile or visually inspect the PDF.

## Findings

1. **MINOR — Missing local scope qualification for a finite bound, not a false positive-rank result.** Location: `thm:ncrank`, lines 708–715. After explicitly treating `r=0`, the theorem continues unconditionally with a principal compression of order `r` and the displayed finite bound containing `1/r`, `2/r`, and `omega_r^(2/r)`. For an affine system, the empty principal compression exists by `lem:principal`, but the finite formula is undefined. The proof and surrounding discussion make the intended positive-rank scope clear. Repair: start the finite-bound sentence with “When `r>0`, for a principal compression …”, and explicitly dispatch `r=0` before the positive-rank proof if desired.

2. **MINOR — Malformed multiplication in the Taylor error bounds.** Location: proof of `thm:smooth-ranks`, lines 974, 977, and 992. The source has `C_0,2^{-T}` and `2C_0,2^{-T}` with literal commas. These display as comma-separated expressions rather than the products needed for the error budget. The intended estimates follow from the adjacent argument and agree with the original smooth-map result. Repair: use `C_0\,2^{-T}` and `2C_0\,2^{-T}`. When the polynomial proof enlarges the domain to the enclosing box, say that `C_0` may be enlarged to bound derivatives there; this does not change the rate or count.

3. **MINOR — Specify the symmetry center of an error body.** Location: representation model, lines 13–17. “Centrally symmetric” can mean symmetric about an unspecified center. Under that reading, the scalar interval `[1,2]` satisfies the listed geometric conditions, but no graph-containing relaxation can satisfy the definition for any nonempty domain, because its exact graph points have error zero outside that interval. The subsequent examples clearly intend symmetry about the origin. Repair: explicitly require `K=-K` (or say “centrally symmetric about the origin”). With the other stated conditions this also guarantees that zero is in the interior. This is a definition clarification; it does not invalidate the componentwise-tolerance theorems proved in this stage.

## Verification and boundary checks

I independently checked the following portions of the argument:

- A parity class need not be convex or measurable; closing its exact graph contact set preserves the continuous midpoint condition. No compactness of integer witnesses or of the full lift is used.
- The exact square formula handles `p=0`, `epsilon=1/4`, and all larger errors. The all-one prefix with full residual retains the input endpoint one, including an empty prefix at depth zero.
- The product area constant, the graph demands at tolerances at least `1/4`, isolated vertices and an empty edge set, and the shift from `L_20` to `L_4` are consistent. The finite product interval bounds imply a gap at most two.
- The indefinite-volume constant rearranges to the stated `48 sqrt(r)` denominator. The capacity-volume bound rearranges to equation `eq:ncrank-finite`; the sum-of-squares certificate gives the displayed cross-product constant.
- Principal compression over the involutive division ring, descent of a maximal deficiency space to the reals, and the orthogonal `Z,W,Q` construction have the claimed dimensions and zero blocks. The rank-zero construction itself is affine and valid; only the finite formula's wording needs qualification.
- Epigraph formulations keep the unbounded vertical direction and allocate integer depth only to negative curvature. The product's convex-lift threshold and the separate nonattainment caveat for a finite LP are consistent.
- The oscillatory proof controls arbitrary compact contacts through indicator functions in `L^2`; the evaluation dimension cancels after taking the appropriate root. The local box lies within the original domain. In the smooth upper bound the Taylor segment remains in the convex cell intersected with the transformed domain.
- The constant-rank tube argument remains valid at the original box boundary because the smoothness and constant-rank hypotheses hold on a neighborhood. It also handles full rank, where the fiber coordinates have dimension zero. The tubes themselves, after intersection with the box, are polyhedra in the original coordinates.
- Perspective homogenization is exact with unbounded continuous auxiliaries; only the binary products need bounds. The case `ell=u>0` remains valid. An ordinary positive-scale box has a full-dimensional ratio slice for the lower bound, even though that slice need not equal the enclosing ratio box used for the upper bound.

Executed checks: Python SHA-256 verification of all five snapshot files; exact SymPy verification of all six four-point difference products, the displayed rank-three polynomial Hessian, and the Hessian formula for `x^2/t`; and 198 independent SciPy linear-program solves for the relaxed folding construction (depths 1–6 at 33 inputs each), compared with its exact folding sequence. All passed; the maximum LP objective discrepancy was zero. These checks support the direct proofs and do not substitute for them. No manuscript or original-source files were edited.
