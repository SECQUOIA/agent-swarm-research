# Independent review of monotone finite-grid transfer

Date: 2026-09-22. Reviewer: a fresh independent agent. Scope: the full
[finite-grid transfer draft](research-20260922-finite-grid-planar.md), with the
continuous planar bound read from
[the planar message note](research-20260922-higher-dimensional-smoothing.md).

**Conclusion.** The transfer is correct for the expected number of distinct
quadratic formulas needed on a nonempty open parameter domain, provided the
continuous bound is uniform under deterministic additive offsets to individual
support costs. The scalar and planar bounds under discussion have that
invariance. The argument does not transfer the expected number of connected
regions, nor higher moments of the number of formulas.

The draft's extension to arbitrary polynomial degree and parameter dimension
is also valid: the proof below uses only the polynomial identity property,
not degree two. One minor wording correction was sent to the author: choose
the smallest power of two satisfying the grid-size lower bound to obtain
the asserted upper bound on its logarithm.

## Precise statement checked

Let `Z` be a nonempty subset of `{0,1}^m`, and let `Omega` be a nonempty open
subset of `R^d`. Give each support a quadratic polynomial `q_z`. Set

```
F_z(t;xi) = q_z(t) + z dot xi.
```

The coordinates of `xi` are independent. Let `P` be the product of continuous
uniform distributions on the coordinate intervals, and `G` the product of
uniform distributions on their respective `N` equally spaced grid points,
including both endpoints. The intervals have positive length and `N>=2`.

For fixed noise, group supports whose complete polynomials `F_z` are
identical. Let `K(xi)` count those distinct polynomial classes which attain
the lower envelope on a nonempty open subset of `Omega`. Equivalently, a
class counted by `K` is strictly below every other distinct polynomial at
some point of `Omega`.

Suppose that, for every collection of deterministic constants `b_z`, the
continuous model with branches `q_z+b_z` has expected number of supports
which are uniquely minimizing somewhere at most `B`. Then

```
E_G K <= B + m |Z|/N <= B + m 2^m/N.
```

It is enough to require the bound uniformly along one family
`b_z=delta a_z`, where the fixed constants `a_z` are pairwise distinct and
`delta` tends to zero through positive values. A continuous bound on
connected unique-minimizer regions supplies a bound on the number of
supports uniquely minimizing somewhere.

## Product replacement and monotonicity

For one fixed support `z`, define

```
E_z = {xi: there is t in Omega with F_z(t;xi)<F_w(t;xi)
       for every w != z}.
```

For each fixed `t`, its strict inequalities describe an open subset of noise
space. Their union over all `t` is open, even though the union need not be
countable. Thus the event is measurable. This step needs no parameter-space
regularity.

If `z_i=1`, decreasing `xi_i` preserves membership in `E_z`: it leaves the
differences from supports with `w_i=1` unchanged and decreases the differences
from supports with `w_i=0`. If `z_i=0`, increasing `xi_i` preserves membership.
Consequently every section of `E_z` in coordinate `i` is a ray, the empty
set, or the whole line. The direction can depend on `z`, which causes no
problem because supports are treated separately.

Normalize one coordinate interval to `[0,1]`. At its grid point
`x_k=k/(N-1)`, the grid distribution has left and right cumulative values
`k/N` and `(k+1)/N`, while the continuous cumulative value is `k/(N-1)`.
Both differences have magnitude at most `1/N`. Between grid points the
continuous cumulative distribution is linear and the grid cumulative
distribution is constant, so the same bound holds. It applies to both open
and closed rays; endpoint atoms do not invalidate it.

Replace coordinates one at a time. Conditioning on the other coordinates
gives the same ray comparison under each mixed product distribution. Each
replacement changes the event probability by at most `1/N`, and therefore

```
|P_G(E_z)-P_P(E_z)| <= m/N.
```

Linearity of expectation, with no independence between the events `E_z`,
gives the claimed additive `m|Z|/N` comparison for the number of supports
uniquely minimizing somewhere. Independence of the original noise
coordinates is required for this replacement argument.

## Atomic ties and distinct formulas

Choose pairwise distinct constants `a_z`. For `delta>0`, let `A_delta(xi)`
count supports uniquely minimizing somewhere for branches
`F_z+delta a_z`. These additional offsets are a proof device; they need not
be realized by coordinate penalties in the optimization instance.

Fix any noise realization. For each polynomial class counted by `K`, choose
a point where it is strictly below every other distinct polynomial. Such
a point exists: begin with an open set where the class attains the envelope
and avoid the zero sets of its differences from the finitely many other
distinct polynomials. Each nonzero polynomial has zero set with empty
interior. The gap at the chosen point is positive.

Within each identical-polynomial class, take its unique support with smallest
`a_z`. For all sufficiently small positive `delta`, that support is uniquely
minimizing at the chosen point: the offsets break its internal ties, and
the positive gap prevents another class from taking over. There are finitely
many counted classes, so

```
K(xi) <= liminf_(delta -> 0+) A_delta(xi).
```

Fatou's lemma along, for example, `delta=1/k`, followed by the support-event
comparison, gives

```
E_G K <= liminf_k E_G A_(1/k)
      <= B + m |Z|/N.
```

The direction of Fatou's inequality is correct. No uniform positive gap over
noise realizations is needed. The offset perturbations leave gradients,
Hessians, common concavity normalizations, and Lipschitz constants unchanged,
so the cited continuous scalar and planar bounds are uniform in `delta`.

## Limitations and significance

- The monotone-event comparison itself works for arbitrary deterministic
  branch functions. The passage from open-envelope formulas to strict
  representatives uses the polynomial identity property. It should not be
  stated for arbitrary continuous functions whose distinct formulas can
  coincide on an open patch.
- The count is of distinct necessary polynomial formulas. A formula may
  win on several disconnected regions. Formula count does not bound region
  count by the same constant, and a first-moment formula bound does not
  control the expected square or higher powers of that count.
- Under atomic noise, counting all support labels that tie for the minimum
  can give an exponential answer even for a single identical polynomial.
  Identical formulas must be deduplicated.
- The offsets only justify a representation-size bound. They do not prove
  that a particular exact algorithm handles grid degeneracies, and do not
  by themselves establish its bit complexity or expected running time.
- Product-distribution replacement for monotone events is elementary. This
  review supports the specialized application, not an independent novelty
  claim for that probability argument or finite-precision smoothing.

## Additional review: conditional higher moments

The subsequently added Section 4 is also correct. Fix a positive integer
`p`. The expansion of `U^p` is a sum over all ordered support `p`-tuples,
with repetition allowed. Each indicator asks whether every member of the
tuple is uniquely minimizing somewhere; the witnessing parameter points
may differ. Along one noise coordinate, each individual activity event is
a ray. Their intersection is an interval, possibly empty or unbounded.
No common witness is needed for this statement.

An interval probability is a difference of two half-line probabilities,
with endpoint conventions chosen to match the interval. Its discrepancy
is therefore at most `2 Delta_i`. Product replacement and summation over
the `|Z|^p` tuples give

```
|E_nu U^p-E_mu U^p| <= 2 |Z|^p sum_i Delta_i.
```

The pointwise tie-selection inequality implies
`K^p <= liminf U_delta^p`. Fatou then gives the claimed grid bound when a
uniform shifted continuous bound `E_mu U^p<=B_p` is supplied. For equal
grids the correction is `2m 2^(mp)/N`. This proof transfers a supplied
higher-moment bound; it does not obtain one from a first-moment estimate.

## Targeted verification

An exact `fractions.Fraction` check tested both cumulative values at every
grid point for `N=2,...,256`: 65,790 threshold endpoint comparisons all
satisfied the discrepancy bound `1/N`. The command was a local Python
heredoc. Between-grid bounds follow from linearity, not from sampling.

The monotonicity, product replacement, tie-selection argument, and Fatou
step were checked mathematically above. No Lean verification or project-wide
checks were run. The continuous planar theorem is a dependency; this review
does not constitute a new independent audit of its curvature and topology
proofs.
