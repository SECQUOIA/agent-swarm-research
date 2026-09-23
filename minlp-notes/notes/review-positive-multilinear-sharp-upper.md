# Independent audit: sharp positive multilinear gap growth

Date: 2026-09-04. Reviewed file:
`results/positive-multilinear-sharp-degree-growth.md`, including the final written
leading-constant refinement, the dimension statement, and the nonnegative-box extension.

**Outcome:** the harmonic coupling proof, the explicit finite-degree bound, and the
leading-constant-one refinement are mathematically correct. Combined with the independently
audited dyadic lower bound, they establish

```
R(d) ~ ln d / ln ln d,
C(n) ~ ln n / ln ln n.
```

Here `R(d)` is the supremum over dimensions, positive multilinear polynomials of degree
at most `d`, and points with positive hull gap; `C(n)` is the analogous supremum with
at most `n` variables. The upper bounds also cover the original term-by-term relaxation
on arbitrary finite nonnegative boxes. No unresolved mathematical issue was found.

This is an independent mathematical agent audit. It is not journal peer review, formal
proof verification, or evidence that every possible prior source has been excluded.
Novelty screening is a separate task.

## 1. Common deficiency formulation and easy classes

The exact identity already checked in the preceding audit is

```
T_e=min(u_e,S_e),
H=max_(E X=x) Σ_e a_e E[X_anchor−∏_(i∈e)X_i],
```

where the anchor attains the monomial's minimum mean `u_e` and
`S_e=Σ_(j≠anchor)(1−x_j)`. Each deficiency is pointwise nonnegative. The full
concave envelope equals the sum of positive monomial concave envelopes because one
comonotone vertex distribution attains all of them simultaneously. The full convex
envelope is the minimum expected polynomial value over vertex distributions with the
specified means. Thus the direction of the optimization identity is correct.

Coordinates are classified globally as low when `x_i≤1/2`, high otherwise. Under
independence, monomials with at least two low coordinates receive deficiency at least
`T_e/2`; all-high monomials receive at least `cT_e/2`, where `c=1−exp(−1)`.
The only remaining class has one low anchor and all other coordinates high. These
three classes partition all nonlinear monomials, including ties at `1/2`. Affine
terms contribute no gap and can be removed. Nonnegative coefficients are required
when summing the per-term guarantees.

## 2. Harmonic coupling: exact marginal normalization

Fix `L≥16`, let `M=exp(L−1)≥d`, and give all coordinates the same uniform
variable `U∈(0,1)`. Low coordinates succeed on `[0,x_i]`. For a high coordinate
with failure mean `p∈(0,1/2)`, put

```
h_p=min(Mp,1),
a_p=1+ln(h_p/p),
q_p(t)=min(1,p/t) 1[t≤h_p] / a_p.
```

Since `M≥1`, `p≤h_p≤1`, so `1≤a_p≤L` and `0≤q_p(t)≤1`.
Direct integration, splitting at `p`, gives

```
∫₀¹ q_p(t) dt = [p+p ln(h_p/p)]/a_p = p.
```

This also handles the saturation case `h_p=1`. For `p=0` the coordinate is fixed
at one; no logarithm or division involving zero is used. The value at `t=0` is
irrelevant because the uniform variable has no atom there.

Conditional on `U`, all high-coordinate failures are independent Bernoulli variables
with these probabilities. These coins are assigned once per coordinate for the entire
polynomial. Consequently the construction is one globally feasible distribution,
including when different monomials share variables. It is not a family of incompatible
monomialwise choices. Neither the coefficients nor a selected anchor for a particular
monomial enters the distribution's definition.

The threshold coupling also uses the same low success events and makes a high
coordinate fail on `[0,p]`. Its marginal failure probability is exactly `p`. For a
unique-low monomial its deficiency is exactly `min(u,p_max)`.

## 3. The active-mass estimate

Consider a unique-low monomial with anchor mean `u≤1/2`, failure means
`p_1,…,p_r`, `r≤d−1`, `S=Σp_j`, and `T=min(u,S)>0`.
On any integration interval with `p_max<t<1`, a leaf is active precisely when
`p_j≥t/M`. Each inactive leaf contributes less than `t/M`, so

```
Σ_(inactive) p_j ≤ r t/M ≤ t,
Σ_(active) p_j ≥ S−t.
```

This estimate uses `M≥d`, not a bound on the total number of variables in the
polynomial. On the active set, all `p_j<t`, hence
`q_j(t)=p_j/(a_j t)≥p_j/(Lt)`. Therefore

```
λ(t):=Σ_j q_j(t) ≥ (S−t)/(Lt).
```

Conditional independence yields a union probability at least
`1−exp(−λ(t))`. The proof correctly applies lower bounds to a smaller deterministic
quantity `z(t)≤λ(t)`, using monotonicity of `1−exp(−z)`. It does not incorrectly
assume that the actual `λ(t)` is small.

## 4. Explicit bound with a uniform mixture

For `L=max(16,1+ln d)`, split the unique-low case at `p_max=T/√L`.

If the maximum is at least that threshold, threshold rounding gives
`min(u,p_max)≥T/√L≥T ln L/L`, since `ln L≤√L` for `L≥1`.
If it is smaller, integrate on `[T/√L,T/2]`. This interval lies inside the low
anchor's success event and inside `(0,1)`. All leaf failure means are below its
lower endpoint. The active mass is at least `T/2`, giving
`z(t)=T/(2Lt)≤1/(2√L)<1`. Hence the conditional union probability is at least
`cT/(2Lt)`. Its integral is

```
cT[ln L−2ln2]/(4L) ≥ cT ln L/(8L),
```

where the last inequality is equivalent to `L≥16`.

The easy classes have independent deficiency at least `cT/2`, which exceeds this
common guarantee. The uniform mixture of the independent, threshold, and harmonic
distributions thus gives

```
H ≥ c ln L /(24L) · T_total.
```

All other contributions are nonnegative. The number of distributions is three,
independent of degree or dimension. This proves the displayed bound for every
`d≥2`, including small degrees through the explicit lower cutoff on `L`.

## 5. Leading constant one

I separately checked the final written refinement with

```
L=max(exp(6),1+ln d),     M=exp(L−1),
b=ln L,                 a=L/b²,         β=1/b,
h=[(1−1/b)(1−1/(2b²))(b−3ln b)]/L.
```

Here `b≥6`, `a>1`, and `h>0`. The quantity `b−3ln b` is positive at six and
increasing thereafter. Thus the proposed integration interval is nonempty:

```
(T/a, βT),     ln(βa)=b−3ln b>0.
```

If `p_max≥T/a`, threshold rounding gives deficiency at least `T/a`. Otherwise,
all leaf means are below every point of that interval. It lies inside `(0,u)`
because `β<1` and `T≤u`. The active-mass estimate now gives

```
λ(t) ≥ z(t):=(1−β)T/(Lt),     0≤z(t)≤a/L=1/b².
```

Although the actual `λ(t)` may be larger, its union probability is at least
`1−exp(−z(t))`. The elementary bound
`1−exp(−z)≥z−z²/2` therefore supplies

```
P(any leaf fails | U=t)
 ≥ (1−1/(2b²))(1−β)T/(Lt).
```

Integration gives exactly `hT`, including the factor `b−3ln b` from the ratio
of the endpoints. No asymptotic approximation is used in this finite inequality.

Let `Z=1/h+a+2/c` and assign probabilities

```
harmonic:    (1/h)/Z,
threshold:   a/Z,
independent: (2/c)/Z.
```

These are positive and sum to one. Each easy monomial receives at least `T/Z`
from independence. Each other monomial receives at least `T/Z` from either the
threshold or harmonic component according to its case. The case analysis selects
which existing guarantee to use; it does not alter the common distribution. Summing
proves `R(d)≤Z`.

As `d→∞`, `L~ln d`, `b~ln ln d`, and

```
h~b/L,     a=L/b²=o(L/b),     2/c=o(L/b).
```

Thus `Z~ln d/ln ln d`. The inverse-efficiency mixture is essential for the stated
leading constant; the uniform mixture only gave a fixed multiplicative constant.
I found no missing factor in the refined weights or in the integral.

## 6. Lower bound interpolation and dimension growth

The audited dyadic example indexed by `ell` has degree
`d_ell=2^(ell−1)+1` and exact gap ratio asymptotic to
`ell/log₂ ell ~ ln d_ell/ln ln d_ell`. Choosing the largest admissible example
for an arbitrary degree allowance `d` changes degree by a bounded factor.
Therefore its logarithm differs from `ln d` by `O(1)`, and the lower ratio remains
asymptotic to `ln d/ln ln d`, with leading constant one. Together with the upper
bound this proves the claimed equivalence for all growing degree allowances, not
merely along a subsequence.

For the dimension supremum, degree is at most dimension, giving the upper bound.
The example dimensions are `n_ell=2^ell+ell`. Choose the largest one not exceeding
`n` and add unused variables; this preserves both gaps. Again the dimensions differ
by at most a bounded factor, yielding the stated equivalence for `C(n)`.

## 7. Finite nonnegative boxes and boundary cases

The nonnegative-box argument is valid for these sharper constants exactly as in the
preceding audit. First remove fixed coordinates. Under the affine map to a unit cube,
every original positive monomial expands as a sum of positive monomials of no larger
degree. Its original exact term gap is at most the sum of the expanded term gaps:
the sum of concave envelopes is a concave majorant of the sum, and the sum of convex
envelopes is a convex minorant. Summing gives

```
T_original ≤ T_expanded,
H_original = H_expanded.
```

Apply the unit-box bound to the expanded polynomial. This proves the same upper
bound for the original, unexpanded relaxation. Duplicate positive terms can be
combined and affine terms removed without changing the gap comparison. The unit-box
examples supply the same lower bounds within this larger class.

The proof also covers the following boundaries:

- An anchor of mean zero has `T=0`, so no positive integration endpoint is required.
- If every leaf failure mean is zero, again `T=0`.
- A high coordinate of mean one is fixed explicitly.
- Ties at `1/2` are classified as low consistently in all three distributions.
- Saturated harmonic supports at one retain the exact normalization formula.
- Degree two is covered by the finite `L` cutoff; the resulting bound is valid but
  intentionally does not optimize the known bilinear constant.
- If the hull gap is zero, the proved inequality forces the term gap to be zero.
  The ratio supremum appropriately excludes division by zero.

The theorem is about feasible distributions and exact relaxation gaps. It does not
assert efficient evaluation of the exact convex envelope. No additional complexity
claim is needed for the mathematical result.
