# Stage 2 independent review 4

## Findings

**No valid major or minor issue identified.** The stage can proceed on the basis of this review. This is an independent mathematical/editorial assessment, not a guarantee against every possible undiscovered error.

I read all 1,296 lines of the frozen `sections/01-foundations.tex` and all 1,571 lines of `sections/02-quadratic-finite.tex`, including every proof, example, and unnumbered algorithmic estimate. I compared both with `revision-stage1-round1/source`, read the stage author/literature reports, and did not consult other reviewers or change manuscript sources.

## Critical checks

- Reconstructed the closure/parity argument, including nonmeasurable original contacts and nonclosed lifts; the disjunction proof handles inactive recession directions correctly. Checked square endpoints, empty prefixes, exact binary products, the product-width/area estimates and four-point obstruction, and the fractional-cover constants.
- Checked scalar principal slicing and the indefinite-volume determinant constant; reconstructed the folding epigraph argument, one-sided inertia slicing and upper construction, product one-sided formula, and projected-facet count. The changed sawtooth paragraph now correctly adds a band to the interpolant, retaining the exact square graph.
- Checked principal Hermitian compression, real shrinking, the covariance fourth-moment identity, capacity scaling, shared coordinate count, and the cross-product certificate. The repaired product-Hessian congruence proves its claim on every positive box. Smooth contact tensorization, Taylor allocations, constant-rank affine-fiber tubes, and positive perspective transfers preserve the actual input domain and the stated formulation model.
- Reconstructed the finite covariance lower/upper constants, certificate inequality, commuting reduction, and dimension-gap example. Checked the rational Jacobi contraction and denominator argument; penalty gradients and Lipschitz bounds; polynomial-radius search, rounded-iterate recurrence, branch approximation, exact scalar repair, and rational grid sandwich. Positive semidefinite-order monotonicity is justified by the displayed derivative even for indefinite Hessians.
- Checked grouped and total-absolute-error reductions, effective output-image equality, oracle rounding, nonlinear input quotient and domain-volume loss; positive block/diagonal allocation; logdet hypograph interior ball, weak oracle and central-ball repair; integer-feature and forest volumes; thin-domain obstruction.
- Reconstructed the entire hardness argument: zero dimension is equivalent to the Max-Cut threshold; disjoint replication supplies a parity-incompatible packing; scaling fixes every tolerance to one; the extra square has optimum exactly one; fixed polynomial replication separates the promised low/high cases for every fixed positive exponent. The text correctly limits coNP membership to the restricted family and does not claim to exclude all sublinear additive functions.

## Independent source and numerical checks

I checked primary source passages independently, not merely the author's notes:

- [GLS 1981](https://ir.cwi.nl/pub/10046/10046D.pdf), printed p.172, Definitions (5)/(6): the cited weak optimizer compares its value with the actual body, supporting the subsequent exact repairs.
- [Zhang–Sra 2016](https://proceedings.mlr.press/v49/zhang16b.pdf), pp.8–9, Lemma 7 and Corollary 8/proof: the curvature factor depends on distance to the comparison point, and the projected recurrence has the required sign and scaling. Downloaded a fresh PDF, extracted it, and inspected the rendered p.8 formula.
- [Dadush–Peikert–Vempala 2011](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf), Theorem B.5, PDF p.39: rational ellipsoid matrix, potentially real center, and factor `(d+1)sqrt(d)` match the import. The manuscript supplies the symmetry argument removing the center.
- [Nicola 2010](https://www.impan.pl/shop/publication/transaction/download/product/90263), printed pp.208–209: Definition 1.1 and its following paragraph support the constant-rank affine-fiber attribution and updated metadata.
- [Yarotsky v3](https://arxiv.org/pdf/1610.01145v3), pp.7–8, Proposition 2/proof: the dyadic square interpolation and telescoping folding identity are correctly attributed. The manuscript separately establishes the formulation count comparison.

As focused sanity checks, 343 independent LP optimizations of the relaxed continuous folding system (depths 1–7, 49 inputs each) matched the exact folding value, with maximum numerical discrepancy zero. For all 64 simple four-vertex graphs, 768 sampled interior points obeyed the vertex/Max-Cut upper bound. These checks supplement the general proofs; they do not establish them.

## Optional preference

None required for this stage. The added proof roadmaps and source-specific distinctions improve standalone readability without changing theorems or weakening hypotheses.
