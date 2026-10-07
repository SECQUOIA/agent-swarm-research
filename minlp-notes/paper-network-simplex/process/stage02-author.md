# Stage 2 author record

Date: 2026-09-07. Author agent: `paper_author`. Status: authored and locally
checked; awaiting the required five independent reviews.

## Completed scope

Added `sections/02-compression.tex` and its input in `main.tex`. The section
fully develops the two general-graph extended formulations, exact observation
elimination, the forest-complement original-coordinate hull, minimum
completion by individual products, and constructive recovery. The accepted
foundations and bibliography were not changed. README now identifies the new
section and checks.

The source proofs are the reopened compressed-hull note and observed-rank
elimination note. Both associated independent reviews and the literature
audit were read. The construction is restated using the accepted notation
and directly invokes the accepted block/state theorem rather than duplicating
its proof.

## Development beyond transcription

1. Added and proved `lem:fixed-arcs`: known fixed arc coordinates can be
   deleted with adjusted balances and affine product substitutions. If all
   fixed coordinates are deleted, the reduced polytope's affine hull is
   exactly its balance affine space. The latter follows by averaging
   coordinate-interior feasible witnesses. This explains precisely how
   capacity-induced ambient degeneracy can be removed before counting cycles.
   No detection complexity or conditional-slice dimension claim is made.
2. Reconstructed the cycle-matrix total-unimodularity proof from incidence
   minors and tree-column replacement determinants. The elimination proof
   includes the explicit bordered determinant for the Schur complement.
3. Made the original-variable coefficient argument explicit for both
   formulations. Residual rows use a single representative arc expression,
   while labels use disjoint product columns; selected observation equations
   disappear as identities. Primitive integer normalization is distinguished
   from the displayed rational row scaling.
4. Added an explicit nonzero bound alongside row and variable counts.
5. Added a worked acyclic unit-capacity K4 example. Three chord observations
   leave a forest complement and give the cut
   `z_13 + z_14 + z_24 <= y`. A specified McCormick-feasible candidate violates
   it by exactly `1/10`. All omitted bounds, especially the residual bounds,
   remain part of the full hull description.
6. Explained direct forest recovery using the correct block state balance
   `A_B f^{B,j} = y_j A_B v_B`, including component consistency. Using the
   unrestricted global balance on a block would obscure articulation effects.

## Proof scrutiny

- Degrees used in path suppression are block degrees, loops count twice,
  and rank one has a separate single-loop core convention.
- At rank at least two, the minimum-degree and Euler counts give
  `k <= 3r-3`; all core path bounds remain finite.
- State coordinate vectors vanish at zero weight by chord identity and
  finite path bounds, including the merged state.
- Observation nullity is computed on the original unobserved graph, with
  isolated vertices included. Suppression preserves the restriction kernel
  because one observed path arc fixes the signed deviation along that path.
- The auxiliary count charges locally observed labels only. Unobserved
  labels are already merged.
- Product completion is minimal only for scalar coordinate additions used
  to reconstruct the ambient circulation space. It is not a lower bound
  for arbitrary lifts or feasible slices at fixed product values.
- Completing observations and then projecting is exact because coordinate
  projection commutes with convexification. Added labels are unnecessary;
  added observation rows are absorbed by the existing row bound.
- Rational exact recovery and numerical LP feasibility are kept distinct.

## Attribution

The general disaggregation and block gluing remain attributed in the accepted
foundations. The reduced-RLT predecessor is cited specifically as Liberti and
Pantelides (2006), Theorem 3.1 and Section 2. The root independently checked
an openly readable author-uploaded full text at
[ResearchGate](https://www.researchgate.net/publication/225718151_An_Exact_Reformulation_Algorithm_for_Large_Nonconvex_NLPs_Involving_Bilinear_Terms),
confirming the full-row-rank reconstruction result and missing-product
elimination. The unsuccessful thesis/CiteSeer retrievals from the earlier
audit are not represented as successful. No new bibliographic entry was
needed. The graph criterion and combined sparse-hull bounds are distinguished
from the classical rank-elimination mechanism.

## Exact checks and build

Commands executed:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python \
  code/network_simplex_review/verify_observed_rank.py
```

Run from the repository root. Result: **204 exact observation patterns passed**,
including rank identity, minimum forest completion, unit elimination
coefficients, and both reconstruction directions. This pre-existing independent
script uses no production formulation code.

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python verification/stage02-exact.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Run from the manuscript directory. The new check enumerates feasible integral
vectors of 80 small unit-capacity directed multigraph flow models, then checks
fixed-coordinate deletion and the exact reduced affine dimension. It includes
loops, repeated arcs, disconnected graphs, zero capacities, and empty reduced
coordinate sets. It also verifies the K4 reconstruction identities, all four
flow vertices, McCormick feasibility, and the exact `1/10` violation. Result:
**PASS**. See `verification/stage02-exact.json`.

The complete manuscript builds to **13 pages**, with no undefined references,
citations, LaTeX warnings, or box warnings. The build output is retained in
`verification/stage02-build.txt`; `stage02-validation.json` records source
hashes and checks. Finite computations supplement the proofs and do not
establish novelty.

## Remaining questions

No unresolved mathematical issue was identified in the stage's stated scope.
The forest condition is sufficient, and minimum completion is expressly not
claimed to characterize minimum extended-formulation dimension. Stronger
original-coordinate results for other graph structures belong to later stages.
