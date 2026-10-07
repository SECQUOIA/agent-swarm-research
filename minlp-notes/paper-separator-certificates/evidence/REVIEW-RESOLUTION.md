# Resolution of manuscript reviews

The mathematical audits and fresh manuscript reviews found no blocking flaw in
the stated theorem chain. This record describes changes actually incorporated,
not a claim of journal peer review. The independent reports are preserved in
`reviews/`.

| Review area | Incorporated resolution |
|---|---|
| Model | Distinguish the supplied decomposition width from the graph's treewidth; remove original fixed coordinates; retain every nonempty touching intersection. |
| Consistency | Give full minimax and closed-envelope proofs, handle the constant-only quotient, require linear cell classes containing constants, and distinguish normalized functionals from valid lower relaxations. Use `chi` for shifts and `n_T` for the edge count. |
| Scalar covering | Prove concentration, chord error, boundary refinement, and all dyadic counts; derive its regularity assumptions from smooth bag data. State that it counts exact-bag separator pieces, not general certificate leaves. |
| Regridding | Use aggregate squared copy disagreement on occurrence subtrees, without a branching parameter. Keep final partition, cumulative creation, and incidence/oracle counts separate. |
| Inexact work | Sum certified local residuals once per selected bag, give aggregate slope/gradient budgets, and require positive local tolerance for finite-precision reconstruction. |
| Polynomial arithmetic | Develop a computable Hessian majorant, affine Taylor models, deterministic endpoint minimizers, common denominators, compact serialization, and actual bit-budget search. State the bit-cost storage model and charge incidence lookup and address handling. Verify the stored center and incumbent belong to the box; charge completed serialization before accepting a trial. |
| Dynamics | Retain the multiplier residual, prove adjoint cancellation at ambient centers, state full-box invariance and derivative promises, and initialize the exact-real incumbent explicitly. |
| Dynamics arithmetic | Enclose the exact recurrence, reset all center coordinates, choose bounded-precision dyadic meshes, and distinguish compressed exact trajectories from expanded rational states. Keep conditioning-only work tied to a first sufficient ratio. |
| Parameter search | Validity holds for every trial, while the sharp final partition formula belongs to a sufficient fixed-ratio run. Bound the first successful output through its actual work budget. |
| Limits and allocation | Give a complete finite dyadic localization counterexample and arbitrary-partition affine-constraint obstruction. State the lower-gap hypothesis separately and identify the staircase as a finite-state example. |
| Editorial integration | Correct the band identity's distance argument and factor two; say no nonconvex local search is required; normalize asymptotic logarithms; remove an uncited coordinate-grid claim; explain independent checking and representation costs. |
| Prior work | Credit classical cost shifting, tree gluing, band approximation, compatible-box decomposition bounds, inexact decomposition, adaptive grids, adjoints, and rational LPs. Acknowledge Robertson--Cheng--Scott only at the level supported by its verified publisher abstract. Restrict novelty to the proved construction and specific contracts. Internal companions have no invented bibliographic identity. |

Unproved smooth-band insertion and multidimensional covering claims are not
used. The paper's open questions concern independent extensions; they leave no
required proof step unfinished in the stated results. All experimental source
tables were excluded because the proof chain is analytic. No experiments were
rerun.
