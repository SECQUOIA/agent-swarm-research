# Development provenance and disposition of companion notes

The manuscript is self-contained with respect to these unpublished repository notes. They are development provenance, not bibliography entries or proof dependencies. Five rank-one results have been incorporated with complete proofs; eight tangential model comparisons were removed. The source files remain in the repository but are not frozen: some were revised after the author pass, for example `results/common-factor-reciprocal-anchor-hulls.md` and `results/common-factor-reciprocal-anchor-full-hull.md`, most recently in commit `367fcbc8` (2026-09-20). No public availability or authorship is inferred.

The paths below are relative to the repository root. SHA256 hashes identify the exact source bytes inspected in the September 9, 2026 author pass; they match the versions in commit `876ca480` (2026-09-09). A current file whose hash differs is a later revision, not the inspected source. Section labels are stable across later theorem renumbering.

## s6:margin-note: Linear optimization over rank-one matrices with row and column sum bounds is strongly NP-hard.

Source: [results/rank-one-row-column-hardness.md](../../results/rank-one-row-column-hardness.md).
SHA256: `4f8bfe1c346b1b9c73751d8db6d3367e45f8ade3718e6833b7955623c61b3e97`.

Appendix B: the results with labels `app:margin-hardness`, `app:margin-certificates`, `app:margin-fpt`. The main hardness, rational certificate, quadratic-field optimum and dimension-parameter algorithm are now proved in the manuscript.

## s6:zero-lower-note: Strong hardness with only unit upper bounds on rank-one flows.

Source: [results/rank-one-zero-lower-hardness.md](../../results/rank-one-zero-lower-hardness.md).
SHA256: `26431afa15e32381c4aa342a0e8765ffaa5bb6cab1cb39ccbe6a2e013f7d70d0`.

Appendix B: Lemma `app:unit-repair` and Corollary `app:unit-hardness`. Both the repair and the exact penalty are proved in full.

## s6:face-note: A correlation-polytope face in the unit-capacity rank-one hull.

Source: [results/rank-one-correlation-face-conic-lower-bounds.md](../../results/rank-one-correlation-face-conic-lower-bounds.md).
SHA256: `bf941c7812b665debcabf929403d2f2986928841069b70a7c6616f9d597ad606`.

Appendix C: Theorem `app:correlation-face`, Corollary `app:exact-conic`, and the exposure inequality in Lemma `app:face-rounding`. The affine inverse, face argument, cone transfer and nonpolyhedrality proof are included.

## s6:stability-note: Quantitative stability of the correlation face and approximate LP lower bounds.

Source: [results/rank-one-correlation-face-stability.md](../../results/rank-one-correlation-face-stability.md).
SHA256: `ca5bac0b73439c524b0e4bbe05380839308d4585ea7c2bf90a22863113a25a02`.

Appendix C: Lemma `app:face-rounding`, Theorem `app:outer-transfer`, and Corollary `app:approx-lp`. The stronger direct slice-distance estimate supplies the same stated accuracy constant. The unused general-objective penalty corollary is not claimed.

## s6:approx-sdp-note: Fine SDP approximations of the unit-capacity rank-one hull require superpolynomial size.

Source: [results/rank-one-approximate-sdp-lower-bound.md](../../results/rank-one-approximate-sdp-lower-bound.md).
SHA256: `cc1d1f75703775f563256830d0f771f5e3fb700f516eb34cf1c3933b548ca602`.

Appendix C: Lemmas `app:slack-factor`, `app:sign-correlation`, and Theorem `app:approx-sdp`. Published pseudo-density inputs are stated with exact locators; the shifted-slack and signed-correlation transfer proofs are complete.

## s6:common-factor-note: Common-factor optimization with a fixed number of linking constraints.

Source: [results/common-factor-fixed-linking-optimization.md](../../results/common-factor-fixed-linking-optimization.md).
SHA256: `9606a446bb8a08d4aa3f010df1b5f9da0f2528a0a7ee09c76902c7587de34f4f`.

Removed the common-factor fixed-linking optimization assertion. Its scalar-dependent leaf model is separate from the physical pooling classifications; no retained theorem uses it.

## s6:anchor-faces-note: Reciprocal-anchor hulls and a joint separating inequality.

Source: [results/common-factor-reciprocal-anchor-hulls.md](../../results/common-factor-reciprocal-anchor-hulls.md).
SHA256: `c9bf1e1fd0ea8810a62b6499dcfc776d8f6a70e3d528fb0cf97726153eff1291`.

Removed reciprocal-anchor one-leaf hull and compatibility assertions. These concern an anchored moment model, not the matrix margin set or the physical algorithms.

## s6:anchor-full-note: Exact reciprocal-anchor hull with arbitrarily many box-bounded leaves.

Source: [results/common-factor-reciprocal-anchor-full-hull.md](../../results/common-factor-reciprocal-anchor-full-hull.md).
SHA256: `6aa7e8e799905725815015c8ec294ee77e7fd81ce3d0f5466df0ddfe2ea45ae7`.

Removed the full reciprocal-anchor rational-separation assertion. No common reciprocal-distribution model is used by the pooling manuscript.

## s6:integer-anchor-note: Exact anchored common-factor hull for an integer scalar.

Source: [results/common-factor-integer-anchor-hull.md](../../results/common-factor-integer-anchor-hull.md).
SHA256: `b835906ba293517824e2458b8c1f4edd3226a2d4448713b794cc7ca41314c346`.

Removed the integer-scalar rounding and separation assertion. The paper studies continuous physical pooling and does not use this model.

## s6:network-universality-note: Sparse network–simplex hulls: universality at simplex dimension two.

Source: [results/network-simplex-universality.md](../../results/network-simplex-universality.md).
SHA256: `911656f39575d8f5bbd6c3a093fde8850bec0a54e4fbcbf630bf266f4a0cf960`.

Removed the sparse network–simplex universality assertion. Its coordinate sections do not preserve physical mixing; no pooling hardness theorem depends on it.

## s6:network-cycle-note: Exact sparse network–simplex hulls for cycle and theta blocks.

Source: [results/network-simplex-cycle-theta-hull.md](../../results/network-simplex-cycle-theta-hull.md).
SHA256: `355c76d9e59cee453a2f3d7aaaa437b7781415646920595c7ea5f3d2aee8ef02`.

Removed the cycle/theta network–simplex hull assertion. The model disaggregates a flow polytope by a simplex; it is not the physical bypass-path algorithm.

## s6:network-parallel-note: Beyond theta blocks: exact subset cuts for parallel-path blocks.

Source: [results/network-simplex-parallel-path-hull.md](../../results/network-simplex-parallel-path-hull.md).
SHA256: `bd06dc18ae787d25bc1c8c7417f24d38207c614a7ee427103fd6fa7f08883fbf`.

Removed the parallel-path subset-cut assertion, which was never transferred to physical pooling.

## s6:power-note: AC power flow feasibility is complete for the existential theory of the reals.

Source: [results/ac-power-flow-existential-reals.md](../../results/ac-power-flow-existential-reals.md).
SHA256: `66c4ca0dd9d650d1e75f0456e38b2d43ff8a3bc5620b3958881635c6ed2d5220`.

Removed the resistive/AC power-flow complexity assertion. The voltage and phase-angle equations form a separate physical model and are not needed to prove pooling completeness.
