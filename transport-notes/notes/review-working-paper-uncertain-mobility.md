# Documentation review: uncertain-mobility working paper

Reviewed 2026-09-07 by `verify_degenerate_adsorption`.

This bounded review checked [the refreshed working paper](working-paper-uncertain-mobility.md) against the risk-moment, generic-fold, finite-precision and scalar-to-bulk source notes and their independent reviews, including [the completed critical-coefficient review](review-critical-risk-mobility.md). No new research or computations were undertaken.

## Scope correction applied and checked

The reviewed version initially specified connected Ω and a one-dimensional closed boundary Γ without requiring Γ to be connected. Connectedness of Ω does not imply connectedness of Γ; an annulus is a counterexample.

This distinction matters for Theorem 4. Its assumption `∫Γ k ≥ κ > 0` controls the reaction only globally. On a disconnected wall, one component could have `k ≡ 0`, while another supplies that positive integral. Even strictly positive surface mobility then leaves the first component without reaction, so the scalar source response there is infinite and the positive-background coercivity argument fails. The supporting [transfer theorem](scalar-to-bulk-design-transfer.md) uses a periodic one-dimensional curve, and [the generic-fold theorem](generic-kinetic-folds.md) explicitly assumes a connected wall.

The author corrected Section 1 to require a fixed bounded smooth cross-section with connected closed boundary and explicitly repeated wall connectedness in Theorem 4. I reread both statements and confirmed the correction. This preserves the scope of the reviewed source results. A theorem for several boundary components would instead need a uniform positive reaction integral on each component and a corresponding extension of the proof.

The documentation review is complete, with no outstanding correction or further scope issue found in the refreshed draft. The displayed constants and powers match the reviewed notes; the critical coefficient is correctly marked independently verified. Sharp supercritical coefficients and the interior finite-resolution crossover remain unclaimed. The finite-bulk statement concerns optimal values at fixed positive bulk diffusivity and nonzero mean tracer speed. The numerical paragraphs correctly distinguish tested designs and discrete optimizations from continuum or asymptotic certification.
