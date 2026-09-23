# Stage 4A: product support orbits

Authored `sections/08b-product-orbits.tex`. No main-file or bibliography changes.

## Coverage

- `2026-09-04-hermitian-product-ball-capacity-rigidity.md`: subsumed by the stronger all-EJA theorem with scalar rays; retained the no-ray support injectivity observation and fixed-field equality profiles.
- `2026-09-04-hermitian-product-ball-active-ray-covering.md`: verified and incorporated, including the finite covering rather than unjustified injectivity, universal-cover obstructions, real orders 3/4 as intermediate possibilities, and circle counts.
- `2026-09-04-real-low-order-cylinder-exclusion-product-balls.md`: verified and incorporated with complete PSD4 Hodge/ruling and PSD3 cylinder/isolation arguments. The one-ball PSD3 obstruction is referenced to the fully proved Section 5 proposition.
- `2026-09-04-symmetric-cone-product-ball-active-ray-saturation.md`: verified and incorporated, including Albert exclusion, general spin dimensions, matching without product splitting, and vanishing of every unrelated dual row.

## Independent checks and development

1. Reconstructed the mixed rank chain using the aggregate dual and the fact that nonnegative C1 scalar factors have zero derivative at zeros. The product identity has nondegenerate mixed pairing at every contact; all individual rank equalities follow.
2. Checked that complementary lower-semicontinuous ranks are constant and that the Section 5 support differential gives a proper local diffeomorphism.
3. Checked real order at least six via the kernel of addition on fundamental groups and Hurewicz. The resulting H2 torsion survives as a direct summand in the target product and contradicts the source.
4. Simplified the source order-five proof: identify the oriented Grassmannian with the quadric using `[u+iv]`; the homogeneous fibration gives H2 = Z; the hyperplane has nonzero cube (degree two), hence nonzero square. Square-zero degree-two rational classes span the source cohomology but cannot span the target if this factor is present. This avoids needing an integral indecomposable calculation or an uncited full quadric ring presentation.
5. Checked that the degree-two assignment is made on universal covers, eliminating decomposable degree-two classes coming from circles. Primitive square-zero integral classes are precisely signed source S2 generators.
6. The PSD4 fixed-kernel locus is an oriented Gr2(R3), whose two Hodge projections both have degree plus or minus one. A map into it cannot realize only one ruling. Applying both distinct assigned cylinders kills every dual row and is impossible.
7. After eliminating PSD4, each PSD3 block serves only its unique assigned S2 row. Other PSD3 blocks and all spin blocks serve only their own distinct assigned source. This isolates the exact Section 5 one-ball obstruction even with scalar rays.
8. Assignment for dimensions beyond two uses an invertible degreewise matrix on cohomological indecomposables and a nonzero determinant term. Circles use a finite-index fundamental-group matrix over Q. No splitting of the covering as a product is assumed. Nonzero restriction degree is preserved as the other fixed coordinates vary by homotopy (and orientation changes in lifted real targets affect only signs).
9. Preserved scope: global C1 factor selections and capacity equality, not arbitrary lifts or arbitrary barrier parameters. The ambient standard-barrier count is just the total Jordan rank of the forced non-ray factors.

## Literature

Primary author PDF for Sankaran–Sarkar was opened via web search:
https://www.imsc.res.in/~sankaran/Papers/grassojm.pdf
Section 2 states the Schubert cohomology description and the integral quaternionic degree-doubling ring isomorphism. Publication metadata is Osaka Journal of Mathematics 46(4) (2009), 1143–1161; arXiv:0805.0509. Suggested key: `SankaranSarkar2009`.

Suggested BibTeX:

```bibtex
@article{SankaranSarkar2009,
  author = {Sankaran, Parameswaran and Sarkar, Swagata},
  title = {Degrees of maps between {Grassmann} manifolds},
  journal = {Osaka Journal of Mathematics},
  volume = {46},
  number = {4},
  pages = {1143--1161},
  year = {2009},
  url = {https://www.imsc.res.in/~sankaran/Papers/grassojm.pdf}
}
```

Existing references `FK1994`, `Hatcher2002` support the EJA/orbit descriptions and classical topology. The quadric identification and degree argument are supplied in the proof rather than attributing an unverified integral-ring locator.

Parent verified the primary HTML of Aubrun–La Piana–Müller-Hermes arXiv:2606.27825v1 and requested key `ALM2026Lorentz`. The section explicitly distinguishes their every-positive-linear-map quantifier from our one smooth nonlinear full-row slack factorization at curvature equality. No sweeping novelty assertion was added.

## Validation

Files are ready for parent integration and the mandatory five independent stage reviews. Compilation remains the parent's integration task because this subtask was instructed not to modify main.tex or bibliography.bib.
