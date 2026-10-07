# Focused review of the convex cubic optimizer set and Hoffman bound

Reviewed [convex-cubic-point-oracle.md](convex-cubic-point-oracle.md),
especially Sections 4--6, on 2026-10-02. No substantive error was found
in the optimizer-set characterization, the uniform Hoffman estimate,
or the polynomial-bit constants. This is a focused mathematical review,
not a literature audit or a duplicate of the full-file review.

The optimizer-set characterization also has a direct proof that does
not use the quantitative constant in (7). If `y` and `u` both minimize
the convex cubic, put `d=u-y`. Convexity makes the objective constant
on their segment. Therefore

```
d'H(y)d = d'H(u)d = 0.
```

Positive semidefiniteness gives `H(y)d=H(u)d=0`. The cubic symmetry
identity (5) then gives `d'H(c)d=0`, so `d` belongs to `K=ker H(c)`.
Along a segment parallel to `K`, the objective changes by exactly
`g_c'd`. This proves both directions of (8), including when every
optimizer lies on the boundary. The affine-slice right-hand side may
be irrational; no step requires computing it.

For (10), the projection normal-cone formula remains valid for a
lower-dimensional, nonempty polyhedron and for real right-hand sides.
Select an independent subset of equality rows and eliminate redundant
active box normals modulo their span, retaining nonnegative
coefficients on the box normals. If the projection displacement is
nonzero, the resulting matrix `R` has between one and `n` independent
integer rows, each with entries bounded by `C`. Thus

```
det(RR') >= 1,
lambda_max(RR') <= (nC)^2,
sigma_min(R) >= (nC)^(-(n-1)).
```

The active outward box normals have nonpositive inner products with
the displacement from the projection to the original feasible box
point. Removing those terms leaves the equality residual, whose
selected coordinates have norm at most `||Ax-b||_2`. This proves the
stated constant `(nC)^(n-1)`, uniformly over irrational `b`. The
zero-displacement case needs no matrix estimate. Redundant equality
rows do not change the argument.

Section 6 clears denominators before invoking (10), so no denominator
factor is missing there. The factor `D` in (12) appears when bounding
the integer residual `A(x-y)`. A positive principal minor of order
`r=rank H(c)` gives the valid lower eigenvalue bound
`D^(-r) M^(-(r-1))`; (11) weakens this safely because `D,M>=1` and
`r<=n`. The product used to define `D`, integer matrix height `C`, and
all powers in (11)--(12) have polynomial binary length and can be
computed in polynomial time. Replacing `R_0^(1/4)` by `R_0` is valid
because `R_0>=1`.

The boundary example `f(t)=t^3` on `[0,1]` confirms that an individual
endpoint Hessian can have a larger kernel than the center Hessian.
Here the phrase "common kernel" means the intersection of all the
Hessian kernels, not equality of their individual kernels. Stating
this explicitly would prevent that possible misreading. Likewise,
"independent subset of rows of A" would make the row-height argument
in Section 5 explicit.

The affine case is handled correctly by the separate exact endpoint
solve. Constant objectives and boxes with every coordinate fixed also
return exact optimizers. Attempts to break the optimizer-set argument
with boundary minima or extra endpoint null directions fail for the
PSD and cubic-symmetry reasons above.

Verification consisted of reading the saved draft and checking these
arguments directly. No numerical tests, external searches, project-wide
verification, or CI inspection were performed for this review.
