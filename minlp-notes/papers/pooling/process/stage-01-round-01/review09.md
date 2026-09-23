# Stage 1, round 1 — review 09

## Verdict

**Major findings present:** the endpoint formulation needs an explicit restriction to upper-bound-only quality specifications (or redundant lower bounds). The face-recognition LP and fixed-pool, fixed-affine-dimension algorithm otherwise withstand this review.

## Finding 1 — missing hypothesis in the endpoint special case

- **Location:** `sections/01-foundations.tex`, lines 641–658, especially “each product upper bound in {0,1}” and the claimed equivalence at lines 647–651; consequent exact-MILP and certificate statements at lines 660–672.
- **Severity:** Major: missing essential hypothesis makes the stated equivalence false under the model introduced earlier in the section.
- **Reason:** The model permits lower product-quality specifications as well as upper ones. Restricting the *upper* specifications to zero or one does not remove or make the lower specifications redundant. The proposed disjunctions only encode the upper specifications. Likewise, arbitrary additional polyhedral quality rows permitted in the facial subsection need to be excluded from this special case.
- **Concrete counterexample:** Take two inputs of scalar quality 0 and 1, one pool, one product, no bypasses, all arc and node upper bounds 1, and all lower flow bounds 0. Give the product exact quality 1 (lower and upper quality bounds both 1). This is itself a facial product specification: `F={1}` is a face of `C=[0,1]`. Send one unit from the quality-0 input through the pool to the product. Here `D=0`, `S=0` because there are no upper-zero products, and all displayed endpoint disjunctions and proposed MILP rows are satisfied. Physical quality feasibility fails because the delivered quality is 0. Thus even retaining the preceding faciality assumption does not repair the statement.
- **Correction:** State at lines 641–642 that the *only* product-quality restrictions are coordinatewise upper bounds in `{0,1}` (equivalently, lower bounds are absent or redundant at zero, and no additional polyhedral quality rows are imposed). Keep lower **flow** bounds: those are correctly handled by branch infeasibility checks. Alternatively, extend the disjunction system to upper-endpoint lower quality requirements, but the narrow explicit hypothesis is the simplest repair.

## Checks of the assigned focus

1. **Recognition LP (lines 600–612): checked.** Membership of an original generator in `R_j` is equivalent to membership in `F_j` because the generator already belongs to `C`. A face forces zero forbidden weight. Conversely, expanding the two endpoints of a segment witnessing a potential face-property failure would give a feasible mixture with positive forbidden weight. The simplex makes the LP bounded, and all coefficients have polynomial rational encoding. Infeasibility correctly recognizes the empty face.

2. **Face enumeration (lines 626–638): checked.** Rational affine coordinates can be obtained by Gaussian elimination. In full relative dimension `d`, every facet contains `d` affinely independent original generators. Supporting hyperplanes are computable and testable with polynomial rational data for fixed `d`. A basis of the active facet normals cuts out the same affine hull of a face because the matching right-hand sides agree at a point of that face. Intersecting with `C` therefore recovers the face. Intersections may be represented by their original generators; this supports exact membership and containment tests. The loose polynomial bound is adequate, and the `d=0` case is separated correctly.

3. **Coverage of every physical flow (lines 614–624): checked.** The minimal face containing an active pool quality contains every positive feed generator; every receiving facial product region contains that entire minimal face. Hence the face tuple preserves the original positive support. An inactive pool may choose any nonempty face because all its incident flows vanish. An omitted arc with a positive lower bound correctly makes the branch infeasible. Node-throughput lower bounds remain in the network problem and are not silently removed.

4. **Network optimization and reconstruction (lines 548–567, 617–638): checked.** Node splitting represents the source, pool, and product throughput bounds; the common return arc can use the sum of source upper bounds. With integer bounds, total unimodularity gives integral branch vertices and hence an integral optimum. With rational bounds, rational LP optimization gives polynomial-size rational flows. Each active pool quality is then `sum_i lambda_i y_i / T`, so reconstruction uses polynomially many rational arithmetic operations on polynomial-size data; an inactive pool can use an input quality. Arbitrary bypasses and routing costs are preserved. The finite union gives an attained optimum under the stated finite flow bounds.

5. **Universal-integrality converse (lines 569–582): checked.** A nonface witness yields positive mass on forbidden original input generators. Unit capacities force every integral nonzero single-product flow to use one input; a feasible such input must be allowed. Thus the rational negative-cost mixture strictly beats all integral flows. Rationality follows from the bounded rational one-product LP, without assuming that the original geometric witness is rational.

## Broader stage checks

I read the entire assigned stage. I checked the standard-model rank-one identity, affine-rank substitution, destination decomposition, single-product LP projection, shortest-path sign argument and support bound, conic-hull equalities and capacitated counterexample, and the cyclic SCC reconstruction/decomposition arguments. I did not identify another mathematical defect in those arguments. In particular, the cyclic reconstruction correctly isolates source-free circulation components, and the destination disaggregation uses head-based absorption fractions consistently with perfect mixing.

The supporting source proofs consulted for the principal assigned focus were `results/pooling-facial-quality-integrality.md` and `notes/pooling-endpoint-quality-structure.md`. Their earlier PASS labels were not treated as proof. No other current-round review report was inspected.

## Verification limits

This is an independent mathematical and encoding audit of Stage 1, not a full novelty search or a verification of every cited paper's attribution. I did not run computational experiments or compile the manuscript. I have not checked later stages, their promised hardness applications, or the completeness of coverage of the whole repository. The bounded-pool algorithm is verified as polynomial for fixed parameters, without asserting a uniform-exponent fixed-parameter algorithm or practical efficiency.
