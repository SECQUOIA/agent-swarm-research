# Second independent review: matching degree bound by harmonic coupling

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed construction: harmonic coupling proposed by `new_directions`.

## Verdict on the proof

The harmonic argument is correct and improves the universal maximum-degree upper
bound to `O(log d/log log d)`, matching the dyadic counterexample's order.
This note independently derives every step, including normalization, shared
marginals, truncation loss, and constants. The precise displayed bound is

```
tbtgap ≤ [24L/((1−e^(−1)) ln L)] chgap,
D≥d,  L=1+ln D≥16.
```

Taking `D=max(d,exp(15))` satisfies the hypotheses for all `d≥2`. The constant
cutoff is permitted because this is an existence theorem for couplings, not a
finite-precision sampling algorithm. An integer cutoff with logarithm at least
15 works as well. This review does not establish literature novelty.

## Full definition and exact marginals

Classify a coordinate as low when `x_i≤1/2` and high otherwise. Let `p_i=1−x_i`
for high coordinates. Use one uniform random variable `U∈(0,1)`. Every low
coordinate is one precisely when `U≤x_i`.

For `p>0`, put

```
h_p = min(Dp,1),
a_p = 1+ln(min(D,1/p)),
q_p(t) = min(1,p/t) 1[t≤h_p] / a_p.
```

For a high coordinate with failure marginal `p`, fail with probability `q_p(U)`,
independently of all other high coordinates conditional on `U`. For `p=0`, the
coordinate is always one, without evaluating the logarithm or dividing by zero.

Because `D≥1`, `p≤h_p≤1`, `a_p≥1`, and `0≤q_p(t)≤1`. Direct integration gives

```
∫_0^1 q_p(t)dt
 = [p+p ln(h_p/p)]/a_p
 = p.
```

Indeed, `h_p/p=min(D,1/p)`. Thus the construction has every prescribed marginal.
All high-coordinate failures are conditionally independent within one global
random vector; no separate termwise couplings are being combined inconsistently.
The variable-dependent normalizers satisfy `a_p≤L`, which is the direction
needed in the lower bound below.

The second distribution uses the same type of common uniform variable but makes
every high coordinate fail deterministically when `U≤p_i`. Its low coordinates
are again one when `U≤x_i`. This is the scale-one coupling from the earlier proof.
The third distribution rounds all coordinates independently with their marginals.

## Monomial deficiency and easy terms

For each monomial choose its minimum-marginal coordinate with marginal `u`, and
write `S` for the sum of failure marginals of the other coordinates. Its
term-by-term gap is `T=min(u,S)`. In any feasible binary distribution, its
deficiency is the probability that the chosen coordinate is one and some other
coordinate is zero; equivalently it is `u−E(product)`.

As independently checked in `notes/review-positive-multilinear-upper-second.md`,
independent rounding provides deficiency at least `(c/2)T`, `c=1−e^(−1)`, for
terms with zero or at least two low coordinates. Every deficiency is nonnegative.
It remains to consider terms with exactly one low coordinate, whose marginal
`u≤1/2` is necessarily the minimum. If `T=0`, the target lower bound is zero and
there is nothing to prove. In the remainder take `T>0`.

## A large failure marginal is handled by the common-threshold coupling

Let `p_max` be the largest failure marginal of the remaining high coordinates.
If `p_max≥T/sqrt(L)`, the scale-one coupling has exact deficiency

```
min(u,p_max) ≥ T/sqrt(L),
```

because `u≥T`. For `L≥16`, `sqrt(L)≥ln L`, so this is at least `T ln L/L` and
therefore at least the common target `c T ln L/(8L)`.

## The harmonic coupling handles the remaining terms

Assume `p_max<T/sqrt(L)`, and integrate over

```
t ∈ [T/sqrt(L), T/2].
```

This is a nonempty interval because `L≥16`; it lies in `[0,u]` and below one.
Every positive failure marginal is strictly below `t`, so an active high
coordinate has conditional failure probability `p_j/(a_(p_j)t)`. Since `t<1`,
being active is equivalent to `Dp_j≥t`.

There are at most `r≤d−1` high coordinates in the term. Every inactive marginal
is smaller than `t/D`, so their sum is at most `rt/D≤t`. The total active
failure marginal is therefore at least

```
S−t ≥ T−t ≥ T/2.
```

The sum `λ(t)` of conditional failure probabilities consequently satisfies

```
λ(t) ≥ [Σ_active p_j]/(Lt) ≥ T/(2Lt) =: z(t).
```

The lower bound itself is at most one: since `t≥T/sqrt(L)`,
`z(t)≤1/(2sqrt(L))≤1/8`. Conditional independence gives

```
P(at least one high failure | U=t)
 ≥ 1−exp(−λ(t))
 ≥ c min(1,λ(t))
 ≥ c z(t).
```

Only the lower bound `z(t)` is required to lie below one; the actual sum
`λ(t)` may be larger. Since the low anchor is certainly one for these values
of `U`, this probability contributes directly to the deficiency. Integrating,

```
G_harmonic
 ≥ [cT/(2L)] ln(sqrt(L)/2)
 ≥ c T ln L/(8L).
```

The last inequality follows from
`ln(sqrt(L)/2)=(ln L)/2−ln2≥(ln L)/4` exactly when `L≥16`.
This checks both the integration constants and the logarithm bases.

## One mixture works for every monomial

Take the uniform mixture of harmonic, scale-one, and independent distributions.
All three have the same prescribed marginals. Every monomial has deficiency at
least `cT ln L/(8L)` in at least one of the three component distributions:
the easy terms use independence, and the exactly-one-low terms use one of the
two cases above. For the easy terms the comparison is valid since
`cT/2≥cT ln L/(8L)` for `L≥16`.

Every contribution omitted from this lower bound is nonnegative. Multiplying by
nonnegative polynomial coefficients, summing, and dividing by three gives

```
chgap ≥ [c ln L/(24L)] tbtgap.
```

This proves the stated constant using an actual global joint distribution.
There is no dependence on the number of variables or monomials in that constant.

## Degree growth and nonnegative boxes

For large `d`, choose `D=d`, giving `L=1+ln d` and the claimed upper order
`log d/log log d`. The small-degree cutoff supplies a finite constant when
`ln ln d` is zero or negative, so the asymptotic notation is not being used as
an invalid numerical bound there. Degree-zero and degree-one terms contribute
zero gap and can be removed.

The previously independently checked positive-expansion argument extends the
bound unchanged to any finite nonnegative box. Under affine box normalization,
each original term expands into positive unit-box monomials of degree no larger
than the original degree. The original term gap is at most the sum of its
expanded term gaps, while the full hull gap is invariant. Zero-width coordinates
are fixed and removed first. Hence the bound applies to the original, unexpanded
term-by-term relaxation.

The sparse dyadic lower construction has degree `2^(L_old−1)+1` and exact ratio
asymptotic to `L_old/log₂ L_old`. Taking the largest admissible `L_old` for a
given degree bound yields the matching `Ω(log d/log log d)` lower order.
Thus, with dimension and positive polynomial unrestricted, the worst gap ratio
for maximum degree at most `d` grows as `Θ(log d/log log d)` as `d→∞`.
The theorem does not claim an exact leading constant or efficient computation
of the convex envelope.

## Full written baseline checked

I subsequently read the complete draft
`results/positive-multilinear-sharp-degree-growth.md`, with
`L=max(16,1+ln d)` and `M=exp(L−1)`. Its normalization, inequalities, boundary
conventions, and final constant agree with the independently checked argument
above. No discrepancy or mathematical error was found.

## Independently checked refinement: leading constant one

The multilinear agent subsequently proposed a refinement that gives the exact
leading asymptotic constant. This reviewer independently verified it. Use the
author's convenient small-degree convention

```
L=max(exp(6),1+ln d),
b=ln L≥6,
M=exp(L−1)≥d,
a=L/b²,
β=1/b.
```

The harmonic distribution is the same construction with cutoff `M` and
normalizers bounded above by `L`. Put

```
h = (1−1/b)(1−1/(2b²)) [b−3ln b]/L.
```

All factors are positive: for `b≥6`, `b−3ln b>0`, because at six it is positive
(`ln6<2`) and its derivative `1−3/b` is positive thereafter. In particular
`βa=L/b³>1`, so the integration interval below has positive length. Also `a>1`,
which ensures the threshold target does not exceed `T`.

For a one-low-coordinate term with `T>0`, if `p_max≥T/a`, the threshold coupling
has deficiency at least `T/a`. Otherwise all `p_j<T/a`. Integrate harmonic gain
on

```
t ∈ [T/a, βT].
```

The interval lies below the anchor marginal `u`, since `β<1` and `T≤u`.
Every failure marginal is below `t`. As before, cutoff-inactive marginals sum
to at most `rt/M≤t`, so the active marginal mass is at least

```
S−t ≥ (1−β)T.
```

Therefore the sum of conditional failure probabilities is at least

```
z(t)=(1−β)T/(Lt).
```

This lower bound satisfies `z(t)≤(1−β)a/L≤1/b²`. Using conditional independence
and the elementary inequality `1−exp(−z)≥z−z²/2` for `z≥0`, the conditional
union probability is at least

```
(1−1/(2b²)) z(t).
```

The actual conditional intensity may exceed `1/b²`; only its displayed lower
bound is substituted into the increasing function `1−exp(−z)`. Integrating gives

```
G_harmonic
 ≥ (1−1/(2b²))(1−β)T/L · ln(βa)
 = hT,
```

because `ln(βa)=ln(L/b³)=b−3ln b`. Thus the two hard-term cases have respective
gains `T/a` and `hT`. Easy terms still have independent gain at least `cT/2`.

Let

```
Z=1/h+a+2/c.
```

Mix the harmonic, threshold, and independent distributions with probabilities
`(1/h)/Z`, `a/Z`, and `(2/c)/Z`, respectively. These are positive and sum to one.
In the corresponding case, each monomial has mixture deficiency at least `T/Z`.
Every other component contributes nonnegatively. Hence

```
tbtgap ≤ Z chgap.
```

As `d→∞`, eventually `L=1+ln d` and `b=ln L`. Since

```
h=(b/L)(1+o(1)),
a=L/b²=o(L/b),
2/c=o(L/b),
```

we have

```
Z=(1+o(1)) L/b
 =(1+o(1)) ln d/ln ln d.
```

The exact dyadic lower family has ratio `(1+o(1)) ln d/ln ln d`, including for
arbitrary degree allowances by selecting the largest admissible dyadic degree.
Together these establish

```
R(d) / [ln d/ln ln d] → 1
```

for the supremum of ratios over all dimensions, nonnegative-coefficient
polynomials of maximum degree at most `d`, and points with positive hull gap.
The same conclusion holds when finite nonnegative boxes are allowed: the
positive-expansion comparison gives the same upper bound and the unit-box
lower family remains admissible. This is an asymptotic statement; it does not
assert equality with that logarithmic expression at small degrees.

## Final full written refinement checked

I reread the completed `results/positive-multilinear-sharp-degree-growth.md`
after the leading-constant refinement was inserted. The written definitions,
positivity conditions, interval estimates, optimized mixture, asymptotic degree
lower transfer, dimension corollary, and nonnegative-box extension are correct.
No missing hypothesis or unresolved proof issue was found.

For the dimension corollary specifically, every polynomial in `n` variables has
degree at most `n`, supplying the same asymptotic upper bound. The largest dyadic
example with `2^ell+ell≤n` has a dimension within a constant factor of `n`, and
unused variables can be added without changing either gap. Its exact lower ratio
therefore supplies the matching leading constant one. Thus the supremum over
`n`-variable polynomials also satisfies `C(n)~ln n/ln ln n`.
