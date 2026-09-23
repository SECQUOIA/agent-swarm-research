# Independent audit: general symmetric output error bodies

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS for the stated strong-separation oracle theorem.** I independently reviewed [the general norm precision candidate](quadratic-general-norm-output-precision.md). The reduction to the nonlinear output image, classical rational ellipsoid rounding, and transfer of the finite covariance bounds establish the claimed `p_conv+O(n log(n+1))` polynomial rational construction. An initially broader aside about weak separation is not needed by this proof; the cited rounding theorem explicitly assumes strong separation.

## Nonlinear image reduction and oracle model

Write the rational map as `f=a+C u`, with `u` listing the quadratic monomials, and factor `C=T B` using a rational basis for its column image. Rational elimination gives polynomial encoding lengths. The resulting dimension `d=rank C` is at most `n(n+1)/2`, independently of the number of outputs. If `d=0`, the exact affine graph is an LP and needs no rounding or integer variables.

The equality of integer minima before and after reduction is correct for both binary LP lifts and arbitrary convex lifts. A formulation for the reduced graph gives the original one by adjoining `w=a(x)+Tz`. Conversely, intersect any original formulation with these affine equations and introduce `z`. This retains every exact graph point, removes only permitted approximation points, and adds no integer coordinates. The reduced error lies in `K_eff={z:Tz in K}` precisely when its embedded original error lies in `K`. The argument does not assume that all errors of the original formulation already lie in the nonlinear image.

The proposed rational upper bounds on `||T||` and its left inverse give the stated inner radius `r_0/c_T` and outer radius `R_0 c_L`. Both radii have polynomial rational encoding. A strong separating inequality for `Tz` pulls back exactly. Its pulled-back normal cannot vanish: a vanishing normal together with the violated inequality would also exclude the origin, which belongs to the body. Query and returned-inequality lengths remain polynomial under rational multiplication.

## Primary rounding theorem checked

I read Definition B.2 and Theorem B.5 in the primary [Dadush, Peikert and Vempala paper](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf). The source uses a rational strong-separation oracle with polynomial output length and a known circumscribing ball. Its rounding theorem returns a rational positive definite ellipsoid matrix, an outer translated covering, and either a small-volume alternative or an inner translate scaled by `1/((d+1)sqrt(d))`. These are the exact features used by the candidate.

The rational threshold `eta=(r/d)^d/2` has polynomial encoding length. The cube `[-r/d,r/d]^d` lies in the known inner ball and has volume `(2r/d)^d>eta`. Since the returned outer ellipsoid contains the body up to translation, its volume cannot be at most `eta`. Thus the inner-sandwich alternative necessarily holds.

Symmetry legitimately removes the unknown center from both inclusions. Averaging the inner translated ellipsoid and its negative gives the centered inner ellipsoid. Applying the outer inclusion to `x` and `-x`, then using ellipsoid symmetry, yields both `x-t` and `x+t` in the centered outer ellipsoid, so their average is `x`. Consequently `E_0 subset K_eff subset beta E_0`, where `beta=(d+1)sqrt(d)` and the rational matrix of `E_0` is `d(d+1)^2 A`. The irrational numerical value of `beta` and the potentially real center never enter the rational formulation coefficients.

## Transfer and final size

Larger permitted error bodies can only decrease the minimum integer count. Therefore `p_conv(g,beta E_0)<=p_conv(g,K_eff)` has the stated direction. The finite ellipsoidal lower bound at tolerance `beta` remains valid even though `beta` is not rational: it is used only in the proof, not as an algorithm input.

Covariance feasibility scales quadratically. Thus `P/beta` maps every covariance feasible at tolerance `beta` to one feasible at tolerance one, preserves the matrix cap, and multiplies its determinant by `beta^(-n)`. The benchmark increase is at most `(n/2)log2 beta`. Combining this with the reviewed constructive upper bound at tolerance one gives the displayed additive count.

Because `d<=n(n+1)/2`, `log beta=O(log(n+1))`. The final additive constant is universal and independent of the number of original outputs, the radius ratio, and the shape of the error body. Those data still affect the algorithm's polynomial running time and coefficient encoding. The reduced quadratic construction has at most polynomially many coordinates and rows, and adjoining the `m` output embedding equations preserves polynomial size. The final formulation does not need to encode the original body or invoke its oracle during optimization: its ellipsoidal error certificate implies containment in the original body.

## Scope of this audit

The proof directly establishes the ambient rational strong-separation model and the variant with a strong oracle directly on the full-dimensional effective section. A claim based only on weak separation would require a suitably quantified additional oracle-reduction or rounding result; Theorem B.5 by itself does not supply that claim. I asked the author to remove that unnecessary broader aside or justify it separately. No change to the main theorem, constants, or construction is needed.


Final scope correction checked: the author replaced the weak-oracle aside by a strong-separation oracle directly for the effective body. Both advertised input models now match the cited theorem. The complete revised candidate passes this audit.
