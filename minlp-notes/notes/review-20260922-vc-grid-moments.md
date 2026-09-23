# Independent review of VC dimension and finite-grid moment bounds

Date: 2026-09-22. Reviewer: `/root/review_vc_grid_moments`.

Reviewed [the higher-moment note](research-20260922-envelope-higher-moments.md),
including its direct finite-grid extension. The probability argument and
constants are correct. The only requested statement changes concern a
measurability convention, the empty parameter domain, and the constant-function
case under atomic noise. These do not affect compact-box applications.

## Proof audit

Fix a nonempty deterministic `Z` contained in `{0,1}^m`, arbitrary finite
deterministic costs, and independent noise coordinates. Assume every closed
interval `J` has probability at most `phi length(J)+tau` under each coordinate.
Set `theta=2phi delta+tau`, for `delta>=0`.

For a fixed coordinate set `I`, conditioning outside `I` makes all pattern-class
minimum costs deterministic. If the near-optimal set shatters `I`, the minimum
in its zero class and each unit-pattern class differ by at most `delta`.
Consequently each remaining coordinate belongs to its own fixed closed
interval of length `2delta`. The thresholds do not depend on other coordinates
in `I`. Independence therefore gives `theta^|I|`. The proof does not multiply
probabilities with mutually dependent thresholds.

Empty pattern classes make shattering impossible. Distinct supports with equal
costs remain distinct members of the near-optimal family; ties do not invalidate
the conditioning. A union bound gives

```
Pr(VCdim(A_delta)>=k) <= binom(m,k) theta^k.
```

For `a=(m+1)^p`, Sauer--Shelah and the integer tail-sum identity give

```
E |A_delta|^p
 <= E a^V
 = 1+sum_(k=1)^m (a^k-a^(k-1)) Pr(V>=k)
 <= (1+a theta)^m
 <= exp(m a theta).
```

This is valid for every real `p>=1`; integrality of `p` is unnecessary. All
variables are bounded by `2^m`, so no integrability interchange is implicit.
Arbitrary deterministic offsets, restricted feasible families, nonidentical
coordinate distributions, and negative costs are allowed. Independence from
the deterministic input must remain explicit.

The parameter-net argument also passes. A support optimal at any parameter,
including one optimal only at a tie, is `2L eta`-near-optimal at the chosen net
point. The net must be deterministic. Convexity bounds the moment of the sum
without independence across net points. The displayed compact-box covering
constants are correct for positive `M` and dimension. A singleton box needs one
net point; the formula continues to give that bound.

## Atomic perturbations and edge cases

For `N` equally spaced points including both endpoints of `[-sigma,sigma]`,
with `sigma>0`, counting points in a closed interval gives

```
Pr(xi_i in J) <= length(J)/(2sigma)+1/N.
```

Thus the finite-grid choices

```
delta=1/[4m phi(m+1)^p],
N>=2m(m+1)^p
```

make the exponent at most one. Taking the next power of two requires
`O_p(log(m+1))` random bits per coordinate. This statement concerns random
sampling and perturbation encoding; it does not establish the bit complexity
of a downstream algorithm.

Three conventions should be explicit:

- Require the parameter domain to be nonempty. Otherwise `K=0`, and the
  constant-function sentence saying `K=1` is false.
- Compact metric parameter domains give immediate measurability. For each
  support, minimizing the continuous maximum of its pairwise cost differences
  over the compact domain yields a continuous function of the noise. Its
  nonpositive sublevel set is precisely the event that this support is ever
  optimal. For a completely arbitrary metric domain, either assume measurability
  or state the result using outer expectation. No such qualification is needed
  for the intended compact boxes.
- With continuous noise and `L=0`, the winner is unique almost surely. With
  atomic noise and `L=0`, several supports may tie everywhere. Apply the same
  moment bound at `delta=0`; do not assert uniqueness. If `m=0` and `Z` and the
  parameter domain are nonempty, `K=1` deterministically.

For an explicit atomic check, take the full cube, zero deterministic costs,
and a symmetric odd grid with one zero point. Each zero noise coordinate
doubles the optimal-support count. Hence
`E K^p=[1+(2^p-1)/N]^m`, which is consistent with the proposed bound but
disproves atomic uniqueness.

## Literature comparison

[Röglin and Teng, April 2, 2009 manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/04/Pareto.pdf)
already establish polynomial fixed moments of smoothed Pareto counts. Their
closest proof ingredient is the generalized winner gap, Section 3.3,
Lemma 3.2, proved in Appendix A through ranks and conditional class minima.
Section 6.1 applies it to expected runtime. Their stated winner-gap model uses
a perturbed linear objective; the present offset and parameter formulation
must be compared at the proof level, not dismissed because its statement uses
different notation. The current VC argument is a short sufficient route, but
its existence does not establish a new general smoothed-moment phenomenon.

[Brunsch and Röglin, revised 2015 abstract](https://arxiv.org/abs/1111.1546v2)
states stronger Pareto moment estimates for several perturbed linear objectives
and one arbitrary objective, plus extensions preserving zero coefficients.
Those results are significant antecedents. This review inspected the abstract,
not its complete proof, and therefore does not settle equivalence.

[Röglin and Vöcking, Section 6.1](https://www.roeglin.org/publications/IPCO05.pdf)
explicitly permit arbitrary adversarial objective functions when perturbing
linear constraints, because their loser and feasibility arguments use a fixed
ranking. This is another reason not to claim that allowing arbitrary
deterministic costs is itself unprecedented.

Searches combining smoothed optimization, VC dimension, Sauer--Shelah,
near-optimal solutions, and higher-gap bounds did not locate this precise
VC-plus-net statement. That unsuccessful search is not evidence of novelty.
The logarithmic finite-grid precision and direct handling of all ties are
useful concrete conclusions. Publication-level priority remains unresolved.

## Targeted verification

In addition to the proof audit, the reviewer ran an inline Python program using
`fractions.Fraction`. It exhaustively enumerated 396 small cases and 10,278
noise outcomes. Cases included every nonempty feasible family for `m<=2`, four
families for `m=3`, three deterministic cost functions, grids of sizes three
and five, and `delta` equal to zero, one quarter, and one half. It checked every
VC tail and the rational moment bound `(1+(m+1)^p theta)^m` for `p=1,2,3`.
All passed. Persistent ties and atomic interval endpoints were included.

These finite checks detect small counterexamples; they do not prove the general
theorem, novelty, or an algorithmic running-time bound. No Lean formalization,
project-wide verification, or CI inspection was performed.
