# Independent review of polynomial input and shell arithmetic

Date: 2026-10-02. Scope: full-draft review of
[nonlinear-shell-certificate.md](nonlinear-shell-certificate.md), focusing
on curvature verification, factor scopes, translated coefficient height,
and the trial-dependent inner radius. The parent review covers the
combined shell and core correctness argument. No tests, external searches,
or CI checks were run for this review.

**Conclusion.** The proposed parameter-dependent bit bound is supported
by the stated explicit fixed-degree model. No substantive issue was found
in these parts of the proof. The author applied two small clarifications requested by the parent:
include `L` and any supplied curvature-proof data in the input accounting,
and condition the norm substitution in equation (24) on a nonnegative
coefficient. The discovery argument already uses `sigma<=g/5`, where
that substitution is valid.

## 1. A verified curvature bound is part of the certificate

For higher-degree input, an arbitrary claimed global bound on
`partial_ii F` is not automatically easy to verify. The draft correctly
provides a concrete certificate format: expand the coordinate second
derivatives, bound each rational monomial over the real box, sum term
upper bounds, and check that `L` dominates the result. Collecting equal
monomials first can preserve cancellations but is not required for
soundness. Fixed total degree makes differentiation, interval arithmetic,
and the sizes of the resulting rational numbers polynomial in the
explicit input length.

The bound applies on the entire continuous box hull, including real
segments between lattice labels. That is sufficient for sequential
coordinate rounding. Verifying curvature only at lattice-feasible points
would not establish the chord inequality. The draft explicitly excludes
that weaker model.

The complexity parameter uses the value of `L` actually verified by
this process. A looser bound may worsen `L/g`; a sharper unsupported
number cannot be used instead. An alternative curvature certificate
must have its size and verification work included. The displayed
polynomial verification claim applies directly to the elementary
monomial format; an alternative verifier's additional cost cannot be
silently omitted.

## 2. Translation preserves width and polynomial height

Each factor is supplied as explicit rational monomials of fixed total
degree at most `d_0`, and its full scope lies in a supplied bag. This
is the correct width model for outer factor tables. Sparsity of the
Hessian only at the proposed point would not suffice.

A monomial `x^alpha` produces at most
`product_i(alpha_i+1)<=2^d_0` terms when translated by the proposed
point. Every descendant uses only variables in the original scope.
Substituting the fixed lattice displacements and keeping only degrees
at most two likewise introduces no new variables or pair interactions.
The Taylor quadratic may be kept as a sum of its translated local
factors and assigned to their original bags.

If `D_0` clears the original rational coefficients and proposed-point
coordinates, every translated coefficient has denominator dividing
`D_0^(d_0+1)`. Binomial coefficients and products of at most `d_0`
input quantities have polynomial bit length for fixed `d_0`.
Summing the absolute higher-degree coefficients factorwise therefore
gives a rational `M` of polynomial encoding length. Cancellation
between factors is unnecessary for the remainder estimate. Using an
overestimate of `M` costs shell levels logarithmically, rather than
changing the numerical parameter `L/g`.

These statements depend on explicit coefficient encoding. An unrestricted
arithmetic circuit can encode a constant with exponentially many bits
even at degree zero. A binary exponent also permits exponentially long
rational evaluations. The draft correctly excludes both models from
its explicit-table bit claim.

## 3. The shrinking radius does not create a precision circle

At trial `delta=2^(-r)`,

```
sigma=L 2^(-2r)/8,
rho=min{r_0,1,sigma/M}.
```

The quantities `r_0`, `D`, and `M` are computed once from the explicit
input and have polynomial bit length. Therefore `rho` and `sigma`
have `poly(I)+O(r)` bits, and

```
J+1=O(1+log(D/rho))=poly(I)+O(r).
```

The radii are computed directly from the current trial; they do not
depend on an unknown optimizer, a sampled denominator, or an output
reconstruction precision. Rebuilding the shells as `rho` decreases
is legitimate. It contributes a factor depending polynomially on
`I+r` to each trial's work.

It would be incorrect to claim that `J` remains polynomial in the
base input alone for all trials. A nonlinear instance may have a very
small positive growth constant. At the first successful trial, however,
the proved margin guarantee bounds `r` by
`O(1+log^+(L/g))`. Its effect is therefore charged to the stated
parameter, as the draft explicitly does.

## 4. Label denominators, local tables, and DP messages

At a fixed trial, all physical shell radii are `2^j rho` and share
the denominator of `rho`. Lattice labels are integer multiples of
input spacings with multipliers bounded by encoded domain-to-spacing
ratios; floors and ceilings create no new denominators. Continuous
labels are starting labels multiplied by powers of `1+2^(-r)`,
with at most `K` such multiplications. Original endpoint clips and
threshold labels are also rational with polynomially many bits.

Consequently one common label denominator has bit length
`poly(I)+O(r+rK)`. At fixed degree, evaluating a factor raises this
denominator to power at most `d_0` and multiplies it by a common
coefficient denominator. Unary corrections add only the rational
denominator of `sigma`; shell and core thresholds also use powers
of the same radius and the integer `n`. All local table entries
therefore have a shared denominator of polynomial bit length in
`I+r+K`.

Each finite message is a minimum of sums of assigned factor entries.
Their denominators do not multiply across bags. Factor evaluation and
comparison, the two-state OR operations, and message storage have
polynomial bit cost in those lengths. There is one shell index shared
by an entire DP evaluation, so the shell count multiplies the work;
it is not raised to the bag size.

The grid count remains
`K=O(delta^(-1) log(2n/delta))`. At first success,
`delta^(-1)<=max{2,sqrt(5L/(2g))}`. Combining the number of trials,
the `poly(I)+O(r)` shell count, and the `K^p` table bound gives
`f_(d_0)(p,max{1,L/g}) poly(I)` after absorbing powers of `log n`.
The input exponent is absolute for each fixed degree bound. This does
not assert a polynomial input-only bound on every generated number
when the conditioning parameter itself is unbounded.

## 5. Acceptance conventions and limits

Both outer and core checks are nonstrict. Thus the discovery threshold
`sigma<=g/5` includes equality. In equation (24), replacing
`(g-4sigma)||z||^2` by `(g-4sigma)rho^2` requires
`g-4sigma>=0`; the author now writes this condition explicitly.
It holds throughout the claimed discovery regime and
does not change the final theorem.

This is a certificate for a supplied rational point under positive
quadratic growth. It does not find a polynomial optimizer, establish
rationality of arbitrary optima, or guarantee termination at a unique
zero-growth minimum. The draft states those limits correctly.
