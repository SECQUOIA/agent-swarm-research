# Dines theorem and boundary examples review

Reviewer: cone-geometry agent. Date: 2026-09-22.

This independent review covers `Dines.lean` and `Boundary.lean` against frozen
claims C09–C12 and the exact examples in Sections 4 and 7 of
`results/quadratic-aggregation-trivial-hull-certificate.md`.

## Two-form convexity and HHC

The Dines theorem is proved, not assumed. Its general interface requires the
actual degree-two scaling and polarization identities for a map to `Fin 2 → ℝ`.
These identities agree with two real quadratic forms. The bundled
`QuadraticMap` specialization discharges them using its algebraic laws, and
`System.homEval_combination` proves the polarization identity directly for the
original symmetric-matrix homogeneous system.

The proof is mathematically sound. To add two image points, it seeks a root of
`c(1-t²)+dt=0`; such a root exists over the reals, including the separate case
`c=0`. The points `z=x+t y` and `w=t x-y` have images summing to
`(1+t²)(Q(x)+Q(y))`. The selected root makes the first image collinear with the
target. If the target is nonzero, at least one of the two collinear images is a
strictly positive multiple of it. Rescaling that preimage by the square root
of the inverse positive coefficient gives the target. The zero target is the
image of zero. Nonnegative scalar multiples of an image are obtained through
square roots, so addition closure gives convexity.

Every intermediate preimage remains in the given linear subspace. Therefore
the conclusion concerns the image of every subspace, not merely the image of
the full ambient space. `System.hhc_pair` specializes to the kernel of each
linear functional in the actual HHC definition. It does not add a Dines, HHC,
rank, dimension, definiteness, or nonempty-interior premise. The zero subspace
and identically zero forms are covered.

## Closed hyperbola example

The formal system is exactly the source example on `R³`:
`f0=x0*x1-1`, `f1=1-x0*x1`, and `f2=x0²-x1²`. The third coordinate remains
free. The half-valued symmetric off-diagonal matrix entries give the required
mixed product, as confirmed by the evaluation identities.

Opposite first two inequalities make the strict system empty. The closed
system is proved equal to `x0*x1=1 ∧ x0²≤x1²` and has the displayed witness
`(1,1,0)`. Multiplying the squared inequality by `x0²` and using
`x0²*x1²=1` gives `x0⁴≤1`, yielding both bounds on `x0`.

The PSD-triviality proof is valid for all real weights, which is stronger than
needed for nonnegative weights. Evaluation on `(1,0,0)`, `(0,1,0)`, `(1,1,0)`,
and `(1,-1,0)` forces `w2=0` and `w0=w1`. The aggregate matrix and vector are
then zero. No nontrivial certificate can exist.

The HHC proof uses the actual two independent homogeneous forms. The linear
map `(u,v) ↦ (u,-u,v)` restores the missing coordinate, including its constant
term after homogenization. Taking a linear image of the proved convex image
of each kernel establishes HHC of this three-constraint system.

## Strip example and Shor witness

The formal system is exactly `f0=x0²-4`, `f1=-x0²+2*x0+3` on `R³`, with both
remaining coordinates free. Its strict feasible set is proved to be
`-2<x0 ∧ x0<-1`, and `(-3/2,0,0)` gives strict feasibility. The valid halfspace
`x0<-1` excludes zero from the ordinary convex hull.

For all real weights, the aggregate is PSD exactly when `w1≤w0`.
Nonnegative, nonzero such weights have `w0>0`, and their value at zero is
`-4*w0+3*w1<0`. Thus even the entire family of globally convex strict
aggregations admits a point outside the hull; the argument does not confuse
global convexity with the source's broader good-aggregation notion. HHC
follows from the proved two-form result.

The covariance slack is the exact matrix `diag(7/2,0,0)`. It is PSD and both
constraint residuals at zero are exactly `-1/2`. Since the outer product of
zero is zero, this slack equals the source's lifted matrix `X`. The general
Shor model supplies the equivalence between covariance slack and the actual
block constraint, and `strip_shor_block_witness` explicitly proves PSD of the
block with this exact `X`. Containment of the hull in the projection follows from
feasible-set containment and convexity of the projection. The witness zero
then gives strict containment. `strip_shor_proper` separately excludes
`(3,0,0)` from the projection: the first constraint has value five there, and
a PSD slack can only increase its residual. Thus the projection is both
proper and strictly larger than the hull, as required.

## Review status and verification

All frozen boundary obligations C09–C12 are satisfied. The final wrappers
explicitly prove the closed hull's absolute coordinate bound and failure of
the certificate equivalence without strict feasibility. They also establish
the strip's convexity, equality with its hull, properness, and difference from
the intersection of all globally convex strict aggregations. The exact block
witness and both strict enlargement and properness of the Shor projection
are present. No mathematical defect, hidden assumption, or coverage gap
remains in these two files.

The author reported successful warning-free targeted builds of
`Formal.QuadraticAggregation.Dines` and
`Formal.QuadraticAggregation.Boundary`. This review did not repeat those
builds; final package compilation and axiom/kernel checks are recorded by the
topic verifier. The review independently inspected the source statements and
proofs, including the final wrappers after their addition.

No files owned by the author were edited. No project-wide checks or CI
inspection were performed.
