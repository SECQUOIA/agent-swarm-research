# Stage 1 independent review — reviewer 2

Reviewed the scope/literature audit, bibliography, README and LaTeX scaffold; checked the original conditioning proof package and the primary Xiong–Freund source. This is a planning review. Unwritten proofs explicitly assigned to later stages are not treated as defects in a completed manuscript.

## Assessment

**No major issues identified at this stage.** The topical boundary is coherent and the scope records the significant newer degenerate-LP development. The treatment of the previously missing Xiong–Freund comparison and the classical status of the degenerate LP limit is appropriately cautious. The stronger all-barrier development is mathematically plausible, and the record clearly labels the more ambitious RHS construction as unverified.

The following minor planning corrections should be made before theorem authoring.

## MINOR 1 — Do not categorically exclude a gap-dependent family of barriers

The Stage 2 obligations say that a gap-dependent sequence of barriers is not covered by a rate constant. That is too broad if the proposed containment proof succeeds. Its constants depend on the barrier through the declared parameter, rather than through other properties of the barrier. Consequently a family `F_g` with uniformly bounded parameters is covered whenever the required center exists at each prescribed gap. What is not justified is a uniform rate constant for an arbitrary family whose parameters grow without bound.

Evidence: writing `K(g)=L(g)-L(g)` and `E_F={v:v^T H_F v<=1}`, the proposed sandwich gives

`E_G ⊆ K(g) ⊆ 2 C_F E_F`, hence `H_F <= 4 C_F^2 H_G`.

The reverse sandwich gives `H_F >= (4 C_G^2)^(-1) H_G`. The interior-ball upper bound and diameter lower bound likewise contain only fixed problem geometry and `C_F`.

Correction: replace the blanket exclusion by a statement distinguishing fixed barriers, uniformly bounded-parameter families, and unrestricted parameter growth. State that each comparison concerns existing centers in the common gap range.

## MINOR 2 — Distinguish numerical coordinate dependence from invariance of exponents under fixed maps

The inventory appropriately includes the Schur invariance example and warns against arbitrary preconditioning claims. It should also require the final boundary paragraph to state that a fixed nonsingular change of reduced coordinates preserves asymptotic conditioning rates up to constants. Otherwise “no cone-coordinate invariant lower bound follows” can be read as denying even invariance of the exponent under a fixed coordinate map.

Evidence: for `H'=T^T H T` with fixed invertible `T`,

`κ(H)/κ(T)^2 <= κ(H') <= κ(T)^2 κ(H)`.

Thus a fixed map preserves a `Theta(g^-p)` law. A map depending on `g`, such as exact Hessian whitening, can change it. Similarly, a family of formulations indexed by a separate perturbation parameter may have nonuniform comparison constants.

Correction: make these quantifiers explicit in the planned coordinate-change proposition. The Schur identity remains valuable, but should not be used to imply failure of fixed-map exponent invariance.

## Verification notes and retained obligations

1. The difference-body candidate has a straightforward proof route. For every vector in the open Dikin ellipsoid, choose its sign to make the objective nonincreasing; this signed vector is the difference of two points of `L(g)`. Symmetry of the difference body recovers the other sign, and compactness gives closure. Conversely, asymmetric containment bounds both endpoints relative to the center, giving the factor `2 C_F`. This avoids the false intermediate statement that the entire centered Dikin ellipsoid lies in the objective sublevel.

2. The maximum-eigenvalue upper bound follows from a relative ball of radius `r` in `P`: contraction toward an optimizer puts a ball of radius `rg/Δ` in `L(g)` for `0<g<=Δ`, so the difference body contains the origin-centered ball of radius `2rg/Δ`. The factor two cancels against its containment in `2C_F E_F`. This supports the proposed all-barrier extension, provided the setup explicitly retains positive relative dimension, nonconstant objective, positive-definite relative Hessian, and the gap range.

3. The full-spectrum polyhedral comparison and `O(g)` weak-projector estimate are believable consequences of equal-gap Loewner comparison. The sharper `O(g^2)` canonical assertion requires the endpoint expansion and block perturbation proof specified in the scope. The oscillatory barrier sharpness witness must receive the promised derivative and barrier-parameter audit; bounded perturbation of function values alone would not establish self-concordance.

4. The scope correctly distinguishes upper error bounds from attained diameter laws and records the numerical-only status of the four fractional-SDP spectral windows. These distinctions must survive introduction and abstract compression.

5. I directly checked Xiong–Freund, Fact 5.2 and Remark 5.1, printed pp.32–33. They use central-path ellipsoids to bound primal–dual sublevel geometry, and Section 5.2 develops Hessian rescaling. The scope accurately identifies this as substantive antecedent and does not assert a first connection between geometry and Hessian conditioning. A final comparison should retain the distinctions between the primal gap and their primal–dual gap, and between equal-gap barrier comparison and their rescaling result. [Primary PDF](https://optimization-online.org/wp-content/uploads/2024/06/arXiv_0715.pdf). The [arXiv record](https://arxiv.org/abs/2406.01942) confirms the July 15, 2024 version and has no journal reference; the bibliography's preprint citation is appropriate.

6. The scaffold honestly announces its incomplete status. No unsupported final theorem, novelty claim, or submission-readiness assertion has been inserted prematurely. No obvious bibliography or build-structure defect was found in the reviewed files.

After the two minor quantifier refinements, Stage 1 is ready to proceed to mathematical development. This conclusion does not certify the later candidate proofs or exhaustive absence of prior art.
