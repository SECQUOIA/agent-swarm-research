# Second independent review: general symmetric output-error bodies

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author and first reviewer. Reviewed [the general-norm candidate](quadratic-general-norm-output-precision.md), including the revised strong-separation assumption and capped volume threshold. The previously reviewed covariance law and rational MILP construction are imported, rather than re-proved here.

**Verdict: pass.** Under the stated rational strong-separation oracle, explicit polynomial oracle-output bound, and known positive inner/outer radii, the reduction gives a rational MILP using at most `p_conv(f,K)+O(n log(n+1))` binaries. The additive constant is independent of ambient output dimension. No remaining substantive mathematical gap was found. The result does not establish the same oracle guarantee from weak separation without further argument, and the revised draft no longer claims it.

## 1. Effective output space and preservation of the benchmark

The rational matrix `C` collects the coefficients of the `n(n+1)/2` quadratic monomials. Thus its image has dimension `d<=n(n+1)/2`, independently of the number of output coordinates. Rational elimination produces a full-column-rank image basis `T` and `B` with `C=T B`, all of polynomial bit length. No orthonormal basis or irrational transformation is required.

For a formulation of the effective graph, introducing the original output and imposing `w=a(x)+Tz` is an affine extension. Its admitted original errors are exactly `T(z-g(x))` and lie in `K`. Conversely, intersecting any original formulation with that same affine equation preserves every exact graph point, because the exact quadratic output lies in this affine image. Every remaining error is in the section defining `K_eff`. Both operations preserve the number and type of integer variables.

This proves equality of the integer minima for arbitrary convex lifts, including unrestricted general integer coordinates. It also proves equality for rational binary linear formulations: the added equations have rational coefficients. Original admitted errors outside the image may be removed in the reverse direction without violating the definition of an approximation. The reduction is a **section**, not an assumption that all original errors already lie in the image.

If `d=0`, every output is affine. Its exact graph over the cube has a rational LP formulation with no integer variables, so the zero-rank case is complete without any rounding call.

## 2. Effective-body radii and oracle encoding

Because `T` is injective, its rational left inverse `L=(T^T T)^(-1)T^T` exists and has polynomial encoding length. Bounds such as one plus the sum of absolute entries dominate the Euclidean operator norms of both matrices. For `||z||<=r_0/c_T`, `||Tz||<=r_0`, which proves the inner inclusion. If `Tz in K`, then `z=L(Tz)` and `||z||<=c_L R_0`, proving the outer inclusion. Thus the effective body is compact, full-dimensional, convex, and symmetric, with polynomial-bit rational radii.

For a rational query `z`, `Tz` has polynomial bit length. The ambient strong oracle either certifies membership or returns an inequality `h^T e<=b` valid for `K` and strictly violated at `Tz`. Multiplication by `T` gives an exact separating inequality for the effective body. Its normal cannot vanish: validity at zero implies `b>=0`, whereas strict violation would require `0>b` if `h^T T=0`. Output bits stay polynomial by the assumed oracle bound and rational matrix arithmetic.

The polynomial runtime is understood relative to a uniform polynomial-time oracle implementation, or the usual polynomial oracle-cost model with its stated output-bit bound. It is not a claim that arbitrary executable code describing a body can be analyzed or run in polynomial time solely from its source-code length.

## 3. Primary rounding theorem and rational centering

The primary author-hosted [Dadush–Peikert–Vempala paper](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf), Theorem B.5, PDF p.39, explicitly assumes strong separation for a circumscribed body and returns a rational positive definite metric matrix. It gives an outer translated ellipsoid and either a small-volume certificate or an inner translated copy scaled by `1/((d+1)sqrt(d))`. Definition (2.5) and its following paragraph, PDF p.6, confirm the convention `E(A)={z:z^T A z<=1}`. These are the exact source statements needed here; the unrelated randomized M-ellipsoid algorithm in the same paper is not being invoked.

Let `r` be the effective inner radius. The cube of half-width `r/d` lies in the radius-`r` Euclidean ball and has volume `(2r/d)^d`. This is strictly greater than `eta=min{1/2,(r/d)^d/2}`. Since an outer ellipsoid has at least the body's volume, the small-volume alternative is impossible. Computing this rational threshold requires only polynomial bit length: exponentiation multiplies the radius encoding length by `d`. Capping by one half avoids irrelevant logarithmic-parameter conventions for large radii.

Write the resulting centered ellipsoid as `E` and its translation as `t`. The inner inclusion and symmetry give both `t+E/beta` and `-t+E/beta` inside the body. Averaging proves `E/beta` is inside. For an arbitrary body point `x`, the outer inclusion at `x` and `-x` puts `x-t` and `x+t` in `E`; their average puts `x` in `E`. Hence centering loses **no extra factor**.

With `beta=(d+1)sqrt(d)`, the smaller ellipsoid has metric `W=beta^2 A=d(d+1)^2 A`. This multiplication, not inversion, is the correct metric transformation when shrinking a metric ellipsoid. The matrix is rational positive definite with polynomial encoding length. The center and any matrix square root need not be represented in the eventual formulation.

## 4. Covariance scaling and inequality directions

For a sandwich `E_0 subset K_eff subset alpha E_0`, enlarging the allowed error body can only lower the minimum integer count. Thus

```
p_conv(g,alpha E_0) <= p_conv(g,K_eff).
```

The imported ellipsoidal lower bound therefore gives `Phi(alpha)-A_n<=p_conv(f,K)`. This is the required direction; the benchmark for the smaller ellipsoid alone would not yield the comparison.

The covariance energy is homogeneous of degree two. If `P` is feasible at tolerance `alpha>=1`, then `P/alpha` still satisfies `0<=P/alpha<=I` and its energy is at most one. Its determinant is divided by `alpha^n`. Hence

```
D(1) >= D(alpha)/alpha^n,
Phi(1) <= Phi(alpha)+(n/2)log_2(alpha).
```

The ellipsoidal construction applied at tolerance one returns a rational MILP whose errors lie in the smaller body `E_0`, and hence in `K_eff`. The affine embedding preserves that validity for `K`. Combining the imported upper bound with the preceding lower bound gives precisely the claimed additive terms. An irrational value of `alpha` causes no computational issue: it is used only in this comparison proof, while the construction receives rational `W` and tolerance one.

## 5. Dimension and bit-complexity conclusion

The imported constants `A_n` and `B_n`, together with the rational-construction loss, are `O(n log(n+1))`. The rounding contribution has size

```
(n/2)log_2((d+1)sqrt(d)) = O(n log(n+1))
```

because `1<=d<=n(n+1)/2`. This includes `d=1`, where the factor is two. Large anisotropy changes the effective radii and the metric's coefficient bits, but not this dimension-only additive estimate against the same problem's optimum.

All subsequent construction inputs have polynomial rational encoding length, and the reviewed correlated-budget algorithm handles the rational positive definite matrix directly. Appending the original output equations adds only polynomially many rational rows and continuous variables. Consequently both the algorithm and its explicit MILP output have polynomial size in the full input and oracle model.

The number of ambient outputs still enters matrix dimensions, oracle query costs, and output size. The result removes it only from the **additive integer-count overhead**. Arbitrary nonsymmetric errors, missing radius data, and weak-oracle-only models are not proved by this argument. If only the effective section is bounded and has its own strong oracle and known radii, the same proof applies directly to that section; no assertion about boundedness in irrelevant output directions is necessary.

This review verifies the reduction and its imported-theorem hypotheses. It does not implement ellipsoid rounding or the full MILP-construction algorithm, and does not establish literature priority for the resulting norm extension.
