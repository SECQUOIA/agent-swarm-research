# Independent arithmetic review of the boundary core-flow theorem

Date: 2026-10-02.

**Verdict: passes the requested arithmetic and output audit. No substantive
blocker found.** This review checks the actual completed
[boundary theorem](../new-direction/smoothed-boundary-core-flow.md),
especially Sections 5–7. It independently checks the argument in the
[focused margin review](flow-boundary-margin-review.md), rather than
treating that review's approval as evidence. The geometric certificate and
probability calculations have a
[separate review](smoothed-boundary-core-flow-adversary.md).

## Quantitative value margin

For a nonzero polynomial `p`, the set `K_delta` is compact whenever it is
nonempty. Positive distance from its zero set excludes every zero of `p`,
so its attained minimum absolute value `m` is positive. The quantified
formula in Section 5 defines exactly `(m^2,infinity)`: its universal
condition is precisely membership in `K_delta`, and the strict scalar
inequality includes every threshold above the attained minimum and excludes
the endpoint. If the zero set is empty, the universal condition is vacuous.
If `K_delta` is empty, the claimed lower bound on that set is vacuous.

The formula has two quantified blocks of size at most `k`, one free scalar,
`O(k)` atoms, and degree at most `max(2d,2)`. A degree-`d` polynomial in
`k` variables has at most `binom(k+d,d)` coefficients. Clearing their
denominators, forming `p^2`, and clearing the denominator of `delta^2`
therefore gives integer coefficient length bounded by

`f_d(k) (H_0 + bits(delta) + 1)`.

Positive denominator clearing preserves the inequalities. In particular,
this operation does not put the coefficient length inside an exponent
depending on `k`.

The fixed-block elimination interface recorded in
[the exact fallback proof, Section 4](../new-direction/polynomial-exact-fallback.md#4-the-primary-theorem-separates-coefficient-height-from-dimension)
then supplies output degree and format bounded by
`(k+1)^(O_d(k^2))`, and integer coefficient length bounded by that
parameter factor times a fixed polynomial in the input coefficient length.
This is the relevant height assertion; an arithmetic-operation bound alone
would not suffice.

After removing constant and identically zero output atoms, the finite
boundary point `m^2` must be a zero of a remaining atom. Otherwise every
atom sign would be locally constant there. Remove any power of the scalar
variable from that atom. Its integer constant coefficient is now nonzero
and has magnitude at least one. If its coefficient bit lengths are at most
`B_0`, reciprocal Cauchy gives

`m^2 >= 1/(1+2^B_0) >= 2^(-(B_0+1))`.

The same dyadic number is a conservative lower bound for `m`. Nonzero
constant polynomials and zero-dimensional faces admit the stated direct
rational bound. Applying the lemma with `delta/2` changes its input length
by only a constant. A single uniform upper bound on format and coefficient
height consequently supplies `mu_0` for every chart without constructing
any chart list or running elimination on sampled coefficients.

For clarity, `B_0` here is the bit bound for **integer output coefficients
after denominator clearing**. The linked margin proof states this explicitly.
Adding those words to the theorem would make the reciprocal Cauchy step
self-contained; it does not change the estimate.

## Uniformity and the order of the precision choices

The chart coefficient bound is independent of the sampled noise. Native
labels have binary length bounded by the base input, polynomial degree is
fixed, and each potential is a sum along a path of at most `s` original
network arcs. Thus every chart, including one selected after sampling,
has the same base coefficient-height bound. The logarithms of the label,
tree, and marginal counts in Section 3 are polynomial in `I`.

The image elimination degree depends on its format, not on sampled
coefficient heights. Its stated parameter factor has polynomial logarithm
in `I`, since `k<=I` in the explicit input model. Therefore `log D`,
`log C_tot`, and the corresponding growth-section bound have the claimed
base polynomial lengths. This does not assert that their numerical values
are polynomial.

The derivative bounds `H,K`, curvature bound, noise scale, and fallback
factor have base encodings of polynomial length. Consequently `rho`,
`g_0`, `A_0`, `delta`, and `tau` also have polynomial base length. The
margin lemma then gives

`bits(mu_0), J, log M <= f_d(k) poly_d(I)`.

The order matters: `delta` is selected before the margin bound, the margin
bound determines `J`, and only then is `M` selected. No occurrence of
sampled coefficient height feeds back into these definitions. Constructing
the ordinary binary denominator of the dyadic `mu_0`, or of the grid law,
costs time proportional to its allowed parameter-dependent length. A
succinct exponent encoding is neither needed nor being substituted for
that cost.

## Expected bit work and proof records

Through level `J`, dyadic query coordinates have `O(J)` bits per coordinate,
and noise coefficients have `O(I+log M)` bits. Fixed-degree substitution,
potential construction, and derivative evaluation therefore produce
`f_d(k) poly_d(I)`-length data. Native integer flows themselves retain their
base binary bounds.

The exact convex-flow interface has a fixed polynomial input exponent.
The polynomial box solver, including exact sign and value comparisons,
has a fixed polynomial coefficient-bit exponent as well. Substituting
`I+J+log M <= f_d(k) poly_d(I)` into either bound preserves the form
`f_d(k) poly_d(I)`. The same holds after multiplying by the number of
levels, face attempts, and original-arc tests. In particular, the added
sampling precision is charged in every affected computation.

Multiplying those costs by the expected grid count and its generation
factor gives the stated bound (2). Its grid estimate applies through the
cutoff because `M>=2^J` implies `M h_j>=1` for every queried level.

For the exceptional branch, keep the two factors separate:

`Pr(fallback) * fallback work`

`<= (1/(4B)) * B (I+log M+1)^e_d`.

The result is still `f_d(k) poly_d(I)` because `e_d` is fixed. The larger
`log M` is not being cancelled by the failure probability; it remains in
the polynomial factor and is explicitly allowed. The same calculation
applies to the proof record. Ordinary successful calls and exact algebraic
computations can record their verification data or computation traces
within their bit-work budgets.

## Output and refinement

The fallback streams through labels and retains one winning flow and one
small-core representation. Comparisons of two candidate values use their
univariate polynomials; no cumulative compositum of the examined labels is
needed. The final objective slice has coefficient length polynomial in
`I+log M`, independently of how many labels were inspected. Re-isolating
the selected root in its own defining polynomial, if needed, removes any
unnecessary comparison precision from the final representation.

Thus the all-draw output length is `f_d(k) poly_d(I)`, and refinement to
`t` bits is `f_d(k) poly_d(I+t)`. These conclusions use the common-root
output contract. They do not require an expanded global minimal polynomial
or retaining the losing candidates. The rational quadratic specialization
is consistent with stationary-face enumeration and rational linear algebra.

## Verification scope

This was a fresh document and mathematical audit. It read the boundary
theorem, the focused margin proof, and the applicable local QE, exact-flow,
fallback, and algebraic-output interfaces. No new delegation, external
research, executable tests, project-wide verification, or CI inspection
was performed.

Targeted document check:

```sh
git diff --no-index --check /dev/null research-20261002/reviews/boundary-core-flow-bit-adversary.md
```

The check reported no whitespace errors; status `1` denotes the new-file
comparison.
