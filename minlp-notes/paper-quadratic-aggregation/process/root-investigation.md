# Coordinator investigation

These are candidate refinements for the assigned stage authors to prove and
the independent reviewers to check, not accepted results merely by being listed.

## A smaller SDP characterization

On the normalized certificate spectrahedron, maximize `trace(A_lambda)` and
each `+b_lambda[j]` and `-b_lambda[j]`. These `2n+1` objectives suffice: a PSD
matrix has zero trace exactly when it is zero. If the spectrahedron is
nonempty, every certificate is trivial precisely when all these optima are
zero. Empty feasibility is handled separately. No polynomial bit-complexity
or floating-point zero-certification claim follows from this characterization.

## Strictness of the weaker hypothesis

In three variables take

```
f1 = x1^2 + x2^2 + x3^2 - 1,
f2 = x1^2 - x2^2 + x3^2 - 1,
f3 = 2*x1*x2 + x3^2 - 1.
```

The strict system contains zero. The first quadratic part is positive
definite, so the three-form Polyak theorem and openness of positive
definiteness give convexity of the hyperplane images near infinity.
On the homogeneous hyperplane `x3=t`, however, the image is
`(x1^2+x2^2, x1^2-x2^2, 2*x1*x2)`. Its values at the first two coordinate
vectors have midpoint `(1,0,0)`, which cannot be an image point because
`y1^2=y2^2+y3^2` throughout the image. Thus HHC fails.

## Shor projection and closure

The manuscript should give its own cone argument to avoid relying on an
unchecked equality of a projection with a closed intersection. Under strict
feasibility, the midpoint identity in the source note handles the nonclosed
cone correctly. If useful, the same argument for convex combinations with
a strict feasible point proves equality of the closures of the Shor
projection and the convex-aggregation intersection; attribute the classical
relationship accurately rather than claiming this as an original theorem.

## Review priorities

- Distinguish globally convex quadratic aggregations from the good
  aggregations in Blekherman--Dey--Sun.
- Check the published/preprint theorem numbering and assumptions separately.
- The closed-system example and its lack of good aggregations need complete
  algebraic arguments, not the historical sampled eigenvalue checks.
- The historical numerical trials mostly check the already-known two-form
  case. They are not evidence of the general theorem's correctness.

## Primary-source closure discrepancy and a stronger example

The coordinator inspected Kojima--Tuncel's original PDF, printed p.759
(PDF page 10), including a rendered image. Theorem 4.2 asserts exact
equality and the text asserts the projection is always closed; the displayed
dual-cone-sum identity omits closure. This is not merely a text-extraction
artifact. The paper must not rely on this assertion. Any discussion of the
source requires independent assessment of its definitions and possible errata.

A useful strictly feasible example is

```
f1 = 2*x1*x2 + 1,
f2 = x1^2 - x1.
```

The strict point `(1/2,-2)` exists. The aggregate Hessian block is
`[[lambda2,lambda1],[lambda1,0]]`, PSD exactly when `lambda1=0` for
nonnegative multipliers. Thus the intersection of convex aggregations is
the closed strip `0<=x1<=1`. In the Shor projection, `x1=0` forces
`X11=0` and `X12=0`, contradicting the first constraint. For `0<x1<1`,
take `X11=(x1^2+x1)/2`, choose `X12=-1/2`, and choose `X22` large
enough that `X-xx^T` is PSD. At `x1=1`, feasibility requires
`x2<=-1/2` and a rank-one lift suffices. Hence the projection is not closed
even under strict feasibility, and its closure is the full strip.
The stage author should prove this exact description and the reviewers
should check it. No priority claim is attached to this elementary example.

## Candidate improvement to the newly discovered frontier construction

The frontier note's Gram completion uses `r>=3k`. An elementary sequential
completion appears to need only `r>=k+2` (hence `r>=4` for its example).
Starting with `Z` and PSD slack `D=W-ZZ^T`, choose a unit eigenvector `u`
of D with eigenvalue `d>0`. Choose a unit vector v in
`ker(Z) intersect ker(u^T B)`, possible since this imposes at most k+1
linear equations on r coordinates. Set `Z_new=Z+sqrt(d)*u*v^T`.
Then `<B,Z_new>=<B,Z>`, and cross terms vanish, so the new Gram slack is
`D-d*u*u^T`, PSD with one smaller rank. At most k steps give exact Gram W.
This proves the same hyperplane completion with a smaller replication
threshold. It needs independent author development and review in stage 4.
Do not claim sharpness. A still smaller threshold may be possible with
Stiefel-manifold arguments, but is not required for the stated conjecture.
