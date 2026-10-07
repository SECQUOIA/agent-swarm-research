# Independent review of the sparse, unbounded global point theorem

Date: 2026-10-03. Verdict: **accept under the stated global-convexity
and explicit-representation promises**. No mathematical repair is
required by this review.

This review read the complete saved
[main theorem](../../global-point/theorem.md) and
[sparse coefficient extension](../../global-point/sparse-coefficient-degree-extension.md).
It independently reconstructed the radius, error-bound, selector, and
bit-complexity arguments after auditing the historical bounded theorem.
The reviewer did not author these new proofs. This is internal research
review and does not establish publication priority.

## Conclusions by claim

| Claim | Verdict |
| --- | --- |
| Rational decision and certificate of unboundedness below | Accept; the Farkas polarity and objective-descent signs are correct. |
| Attainment and a computable radius for the minimum-norm optimizer | Accept; bounded representatives are proved before attainment is asserted. |
| Effective error bound on the full unbounded polyhedron | Accept; the Bregman argument requires a bound only on the chosen optimizer. |
| Sparse explicit polynomial, with numerical degree charged | Accept; no tensor grid or expanded affine substitution is performed. |
| One fixed minimum-norm optimizer across all precisions | Accept; the enlarged regularization denominator handles projection onto an unbounded optimizer set. |
| Feasible rational output and an objective enclosure | Accept; the sparse separation oracle and the existing exact-feasibility repair meet the bit model. |

## 1. Averaged curvature and the radius

For any base point `a` and displacement `d`, the Bregman polynomial

```text
h(t)=f(a+td)-f(a)-t grad f(a)'d
```

is nonnegative on the entire real line. On `[0,1]`, convexity implies
`0<=h(t)<=t h(1)<=h(1)`. The Lagrange numerator's second derivative
at zero is a sum of at most `D(D-1)` terms of absolute value at most
one. The denominator has absolute value at least `D^(-D)`. Summing
over `D+1` basis polynomials gives the stated conservative factor
`K_D=(D+1)D^(D+2)`. Thus the tangent quadratic inequality is valid
without assuming a positive definite pointwise Hessian.

Its integral over the unit cube is a rational quadratic minorant

```text
f(x)>=c+ell'x+x'Mx/K_D.
```

Every entry of `M`, `ell`, and `c` is computable by sparse
differentiation and monomial integration. Multiplication by a coordinate
in the displayed formulas only shifts an exponent. It does not require
a dense polynomial expansion. There are polynomially many resulting
terms, and denominator products have polynomial length in the input and
the numerical degree.

For `d in ker M`, the continuous nonnegative integrand
`d'Hess f(a)d` has zero integral, hence vanishes on the cube.
Polynomial identity and positive semidefiniteness give
`Hess f(a)d=0` everywhere. The converse is immediate. Therefore the
kernel is exactly the common Hessian kernel, not merely a sampled
approximation. The rational orthogonal projector `Pi` and
`w=-(Id-Pi)grad f(0)` satisfy

```text
f(x)=f(Pi x)-w'x,
ell=Pi ell-w.
```

The nonzero-eigenvalue product of the integer PSD matrix `Q_M M` is
the sum of its maximal-rank principal minors and is a positive integer.
Bounding all other eigenvalues by `n C_M` proves the displayed lower
curvature constant on `range M`. The rank-zero branch also works: both
sides of the quadratic bound vanish, and no positive eigenvalue is
silently assumed.

The polar-cone test

```text
w=B'lambda+Mz, lambda>=0
```

has the correct sign for the recession cone `{d:Bd<=0}`. Its failure
is equivalent to a direction with `Bd<=0`, `Md=0`, and `w'd>0`.
Normalize to `w'd=1`; then `f(a+td)=f(a)-t`. Conversely a feasible
certificate gives, on `P`,

```text
f(x)>=beta-A ||Pi x||+rho ||Pi x||^2.
```

The explicit `T` bounds `||Pi x||` on the reference sublevel
`f(x)<=F`. The bounds on `w'x` from both sides are valid and essential.
In particular the lower bound follows from

```text
w'x=f(Pi x)-f(x)
    >=f(0)-||grad f(0)||_1 T-F.
```

A one-sided constraint bound alone would not control `|w'x|`; the
proof does not make that error.

Stacking `M` and `w'` gives equal-value slices. In each slice, the
integer-row Hoffman bound applied to the fixed feasible reference point
`a` gives a representative of norm strictly below the displayed `R`.
The estimate `||My||_1<=n^2 m_0 T` suffices, so the claimed `Y` bounds
the complete equality right-hand side. A displacement in the slice is
in `ker M` and orthogonal to `w`; the decomposition above proves exact
equality of objective values.

This argument applies to every point of the nonempty reference
sublevel, whether or not an optimum is already known to exist. A
minimizing sequence therefore has bounded equally good representatives.
Compactness and continuity prove attainment. The minimum-norm optimizer
then exists and has norm at most `R`. There is no circular use of an
attaining optimizer in constructing the radius.

## 2. Sparse coefficients and the global error bound

The coefficient matrix of `grad f(z)'d` has at most `n` times the
number of input monomials in rows. Its kernel is exactly the global
translation-invariance space of `f`. Unlike the historical
multivariate sample-gradient construction, it does not have a
fixed-degree-dependent row count.

The tensor interpolation argument bounds a coefficient by
`B_(D-1)^n` times the polynomial's supremum on the unit cube.
This is a proof inequality. The algorithm computes only the scalar
integer `B_(D-1)^n`, whose length is `O(nD log(D+1))`; it never
constructs the exponentially many tensor-grid points.

Fix the minimum-norm optimizer `p`, whose norm has now been bounded.
For arbitrary feasible `x`, the Bregman segment from `p` to `x`
has gap at most `E`. The midpoint/Jensen estimate evaluates the
auxiliary polynomial at `2c-p`, with `c` in the unit cube. Thus its
coefficient majorant uses only the radius of `p`. No bound on the norm
of `x`, on the segment displacement, or on all other optimizers is
needed. The univariate extrapolation step remains valid for an
arbitrarily long displacement because its parameter interval is
`[0,1]` along that displacement.

Coefficient extraction then bounds the known rational row residual by
`constant * E^(1/D)`. The zero-gap argument establishes the exact
optimizer slice. The same right-hand-side-uniform Hoffman lemma works
on unbounded polyhedra, so this proves the stated error bound for all
`x in P` with gap at most one. It is stronger than a box-only bound,
and that stronger assertion is supported by the proof.

## 3. The fixed selector on an unbounded optimizer set

The regularized objective on the original polyhedron is coercive
because `f` is bounded below. Its unique minimizer `x_tau` satisfies
`||x_tau||<=||p||<=R`. Therefore the rational box intersection used
by the algorithm contains both `p` and `x_tau` and has the correct
unregularized and regularized optimal values.

The nearest point `s` to `x_tau` in the original optimizer set need
not lie in that box. The proof correctly handles this rather than
reusing the old bounded-domain norm estimate. With
`e=||s-x_tau||`, the known point `p` gives `e<=2R`, whence

```text
gap(x_tau)<=tau (||s||^2-||x_tau||^2)
          <=tau e(2||x_tau||+e)<=4R tau e.
```

Combining this with the global error bound and the stated denominator
`4*8^(D-1)` in `tau` gives `e<=epsilon^2/(8R)`. Projection
optimality `p'(s-p)>=0`, together with `||x_tau||<=||p||`, then
gives `||x_tau-p||<=epsilon/2`. This establishes the declared
selector rather than just distance to some optimizer.

The strong-convexity solve error is the other `epsilon/2`. In
particular `tau R^2<=1` for all the allowed `D>=2`, `R>=1`,
`Gamma>=1`, and `epsilon<=1`, so the unit-gap hypothesis is used
within its valid range. All norm penalties are in original coordinates.

## 4. Bit complexity and verification limits

All radius arithmetic, linear programs, denominator products, sparse
derivatives, and coefficient majorants have polynomial bit cost in
`I,D`. After affine-hull reduction, exact value and gradient queries
evaluate the rational affine map first and retain the original sparse
polynomial. The query value can have length proportional to the
numerical degree times the query length; that is within the stated
bound. A theorem polynomial only in binary exponent length would not
follow, and is not claimed.

The relative inner and outer radii and exact-feasibility repair are
pure rational-polyhedral operations. Bounds on reduced gradients follow
from the chain rule and a rational matrix norm; they do not require
expanding the substituted polynomial. The tangent certificate can be
computed in original coordinates. Its transfer from the constructed
box to the original polyhedron uses the proved radius reduction. The
result is conditional on the global-convexity promise, as stated.

The required regularization and objective accuracy have
`poly(I,D,q)` binary length. No step charges numerical work proportional
to `1/tau`, invokes a real-algebraic fallback, enumerates constraint
active sets, or constructs an interpolation grid.

The review consisted of complete-file reading and the independent
analytic reconstruction above. It did not duplicate the author's
fixture diagnostics or claim to have implemented a general ellipsoid
solver. Targeted Markdown checks of this review's local links, paired
fences, and whitespace are recorded in the review-directory check.
No project-wide verification or CI inspection was performed.

Integration should retain the credited prior results on small minimizer
bounds, objective-gap approximation, and unboundedness detection. This
audit establishes correctness of the displayed point and constant
construction; it does not determine whether those contributions are
novel relative to all prior work.
