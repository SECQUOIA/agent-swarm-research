# Independent review: nonlinear input-rank precision

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author. Reviewed [the nonlinear input-rank candidate](quadratic-nonlinear-input-rank-precision.md), including its explicit LP separator, convex-domain qualification, and named reduced output map. The already reviewed covariance, general-norm, and polynomial-construction results are imports.

**Verdict: pass.** The rational construction has additive integer-count overhead `O(r log(r+1))`, where `r` is the rank of the stacked symmetric Hessians. The exact quotient, domain normalization, and volume correction justify replacing the ambient input dimension by this rank. No remaining substantive gap was found. Runtime and continuous formulation size still depend on the full input encoding, and literature priority is not assessed here.

## 1. Common kernel and exact quotient

Because the Hessians are symmetric, their common row span equals the span of their column spaces. The chosen full-row-rank rational matrix `U` therefore satisfies `ker U=intersection_j ker H_j`. For `F=U^T(UU^T)^(-1)`, `UF=I`, and `FU` is the symmetric orthogonal projection onto that row space. Consequently `H_j=(FU)^T H_j(FU)=U^T G_j U` with `G_j=F^T H_j F`.

All these matrices have polynomial rational encoding length by exact elimination. With `c=(1/2)1`, an explicit affine remainder is

```
a_j(x)=(a_j+H_j c)^T x+b_j-(1/2)c^T H_j c.
```

It verifies the exact identity `f_j(x)=a_j(x)+(1/2)[U(x-c)]^T G_j[U(x-c)]`. In particular, affine coefficients may vary freely along a fiber of `U`; subtracting this affine map removes that variation before projection.

To obtain the reduced formulation, retain the original variables as continuous lifted variables and impose the affine image relations for `z` and the residual output. No explicit elimination of a possibly complicated projection is required. Restricting the original inputs to their cube first is harmless and ensures that every admitted reduced input lies in `Z`. Every exact reduced graph point is reached because the definition of `Z` supplies a cube preimage. Every admitted error is the original error and remains in `K`.

Conversely, coupling a reduced formulation to any original input with `z=U(x-c)` and restoring the affine remainder gives the original graph approximation. The latent preimage used by a reduced formulation need not equal that original input: their shared `z` is enough, since the nonlinear map depends only on `z`. Both constructions preserve integer variables, convexity of the lift, and rationality for binary linear lifts. This proves equality of both minima.

When `r=0`, all Hessians vanish and the exact graph is a rational LP. When `r>0`, not all reduced Hessians can vanish, since `H_j=U^T G_j U`; the later zero-output-image branch therefore introduces no extra degeneracy.

## 2. Zonotope separation and radii

The zonotope is centered, symmetric, compact, convex, and full-dimensional because `U` has full row rank. Its displayed membership problem is a rational LP. For an outside query, the second LP in `h,v` correctly produces strong separation: its inequalities imply

```
sup_{y in Z} h^T y=(1/2)||U^T h||_1
                 <=(1/2)sum_i v_i < h^T z.
```

Strict separation exists for an outside point of a compact convex set; positive scaling makes its gap at least one and proves feasibility of that second LP. Exact rational LP returns a feasible certificate with polynomial bit length in the matrix and query encoding. The unbounded scale of this certificate is harmless in the binary model. Thus this is the strong rational oracle required by the imported rounding theorem, not just approximate membership.

For independent columns `U_J`, the stated `c_inv` bounds the Euclidean operator norm of their inverse. A point in the ball of radius `1/(2c_inv)` therefore has preimage in `[-1/2,1/2]^r`. Setting all other input coordinates to zero embeds this parallelotope in `Z`. The sum-of-absolute-entries bound likewise gives the stated rational outer radius. Inversion and these bounds have polynomial encoding length even if the chosen columns are poorly conditioned.

The classical strong-oracle rounding import therefore applies to the domain, yielding a rational metric matrix `A` with the stated factor `(r+1)sqrt(r)`. Its assumptions and source were separately checked in [the general-norm review](review-quadratic-general-norm-output-precision-second.md).

## 3. Rational normalization and volume

For positive definite rational `A`, exact unpivoted LDL factorization is valid: every pivot is positive. Its entries have polynomial bit length. A dyadic number within a factor two of each positive pivot square root can be chosen through rational square comparisons, with polynomially bounded binary exponent.

The matrix order follows by congruence:

```
A=L diag(D_ii)L^T,
R^T R=L diag(b_i^2)L^T,
D_ii <= b_i^2 <= 4D_ii.
```

Hence `A<=R^T R<=4A`. The directions of both geometric inclusions are correct. For `||y||<=1/beta`, its preimage `z=R^(-1)y` satisfies `z^T A z<=||y||^2`, and so belongs to the inner ellipsoid in `Z`. For `z in Z`, the outer ellipsoid gives `||Rz||<=2`.

The affine map `y=(1/2)1+(1/4)Rz` is invertible on the reduced input space, has a rational inverse of polynomial bit length, and maps the domain into the unit cube. Its domain image contains a ball of radius `1/(4beta)` about the cube center, hence a cube of side `1/(2beta sqrt(r))=1/[2r(r+1)]`. This proves the exact stated volume lower bound.

The transformed quadratics and all affine remainders are rational with polynomial encoding length. The transformed domain may have many facets, but its exact linear lift through the original cube has only polynomial size. Restriction to that domain therefore costs no extra integers and does not require writing a facet description.

## 4. Covariance lower bound on the normalized domain

The revised domain lemma explicitly assumes compactness, full dimension, and convexity. Convexity ensures that the midpoint of two graph inputs remains in the domain, so the original parity argument still forces its output error to satisfy the budget. This qualification matters; the draft's initial statement for an arbitrary compact domain was broader than the supplied argument and has been corrected.

All parity supports lie in the unit cube. Taking closures preserves their pairwise quadratic inequalities and their cover of the domain. Their covariance caps and fourth-moment bounds are therefore exactly those in the imported theorem, in dimension `r`. Each support has volume at most `2^(A_r-Phi(t))`. Covering the domain by at most `2^p` supports gives

```
log_2 vol(Omega) <= p+A_r-Phi(t),
p >= Phi(t)-A_r+log_2 vol(Omega).
```

The volume term has the displayed sign. No unit-volume assumption survives unnoticed, and no new factor involving the original input dimension is introduced.

## 5. Output reduction and final count

The revised notation writes `q(y)=b(y)+T q_bar(y)` before constructing the output ellipsoid. The effective body and ellipsoid live in the `d` output coordinates of `q_bar`, and `Phi` uses its Hessians. Thus all matrix dimensions in the covariance comparison agree. The effective output dimension is at most `r(r+1)/2`, regardless of the original output count.

Enlarging the effective error body to `alpha E_0` can only decrease its minimum integer count. Combining that fact with the volume-corrected lower bound and the homogeneous covariance scaling gives equation (7) with the correct direction. The polynomial construction can be run on the entire containing cube with the same transformed Hessians and ellipsoid benchmark. Restricting its output to the actual domain afterward only removes points and retains every required graph point.

Restoring the reduced output's affine part and then the original affine fiber-dependent output map gives exactly the original error vector. Thus the final MILP is valid for the original problem. Its additional count is

```
A_r+B_r+O(r)+r log_2[2r(r+1)]+(r/2)log_2(alpha),
```

which is `O(r log(r+1))` because `alpha=(d+1)sqrt(d)` and `d<=r(r+1)/2`. All anisotropy and rational conditioning affect encoding and runtime, or the benchmark optimum itself; they do not add an ambient-dimension term to this estimate.

## 6. Reproducible checks and limits

I read and reran the author's [exact checker](../code/quadratic_rank/check_nonlinear_input_rank.py). It passed 21 common-kernel quotient and affine-remainder cases and 21 rational LDL sandwiches and inverse-map cases. These checks use exact rational arithmetic. They do not implement zonotope separation, oracle rounding, or the imported full MILP algorithm.

The proof checks above cover the formulation-minimum equality, domain volume, oracle conditions, and complexity transfers that those algebraic tests cannot establish. The result is a rank-sensitive additive guarantee, not an assertion that arbitrary low-rank curved domains have exact MILP descriptions.
