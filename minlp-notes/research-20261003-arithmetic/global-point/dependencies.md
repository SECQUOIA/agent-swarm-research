# Dependencies and claim boundaries

Date: 2026-10-03.

The [main theorem](theorem.md) has three components with different
relationships to prior work.

| Component | Status and dependency |
| --- | --- |
| Finite minimum is attained at a point of polynomial logarithmic norm; unboundedness detection; objective-gap approximation | Already established by Slot, Steurer, and Wiedmer, *Hesse's Redemption*, Theorem 1.1 and Corollary 1.2. Sections 2--3 give a self-contained, explicitly computable radius construction for use in the point theorem. |
| Effective error bound with exponent `1/D` and polynomial-bit constant | Extends the repo's bounded fixed-degree Bregman/Hoffman proof by using sparse gradient coefficient rows and a conceptual interpolation inequality. No gradient grid is constructed. |
| Approximation of the same minimum-norm optimizer at every requested precision | Follows from the effective error bound and a quantitative quadratic-regularization schedule. It is stronger in output contract than objective-gap approximation. |

The elementary ingredients used without a new implementation are rational
linear programming and its Farkas/duality certificates, rational linear
algebra with polynomial bit bounds, univariate interpolation, projection
onto nonempty closed convex sets, and the convex ellipsoid/value interface.
The integer-minor Hoffman estimate is proved in the linked original note
and checked again in the independent review.

The averaged quadratic lower bound is computed from sparse coefficients by
exact integration over the unit cube. The proof uses no Hessian determinant
identity test, no computation of irrational eigenvectors, and no assumption
that the objective is strongly convex. The estimate from the proof of
Ahmadi, Chaudhry, and Zhang's Lemma 5 is a conceptual antecedent; Section 2
provides its own looser interpolation proof and does not depend on that
source's constant.

The value interface is the existing [convex-polytope interface](../../research-20261002/new-direction/convex-polytope-value-interface.md#1-convex-value-interface),
with sparse evaluation retained through affine-hull maps. Its exact
real-algebraic fallback is not used. The proof is an algorithmic complexity
result; no generic ellipsoid implementation has been added in this folder.

The global-convexity premise is a promise or requires a separately charged
certificate. The theorem is uniform in the numerical degree, so its
input-polynomial interpretation requires unary or polynomially bounded
degree. Convexity only on the feasible domain, succinct arithmetic circuits,
and exact arithmetic output are outside its scope.

The [source audit](../literature/source-audit.md) compares the claims to the
primary literature and records corrections needed when reading the source
formulas. The present radius proof does not rely on the disputed formulas.
Neither a mathematical review nor these diagnostics establishes publication
priority.
