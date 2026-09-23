# Independent review of the higher-order spatial-cover lower bound

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-higher-sos-investigation.md`.

**Verdict: PASS.** The incidence-Gram decomposition, homogenization,
conditional moments, all truncated box-preordering inequalities, equality
degree constraints, and resulting cover bound are correct. A zero-weight
conditioning paragraph can be simplified, but it does not invalidate the
proof. Novelty is outside this correctness review.

## Incidence-Gram decomposition

For homogeneous squarefree monomials of degree `d`, an entry with
intersection size `ell` is `(t)_(2d-ell)/(s)_(2d-ell)`. The claimed sum of
incidence-Gram entries is

```
1/(s)_(2d) * sum_{j=0}^ell C(ell,j)(t)_(2d-j)(s-t)_j.
```

Factoring out `(t)_(2d-ell)` leaves

```
sum_{j=0}^ell C(ell,j)(t-2d+ell)_(ell-j)(s-t)_j
= (s-2d+ell)_ell.
```

This is precisely the missing denominator factor. The calculation is a
polynomial identity, so it remains valid when the factored expression is
zero; no division by that expression is required. Each incidence matrix
`P_j` is a Gram matrix of the vectors indexed by contained `j`-subsets.
Every coefficient is nonnegative because `(t)_(2d-j)` has no negative
factors when `t>=2d-1`, and `(s-t)_j` has none when `s-t>=2d-1`.
The denominator `(s)_(2d)` is positive for the permitted integer `s>=2d`.

Independent symbolic verification with SymPy expanded both sides of the
entry identity for every `ell=0,...,d` and every `d=1,...,6`; all 27
identities passed exactly as polynomials in `s,t`. This is supplementary
to the preceding algebraic proof.

## Homogenization and equality degrees

For a squarefree set `S` of size `a<=d`, define

```
P_a(z) = (z-a)_(d-a)/(d-a)!.
```

In the Boolean quotient,

```
sum_{T containing S, |T|=d} u_T = u_S P_a(sum_i u_i).
```

The denominator `P_a(t)=C(t-a,d-a)` is strictly positive under Lemma A's
hypotheses, including `d=1,t=1`. If `a=d` the homogenization is already
the original monomial. Otherwise `P_a(z)-P_a(t)` is divisible by `z-t`
with quotient of degree `d-a-1`. Consequently the difference between the
monomial and its homogeneous replacement equals the cardinality polynomial
times a polynomial of degree at most `d-1`, modulo Boolean identities.

Multiplication by any polynomial of degree at most `d` requires cardinality
identities only through multiplier degree `2d-1`, exactly the range proved
in Lemma A. The functional vanishes automatically on Boolean identities
and their allowable multiples because it is defined by Boolean reduction.
Replacing the monomials in `p` gives `p-H=e Q` in the Boolean quotient,
where `deg(Q)<=d-1`; hence

```
E[p^2-H^2] = E[e Q(p+H)] = 0.
```

This verifies the degree bookkeeping needed to pass from a homogeneous
Gram matrix to positivity on every polynomial of degree at most `d`.
The cardinality recurrence itself never asks for a denominator beyond
`(s)_s`, because its squarefree multiplier degree is at most `2d-1<=s-1`.

## Conditioning and all preordering localizers

Boolean reduction of any product of `u_i` and `1-u_i` either gives zero
or an indicator on disjoint sets `A,B`. Repeated factors cause no issue.
Write `a=|A|`, `b=|B|`, `v=a+b`. For a squarefree set `C` outside
`A union B`, the exact uncancelled conditioning identity is

```
E[I_{A,B} u_C]
 = (t)_(a+|C|)(s-t)_b / (s)_(v+|C|).
```

If `pi=(t)_a(s-t)_b/(s)_v` is positive, this equals
`pi (t-a)_|C|/(s-v)_|C|`. Expansion then proves conditioning for the
restricted polynomial square. No remaining moment beyond degree `s-v`
is requested: if its degree is `d>=1`, then

```
v+2d <= 2r <= s.
```

The hypotheses for Lemma A follow directly:

```
s-v >= 2d,
t-a >= 2r-1-a >= 2d-1,
s-t-b >= 2r-1-b >= 2d-1.
```

For a constant restricted polynomial, the expectation is its squared value
times `pi>=0`. For a nonconstant original polynomial, the original degree
constraint gives `v<=2r-2`; all factors defining `pi` are then strictly
positive. Thus the draft's zero-weight conditioning discussion can be
replaced by a simpler observation: zero weight can occur only when the
original polynomial is constant. In that case nonnegativity is immediate.
If every remaining coordinate has been fixed, the restricted polynomial
is also constant, so no zero-variable conditional denominator is needed.

This proves positivity for the full truncated preordering, including
high-degree slack products with constant square multipliers, not merely
the ordinary moment matrix and single-slack localizers.

## Substitution, cover bound, and linear-order scope

Let `b=|R|` to distinguish this count from the hierarchy order `r`.
Because `k-2r+2` is an integer,

```
b < k-2r+2  implies  k-b >= 2r-1.
```

The same argument applies to `z`. Removing any `b` witness coordinates
therefore leaves at least `2r-1` unit coordinates and `2r-1` zero
coordinates. The remaining fractional cardinality satisfies
`t,s-t>=2r-1`, and the remaining dimension satisfies `s>=2r`, including
the special case `r=1`.

Substitution of restricted coordinates by their witness values makes all
their bound slacks nonnegative constants and cannot increase polynomial
degrees. Every requested preordering inequality consequently follows from
Lemma B. The original equality becomes `sum_U u_i-t`, and its substituted
multiplier still has degree at most `2r-1`; Lemma A applied with `d=r`
supplies every requested equality identity. Boolean second moments give
zero objective on unrestricted coordinates. The objective on restricted
coordinates is exactly `|M intersect R|p(1-p)`.

Thus `|R|<q_r` prevents pruning, with

```
q_r=min(k-2r+2,z-2r+2,m(1/2-2epsilon)).
```

The existing avoidance/counting proof applies unchanged. The reciprocal
coverage bound is a minimum of the two stated exponential terms. The
argument permits real-valued `q_r`; it introduces no rounding gap.

In the balanced case `n=3t`, if `r<=ct` for fixed `c<1/2`, then
`q_r>=min((1-2c)t,t(1/2-2epsilon))`, which is linear in `n` for fixed
`epsilon<1/4`. At `epsilon=1/8`, preserving `q_r=t/4` is equivalent to
`r<=3t/8+1`, exactly as stated. At `r=1`, the relaxation and bound reduce
to the preceding SDP–RLT result.

## A useful sharpness fact about this functional

Although Lemma A's PSD sufficient condition is not optimal, the two-sided
condition in Lemma B is essentially necessary for this particular
fractional-cardinality functional with the **full** degree-`2r` box
preordering.

Suppose `s>=2r` and `0<t<s` is noninteger. If `t<2r-1`, set
`ell=floor(t)+2<=2r`. A product of `ell` distinct lower-bound slacks has
expectation

```
E[prod_{i=1}^ell u_i] = (t)_ell/(s)_ell < 0,
```

because exactly its last numerator factor is negative. Applying the same
argument to upper-bound slacks proves that `s-t<2r-1` is also impossible.
Consequently full-preordering positivity for noninteger parameters requires
`t>2r-1` and `s-t>2r-1`; Lemma B proves sufficiency. Integer parameters
are separate: the functional is an actual uniform fixed-cardinality
distribution and is positive at every available degree.

Exact rational checks confirmed the negative-product obstruction for every
half-integer below the threshold at orders `1,...,6`. A sharper theorem
about the moment matrix alone cannot improve the current full-preordering
tradeoff without changing the functional or the oracle model.

## Additional closure and limits

The affine-Farkas argument from the SDP–RLT review extends to this degree.
Represent each affine inequality valid on `B intersect F` as a nonnegative
constant plus a nonnegative combination of box slacks plus an unrestricted
multiple of the equality. Expanding any product of such inequalities times
a square, within degree `2r`, leaves nonnegative combinations of existing
preordering expressions. Every term containing the equality vanishes using
the available equality multiplier degree `2r-1`. Thus those additional
affine-product localizers do not strengthen the oracle.

This argument does not cover arbitrary nonlinear valid cuts, symmetry
constraints, non-coordinate branching, or objective-cutoff localizers.
Objective-based tightening requires the charged augmented-cover convention
already reviewed in `notes/review-spatial-bb-sdp-rlt.md`. Granting a
high-order SDP as an oracle does not make its computation inexpensive;
the theorem is a cover-size statement even when that oracle is granted.

## Subsequent audit of the unique-minimizer perturbation

The author's added perturbation corollary also **passes** review. The Hessian
of the perturbed objective remains `-2I`, so every minimizing point is a
vertex: a nonvertex lies strictly between two distinct feasible points and
strict concavity would make its objective exceed at least one endpoint's.
At every vertex the quadratic part is `1/4`. Sorting the distinct positive
coefficients gives exactly the stated unique minimizing vertex. For a half
coordinate `j<=k`, the excess linear cost over the displayed minimizer is
`(d_(k+1)-d_j)/2>0`; for `j>k+1`, the excess is
`(d_j-d_(k+1))/2>0`. Other selections of unit coordinates only increase cost.

No nonidentity variable permutation preserves the objective polynomial,
because its distinct linear coefficients would have to be preserved
coordinate by coordinate. This removes literal permutation symmetry of the
model; it does not remove the obvious opportunity to solve this particular
family analytically outside the specified oracle-and-cover model.

Every first moment of the constructed functional lies in `[0,1]`, so its
perturbation value is at most `sum_i d_i<=eta`, while the true perturbed
optimum is at least `1/4`. Consequently replacing `h` by
`m(1/2-2epsilon-2eta)` gives exactly the strict below-target objective
needed by the cover proof. The formula

```
q_(r,eta)=min(k-2r+2,z-2r+2,m(1/2-2epsilon-2eta))
```

is correct. At `epsilon=1/8`, `eta=1/32`, it gives `h_eta=3t/16`, hence
exponent `3t/32=n/32`; the permitted order is exactly
`r<=13t/32+1`.

Finally `OPT_d<=1/4+eta`. When `eta<epsilon`, the original chord tree with
tolerance `epsilon-eta` gives base-objective lower bound
`1/4+eta-epsilon>=OPT_d-epsilon`; the positive linear perturbation cannot
lower this bound. Thus the claimed `O(2^n)` upper certificate and
`2^{Theta(n)}` size classification for the explicit perturbed family are
valid within the stated certification model.
